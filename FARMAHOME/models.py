from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class DatoReparto(models.Model):
    
    def __str__(self):
        return f'Repartir en: {self.direccion}\nEn el CP: {self.cp}\nMovil: {self.movil}'
    
    dia_cita = models.DateTimeField(('CITA'))
    cp = models.PositiveBigIntegerField(('CÓDIGO POSTAL'))
    direccion = models.CharField(('DIRECCIÓN'), max_length=200)
    nhc = models.CharField(('NHC'), max_length=10)
    movil = models.PositiveBigIntegerField(('MÓVIL'))
    agenda = models.CharField(('AGENDA'), max_length=30, blank = True, null = True)
    estado = models.CharField(('ESTADO'), max_length=100, blank = True, null = True)
    DNI = models.CharField(('DNI'), max_length=9, blank = True, null = True)
    incidencias = models.CharField(('INCIDENCIAS'), max_length=200,  blank = True, null = True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.CharField(('USUARIO'), max_length=100, blank = True, null = True)

    class Meta:
        permissions = (('can_download_data', 'Can download data.'),
                       ('can_upload_data','Can upload data.'),
                       ('can_register_data','Can register data.'),)