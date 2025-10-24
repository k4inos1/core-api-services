from django.db import models


class Equipo(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
