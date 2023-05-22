from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import DatoReparto, Ruta
from .forms import FormularioEntregarPedido, FormularioSubirDocumento, FormularioBusquedaEntregas
from datetime import datetime, timedelta
import pandas as pd
import xlwt
#from sqlalchemy import create_engine

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request,"Invalid username or password.")
            else:
                login(request, user)
                return redirect("/")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="FARMAHOME/login.html", context={"form":form})

@login_required
def index(request):
    if request.method == "POST":

        ruta = Ruta.objects.filter(usuario=request.user.username, fecha_inicio__date=timezone.now().date())
        fecha = datetime.now()

        if 'inicio_ruta' in request.POST:
            if len(ruta) == 0:
                new_value = Ruta(
                        usuario = request.user.username,
                        fecha_inicio = fecha)
                new_value.save()

                messages.success(request,f"Fecha inicio de la ruta registrada correctamente: {datetime.strftime(fecha,'%d-%m-%Y %H:%M:%S')}")
            else:
                messages.warning(request,f"Ya has registrado un inicio de ruta hoy para el usuario: {request.user.username}. No se puede registrar un nuevo inicio.")

        elif 'fin_ruta' in request.POST:
            if len(ruta) == 0:
                messages.warning(request,f"No se ha registrado ningún inicio de ruta hoy para el usuario: {request.user.username}. Por lo tanto, no se puede finalizar la ruta.")
            else:
                if ruta[0].fecha_fin:
                    messages.warning(request,f"Ya has registrado un fin de ruta hoy para el usuario: {request.user.username}. No se puede registrar un nuevo final.")
                else:
                    pedidos_pendientes = DatoReparto.objects.filter(fecha_cita__date=timezone.now().date(), estado_entrega = 'Pendiente')
                    if len(pedidos_pendientes) != 0:
                        print(pedidos_pendientes)
                        print(len(pedidos_pendientes))
                        messages.warning(request,'Todavia quedan entregas con estado "Pendiente". No se puede finalizar la ruta si quedan entregas pendientes.')
                    else:
                        ruta[0].fecha_fin = fecha
                        ruta[0].save()

                        messages.success(request,f"Fecha fin de la ruta registrada correctamente: {datetime.strftime(fecha,'%d-%m-%Y %H:%M:%S')}")

        else:
            messages.error(request,"An error has ocurred and we have not been able to register the datetime.")
            
    else:
        pass

    context = {}
    return render(request, "FARMAHOME/index.html", context)

@login_required
@permission_required(perm='FARMAHOME.can_upload_data', raise_exception=True)
def subir_datos(request):
    if request.method == 'POST':
        file = request.FILES
        if len(file.keys()) == 0:
            messages.error(request,"You have not attached any files. Please attach a file before clicking upload.")

            form = FormularioSubirDocumento()

            return render(request, "FARMAHOME/subir_documento.html", {"form":form})

        elif file['archivo'].name.split('.')[-1] in ('xlsx','xls'):
            file = pd.read_excel(file['archivo'])

            columnas_preestablecidas = ['CITA','CÓDIGO POSTAL','DIRECCIÓN','NHC','MÓVIL','AGENDA','ESTADO']
            if any([columna not in file.columns for columna in columnas_preestablecidas]):
                form = FormularioSubirDocumento()

                messages.error(request,"The file does not contain the columns it should contain. Please, check the file you are trying to upload.")

                return render(request, "FARMAHOME/subir_documento.html", {"form":form})
            
            for index in file.index:
                new_value = DatoReparto(
                    fecha_cita = file.loc[index,'CITA'],
                    codigo_postal = file.loc[index,'CÓDIGO POSTAL'],
                    direccion = file.loc[index,'DIRECCIÓN'],
                    nhc = file.loc[index,'NHC'],
                    movil = file.loc[index,'MÓVIL'],
                    agenda_cita = file.loc[index,'AGENDA'],
                    estado_entrega = 'Pendiente'
                )
                new_value.save()
            
            return render(request, "FARMAHOME/index.html", {})

        else:
            messages.error(request,"The file format is not valid. Please upload an .xlsx or .xls file.")
            form = FormularioSubirDocumento()

            return render(request, "FARMAHOME/subir_documento.html", {"form":form})

    else:
        form = FormularioSubirDocumento()

        return render(request, "FARMAHOME/subir_documento.html", {"form":form})

