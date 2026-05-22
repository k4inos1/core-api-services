from django.apps import apps
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DatoEntrenamiento, Equipo, Evento, ModeloIA, Mantenimiento, Recomendacion, Recurso
from .serializers import (
    DatoEntrenamientoSerializer,
    EquipoSerializer,
    EventoSerializer,
    ModeloIASerializer,
    MantenimientoSerializer,
    RecomendacionSerializer,
    RecursoSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class EquipoViewSet(BaseViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    search_fields = ['nombre', 'empresa_nombre', 'numero_serie']
    ordering_fields = ['nombre', 'es_critico', 'fecha_creacion']


class MantenimientoViewSet(BaseViewSet):
    queryset = Mantenimiento.objects.select_related('equipo').all()
    serializer_class = MantenimientoSerializer
    search_fields = ['descripcion', 'tecnico_asignado']
    ordering_fields = ['prioridad', 'fecha_programada', 'estado']


class RecursoViewSet(BaseViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    search_fields = ['nombre', 'especialidad']
    ordering_fields = ['tipo', 'nombre', 'calificacion']


class EventoViewSet(BaseViewSet):
    queryset = Evento.objects.select_related('equipo').all()
    serializer_class = EventoSerializer
    search_fields = ['descripcion']
    ordering_fields = ['severidad', 'fecha_evento', 'resuelto']


class DatoEntrenamientoViewSet(BaseViewSet):
    queryset = DatoEntrenamiento.objects.all()
    serializer_class = DatoEntrenamientoSerializer
    search_fields = ['consulta', 'contenido_raw']
    ordering_fields = ['fecha_creacion']


class ModeloIAViewSet(BaseViewSet):
    queryset = ModeloIA.objects.all()
    serializer_class = ModeloIASerializer
    search_fields = ['nombre', 'version', 'estado']
    ordering_fields = ['activo', 'precision_actual', 'fecha_creacion']


class RecomendacionViewSet(BaseViewSet):
    queryset = Recomendacion.objects.select_related('equipo').all()
    serializer_class = RecomendacionSerializer
    search_fields = ['titulo', 'descripcion', 'accion_sugerida']
    ordering_fields = ['prioridad', 'confianza', 'fecha_creacion']


class DatabaseExplorerViewSet(viewsets.ViewSet):
    serializer_class = None

    @action(detail=False, methods=['get'])
    def tables(self, request):
        tables_info = []
        for model in apps.get_app_config('api').get_models():
            tables_info.append(
                {
                    'name': model._meta.db_table,
                    'model': model.__name__,
                    'count': model.objects.count(),
                    'fields': [field.name for field in model._meta.fields],
                }
            )
        return Response({'tables': tables_info})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response(
            {
                'total_equipos': Equipo.objects.count(),
                'equipos_criticos': Equipo.objects.filter(es_critico=True).count(),
                'total_mantenimientos': Mantenimiento.objects.count(),
                'mantenimientos_pendientes': Mantenimiento.objects.filter(estado=1).count(),
                'total_recursos': Recurso.objects.count(),
                'recursos_disponibles': Recurso.objects.filter(disponible=True).count(),
                'total_eventos': Evento.objects.count(),
                'eventos_no_resueltos': Evento.objects.filter(resuelto=False).count(),
                'total_datos_ia': DatoEntrenamiento.objects.count(),
                'datos_ia_usados': DatoEntrenamiento.objects.filter(usado_entrenamiento=True).count(),
            }
        )

    @action(detail=False, methods=['get'])
    def browse(self, request):
        table_name = request.query_params.get('table', 'equipo')
        limit = int(request.query_params.get('limit', 10))
        model_map = {
            'equipo': Equipo,
            'mantenimiento': Mantenimiento,
            'recurso': Recurso,
            'evento': Evento,
            'dato_entrenamiento': DatoEntrenamiento,
            'modelo_ia': ModeloIA,
            'recomendacion': Recomendacion,
        }
        model = model_map.get(table_name)
        if not model:
            return Response({'error': 'Tabla no encontrada'}, status=400)

        data = []
        for obj in model.objects.all()[:limit]:
            item = {}
            for field in model._meta.fields:
                value = getattr(obj, field.name)
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                elif isinstance(value, (dict, list)):
                    value = str(value)
                item[field.name] = value
            data.append(item)

        return Response(
            {
                'table': table_name,
                'count': model.objects.count(),
                'data': data,
                'fields': [field.name for field in model._meta.fields],
            }
        )


class IADashboardViewSet(viewsets.ViewSet):
    serializer_class = ModeloIASerializer

    @action(detail=False, methods=['get'])
    def evolution(self, request):
        modelo = ModeloIA.objects.filter(activo=True).first()
        if not modelo:
            modelo = ModeloIA.objects.create(
                nombre='EV4-ML-Model',
                version='1.0.0',
                hiperparametros={'epochs': 100, 'learning_rate': 0.001},
            )
        return Response(
            {
                'nombre': modelo.nombre,
                'version': modelo.version,
                'precision_actual': modelo.precision_actual,
                'datos_entrenamiento': modelo.datos_entrenamiento,
                'epocas_completadas': modelo.epocas_completadas,
                'historial': modelo.historial_metricas,
                'estado': modelo.estado,
                'hiperparametros': modelo.hiperparametros,
            }
        )

    @action(detail=False, methods=['get'])
    def data_pipeline(self, request):
        total = DatoEntrenamiento.objects.count()
        usados = DatoEntrenamiento.objects.filter(usado_entrenamiento=True).count()
        por_conjunto = {
            'train': DatoEntrenamiento.objects.filter(conjunto='train').count(),
            'val': DatoEntrenamiento.objects.filter(conjunto='val').count(),
            'test': DatoEntrenamiento.objects.filter(conjunto='test').count(),
        }
        return Response(
            {
                'total_datos': total,
                'datos_usados': usados,
                'datos_disponibles': total - usados,
                'distribucion': por_conjunto,
                'porcentaje_uso': (usados / total * 100) if total > 0 else 0,
            }
        )
