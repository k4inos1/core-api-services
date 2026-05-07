from rest_framework.routers import DefaultRouter

from .views import (
    FaenaViewSet,
    MantencionViewSet,
    OperarioViewSet,
    RegistroIncidenteViewSet,
    VehiculoViewSet,
)

router = DefaultRouter()
router.register('vehiculos', VehiculoViewSet, basename='entregables-vehiculo')
router.register('operarios', OperarioViewSet, basename='entregables-operario')
router.register('mantenciones', MantencionViewSet, basename='entregables-mantencion')
router.register('faenas', FaenaViewSet, basename='entregables-faena')
router.register('incidentes', RegistroIncidenteViewSet, basename='entregables-incidente')

urlpatterns = router.urls
