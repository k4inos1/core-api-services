from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import re


class Vehiculo(models.Model):
    """Modelo para representar vehículos y maquinaria forestal"""
    TIPOS = [
        ('camion', 'Camión Forestal'),
        ('cosechadora', 'Cosechadora Forestal'),
        ('skidder', 'Skidder'),
        ('grua', 'Grúa Forestal'),
        ('camioneta', 'Camioneta'),
        ('excavadora', 'Excavadora'),
    ]
    
    ESTADOS = [
        ('operativo', 'Operativo'),
        ('en_mantencion', 'En Mantención'),
        ('fuera_servicio', 'Fuera de Servicio'),
        ('reparacion', 'En Reparación'),
    ]
    
    patente = models.CharField(max_length=10, unique=True, verbose_name="Patente")
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo de Vehículo")
    marca = models.CharField(max_length=100, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    año = models.IntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name="Año"
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='operativo', verbose_name="Estado")
    horas_uso = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Horas de Uso",
        help_text="Total de horas de operación"
    )
    capacidad_carga = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Capacidad de Carga (ton)",
        help_text="Capacidad en toneladas"
    )
    fecha_adquisicion = models.DateField(verbose_name="Fecha de Adquisición")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.patente} - {self.get_tipo_display()}"
    
    def requiere_mantencion(self):
        """Verifica si el vehículo requiere mantención (cada 500 horas)"""
        return self.horas_uso % 500 < 50 and self.horas_uso > 0


class Operario(models.Model):
    """Modelo para representar operarios forestales"""
    ROLES = [
        ('operador', 'Operador de Maquinaria'),
        ('chofer', 'Chofer'),
        ('mecanico', 'Mecánico'),
        ('supervisor', 'Supervisor de Faena'),
        ('jefe_cuadrilla', 'Jefe de Cuadrilla'),
    ]
    
    rut = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="RUT",
        help_text="Formato: 12345678-9"
    )
    nombre = models.CharField(max_length=200, verbose_name="Nombre Completo")
    rol = models.CharField(max_length=20, choices=ROLES, verbose_name="Rol")
    licencia = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Licencia de Conducir",
        help_text="Ej: A1, A2, A3, A4, A5"
    )
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    fecha_ingreso = models.DateField(default=timezone.now, verbose_name="Fecha de Ingreso")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Operario"
        verbose_name_plural = "Operarios"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_rol_display()}"
    
    @staticmethod
    def validar_rut(rut):
        """Valida formato y dígito verificador de RUT chileno"""
        rut = rut.replace('.', '').replace('-', '').upper()
        if len(rut) < 2:
            return False
        
        cuerpo = rut[:-1]
        dv = rut[-1]
        
        if not cuerpo.isdigit():
            return False
        
        # Algoritmo de validación
        suma = 0
        multiplo = 2
        for i in reversed(cuerpo):
            suma += int(i) * multiplo
            multiplo = multiplo + 1 if multiplo < 7 else 2
        
        dv_calculado = 11 - (suma % 11)
        dv_calculado = 'K' if dv_calculado == 10 else ('0' if dv_calculado == 11 else str(dv_calculado))
        
        return dv == dv_calculado


