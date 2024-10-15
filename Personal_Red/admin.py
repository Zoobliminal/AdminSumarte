from django.contrib import admin
from .models import ControlDiario, ControlDiarioLinea

# Register your models here.
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