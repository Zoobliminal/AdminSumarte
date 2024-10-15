from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from Avisos.models import Aviso, imageComentAviso
from Autenticacion.models import PerfilUsuario  
from .models import trabajadorAsignadoAviso, HistorialAviso
from .forms import formImageComentAviso, AsignarTrabajadorForm, NuevoAvisoForm, editarAvisoForm
from .telegram_utils import send_telegram_message
from django.core.paginator import Paginator
import requests

# Avisos/views.py

from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .data_to_load import load_initial_data

@staff_member_required  # Solo personal autorizado puede ejecutar esto
def cargar_datos_iniciales(request):
    load_initial_data()
    return HttpResponse("Datos iniciales cargados con éxito.")

# Create your views here.
@login_required(login_url="/accounts/login/login")
def avisos(request):
    avisos=Aviso.objects.all()
    imagenes=imageComentAviso.objects.all()
    trabajadores=trabajadorAsignadoAviso.objects.all()
    
    ahora = timezone.now()
    
   
    # Verificar si se ha enviado el checkbox para filtrar por avisos asignados al usuario
    #if 'mis_avisos' in request.GET:
    
    # Filtrar por avisos en los que el usuario conectado está asignado como trabajador y no está finalizado
    if not request.user.is_staff:
        avisos = avisos.filter(asignamientos__trabajador=request.user, finalizado=False) 
    else: #Para los admins mostrar todos los abiertos y cerrados hace menos de 48 horas
        avisos = Aviso.objects.filter(finalizado=False) | Aviso.objects.filter(finalizado=True,fecha_resolucion__gte=ahora - timedelta(hours=48)  
    )
    
    avisos = avisos.order_by('finalizado', '-created') 
   
    if request.method == 'POST':
        form = formImageComentAviso(request.POST, request.FILES)
        if form.is_valid():
            form.aviso_id = avisos.id
            form.usuario = request.user
            form.save()
    else:
        form = formImageComentAviso()
    
    context = {
        "avisos":avisos,  
        "imagenes":imagenes, 
        "trabajadores":trabajadores, 
        "form_comentario":formImageComentAviso,
        "form_trabajadores":AsignarTrabajadorForm, 
        
    }
        
    return render(request, 'Avisos/avisos.html', context)



@method_decorator(staff_member_required, name='dispatch')
class EditarAvisoView(UpdateView):
    model = Aviso
    form_class = editarAvisoForm
    template_name = 'Avisos/aviso_editar.html'
    success_url = reverse_lazy('avisos')

    def form_valid(self, form):
        # Puedes agregar lógica adicional aquí si es necesario
        return super().form_valid(form)


@staff_member_required(login_url="/accounts/login/login")
def reabrir_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)
    
    if aviso.finalizado:
        aviso.finalizado = False
        aviso.estatus = 'pendiente'  # Puedes cambiar esto al estado deseado
        aviso.fecha_resolucion = None  # Remover la fecha de resolución 
        aviso.save()
        
        # Registrar el cambio en el historial si lo tienes
        HistorialAviso.objects.create(
            aviso=aviso,
            usuario=request.user,
            accion='reapertura',
            comentario='El aviso fue reabierto.'
        )
    
    return redirect('avisos')  


   
@staff_member_required(login_url="/accounts/login/login")
def asignar_trabajador(request, aviso_id):
    
    aviso = get_object_or_404(Aviso, id=aviso_id)
   
    if request.method == 'POST':
        form = AsignarTrabajadorForm(request.POST)
        
        if form.is_valid():
            try:
                asignacion = form.save(commit=False)
                asignacion.aviso = aviso
                asignacion.save()
                
                 # Verificar si se debe enviar notificación
                if 'enviar_notificacion_telegram' in request.POST: 
                    Perfil = PerfilUsuario.objects.filter(user=asignacion.trabajador).first()  # Obtener el perfil del trabajador
                    Chat_id_Usuario = Perfil.chat_id
                    usuario_autenticado = request.user.username  
                    fecha_formateada = aviso.created.strftime('%d/%m/%Y - %H:%M')
                    message =   (f"*NUEVO AVISO:*\n\n"
                                                        
                                 f"*Nombre:* {aviso.nombre}\n\n" 
                                 f"*Tlf.contacto:* {aviso.telefono}\n\n" 
                                 f"*Fecha del aviso:* {fecha_formateada}\n\n"   
                                 f"*Dirección:* {aviso.direccion}\n\n"
                                 f"*Motivo:* {aviso.motivo}\n\n"
                                 f"*Asignación registrada por {usuario_autenticado}*\n\n"   
                                 #f"www.sumarte.gal"
                                )
                               
                    send_telegram_message(Chat_id_Usuario, message) 
                              
                return redirect('avisos')  
            except Exception as e:
                print(e)
                return redirect('avisos') 
            
        form = AsignarTrabajadorForm(aviso=aviso)
        
    # Contexto para la plantilla
    context ={
        'aviso': aviso,
        'form_trabajadores': form,  # Instancia del formulario
        #'perfiles': perfiles,  # Lista de perfiles para selección
    }
    
    # Renderizar la plantilla
    return render(request, 'Avisos/avisos.html', context)





