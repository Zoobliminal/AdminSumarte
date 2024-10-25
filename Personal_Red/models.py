from django.db import models
from django.contrib.auth.models import User

class LineaAgenda(models.Model): # Modelo para las lineas de la agenda diaria Personal_Red
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Asociado al usuario actual
    fecha_inicio = models.DateField()  # Fecha de inicio del evento
    hora_inicio = models.TimeField()  # Hora de inicio del evento
    fecha_fin = models.DateField()  # Fecha de fin del evento
    hora_fin = models.TimeField()  # Hora de fin del evento
    descripcion = models.CharField(max_length=255, blank=True, null=True)  # Descripción opcional del evento

    def __str__(self):
        return f"Evento de {self.usuario.username} desde {self.fecha_inicio} {self.hora_inicio} hasta {self.fecha_fin} {self.hora_fin}"



# Modelo para el control diario (hoja mensual)
class ControlDiario(models.Model):
    año = models.IntegerField()
    mes = models.IntegerField(choices=[(i, i) for i in range(1, 13)])  # Lista de meses
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        unique_together = ('año', 'mes')  # Garantiza que no se repita el mes y año

    def __str__(self):
        return f"Registro {self.nombre_mes()} {self.año}"

    def nombre_mes(self):
        meses = [
            "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
        ]
        return meses[self.mes - 1]  # Restamos 1 porque la lista es cero-indexada

    
    

# Modelo para el control  diario (un registro cada día)
class ControlDiarioLinea(models.Model):
    control_diario = models.ForeignKey(ControlDiario, on_delete=models.CASCADE, related_name="dias")
    dia = models.IntegerField()  # Día del mes
    punto = models.CharField(max_length=10)  # Cambiado a CharField con un límite de caracteres de 10
    cloro_libre = models.DecimalField(max_digits=3, decimal_places=1, help_text="Concentración de Cloro libre en ppm (≤ 1,0 ppm)")
    cloro_combinado = models.DecimalField(max_digits=3, decimal_places=1, help_text="Concentración de Cloro combinado en ppm (≤ 2,0 ppm)")
    ph = models.DecimalField(max_digits=3, decimal_places=1, help_text="Nivel de pH (6,5 – 9,5)")
    turbidez = models.DecimalField(max_digits=3, decimal_places=1, help_text="Nivel de turbidez en UNF (≤ 4 UNF)")
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="registros_mensuales")

    class Meta:
        unique_together = ('control_diario', 'dia')  # Un día solo puede tener un registro para ese mes
        
    def save(self, *args, **kwargs):
        # Convertir 'punto' a mayúsculas antes de guardar
        self.punto = self.punto.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Registro Día {self.dia} - Punto {self.punto}"


class CambioZona(models.Model):
    poblacion_abastecida = models.CharField(max_length=100)
    origen_agua = models.CharField(max_length=100)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    motivo_cambio = models.TextField()

    def __str__(self):
        return f"Cambio en {self.poblacion_abastecida} - Inicio: {self.fecha_hora_inicio}"

class TratamientoAgua(models.Model):
    fecha_mantenimiento = models.DateField()
    tipo_mantenimiento = models.CharField(max_length=100)  # Ej. "Cloración", "Revisión"
    sustancia_empleada = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100)  # O puedes usar un ForeignKey si tienes un modelo de Proveedor
    documentacion_disponible = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Mantenimiento {self.tipo_mantenimiento} - {self.sustancia_empleada} ({self.fecha_mantenimiento})"

class ManipuladorAlimentos(models.Model):
    manipulador = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona al trabajador
    actividad_en_empresa = models.CharField(max_length=200)
    formacion = models.CharField(max_length=100)  # Ej. "Manipulador de alimentos"
    fecha_certificado = models.DateField()

    def __str__(self):
        return f"{self.manipulador} - {self.tarea_realizada} - {self.fecha_certificado}"