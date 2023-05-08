from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import DatoReparto
from .forms import FormularioEntregarPedido, FormularioSubirDocumento
from datetime import datetime
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
    context = {}
    return render(request, "FARMAHOME/index.html", context)

@login_required
@permission_required(perm='FARMAHOME.can_upload_data', raise_exception=True)
def subir_datos(request):
    if request.method == 'POST':
        file = request.FILES
        if file['archivo'].name.split('.')[-1] in ('xlsx','xls'):
            file = pd.read_excel(file['archivo'])

            columnas_preestablecidas = ['CITA','CÓDIGO POSTAL','DIRECCIÓN','NHC','MÓVIL','AGENDA','ESTADO']
            if any([columna not in file.columns for columna in columnas_preestablecidas]):
                form = FormularioSubirDocumento()

                messages.error(request,"El archivo no tiene las columnas que debe contener. Por favor, revisa el documento que intenta subir.")

                return render(request, "FARMAHOME/subir_documento.html", {"form":form})
            #file.rename({
                        #'CITA':'dia_cita',
                        #'CÓDIGO POSTAL':'cp',
                        #'DIRECCIÓN':'direccion',
                        #'NHC':'nhc',
                        #'MÓVIL':'movil',
                        #'AGENDA':'agenda',
                        #'ESTADO':'estado'}, axis='columns', inplace=True)
            #engine = create_engine('sqlite:///db.sqlite3')
            #file.to_sql('FARMAHOME_datoreparto', index=False, if_exists='append', con=engine)
            for index in file.index:
                new_value = DatoReparto(
                    dia_cita = file.loc[index,'CITA'],
                    cp = file.loc[index,'CÓDIGO POSTAL'],
                    direccion = file.loc[index,'DIRECCIÓN'],
                    nhc = file.loc[index,'NHC'],
                    movil = file.loc[index,'MÓVIL'],
                    agenda = file.loc[index,'AGENDA'],
                    estado = file.loc[index,'ESTADO']
                )
                new_value.save()
            
        elif file['archivo'].name.split('.')[-1] == 'csv':
            #file = pd.read_csv(file['archivo'])
            pass

        else:
            #return render(request, "FARMAHOME/index.html", {})
            pass

        return render(request, "FARMAHOME/index.html", {})
    else:
        form = FormularioSubirDocumento()

        return render(request, "FARMAHOME/subir_documento.html", {"form":form})

@login_required
def ver_pedidos(request):
    todos_pedidos = DatoReparto.objects.filter(dia_cita__date=timezone.now().date())
    return render(request, "FARMAHOME/ver_pedidos.html", {'todos_pedidos':todos_pedidos} )

@login_required
@permission_required(perm='FARMAHOME.can_register_data', raise_exception=True)
def entregar_pedido(request,id=None):
    if id: # It means we have accessed this page from Editar pedido, and we only want to see that pedido in particular.
        if request.method == 'POST':
            form = FormularioEntregarPedido(request.POST)
            if form.is_valid():
                direccion_selected = request.POST.get('direccion', False)
                entrega = get_object_or_404(DatoReparto, direccion=direccion_selected, dia_cita__date=timezone.now().date())
                
                entrega.DNI = request.POST.get('dni', False)
                entrega.estado = request.POST.get('estado', False)
                entrega.fecha_registro = datetime.now()
                entrega.incidencias = request.POST.get('incidencias', None)
                entrega.usuario_registro = request.user.username

                entrega.save()
                return HttpResponseRedirect('/')
        else:
            entrega = get_object_or_404(DatoReparto, pk=id)
            form = FormularioEntregarPedido(initial={'direccion':entrega.direccion,'estado':entrega.estado,'dni':entrega.DNI})
        return render(request, "FARMAHOME/entregar_pedido.html", {'form':form})
    
    else: # It means we have accessed this page from Entregar pedidos, so we do not pass any id and we want to see all pedidos.
        if request.method == 'POST':
            form = FormularioEntregarPedido(request.POST)
            if form.is_valid():
                direccion_selected = request.POST.get('direccion', False)
                entrega = get_object_or_404(DatoReparto, direccion=direccion_selected, dia_cita__date=timezone.now().date())
                
                entrega.DNI = request.POST.get('dni', False)
                entrega.estado = request.POST.get('estado', False)
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
def exportar_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename= FARMAHOME_{timezone.now().year}_{timezone.now().month}_{timezone.now().day}.xls'

    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet = work_book.add_sheet('Datos')

    font_style = xlwt.XFStyle()

    font_style.font.bold = True
    row_num = 0
    columns = ['CITA', 'CÓDIGO POSTAL', 'DIRECCIÓN', 'NHC', 'MÓVIL', 'AGENDA', 'ESTADO', 'DNI', 'INCIDENCIAS', 'FECHA ENTREGA', 'USUARIO REGISTRO']
    for col_num in range(len(columns)):
        work_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = DatoReparto.objects.filter(dia_cita__date=timezone.now().date()).values_list('dia_cita', 'cp', 'direccion', 'nhc', 'movil', 'agenda', 'estado', 'DNI', 'incidencias', 'fecha_registro', 'usuario_registro')
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