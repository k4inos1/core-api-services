from django.contrib import admin
from .models import Vehiculo, Operario, Mantencion, Faena, RegistroIncidente


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    """Administración de vehículos forestales"""
    list_display = ['patente', 'tipo', 'marca', 'modelo', 'año', 'estado', 'horas_uso']
    list_filter = ['tipo', 'estado', 'marca', 'año']
    search_fields = ['patente', 'marca', 'modelo']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('patente', 'tipo', 'marca', 'modelo', 'año')
        }),
        ('Estado y Operación', {
            'fields': ('estado', 'horas_uso', 'capacidad_carga')
        }),
        ('Fechas', {
            'fields': ('fecha_adquisicion', 'fecha_creacion')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Operario)
class OperarioAdmin(admin.ModelAdmin):
    """Administración de operarios forestales"""
    list_display = ['nombre', 'rut', 'rol', 'licencia', 'activo', 'fecha_ingreso']
    list_filter = ['rol', 'activo', 'fecha_ingreso']
    search_fields = ['nombre', 'rut']
    date_hierarchy = 'fecha_ingreso'
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('rut', 'nombre', 'telefono')
        }),
        ('Información Laboral', {
            'fields': ('rol', 'licencia', 'fecha_ingreso', 'activo')
        }),
    )


@admin.register(Mantencion)
class MantencionAdmin(admin.ModelAdmin):
    """Administración de mantenciones"""
    list_display = ['vehiculo', 'tipo', 'estado', 'fecha_programada', 'fecha_realizada', 'costo', 'mecanico']
    list_filter = ['tipo', 'estado', 'fecha_programada', 'vehiculo']
    search_fields = ['vehiculo__patente', 'descripcion']
    date_hierarchy = 'fecha_programada'
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('vehiculo', 'tipo', 'estado')
        }),
        ('Descripción', {
            'fields': ('descripcion', 'repuestos_utilizados')
        }),
        ('Fechas', {
            'fields': ('fecha_programada', 'fecha_realizada', 'fecha_creacion')
        }),
        ('Responsable y Costos', {
            'fields': ('mecanico', 'costo', 'horas_vehiculo')
        }),
    )


@admin.register(Faena)
class FaenaAdmin(admin.ModelAdmin):
    """Administración de faenas forestales"""
    list_display = ['nombre', 'tipo', 'ubicacion', 'vehiculo', 'operario', 'estado', 'fecha_inicio', 'metros_cubicos']
    list_filter = ['tipo', 'estado', 'fecha_inicio', 'vehiculo']
    search_fields = ['nombre', 'ubicacion']
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo', 'ubicacion', 'estado')
        }),
        ('Asignación', {
            'fields': ('vehiculo', 'operario')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_termino', 'fecha_creacion')
        }),
        ('Métricas', {
            'fields': ('metros_cubicos', 'hectareas')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )


@admin.register(RegistroIncidente)
class RegistroIncidenteAdmin(admin.ModelAdmin):
    """Administración de registros de incidentes de seguridad"""
    list_display = ['faena', 'tipo', 'gravedad', 'fecha_incidente', 'operario_involucrado', 'reportado_por']
    list_filter = ['tipo', 'gravedad', 'fecha_incidente']
    search_fields = ['descripcion', 'faena__nombre', 'reportado_por']
    date_hierarchy = 'fecha_incidente'
    
    fieldsets = (
        ('Información del Incidente', {
            'fields': ('faena', 'tipo', 'gravedad', 'fecha_incidente')
        }),
        ('Descripción', {
            'fields': ('descripcion', 'medidas_tomadas')
        }),
        ('Involucrados', {
            'fields': ('operario_involucrado', 'vehiculo_involucrado', 'reportado_por')
        }),
    )