@login_required
def ver_pedidos(request,fecha=timezone.now().date()):
    if request.method == 'POST':
        form = FormularioBusquedaEntregas(request.POST)
        if form.is_valid():
            fecha = request.POST.get('fecha', False)
            fecha_busqueda = datetime.strptime(fecha,'%Y-%m-%d').date()
    else:
        if fecha == 'hoy':
            fecha_busqueda = timezone.now().date()
        elif fecha == 'ayer': fecha_busqueda = timezone.now().date() - timedelta(days=1)
        else: fecha_busqueda = fecha
        form = FormularioBusquedaEntregas(initial={'fecha':fecha_busqueda})
    
    todos_pedidos = DatoReparto.objects.filter(fecha_cita__date=fecha_busqueda)

    context = {'todos_pedidos': todos_pedidos,
               'fecha_actual': timezone.now().date(),
               'fecha_busqueda':fecha_busqueda.strftime('%d-%m-%Y'),
               'form':form}

    return render(request, "FARMAHOME/ver_pedidos.html", context=context )

@login_required
@permission_required(perm='FARMAHOME.can_register_data', raise_exception=True)
def entregar_pedido(request,id=None):
    if id: # It means we have accessed this page from Editar pedido, and we only want to see that pedido in particular.
        if request.method == 'POST':
            form = FormularioEntregarPedido(request.POST)
            if form.is_valid():
                direccion_selected = request.POST.get('direccion', False)
                entrega = get_object_or_404(DatoReparto, direccion=direccion_selected, fecha_cita__date=timezone.now().date())
                
                entrega.DNI = request.POST.get('dni', False)
                entrega.estado_entrega = request.POST.get('estado_entrega', False)
                entrega.fecha_registro = datetime.now()
                entrega.incidencias = request.POST.get('incidencias', None)
                entrega.usuario_registro = request.user.username

                entrega.save()
                return HttpResponseRedirect('/')
        else:
            entrega = get_object_or_404(DatoReparto, pk=id)
            form = FormularioEntregarPedido(initial={'direccion':entrega.direccion,'estado_entrega':entrega.estado_entrega,'dni':entrega.DNI})
        return render(request, "FARMAHOME/entregar_pedido.html", {'form':form})
    
    else: # It means we have accessed this page from Entregar pedidos, so we do not pass any id and we want to see all pedidos.
        if request.method == 'POST':
            form = FormularioEntregarPedido(request.POST)
            if form.is_valid():
                direccion_selected = request.POST.get('direccion', False)
                entrega = get_object_or_404(DatoReparto, direccion=direccion_selected, fecha_cita__date=timezone.now().date())
                
                entrega.DNI = request.POST.get('dni', False)
                entrega.estado_entrega = request.POST.get('estado_entrega', False)
                entrega.fecha_registro = datetime.now()
                entrega.incidencias = request.POST.get('incidencias', None)
                entrega.usuario_registro = request.user.username

                entrega.save()
                return HttpResponseRedirect('/')
        else:
            form = FormularioEntregarPedido()

        return render(request, "FARMAHOME/entregar_pedido.html", {"form":form})

@login_required
@permission_required(perm='FARMAHOME.can_download_data', raise_exception=True)
def exportar_excel(request,fecha=None):
    response = HttpResponse(content_type='application/ms-excel')

    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet = work_book.add_sheet('Datos')

    font_style = xlwt.XFStyle()

    font_style.font.bold = True
    row_num = 0
    columns = ['CITA', 'CÓDIGO POSTAL', 'DIRECCIÓN', 'NHC', 'MÓVIL', 'AGENDA', 'ESTADO', 'DNI', 'INCIDENCIAS', 'FECHA ENTREGA', 'USUARIO REGISTRO']
    for col_num in range(len(columns)):
        work_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    fecha_descarga = datetime.strptime(fecha, '%d-%m-%Y').date()
    response['Content-Disposition'] = f'attachment; filename= FARMAHOME_{fecha_descarga.year}_{fecha_descarga.month}_{fecha_descarga.day}.xls'
    rows = DatoReparto.objects.filter(fecha_cita__date=fecha_descarga).values_list('fecha_cita', 'codigo_postal', 'direccion', 'nhc', 'movil', 'agenda_cita', 'estado_entrega', 'DNI', 'incidencias', 'fecha_registro', 'usuario_registro')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            work_sheet.write(row_num, col_num, str(row[col_num]), font_style)

    work_book.save(response)

    return response

@login_required
def user_logout(request):
    logout(request)
    return redirect("FARMAHOME:user_login")