# def send_telegram_message(chat_id, message):
#     url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
#     payload = {
#         'chat_id': chat_id,
#         'text': message,
#         'parse_mode': 'Markdown'  # O 'HTML' si lo configuramos como HTML
#     }
#     response = requests.post(url, data=payload)
#     return response.json()



@login_required(login_url="/accounts/login/login")
def agregarImageComentAviso(request, aviso_id):
    # Obtener el aviso por id
    aviso = get_object_or_404(Aviso, id=aviso_id)
    
    # Obtener todas las imágenes relacionadas con el aviso (no es necesario obtener la imagen por usuario)
    imagenes = imageComentAviso.objects.filter(aviso=aviso)
    
    if request.method == 'POST':
        # Formulario para añadir comentario/imagen
        form = formImageComentAviso(request.POST, request.FILES)
        if form.is_valid():
            # Crear una instancia del formulario pero no guardarla aún
            comentario = form.save(commit=False)
            # Asignar el aviso y el usuario antes de guardar
            comentario.aviso = aviso  # Asegúrate de que este aviso no es None
            comentario.usuario = request.user
            comentario.save()  # Guardar finalmente
            
                                   
        return redirect('avisos')  
    
        
    else:
        form = formImageComentAviso()  # Crear una instancia del formulario vacío

    # Contexto para la plantilla
    context = {
        'aviso': aviso,         
        'imagenes': imagenes,   # Imágenes relacionadas con este aviso
        'form_comentario': form, # Instancia del formulario, no la clase
    }
    
    # Renderizar la plantilla
    return render(request, 'Avisos/avisos.html', context)



@login_required(login_url="/accounts/login/login")
def eliminar_comentario(request, comentario_id):
    
    comentario = get_object_or_404(imageComentAviso, id=comentario_id)
    
    # Verificar que el usuario sea el propietario del comentario
    if comentario.usuario == request.user:
        comentario.delete()
        
    return redirect('avisos')



@staff_member_required(login_url="/accounts/login/login")
def eliminar_asignacion(request, trabajador_id):
    
    asignacion = get_object_or_404(trabajadorAsignadoAviso, id=trabajador_id)
   
    asignacion.delete()
    
    return redirect('avisos')




@login_required(login_url="/accounts/login/login")
def cambiar_estado(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)
    
    if request.method == 'POST':
        nuevo_estatus = request.POST.get('estatus')
        if nuevo_estatus in ['pendiente', 'en_proceso', 'resuelto', 'sin_resolver']:
            aviso.estatus = nuevo_estatus
            aviso.finalizado = False
        else:
            aviso.estatus = nuevo_estatus
            aviso.fecha_resolucion = timezone.now()
            aviso.finalizado = True

        aviso.save()
            
        # Registrar el cambio de estado en el historial
        HistorialAviso.objects.create(
        aviso=aviso,
        usuario=request.user,
        accion='cambio_de_estado',
        comentario=f'El estado fue cambiado a {nuevo_estatus}.')
        
        return redirect('avisos')  # Redirigir a la vista que muestra los avisos

    return redirect('avisos')  # Si no es POST, simplemente redirige



def avisos_cerrados(request):
    avisos_list = Aviso.objects.filter(finalizado=True).order_by('-created')  # Filtrar y ordenar los avisos cerrados
    paginator = Paginator(avisos_list, 10)  # Mostrar 10 avisos por página
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Avisos/avisos_cerrados.html', {'page_obj': page_obj})
    # avisos=Aviso.objects.all()
    # return render (request, "Avisos/avisos_cerrados.html",{"avisos":avisos})
   


def aviso_nuevo(request):
    if request.method == 'POST':
        form_nuevoAviso = NuevoAvisoForm(request.POST)
        if form_nuevoAviso.is_valid():
            aviso = form_nuevoAviso.save(commit=False)
            aviso.Usuario = request.user  # Asigna el usuario conectado al aviso
            aviso.save()
            return redirect('avisos')  # Redirige a la lista de avisos o donde desees
    else:
        form_nuevoAviso = NuevoAvisoForm()
    
    return render(request, 'avisos/aviso_nuevo.html', {'form': form_nuevoAviso})   


@login_required(login_url="/accounts/login/login")
def aviso_detalle(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)
    trabajadores_asignados = aviso.asignamientos.all()  # assuming 'asignamientos' is the related_name
    comentarios = aviso.imageComentAvisos.all()  # assuming 'imageComentAvisos' is the related_name

    context = {
        'aviso': aviso,
        'trabajadores_asignados': trabajadores_asignados,
        'comentarios': comentarios,
    }
    return render(request, 'Avisos/aviso_detalle.html', context)


   