# Generated by Django 3.2.5 on 2023-05-08 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FARMAHOME', '0004_datoreparto_usuario_registro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datoreparto',
            old_name='dia_cita',
            new_name='fecha_cita',
        ),
    ]
