from django.http import JsonResponse, HttpRequest
from .models import Equipo
from .filters import EquipoFilter


def lista_equipos(request: HttpRequest) -> JsonResponse:
    """Devuelve un listado JSON de equipos filtrado por parámetros de consulta.
    """
    # Queryset base ordenado por id
    queryset = Equipo.objects.all().order_by('id')

    # Aplicar filtros usando django-filter
    filtro = EquipoFilter(request.GET, queryset=queryset)

    # Serializar campos seleccionados a una lista de diccionarios
    resultados = list(
        filtro.qs.values('id', 'nombre', 'categoria',
                         'estado', 'ubicacion', 'fecha_ingreso')
    )

    return JsonResponse({'cantidad': len(resultados), 'resultados': resultados})