class Mantencion(models.Model):
    """Modelo para representar mantenciones de vehículos"""
    TIPOS = [
        ('preventiva', 'Preventiva'),
        ('correctiva', 'Correctiva'),
        ('emergencia', 'Emergencia'),
        ('revision', 'Revisión Técnica'),
    ]
    
    ESTADOS = [
        ('programada', 'Programada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='mantenciones',
        verbose_name="Vehículo"
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo de Mantención")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='programada', verbose_name="Estado")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_programada = models.DateField(verbose_name="Fecha Programada")
    fecha_realizada = models.DateField(null=True, blank=True, verbose_name="Fecha Realizada")
    mecanico = models.ForeignKey(
        Operario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mantenciones_realizadas',
        verbose_name="Mecánico Responsable"
    )
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Costo (CLP)"
    )
    repuestos_utilizados = models.TextField(blank=True, verbose_name="Repuestos Utilizados")
    horas_vehiculo = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Horas del Vehículo",
        help_text="Horas de uso al momento de la mantención"
    )
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro")
    
    class Meta:
        verbose_name = "Mantención"
        verbose_name_plural = "Mantenciones"
        ordering = ['-fecha_programada']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.vehiculo.patente} ({self.fecha_programada})"
    
    def esta_vencida(self):
        """Verifica si la mantención programada está vencida"""
        if self.estado == 'completada':
            return False
        return timezone.now().date() > self.fecha_programada


class Faena(models.Model):
    """Modelo para representar faenas forestales"""
    ESTADOS = [
        ('planificada', 'Planificada'),
        ('en_curso', 'En Curso'),
        ('pausada', 'Pausada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPOS = [
        ('corta', 'Corta de Árboles'),
        ('transporte', 'Transporte de Troncos'),
        ('plantacion', 'Plantación'),
        ('raleo', 'Raleo'),
        ('limpieza', 'Limpieza de Terreno'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la Faena")
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo de Faena")
    ubicacion = models.CharField(
        max_length=200,
        verbose_name="Ubicación",
        help_text="Sector forestal o coordenadas"
    )
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='faenas',
        verbose_name="Vehículo Asignado"
    )
    operario = models.ForeignKey(
        Operario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='faenas_asignadas',
        verbose_name="Operario Responsable"
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='planificada', verbose_name="Estado")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_termino = models.DateField(null=True, blank=True, verbose_name="Fecha de Término")
    metros_cubicos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Metros Cúbicos (m³)",
        help_text="Volumen de madera procesada"
    )
    hectareas = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Hectáreas",
        help_text="Superficie trabajada"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro")
    
    class Meta:
        verbose_name = "Faena"
        verbose_name_plural = "Faenas"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"
    
    def duracion_dias(self):
        """Calcula la duración de la faena en días"""
        if self.fecha_termino:
            return (self.fecha_termino - self.fecha_inicio).days
        return (timezone.now().date() - self.fecha_inicio).days


class RegistroIncidente(models.Model):
    """Modelo para registrar incidentes de seguridad en faenas"""
    TIPOS = [
        ('accidente', 'Accidente'),
        ('incidente', 'Incidente'),
        ('casi_accidente', 'Casi Accidente'),
        ('condicion_insegura', 'Condición Insegura'),
    ]
    
    GRAVEDAD = [
        ('leve', 'Leve'),
        ('moderado', 'Moderado'),
        ('grave', 'Grave'),
        ('critico', 'Crítico'),
    ]
    
    faena = models.ForeignKey(
        Faena,
        on_delete=models.CASCADE,
        related_name='incidentes',
        verbose_name="Faena"
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo de Incidente")
    gravedad = models.CharField(max_length=20, choices=GRAVEDAD, verbose_name="Gravedad")
    descripcion = models.TextField(verbose_name="Descripción del Incidente")
    fecha_incidente = models.DateTimeField(default=timezone.now, verbose_name="Fecha del Incidente")
    operario_involucrado = models.ForeignKey(
        Operario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidentes',
        verbose_name="Operario Involucrado"
    )
    vehiculo_involucrado = models.ForeignKey(
        Vehiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidentes',
        verbose_name="Vehículo Involucrado"
    )
    medidas_tomadas = models.TextField(blank=True, verbose_name="Medidas Tomadas")
    reportado_por = models.CharField(max_length=200, verbose_name="Reportado Por")
    
    class Meta:
        verbose_name = "Registro de Incidente"
        verbose_name_plural = "Registros de Incidentes"
        ordering = ['-fecha_incidente']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.faena.nombre} ({self.fecha_incidente.date()})"
