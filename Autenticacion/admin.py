from .models import PerfilUsuario
from django.contrib import admin

# Register your models here.
class PerfilUsuarioAdmmin(admin.ModelAdmin):
    list_display=("user","chat_id", "created", "updated")
    search_fields=("user","chat_id")
    readonly_fields=("created", "updated") #por ser autorellenables hay que añadirlos manualmente para verlos en el panel.admin
    

admin.site.register(PerfilUsuario, PerfilUsuarioAdmmin )