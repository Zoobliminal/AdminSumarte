# Generated by Django 5.0.3 on 2024-09-13 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CambioContador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contrato', models.CharField(blank=True, max_length=5, null=True)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('numero_viejo', models.CharField(blank=True, max_length=20, null=True)),
                ('numero_nuevo', models.CharField(blank=True, max_length=20, null=True)),
                ('lectura_viejo', models.CharField(blank=True, max_length=10, null=True)),
                ('lectura_nuevo', models.CharField(blank=True, max_length=10, null=True)),
                ('imagen_viejo', models.ImageField(blank=True, null=True, upload_to='Avisos')),
                ('imagen_nuevo', models.ImageField(blank=True, null=True, upload_to='Avisos')),
                ('notas', models.CharField(blank=True, max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='actualizado')),
            ],
            options={
                'verbose_name': 'cambio',
                'verbose_name_plural': 'cambios',
                'ordering': ['-created'],
            },
        ),
    ]
