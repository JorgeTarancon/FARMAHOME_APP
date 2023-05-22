from django.db import models
#from django.contrib.auth.models import AbstractUser

# Create your models here.

class DatoReparto(models.Model):
    
    def __str__(self):
        return f'Repartir en: {self.direccion}\nEn el CP: {self.codigo_postal}\nMovil: {self.movil}'
    
    fecha_cita = models.DateTimeField(('CITA'))
    codigo_postal = models.PositiveBigIntegerField(('CÓDIGO POSTAL'))
    direccion = models.CharField(('DIRECCIÓN'), max_length=200)
    nhc = models.CharField(('NHC'), max_length=10)
    movil = models.PositiveBigIntegerField(('MÓVIL'))
    agenda_cita = models.CharField(('AGENDA'), max_length=30, blank = True, null = True)
    estado_entrega = models.CharField(('ESTADO'), max_length=100, blank = True, null = True)
    DNI = models.CharField(('DNI'), max_length=9, blank = True, null = True)
    incidencias = models.CharField(('INCIDENCIAS'), max_length=200,  blank = True, null = True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.CharField(('USUARIO'), max_length=100, blank = True, null = True)

    class Meta:
        permissions = (('can_download_data', 'Can download data.'),
                       ('can_upload_data','Can upload data.'),
                       ('can_register_data','Can register data.'),)
        
class Ruta(models.Model):
    usuario = models.CharField(('USUARIO'), max_length=150, blank=False, null=False)
    fecha_inicio = models.DateTimeField(('FECHA_INICIO'), blank=False, null=False)
    fecha_fin = models.DateTimeField(('FECHA_FIN'), blank=False, null=True)
    
    class Meta:
        permissions = (('can_register_route','Can register route.'),)