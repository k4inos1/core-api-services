from typing import Dict, Any, Optional
from contextlib import suppress
from django.contrib.auth import get_user_model

from .models import Equipo, CambioEquipo

UserModel = get_user_model()


def registrar_equipo(data: Dict[str, Any]) -> Equipo:
    """Crea y retorna un Equipo a partir de un diccionario de datos."""
    campos_permitidos = ['nombre', 'categoria',
                         'estado', 'fecha_ingreso', 'ubicacion']
    campos = {k: data[k] for k in campos_permitidos if k in data}
    return Equipo.objects.create(**campos)


def consultar_equipos(filtros: Dict[str, Any]):
    """Consulta equipos según los filtros proporcionados."""
    qs = Equipo.objects.all()
    if 'estado' in filtros and filtros['estado']:
        qs = qs.filter(estado=filtros['estado'])
    if 'ubicacion' in filtros and filtros['ubicacion']:
        qs = qs.filter(ubicacion=filtros['ubicacion'])
    if 'categoria' in filtros and filtros['categoria']:
        qs = qs.filter(categoria=filtros['categoria'])
    return qs


def registrar_cambio_equipo(
    equipo: Equipo,
    campo: str,
    valor_anterior: Any,
    valor_nuevo: Any,
    usuario: Optional[object] = None,
):
    """Registra un cambio en `CambioEquipo`.

    `usuario` puede ser un username (str), una instancia User o None. Si se
    recibe un username se intenta resolver al User correspondiente; si no se
    encuentra, se deja `usuario=None`.
    """
    user_obj = None
    if usuario:
        if isinstance(usuario, str):
            user_obj = UserModel.objects.filter(username=usuario).first()
        else:
            # Asumimos que es una instancia de User
            user_obj = usuario

    CambioEquipo.objects.create(
        equipo=equipo,
        modified_field=campo,
        valor_anterior=str(valor_anterior) if valor_anterior is not None else '',
        valor_nuevo=str(valor_nuevo) if valor_nuevo is not None else '',
        # fecha_modificacion es auto_now_add en el modelo; no es necesario
        usuario=user_obj,
    )


def actualizar_equipo(equipo_id: int, datos_actualizados: Dict[str, Any], usuario: str = '') -> Optional[Equipo]:
    """Actualiza un Equipo existente, registra los cambios y devuelve la instancia."""
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        return None

    cambios_realizados = False
    for campo, valor_nuevo in datos_actualizados.items():
        if hasattr(equipo, campo):
            valor_anterior = getattr(equipo, campo)
            if valor_anterior != valor_nuevo:
                setattr(equipo, campo, valor_nuevo)
                registrar_cambio_equipo(
                    equipo, campo, valor_anterior, valor_nuevo, usuario)
                cambios_realizados = True

    if cambios_realizados:
        equipo.save()

    return equipo


def dar_de_baja_equipo(equipo_id: int, usuario: str = '') -> Optional[Equipo]:
    try:
        equipo = Equipo.objects.get(id=equipo_id)
        valor_anterior = equipo.estado
        equipo.estado = 'Dado de baja'
        equipo.save()
        registrar_cambio_equipo(
            equipo, 'estado', valor_anterior, equipo.estado, usuario)
        return equipo
    except Equipo.DoesNotExist:
        return None


def eliminar_equipo(equipo_id: int, usuario: str = '') -> None:

    with suppress(Equipo.DoesNotExist):
        equipo = Equipo.objects.get(id=equipo_id)
        registrar_cambio_equipo(
            equipo,
            'eliminado',
            str(equipo),
            'Equipo eliminado',
            usuario
        )
        equipo.delete()
