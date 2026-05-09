from django.contrib import admin
from typing import TYPE_CHECKING

from .models import Equipo
from .models import CambioEquipo


if TYPE_CHECKING:
    from django.contrib import admin as _admin
    from .models import Equipo as _EquipoType, CambioEquipo as _CambioEquipoType

    BaseEquipoAdmin = _admin.ModelAdmin[_EquipoType]
    BaseCambioAdmin = _admin.ModelAdmin[_CambioEquipoType]
else:
    BaseEquipoAdmin = admin.ModelAdmin
    BaseCambioAdmin = admin.ModelAdmin


@admin.register(Equipo)
class EquipoAdmin(BaseEquipoAdmin):

    list_display = ('nombre', 'categoria', 'estado',
                    'fecha_ingreso', 'ubicacion')
    list_filter = ('categoria', 'estado', 'ubicacion')
    search_fields = ('nombre', 'categoria', 'ubicacion')
    ordering = ('-fecha_ingreso',)


@admin.register(CambioEquipo)
class CambioEquipoAdmin(BaseCambioAdmin):

    list_display = ('equipo', 'modified_field', 'valor_anterior',
                    'valor_nuevo', 'fecha_modificacion', 'usuario')
    readonly_fields = ('equipo', 'modified_field', 'valor_anterior',
                       'valor_nuevo', 'fecha_modificacion', 'usuario')
    fields = readonly_fields
    search_fields = ('equipo__nombre', 'modified_field', 'usuario')
    ordering = ('-fecha_modificacion',)
