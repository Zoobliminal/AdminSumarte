from django.contrib import admin

from .models import Aviso, imageComentAviso, trabajadorAsignadoAviso

# Register your models here.
class AvisoAdmin(admin.ModelAdmin):
    list_display=("id","direccion","motivo","updated", "finalizado")
    search_fields=("nombre", "direccion", "finalizado")
    readonly_fields=("created", "updated") #por ser autorellenables hay que añadirlos manualmente para verlos en el panel.admin
    
class ImageComentAvisoAdmin(admin.ModelAdmin):
     list_display=("aviso","imagen","comentario","updated")
     readonly_fields=("created", "updated") #por ser autorellenables hay que añadirlos manualmente para verlos en el panel.admin
   
class trabajadorAsignadoAvisoAdmin(admin.ModelAdmin):
     list_display=("aviso","trabajador","updated")
     readonly_fields=("created", "updated") #por ser autorellenables hay que añadirlos manualmente para verlos en el panel.admin 
    
admin.site.register(Aviso, AvisoAdmin )
admin.site.register(imageComentAviso, ImageComentAvisoAdmin)
admin.site.register(trabajadorAsignadoAviso, trabajadorAsignadoAvisoAdmin)

