from django.contrib import admin

from .models import CambioContador, LecturaAbonado

# Register your models here.
class CambioContadorAdmin(admin.ModelAdmin):
    list_display=("contrato","direccion","numero_viejo", "numero_nuevo", "imagen_viejo", "imagen_nuevo","fecha_cambio","notas", "actualizado_compass")
    search_fields=("contrato", "direccion", "numero_viejo", "numero_nuevo")
    readonly_fields=("created", "updated") #por ser autorellenables hay que añadirlos manualmente para verlos en el panel.admin

class LecturaAbonadoAdmin(admin.ModelAdmin):
    list_display=("contrato","direccion","contador", "lectura", "fecha_lectura","notas", "imagen_aviso","imagen_contador","grabada")
    search_fields=("contrato", "direccion", "contador")
    readonly_fields=("created", "updated") #por ser autorellenables hay que añadirlos manualmente para verlos en el panel.admin
    

admin.site.register(CambioContador, CambioContadorAdmin )
    

admin.site.register(LecturaAbonado, LecturaAbonadoAdmin )