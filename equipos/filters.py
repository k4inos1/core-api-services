import django_filters
from .models import Equipo


class EquipoFilter(django_filters.FilterSet):
    fecha_ingreso = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Equipo
        fields = {
            'categoria': ['exact', 'icontains'],
            'estado': ['exact', 'icontains'],
            'ubicacion': ['exact', 'icontains'],
            'fecha_ingreso': ['exact'],
        }
