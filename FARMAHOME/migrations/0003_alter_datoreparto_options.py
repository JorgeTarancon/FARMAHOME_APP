# Generated by Django 3.2.5 on 2023-05-08 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FARMAHOME', '0002_alter_datoreparto_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datoreparto',
            options={'permissions': (('can_download_data', 'Can download data.'), ('can_upload_data', 'Can upload data.'), ('can_register_data', 'Can register data.'))},
        ),
    ]
