from django.db import models
from django.contrib.auth import get_user_model


class Equipo(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CambioEquipo(models.Model):
    """Registro de cambios en un Equipo para trazabilidad/auditoría."""
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE,
                               related_name='cambios')  # Referencia al equipo modificado
    modified_field = models.CharField(max_length=50)
    valor_anterior = models.CharField(
        max_length=255, blank=True)  # Valor anterior del campo
    valor_nuevo = models.CharField(
        max_length=255, blank=True)  # Nuevo valor del campo
    fecha_modificacion = models.DateTimeField(
        auto_now_add=True)  # Fecha y hora del cambio
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cambios_realizados'
    )  # Usuario que realizó el cambio

    class Meta:
        ordering = ['-fecha_modificacion']

    def __str__(self):
        equipo_str = str(self.equipo)
        if len(equipo_str) > 20:
            equipo_str = f"{equipo_str[:17]}..."
        field_str = self.modified_field
        if len(field_str) > 15:
            field_str = f"{field_str[:12]}..."
        fecha_str = self.fecha_modificacion.strftime("%Y-%m-%d %H:%M")
        return f"{field_str} change in '{equipo_str}' @ {fecha_str}"
