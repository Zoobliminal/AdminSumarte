# Generated by Django 5.1.2 on 2024-10-25 22:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instalacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('DEP', 'Depósito'), ('BOM', 'Bombeo'), ('ETAP', 'Estación de Tratamiento de Agua Potable'), ('EDAR', 'Estación de Depuración de Aguas Residuales')], max_length=4)),
                ('ubicacion', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MantenimientoCloracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana_inicio', models.DateField()),
                ('semana_fin', models.DateField()),
                ('fijacion_tuberias', models.BooleanField(default=False)),
                ('racor_manguera', models.BooleanField(default=False)),
                ('fugas_tanque_cloro', models.BooleanField(default=False)),
                ('comprobar_dosificaciones', models.BooleanField(default=False)),
                ('niveles_depositos', models.BooleanField(default=False)),
                ('cuba_reactivo', models.BooleanField(default=False)),
                ('observaciones', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MantenimientoEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_equipo', models.CharField(choices=[('Clorador', 'Clorador'), ('Bomba', 'Bomba'), ('Filtro', 'Filtro')], max_length=50)),
                ('tipo_mantenimiento', models.CharField(max_length=100)),
                ('fecha_hora_limpieza', models.DateTimeField()),
                ('proveedor', models.CharField(max_length=100)),
                ('descripcion_trabajo', models.TextField()),
                ('firma_responsable', models.CharField(max_length=100)),
                ('documentacion', models.FileField(blank=True, null=True, upload_to='documentacion_mantenimiento/')),
            ],
        ),
        migrations.CreateModel(
            name='MantenimientoInfraestructura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_infraestructura', models.CharField(choices=[('PT', 'Planta de Tratamiento'), ('DEP', 'Depósito'), ('RD', 'Red de Distribución')], max_length=3)),
                ('fecha_prevista', models.DateField()),
                ('fecha_realizada', models.DateField(blank=True, null=True)),
                ('documentacion', models.FileField(blank=True, null=True, upload_to='mantenimiento_documentacion/')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_empresa', models.CharField(max_length=100)),
                ('nombre_contacto', models.CharField(max_length=100)),
                ('cif', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=15)),
                ('direccion', models.CharField(max_length=200)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('servicios_productos', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RenovacionInstalacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obras_a_realizar', models.CharField(max_length=200)),
                ('trabajo_realizado', models.TextField()),
                ('fecha_prevista', models.DateField()),
                ('inversion_inicial', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localizacion', models.CharField(max_length=200)),
                ('fecha_hora_incidencia', models.DateTimeField()),
                ('descripcion', models.TextField()),
                ('medidas_correctoras', models.TextField()),
                ('fecha_hora_puesta_a_punto', models.DateTimeField(blank=True, null=True)),
                ('trabajador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InspeccionMensualDeposito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_programada', models.DateField()),
                ('fecha_realizada', models.DateField(blank=True, null=True)),
                ('elementos_cierre', models.BooleanField()),
                ('senalizacion', models.BooleanField()),
                ('estado_valvulas', models.BooleanField()),
                ('canalizaciones', models.BooleanField()),
                ('instalaciones', models.BooleanField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('trabajador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('instalacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspecciones_mensuales', to='Instalaciones.instalacion')),
            ],
        ),
        migrations.CreateModel(
            name='InspeccionAnualDeposito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_programada', models.DateField()),
                ('fecha_realizada', models.DateField(blank=True, null=True)),
                ('revision_fisuras', models.CharField(choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')], max_length=20)),
                ('revision_corrosion', models.CharField(choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')], max_length=20)),
                ('revision_materiales_sellado', models.CharField(choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')], max_length=20)),
                ('revision_paramentos_exteriores', models.CharField(choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')], max_length=20)),
                ('existencia_sedimentos', models.CharField(choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')], max_length=20)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('trabajador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('instalacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspecciones_anuales', to='Instalaciones.instalacion')),
            ],
        ),
        migrations.CreateModel(
            name='LimpiezaDeposito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion_deposito', models.CharField(max_length=100)),
                ('fecha_hora_limpieza', models.DateTimeField()),
                ('procedimiento', models.TextField(default='1. Vaciado del depósito por el desagüe de fondo.\n2. Barrido de los sólidos depositados sobre la superficie inferior hacia desagüe.\n3. Limpieza de las paredes y suelo con cepillos utilizando hipoclorito de sodio para la eliminación de suciedad y desinfección de superficies.\n4. Retirada de restos y aclarado con máquina de agua a presión (trabajando con agua tratada).\n5. Llenado del depósito hasta ¼ de la capacidad con agua limpia y posterior vaciado.\n6. Llenado definitivo del depósito con agua limpia comprobando continuamente el nivel de cloro hasta alcanzar el valor paramétrico deseado, normalmente entre 0,50 -0,70 mg/l.\n7. Apertura del depósito a red de distribución.')),
                ('fecha_hora_fin_limpieza', models.DateTimeField(blank=True, null=True)),
                ('sustancias_empleadas', models.CharField(max_length=200)),
                ('valor_cloro_medido', models.DecimalField(decimal_places=2, max_digits=5)),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MantenimientoRenovacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_mantenimiento', models.CharField(max_length=50)),
                ('fecha_programada', models.DateField(blank=True, null=True)),
                ('fecha_realizada', models.DateField(blank=True, null=True)),
                ('detalles', models.TextField(blank=True, null=True)),
                ('obras_a_realizar', models.CharField(max_length=200)),
                ('trabajo_realizado', models.TextField(blank=True, null=True)),
                ('inversion_inicial', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('instalacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mantenimientos', to='Instalaciones.instalacion')),
                ('trabajador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]