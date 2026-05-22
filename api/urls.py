from rest_framework.routers import DefaultRouter

from .views import (
    DatabaseExplorerViewSet,
    DatoEntrenamientoViewSet,
    EquipoViewSet,
    EventoViewSet,
    IADashboardViewSet,
    ModeloIAViewSet,
    MantenimientoViewSet,
    RecomendacionViewSet,
    RecursoViewSet,
)

router = DefaultRouter()
router.register('equipos', EquipoViewSet, basename='api-equipo')
router.register('mantenimientos', MantenimientoViewSet, basename='api-mantenimiento')
router.register('recursos', RecursoViewSet, basename='api-recurso')
router.register('eventos', EventoViewSet, basename='api-evento')
router.register('datos-entrenamiento', DatoEntrenamientoViewSet, basename='api-dato-entrenamiento')
router.register('modelos-ia', ModeloIAViewSet, basename='api-modelo-ia')
router.register('recomendaciones', RecomendacionViewSet, basename='api-recomendacion')
router.register('db', DatabaseExplorerViewSet, basename='api-db')
router.register('ia-dashboard', IADashboardViewSet, basename='api-ia-dashboard')

urlpatterns = router.urls
