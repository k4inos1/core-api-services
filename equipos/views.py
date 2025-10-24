from django.http import JsonResponse
from django.views import View
from .models import Equipo
from .filters import EquipoFilter


def equipos_list(request):
    """Return a JSON list of equipos filtered by query params.

    Supported params: categoria, estado, ubicacion, fecha_ingreso_after, fecha_ingreso_before
    Uses django-filter for flexible filtering via query params.
    """
    qs = Equipo.objects.all().order_by('id')
    f = EquipoFilter(request.GET, queryset=qs)
    qs_filtered = f.qs
    data = list(qs_filtered.values('id', 'nombre', 'categoria', 'estado', 'fecha_ingreso', 'ubicacion'))
    return JsonResponse({'count': len(data), 'results': data})
