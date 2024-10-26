from django.contrib import admin
from .models import Instalacion

@admin.register(Instalacion)
class InstalacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'ubicacion', 'fecha_creacion')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'ubicacion')
    ordering = ('fecha_creacion',)
    date_hierarchy = 'fecha_creacion'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()  # Optimiza las consultas a la base de datos

from .models import InspeccionMensualDeposito, InspeccionAnualDeposito

@admin.register(InspeccionMensualDeposito)
class InspeccionMensualDepositoAdmin(admin.ModelAdmin):
    list_display = ('instalacion', 'fecha_programada', 'fecha_realizada', 'trabajador', 'elementos_cierre', 'senalizacion', 'estado_valvulas', 'canalizaciones', 'instalaciones')
    list_filter = ('instalacion', 'fecha_programada', 'trabajador', 'elementos_cierre', 'senalizacion', 'estado_valvulas')
    search_fields = ('instalacion__nombre', 'observaciones', 'trabajador__username')
    date_hierarchy = 'fecha_programada'
    list_editable = ('fecha_realizada', 'trabajador', 'elementos_cierre', 'senalizacion', 'estado_valvulas', 'canalizaciones', 'instalaciones')
    ordering = ('-fecha_programada',)
    fieldsets = (
        (None, {
            'fields': ('instalacion', 'fecha_programada', 'fecha_realizada', 'trabajador')
        }),
        ('Estado de Inspección', {
            'fields': ('elementos_cierre', 'senalizacion', 'estado_valvulas', 'canalizaciones', 'instalaciones', 'observaciones')
        }),
    )


@admin.register(InspeccionAnualDeposito)
class InspeccionAnualDepositoAdmin(admin.ModelAdmin):
    list_display = ('instalacion', 'fecha_programada', 'fecha_realizada', 'trabajador', 'revision_fisuras', 'revision_corrosion', 'revision_materiales_sellado', 'revision_paramentos_exteriores', 'existencia_sedimentos')
    list_filter = ('instalacion', 'fecha_programada', 'trabajador', 'revision_fisuras', 'revision_corrosion', 'revision_materiales_sellado')
    search_fields = ('instalacion__nombre', 'observaciones', 'trabajador__username')
    date_hierarchy = 'fecha_programada'
    list_editable = ('fecha_realizada', 'trabajador', 'revision_fisuras', 'revision_corrosion', 'revision_materiales_sellado', 'revision_paramentos_exteriores', 'existencia_sedimentos')
    ordering = ('-fecha_programada',)
    fieldsets = (
        (None, {
            'fields': ('instalacion', 'fecha_programada', 'fecha_realizada', 'trabajador')
        }),
        ('Revisiones', {
            'fields': ('revision_fisuras', 'revision_corrosion', 'revision_materiales_sellado', 'revision_paramentos_exteriores', 'existencia_sedimentos', 'observaciones')
        }),
    )
