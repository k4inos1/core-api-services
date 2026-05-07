from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Faena, Mantencion, Operario, RegistroIncidente, Vehiculo
from .serializers import (
    FaenaSerializer,
    MantencionSerializer,
    OperarioSerializer,
    RegistroIncidenteSerializer,
    VehiculoSerializer,
)


class BaseForestalViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class VehiculoViewSet(BaseForestalViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filterset_fields = ['tipo', 'estado', 'activo']
    search_fields = ['patente', 'marca', 'modelo']
    ordering_fields = ['fecha_creacion', 'horas_uso', 'año']


class OperarioViewSet(BaseForestalViewSet):
    queryset = Operario.objects.all()
    serializer_class = OperarioSerializer
    filterset_fields = ['rol', 'activo']
    search_fields = ['rut', 'nombre', 'telefono']
    ordering_fields = ['nombre', 'fecha_ingreso']


class MantencionViewSet(BaseForestalViewSet):
    queryset = Mantencion.objects.select_related('vehiculo', 'mecanico').all()
    serializer_class = MantencionSerializer
    filterset_fields = ['tipo', 'estado', 'vehiculo', 'mecanico']
    search_fields = ['descripcion', 'repuestos_utilizados']
    ordering_fields = ['fecha_programada', 'fecha_realizada', 'costo']


class FaenaViewSet(BaseForestalViewSet):
    queryset = Faena.objects.select_related('vehiculo', 'operario').all()
    serializer_class = FaenaSerializer
    filterset_fields = ['tipo', 'estado', 'vehiculo', 'operario', 'activo']
    search_fields = ['nombre', 'ubicacion', 'observaciones']
    ordering_fields = ['fecha_inicio', 'fecha_termino', 'fecha_creacion']


class RegistroIncidenteViewSet(BaseForestalViewSet):
    queryset = RegistroIncidente.objects.select_related(
        'faena', 'operario_involucrado', 'vehiculo_involucrado'
    ).all()
    serializer_class = RegistroIncidenteSerializer
    filterset_fields = ['tipo', 'gravedad', 'faena']
    search_fields = ['descripcion', 'reportado_por', 'medidas_tomadas']
    ordering_fields = ['fecha_incidente']
