# Generated by Django 3.2.5 on 2023-05-22 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FARMAHOME', '0006_auto_20230508_1516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datoreparto',
            options={'permissions': (('can_download_data', 'Can download data.'), ('can_upload_data', 'Can upload data.'), ('can_register_data', 'Can register data.'), ('can_register_route', 'Can register route.'))},
        ),
    ]
