# Evaluación — Backend (TI3041 Ev.2)

Este repositorio contiene la implementación del ejercicio de evaluación **TI3041 Ev.2**. El propósito inmediato de este commit es iniciar el proyecto, documentar los requerimientos extraídos del material entregado y dejar instrucciones claras para continuar con el desarrollo e integración en GitHub.

## Resumen

Basado en la "Escala de Apreciación – TI3041 Ev.2" (documento recibido), el ejercicio es una evaluación práctica de backend. El objetivo principal es entregar un servicio backend que cumpla criterios funcionales, de calidad y documentación. Aquí se lista un análisis de requerimientos, criterios de aceptación y un plan de trabajo.

# TI3041 — Evaluación 2: Inventario Escolar (Django)

Resumen corto
------------
Este repositorio contiene la solución solicitada para la Evaluación N°2 (Programación Backend, TI3041) — una aplicación Django mínima que implementa el modelo y la gestión de equipos requerida por la guía: proyecto `inventario_escolar`, app `equipos`, conexión a base de datos (SQLite) y uso del Django Admin.

Alcance
-------
Se implementaron únicamente los requerimientos de la guía de la evaluación:

- Crear proyecto Django `inventario_escolar`.
- Configurar conexión a base de datos (SQLite) en `settings.py`.
- Crear aplicación `equipos` y añadirla a `INSTALLED_APPS`.
- Definir el modelo `Equipo` con los campos: `nombre`, `categoria`, `estado`, `fecha_ingreso`, `ubicacion`.
- Ejecutar migraciones (migrations incluidas en el repo) y garantizar que `manage.py runserver` arranca.
- Registrar `Equipo` en Django Admin y personalizar la vista (requisito explícito).

Cambios intencionados para diferenciación
-----------------------------------------
El código se limitó a los requerimientos. Para aportar una diferencia útil respecto a implementaciones similares (p. ej. repositorios de compañeros) se hicieron pequeñas mejoras enfocadas en la usabilidad del Admin sin ampliar el alcance funcional:

- Admin: además de `list_display` requerido, se añadieron `list_filter`, `search_fields` y `ordering` para una gestión más cómoda de registros desde el Admin. Esto no altera la funcionalidad requerida pero mejora la experiencia al evaluar/administrar datos.

Estructura del repositorio
--------------------------
```
ti3041-ev2-backend/
├─ manage.py
├─ requirements.txt
├─ inventario_escolar/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
└─ equipos/
   # TI3041 — Evaluación 2: Inventario Escolar (Backend Django)

   Este repositorio contiene la implementación de la evaluación práctica **TI3041 Ev.2**: una aplicación backend sencilla para la gestión de equipos escolares.

   ## Resumen rápido

   - Proyecto Django: `inventario_escolar`
   - App principal: `equipos` (modelo `Equipo` + auditoría `CambioEquipo`)
   - Base de datos por defecto: SQLite (configurada en `settings.py`)
   - Admin de Django personalizado para gestión rápida
   - Scripts útiles: `seed_equipos` (poblar datos), `ensure_superuser` (crear superusuario no interactivo)

   ## Requisitos (recomendados)

   - Python 3.11 o 3.12 (funciona en 3.14 con un parche localizado en `manage.py`; ver nota de compatibilidad más abajo)
   - pip

   ## Instalación y ejecución (PowerShell)

   1. Abrir PowerShell y situarse en la carpeta del proyecto:

   ```powershell
   cd "C:\Users\Ricardo\evaluacion backend"
   ```

   2. Crear y activar el entorno virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   3. Instalar las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

   4. Migraciones y (opcional) crear un superusuario interactivo:

   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

   5. Alternativa: crear superusuario no interactivo (comando incluido):

   ```powershell
   python manage.py ensure_superuser --username admin --email admin@admin.com --password admin
   ```

   6. Cargar datos de ejemplo (opcional):

   ```powershell
   python manage.py seed_equipos --count 10
   ```

   7. Ejecutar el servidor de desarrollo:

   ```powershell
   python manage.py runserver
   ```

   Abrir el Admin: http://127.0.0.1:8000/admin/ (inicia sesión con el superusuario creado).

   ## Tests

   Ejecutar la suite de tests:

   ```powershell
   python manage.py test --verbosity=2
   ```

   ## Funcionalidades adicionales incluidas

   - Auditoría: `CambioEquipo` registra cambios por campo cuando se actualiza un `Equipo`.
   - Capa de servicios: `equipos/services.py` contiene funciones para crear/actualizar/dar de baja/eliminar equipos y registrar auditoría.
   - Admin:
     - `Equipo` con `list_display`, `list_filter`, `search_fields` y acciones (p. ej. marcar como "Dado de baja", exportar a CSV).
     - `CambioEquipo` registrado como solo lectura para inspección.
   - Comandos de gestión: `seed_equipos` y `ensure_superuser`.

   ## Nota de compatibilidad (importante)

   En algunos entornos de Python 3.14 se han observado incompatibilidades con bibliotecas o con el comportamiento de ciertas APIs internas. Para garantizar que esta evaluación sea reproducible en la máquina del evaluador se incluyó un parche localizado en `manage.py` que:

   - añade una pequeña compatibilidad para `pkgutil.find_loader` cuando no existe (mapea a `importlib.util.find_spec`), y
   - contiene una corrección defensiva para evitar un fallo conocido al copiar contextos de plantilla en ciertas versiones.

   Recomendación: para una entrega limpia, la opción preferible es usar Python 3.11 o 3.12 en lugar de 3.14; si prefieres, quito el parche antes de publicar el repositorio remoto y confirmamos la versión de Python objetivo.

   ## Checklist de aceptación (mapeo a la escala de apreciación)

   - [x] Proyecto Django creado (`inventario_escolar`) y app `equipos` registrada.
   - [x] Modelo `Equipo` con campos mínimos requeridos.
   - [x] Admin de Django registrado y personalizado (listados y filtros).
   - [x] Migraciones incluidas y ejecutables.
   - [x] `manage.py runserver` arranca en el entorno del evaluador (tras las correcciones aplicadas localmente).
   - [x] Tests básicos incluidos y verdes en el entorno del autor y del evaluador local (ver `equipos/tests*.py`).
   - [x] Seed data y comando para crear superusuario no interactivo incluidos.

   ## Siguientes pasos sugeridos (opcional)

   - Añadir API REST con Django REST Framework (endpoints CRUD para `Equipo` / `CambioEquipo`).
   - Añadir GitHub Actions que ejecuten tests automáticamente en cada push.
   - Dockerizar la aplicación para facilitar la evaluación en un contenedor reproducible.

   ## Cómo publicar en GitHub (resumen)

   1. Crear repo en GitHub (web UI o `gh`).
   2. Añadir remote y empujar `main`:

   ```powershell
   git remote add origin https://github.com/<tu-usuario>/ti3041-ev2-backend.git
   git branch -M main
   git push -u origin main
   ```

   ## Créditos / Autor

   Ricardo — implementación para la evaluación TI3041 Ev.2

