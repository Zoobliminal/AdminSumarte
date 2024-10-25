# Create your models here.



from django.db import models

# 1º - DEFINICION DE LAS TABLAS DE LA APLICACION DENTRO DEL PROYECTO

   

# class AgendaHoja(models.Model):
    
#     trabajador =  models.CharField(max_length=100,blank=False, null=False)
#     fecha_hoja = models.CharField(max_length=25,blank=False, null=False, verbose_name="Fecha de hoja")
#     siete =  models.CharField(max_length=500,blank=True, null=True, verbose_name="07:00")
#     sieteymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="07:30")
#     ocho =  models.CharField(max_length=500,blank=True, null=True, verbose_name="08:00")
#     ochoymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="08:30")
#     nueve =  models.CharField(max_length=500,blank=True, null=True, verbose_name="09:00")
#     nueveymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="09:30")
#     diez =  models.CharField(max_length=500,blank=True, null=True, verbose_name="10:00")
#     diezymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="10:30")
#     once =  models.CharField(max_length=500,blank=True, null=True, verbose_name="11:00")
#     onceymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="11:30")
#     doce =  models.CharField(max_length=500,blank=True, null=True, verbose_name="12:00")
#     doceymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="12:30")
#     trece =  models.CharField(max_length=500,blank=True, null=True, verbose_name="13:00")
#     treceymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="13:30")
#     catorce =  models.CharField(max_length=500,blank=True, null=True, verbose_name="14:00")
#     catorceymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="14:30")
#     quince =  models.CharField(max_length=500,blank=True, null=True, verbose_name="15:00")
#     quinceymedia =  models.CharField(max_length=500,blank=True, null=True, verbose_name="15:30")
#     extra_1 =  models.CharField(max_length=500,blank=True, null=True, verbose_name="Extra - 1")
#     extra_2 =  models.CharField(max_length=500,blank=True, null=True, verbose_name="Extra - 2")
#     extra_3 =  models.CharField(max_length=500,blank=True, null=True, verbose_name="Extra - 3")
#     extra_4 =  models.CharField(max_length=500,blank=True, null=True, verbose_name="Extra - 4")
#     created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
#     updated = models.DateTimeField(auto_now=True, verbose_name="actualizado") 
    
    
    