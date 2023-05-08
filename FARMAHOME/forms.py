from django import forms
from .models import DatoReparto
import datetime
        
class FormularioEntregarPedido(forms.Form):
    ESTADOS = (
                ("Sin revisar", "Sin revisar"),
                ("Entregado en domicilio", "Entregado en domicilio"),
                ("Entregado en otra dirección", "Entregado en otra dirección"),
                ("No entregado: Direccion errónea", "No entregado: Direccion errónea"),
                ("No entregado: No hay nadie en casa", "No entregado: No hay nadie en casa"),
            )

    direccion = forms.ModelChoiceField(queryset = DatoReparto.objects.filter(estado_entrega='Sin revisar', fecha_cita__date=datetime.date.today())\
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
                            min_length = 9,
                            max_length = 9,
                            required = True,
                            label = 'DNI')
    
    incidencias = forms.CharField(
                                    max_length = 200,
                                    required = False,
                                    label = 'Incidencias durante la entrega')
    
class FormularioSubirDocumento(forms.Form):
    documento = forms.FileField(
                                label = 'Documento',
                                required = True)