
from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo de usuario
    chat_id = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Campo para chat_id de Telegram
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado") 
    
    def __str__(self):
        return f'Perfil de {self.user.username}'