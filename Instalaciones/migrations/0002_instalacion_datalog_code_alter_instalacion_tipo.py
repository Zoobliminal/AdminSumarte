# Generated by Django 5.1.2 on 2024-10-26 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instalaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instalacion',
            name='datalog_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instalacion',
            name='tipo',
            field=models.CharField(choices=[('DEP', 'Depósito'), ('BOM', 'Bombeo'), ('ETAP', 'E.T.A.P.'), ('EDAR', 'E.D.A.R.')], max_length=4),
        ),
    ]