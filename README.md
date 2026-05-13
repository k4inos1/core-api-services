# Core API Services

Backend Django unificado para exponer servicios REST de los dominios consolidados en este repositorio.

## Arquitectura actual

- **`inventario_escolar`**: proyecto base y configuración compartida.
- **`equipos`**: API del inventario escolar original.
- **`entregables`**: app portada desde `aplicacion_django` con vehículos, operarios, mantenciones, faenas e incidentes.
- **`api`**: app portada desde `ev_4_django` con mantenimiento industrial, recursos, eventos y componentes de IA.
- **Django REST Framework** y **django-filter** quedan configurados globalmente para filtros, búsqueda y ordenamiento.

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
```

## Ejecución

```bash
python manage.py runserver
```

## Endpoints principales

- `/equipos/` — inventario escolar existente.
- `/entregables/vehiculos/`, `/entregables/operarios/`, `/entregables/mantenciones/`, `/entregables/faenas/`, `/entregables/incidentes/`.
- `/api/equipos/`, `/api/mantenimientos/`, `/api/recursos/`, `/api/eventos/`, `/api/datos-entrenamiento/`, `/api/modelos-ia/`, `/api/recomendaciones/`.
- `/api/db/tables/`, `/api/db/stats/`, `/api/db/browse/`, `/api/ia-dashboard/evolution/`, `/api/ia-dashboard/data_pipeline/`.

## Desarrollo

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test --verbosity=2
```

## Dependencias unificadas

El archivo `requirements.txt` mantiene únicamente las dependencias necesarias para este backend consolidado: Django, Django REST Framework y django-filter.
