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


