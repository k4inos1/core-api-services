from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import EquipoFilter
from .models import Equipo
from .serializers import EquipoSerializer


@api_view(['GET'])
def lista_equipos(request):
    """Devuelve un listado JSON de equipos filtrado por parámetros de consulta."""
    queryset = Equipo.objects.all().order_by('id')
    filtro = EquipoFilter(request.GET, queryset=queryset)
    serializer = EquipoSerializer(filtro.qs, many=True)
    return Response({'cantidad': len(serializer.data), 'resultados': serializer.data})
