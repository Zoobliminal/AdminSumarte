# Generated by Django 5.0.3 on 2024-10-02 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Avisos', '0003_alter_historialaviso_accion'),
    ]

    operations = [
        migrations.AddField(
            model_name='aviso',
            name='latitud',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='aviso',
            name='longitud',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
