# CARGA AUTOMATICA DE DATOS FICTICIOS INICIALES
# http://localhost:8000/avisos/cargar_datos_iniciales/


from .models import Aviso, trabajadorAsignadoAviso
from django.contrib.auth.models import User, Group

def load_initial_data():
    
     # Crear el grupo Administracion con permisos de staff
    admin_group, created = Group.objects.get_or_create(name='Administracion')
    
    # Crear el grupo Trabajadores sin permisos de staff
    trabajadores_group, created = Group.objects.get_or_create(name='Trabajadores')
    
     # Crear un superusuario si no existe
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        admin_user.groups.add(admin_group)  # Asignar al grupo Administracion
    
    # Crear usuarios de ejemplo
    if not User.objects.filter(username='admin_user').exists():
        admin_user = User.objects.create_user('admin_user', 'admin_user@example.com', 'password')
        admin_user.is_staff = True  # Permiso de staff
        admin_user.save()
        admin_user.groups.add(admin_group)  # Asignar al grupo Administracion

    if not User.objects.filter(username='trabajador1').exists():
        trabajador1 = User.objects.create_user('Diego.Boedo', 'diego.boedo@sumarte.gal', 'adminadmin')
        trabajador1.is_staff = False  # Sin permisos de staff
        trabajador1.save()
        trabajador1.groups.add(trabajadores_group)  # Asignar al grupo Trabajadores

    if not User.objects.filter(username='trabajador2').exists():
        trabajador2 = User.objects.create_user('Manel.Puente', 'manel.puente@sumarte.gal', 'adminadmin')
        trabajador2.is_staff = False  # Sin permisos de staff
        trabajador2.save()
        trabajador2.groups.add(trabajadores_group)  # Asignar al grupo Trabajadores
        
    if not User.objects.filter(username='trabajador3').exists():
        trabajador3 = User.objects.create_user('Martina.Chaos', 'martina.chaos@sumarte.gal', 'adminadmin')
        trabajador3.is_staff = True  # Con permisos de staff
        trabajador3.save()
        trabajador3.groups.add(admin_group)  # Asignar al grupo Administracion



   

    # Crear avisos de ejemplo
    aviso1 = Aviso.objects.create(
        Usuario=trabajador3,
        contrato="12345",
        nombre="Joaquín Sabina",
        telefono="123456789",
        registro="A-001",
        direccion="Boulevard de los sueños rotos, 44",
        motivo="Fuga de agua",
        estatus="pendiente"
    )

    aviso2 = Aviso.objects.create(
        Usuario=trabajador3,
        contrato="54321",
        nombre="Residente",
        telefono="987654321",
        registro="A-002",
        direccion="Calle 13",
        motivo="Avería alcantarillado",
        estatus="En_proceso"
    )
    
    aviso3 = Aviso.objects.create(
        Usuario=trabajador3,
        contrato="22122",
        nombre="Manu Chao",
        telefono="123456789",
        registro="A-001",
        direccion="Av. Estación Esperanza, sn",
        motivo="Fuga de agua",
        estatus="pendiente"
    )

    aviso4 = Aviso.objects.create(
        Usuario=trabajador3,
        contrato="54321",
        nombre="Julio Iglesias",
        telefono="987654321",
        registro="A-002",
        direccion="Avenida Meicende 742",
        motivo="Avería eléctrica",
        estatus="resuelto"
    )
    
    aviso5 = Aviso.objects.create(
        Usuario=trabajador3,
        contrato="54321",
        nombre="Lola Flores",
        telefono="987654321",
        registro="A-002",
        direccion="Plaza Galicia 72",
        motivo="Avería general",
        estatus="cerrardo"
    )
    

    # Asignar trabajadores a avisos
    trabajadorAsignadoAviso.objects.create(aviso=aviso1, trabajador=trabajador1)
    trabajadorAsignadoAviso.objects.create(aviso=aviso2, trabajador=trabajador2)
    trabajadorAsignadoAviso.objects.create(aviso=aviso4, trabajador=trabajador2)
    
    print("Datos iniciales de usuarios y grupos cargados correctamente.")
