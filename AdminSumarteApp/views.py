from django.shortcuts import render, HttpResponse
from django.template import Template, Context
from django.shortcuts import render
# from AdminSumarteApp.models import AgendaHoja
from django.conf import settings
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.

def home(request):  
    return render (request, "AdminSumarteApp/home.html")

#def cambios_contador(request):
#    return render (request, "AdminSumarteApp/cambios_contador.html")

def gestion_corte(request):
    listaComentarios=["Comentario de usuario que se pueda decir que es un comentario algo largo, para ver el formateo del campo de texto 1","Comentario de usuario 2", "Comentario de usuario 3"]
    return render (request, "AdminSumarteApp/gestion_corte.html", {"comentarios":listaComentarios})


# def fichaje(request):
#     return render (request, "AdminSumarteApp/fichaje.html")



@login_required(login_url="/accounts/login/login")
def calendario_jornada(request):
    fecha= datetime.datetime.now()
    formatFecha = str(fecha.day) + " / " + str(fecha.month) + " / " + str(fecha.year)
    return render (request, "AdminSumarteApp/calendario_jornada_inicio.html",{"fecha_actual":formatFecha})
    #nombre=""
    #AgendaHojas=AgendaHoja.objects.filter(trabajador__icontains=nombre)
    #return render (request, "AdminSumarteApp/calendario_jornada.html",{"AgendaHojas":AgendaHojas})
    

def busca_hoja_jornada(request):
   
    # try:
    #    is_private = request.POST['is_private']
    #except MultiValueDictKeyError:
    #   is_private = False
    try:
        if request.GET["select_nombre"]:
            nombre = request.GET["select_nombre"]     
            fecha= datetime.datetime.now()
            format_fecha = str(fecha.day) + " / " + str(fecha.month) + " / " + str(fecha.year)  
            AgendaHojas=AgendaHoja.objects.filter(trabajador__icontains='Diego', fecha_hoja__icontains=format_fecha) # icontains es igual al LIKE de SQL 
                                                                        # LIKE raqueta: devuelve raquetass, araquetas...etc
    except:
        nombre="Diego"
               
    return render(request, "calendario_jornada.html", {"AgendaHojas":AgendaHojas})