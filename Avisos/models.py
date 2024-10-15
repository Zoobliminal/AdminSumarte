from .telegram_utils import send_telegram_message
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.conf import settings  # Required to assign User as a borrower


class Aviso(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="avisos") 
    contrato = models.CharField(max_length=5,blank=True, null=True)
    nombre = models.CharField(max_length=25,blank=True, null=True)
    telefono = models.CharField(max_length=15,blank=True, null=True)
    registro = models.CharField(max_length=10,blank=True, null=True)
    direccion = models.CharField(max_length=50,blank=True, null=True)
    motivo = models.CharField(max_length=500, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)  # Fecha en que fue resuelta (si aplica)
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado") 
    finalizado = models.BooleanField(auto_created=False, default=False, blank=True, null=True)
    estatus = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('sin_resolver', 'Sin Resolver'),
        ('cerrado', 'Cerrado'),
    ], default='pendiente')
    trabajadores = models.ManyToManyField(User, related_name="trabajadores_aviso", blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
   
    class Meta:
        verbose_name='aviso'
        verbose_name_plural = 'avisos'
        ordering = ['-created']
    
    #def __str__(self) :
    #    return self.direccion




class imageComentAviso(models.Model):
    aviso=models.ForeignKey(Aviso, on_delete=models.CASCADE, auto_created=True, related_name="imageComentAvisos")
    usuario=models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="imageComentAvisos")
    imagen=models.ImageField(upload_to='Avisos', blank=True, null=True, default='Avisos/aviso_default.jpg')
    comentario = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado") 

    
    class Meta:
        db_table='imagenes_aviso'
        verbose_name='Imagen / comentario'
        verbose_name_plural='Imagenes y comentarios'
        ordering=['id'] 
    
    def __str__(self):
        return f"Comentario de {self.usuario} en aviso {self.aviso.id} - {self.created.strftime('%d/%m/%Y %H:%M')}"
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Notificar a los trabajadores asignados
        
        trabajadores_asignados = trabajadorAsignadoAviso.objects.filter(aviso=self.aviso, notificacion_activa=True)
        for asignacion in trabajadores_asignados:
            perfil_usuario = asignacion.trabajador.perfilusuario 
            if perfil_usuario.chat_id:
                message = (f"{self.aviso.direccion}\n\n"
                        f"{self.usuario.username}:\n"
                        f"{self.comentario}\n"
                )
                send_telegram_message(perfil_usuario.chat_id, message)
  
  
    
class trabajadorAsignadoAviso(models.Model):
    aviso=models.ForeignKey(Aviso, on_delete=models.CASCADE, auto_created=True, related_name="asignamientos")
    trabajador=models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="asignamientos")    
    notificacion_activa = models.BooleanField(auto_created=False, default=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado") 
    
    class Meta:
        db_table='trabajador_asignado_aviso'
        verbose_name='Trabajador asignado'
        verbose_name_plural='Trabajador - asignamiento'
        ordering=['id'] 
  
        # Evitar que un trabajador se asigne dos veces al mismo aviso
        constraints = [
            models.UniqueConstraint(fields=['aviso', 'trabajador'], name='unico_trabajador_por_aviso')
        ]
    
    def __str__(self):
        return f"Asignación de {self.trabajador} al aviso {self.aviso.id}"
        


class HistorialAviso(models.Model):
    ACCION_CHOICES = [
        ('cambio_de_estado', 'Cambio de Estado'),
        ('asignacion_de_trabajador', 'Asignación de Trabajador'),
    ]
    
    aviso = models.ForeignKey('Aviso', on_delete=models.CASCADE, related_name="historial")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que realiza la acción
    accion = models.CharField(max_length=50, choices=ACCION_CHOICES)  # Tipo de acción
    comentario = models.TextField(blank=True, null=True)  # Detalles adicionales
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la acción

    def __str__(self):
        return f"{self.accion} para Aviso {self.aviso.id} por {self.usuario.username} el {self.fecha}"

    class Meta:
        verbose_name = 'Historial de Aviso'
        verbose_name_plural = 'Historiales de Avisos'
        ordering = ['-fecha']