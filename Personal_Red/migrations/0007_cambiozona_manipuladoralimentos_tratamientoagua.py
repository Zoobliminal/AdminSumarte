# Generated by Django 5.1.2 on 2024-10-25 22:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personal_Red', '0006_lineaagenda'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CambioZona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poblacion_abastecida', models.CharField(max_length=100)),
                ('origen_agua', models.CharField(max_length=100)),
                ('fecha_hora_inicio', models.DateTimeField()),
                ('fecha_hora_fin', models.DateTimeField(blank=True, null=True)),
                ('motivo_cambio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ManipuladorAlimentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad_en_empresa', models.CharField(max_length=200)),
                ('formacion', models.CharField(max_length=100)),
                ('fecha_certificado', models.DateField()),
                ('manipulador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TratamientoAgua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_mantenimiento', models.DateField()),
                ('tipo_mantenimiento', models.CharField(max_length=100)),
                ('sustancia_empleada', models.CharField(max_length=100)),
                ('proveedor', models.CharField(max_length=100)),
                ('documentacion_disponible', models.TextField(blank=True, null=True)),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
