from django.contrib import admin
# from .models import AgendaHoja   

# Register your models here.
admin.site.site_header ="ADMINISTRACION SUMARTE"
admin.site.index_title ="Secciones"


# class AgendaHojaAdmin(admin.ModelAdmin):
#     list_display=("fecha_hoja","trabajador", "created", "updated")
#     search_fields=("fecha_hoja","trabajador")
#     readonly_fields=("created", "updated") #por ser autorellenables hay que añadirlos manualmente para verlos en el panel.admin
    

# admin.site.register(AgendaHoja, AgendaHojaAdmin )