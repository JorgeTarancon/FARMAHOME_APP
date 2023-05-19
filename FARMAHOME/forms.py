from django import forms
from .models import DatoReparto
import datetime
        
class FormularioEntregarPedido(forms.Form):
    ESTADOS = (
                ("Pendiente", "Pendiente"),
                ("Entregado en domicilio", "Entregado en domicilio"),
                ("Entregado en otra dirección", "Entregado en otra dirección"),
                ("No entregado: Direccion errónea", "No entregado: Direccion errónea"),
                ("No entregado: No hay nadie en casa", "No entregado: No hay nadie en casa"),
                ("Cancelada entrega en domicilio","Cancelada entrega en domicilio"),
            )

    direccion = forms.ModelChoiceField(queryset = DatoReparto.objects.filter(estado_entrega='Pendiente', fecha_cita__date=datetime.date.today())\
                                                                        .values_list('direccion', flat=True),
                                       #empty_label = None,
                                       required = True,
                                       to_field_name = 'direccion',
                                       label = 'Direccion'
                                       )
    estado_entrega = forms.ChoiceField(
                                choices = ESTADOS,
                                required = True,
                                label = 'Estado de la entrega')
    
    dni = forms.CharField(
                            max_length = 15,
                            required = True,
                            label = 'DNI o nombre')
    
    incidencias = forms.CharField(
                                    max_length = 200,
                                    required = False,
                                    label = 'Incidencias durante la entrega')
    
class FormularioSubirDocumento(forms.Form):
    documento = forms.FileField(
                                label = 'Documento',
                                required = True)

class FormularioBusquedaEntregas(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'
        
    fecha = forms.DateField(widget=DateInput,
                            label='Otra fecha',
                            initial=datetime.date.today())