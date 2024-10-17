from django.contrib import admin
from .models import ControlDiario, ControlDiarioLinea

# Register your models here.

from .models import LineaAgenda

class LineaAgendaAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista
    list_display = ('usuario', 'fecha_inicio', 'hora_inicio', 'fecha_fin', 'hora_fin', 'descripcion')
    
    # Filtros para que los administradores puedan filtrar las entradas
    list_filter = ('usuario', 'fecha_inicio', 'fecha_fin')  # Filtro por usuario y fechas
    
    # Barra de búsqueda
    search_fields = ('usuario__username', 'descripcion')  # Buscar por nombre de usuario o descripción
    
    # Ordenar por la fecha de inicio
    ordering = ('fecha_inicio', 'hora_inicio')  # Ordenar primero por fecha, luego por hora
    
    # Habilitar jerarquía de fechas para ver las entradas por día
    date_hierarchy = 'fecha_inicio'
    
    # Definir el número de entradas por página
    list_per_page = 20
    
    # Personalizar el formulario de edición
    fieldsets = (
        (None, {
            'fields': ('usuario', 'fecha_inicio', 'hora_inicio', 'fecha_fin', 'hora_fin', 'descripcion')
        }),
    )

# Registrar el modelo con su administrador
admin.site.register(LineaAgenda, LineaAgendaAdmin)

class ControlDiarioAdmin(admin.ModelAdmin):
    list_display = ("id", "año", "mes", "created", "updated")  # Agregar los campos a la lista de visualización
    search_fields = ("año", "mes")
    readonly_fields = ("created", "updated")  # Campos de solo lectura

    list_filter = ("año", "mes")
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si hay un objeto, vuelve solo a 'created' y 'updated'
            return self.readonly_fields + ('año', 'mes')
        return self.readonly_fields

admin.site.register(ControlDiario, ControlDiarioAdmin)

class ControlDiarioLineaAdmin(admin.ModelAdmin):
    list_display = ("control_diario", "dia", "punto", "responsable")
    search_fields = ("control_diario__año", "control_diario__mes", "dia")
    list_filter = ("control_diario", "responsable")
    readonly_fields = ("responsable",)

admin.site.register(ControlDiarioLinea, ControlDiarioLineaAdmin)