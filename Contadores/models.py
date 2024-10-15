from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Required to assign User as a borrower


class CambioContador(models.Model):
    
    contrato = models.CharField(max_length=5,blank=True, null=True)
    direccion = models.CharField(max_length=250,blank=True, null=True)
    
    numero_viejo = models.CharField(max_length=20,blank=True, null=True)
    lectura_viejo = models.CharField(max_length=10,blank=True, null=True)
    imagen_viejo = models.ImageField(upload_to='Contadores', blank=True, null=True, default='Contadores\default.jpg',)
    
    numero_nuevo = models.CharField(max_length=20,blank=True, null=True) 
    lectura_nuevo = models.CharField(max_length=10,blank=True, null=True)
    imagen_nuevo = models.ImageField(upload_to='Contadores', blank=True, null=True, default='Contadores\default.jpg')
    
    fecha_cambio = models.DateField(blank=True, null=True)
    notas = models.CharField(max_length=500,blank=True, null=True)
    
    actualizado_compass = models.BooleanField(default="False", null="False", verbose_name="Actualizado en Compass")
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado") 
    
   
    class Meta:
        verbose_name='cambio de contador'
        verbose_name_plural = 'cambios de contador'
        ordering = ['-created']
    
    def __str__(self) :
        return self.direccion
    
    
    
class LecturaAbonado(models.Model):
    
    contrato = models.CharField(max_length=5,blank=True, null=True)
    direccion = models.CharField(max_length=250,blank=True, null=True)
    contador = models.CharField(max_length=20,blank=True, null=True)
    lectura = models.CharField(max_length=20,blank=True, null=True)
    imagen_aviso = models.ImageField(upload_to='Contadores', blank=True, null=True, default='Contadores\default.jpg')
    imagen_contador = models.ImageField(upload_to='Contadores', blank=True, null=True, default='Contadores\default.jpg')
    fecha_lectura = models.DateField(blank=True, null=True)
    notas = models.CharField(max_length=500,blank=True, null=True)
    grabada = models.BooleanField(default="False", null="False", verbose_name="Grabada")
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado") 
    
   
    class Meta:
        verbose_name='Lectura de abonado'
        verbose_name_plural = 'Lecturas de abonado'
        ordering = ['-created']
    
    #def __str__(self) :
    #    return self.direccion