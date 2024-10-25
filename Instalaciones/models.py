from django.db import models
from django.contrib.auth.models import User


class Instalacion(models.Model):
    TIPO_INSTALACION = [
        ('DEP', 'Depósito'),
        ('BOM', 'Bombeo'),
        ('ETAP', 'Estación de Tratamiento de Agua Potable'),
        ('EDAR', 'Estación de Depuración de Aguas Residuales'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=4, choices=TIPO_INSTALACION)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"




class InspeccionMensualDeposito(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE, related_name='inspecciones_mensuales')
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(blank=True, null=True)
    trabajador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    elementos_cierre = models.BooleanField()
    senalizacion = models.BooleanField()
    estado_valvulas = models.BooleanField()
    canalizaciones = models.BooleanField()
    instalaciones = models.BooleanField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inspección Mensual de {self.instalacion}"




class InspeccionAnualDeposito(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE, related_name='inspecciones_anuales')
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(blank=True, null=True)
    trabajador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    revision_fisuras = models.CharField(max_length=20, choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')])
    revision_corrosion = models.CharField(max_length=20, choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')])
    revision_materiales_sellado = models.CharField(max_length=20, choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')])
    revision_paramentos_exteriores = models.CharField(max_length=20, choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')])
    existencia_sedimentos = models.CharField(max_length=20, choices=[('Correcto', 'Correcto'), ('No Correcto', 'No Correcto')])
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inspección Anual de {self.instalacion}"




class LimpiezaDeposito(models.Model):
    identificacion_deposito = models.CharField(max_length=100)
    fecha_hora_limpieza = models.DateTimeField()
    procedimiento = models.TextField(
        default=(
            "1. Vaciado del depósito por el desagüe de fondo.\n"
            "2. Barrido de los sólidos depositados sobre la superficie inferior hacia desagüe.\n"
            "3. Limpieza de las paredes y suelo con cepillos utilizando hipoclorito de sodio para la eliminación de suciedad y desinfección de superficies.\n"
            "4. Retirada de restos y aclarado con máquina de agua a presión (trabajando con agua tratada).\n"
            "5. Llenado del depósito hasta ¼ de la capacidad con agua limpia y posterior vaciado.\n"
            "6. Llenado definitivo del depósito con agua limpia comprobando continuamente el nivel de cloro hasta alcanzar el valor paramétrico deseado, normalmente entre 0,50 -0,70 mg/l.\n"
            "7. Apertura del depósito a red de distribución."
        )
    )
    fecha_hora_fin_limpieza = models.DateTimeField(blank=True, null=True)
    sustancias_empleadas = models.CharField(max_length=200)
    valor_cloro_medido = models.DecimalField(max_digits=5, decimal_places=2)  # En mg/l o ppm
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Limpieza de {self.identificacion_deposito} - {self.fecha_hora_limpieza}"




class MantenimientoRenovacion(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE, related_name='mantenimientos', null=True, blank=True)
    tipo_mantenimiento = models.CharField(max_length=50)  # Ej. "Cloración", "Revisión de equipo técnico"
    fecha_programada = models.DateField(blank=True, null=True)
    fecha_realizada = models.DateField(blank=True, null=True)
    trabajador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    detalles = models.TextField(blank=True, null=True)
    obras_a_realizar = models.CharField(max_length=200)
    trabajo_realizado = models.TextField(blank=True, null=True)
    inversion_inicial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Mantenimiento {self.tipo_mantenimiento} en {self.instalacion or 'Sin instalación asignada'}"




class MantenimientoCloracion(models.Model):
    semana_inicio = models.DateField()
    semana_fin = models.DateField()

    # Verificaciones de Bombas Dosificadoras
    fijacion_tuberias = models.BooleanField(default=False)
    racor_manguera = models.BooleanField(default=False)
    fugas_tanque_cloro = models.BooleanField(default=False)

    # Verificaciones de Dosificaciones
    comprobar_dosificaciones = models.BooleanField(default=False)
    niveles_depositos = models.BooleanField(default=False)
    cuba_reactivo = models.BooleanField(default=False)

    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Mantenimiento Cloración - Semana {self.semana_inicio} a {self.semana_fin}"       




class MantenimientoInfraestructura(models.Model):
    TIPO_INFRAESTRUCTURA = [
        ('PT', 'Planta de Tratamiento'),
        ('DEP', 'Depósito'),
        ('RD', 'Red de Distribución'),
    ]

    tipo_infraestructura = models.CharField(max_length=3, choices=TIPO_INFRAESTRUCTURA)
    fecha_prevista = models.DateField()
    fecha_realizada = models.DateField(blank=True, null=True)
    documentacion = models.FileField(upload_to='mantenimiento_documentacion/', blank=True, null=True)

    def __str__(self):
        return f"Mantenimiento {self.get_tipo_infraestructura_display()} - Previsto: {self.fecha_prevista}"



class MantenimientoEquipo(models.Model):
    TIPO_EQUIPO_CHOICES = [
        ('Clorador', 'Clorador'),
        ('Bomba', 'Bomba'),
        ('Filtro', 'Filtro'),
        # Añadir otros tipos de equipo según se requiera
    ]

    tipo_equipo = models.CharField(max_length=50, choices=TIPO_EQUIPO_CHOICES)
    tipo_mantenimiento = models.CharField(max_length=100)
    fecha_hora_limpieza = models.DateTimeField()
    proveedor = models.CharField(max_length=100)
    descripcion_trabajo = models.TextField()
    firma_responsable = models.CharField(max_length=100)
    documentacion = models.FileField(upload_to='documentacion_mantenimiento/', blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_equipo} - {self.tipo_mantenimiento} - {self.fecha_hora_limpieza}"


class RenovacionInstalacion(models.Model):
    obras_a_realizar = models.CharField(max_length=200)
    trabajo_realizado = models.TextField()
    fecha_prevista = models.DateField()
    inversion_inicial = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Renovación - {self.obra} - Fecha Prevista: {self.fecha_prevista}"

class Incidencia(models.Model):
    localizacion = models.CharField(max_length=200)
    fecha_hora_incidencia = models.DateTimeField()
    descripcion = models.TextField()
    medidas_correctoras = models.TextField()
    fecha_hora_puesta_a_punto = models.DateTimeField(blank=True, null=True)
    trabajador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Incidencia en {self.localizacion} - {self.fecha_hora_incidencia}"

class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    nombre_contacto = models.CharField(max_length=100)
    cif = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    correo_electronico = models.EmailField()
    servicios_productos = models.TextField()

    def __str__(self):
        return self.nombre_empresa