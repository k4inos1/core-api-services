# Evaluación — Backend (TI3041 Ev.2)

Este repositorio contiene la implementación del ejercicio de evaluación **TI3041 Ev.2**. El propósito inmediato de este commit es iniciar el proyecto, documentar los requerimientos extraídos del material entregado y dejar instrucciones claras para continuar con el desarrollo e integración en GitHub.

## Resumen ejecutivo

Basado en la "Escala de Apreciación – TI3041 Ev.2" (documento recibido), el ejercicio es una evaluación práctica de backend. El objetivo principal es entregar un servicio backend que cumpla criterios funcionales, de calidad y documentación. Aquí se lista un análisis de requerimientos, criterios de aceptación y un plan de trabajo.

## Requerimientos (extraídos / inferidos)

Nota: el PDF original contiene la rúbrica de evaluación. Donde falta detalle técnico he inferido suposiciones razonables (las enumero abajo). Si prefieres que siga exactamente el enunciado del PDF explícame qué apartados debo priorizar.

- Requerimientos funcionales (esperados):
  - Implementar una API RESTful para la lógica solicitada en la evaluación.
  - Endpoints básicos: CRUD para la(s) entidad(es) principales (crear, leer, actualizar, eliminar).
  - Validaciones de entrada y manejo claro de errores con códigos HTTP adecuados.
  - Persistencia: uso de una base de datos (puede ser SQLite/Postgres/MySQL según lo requerido).

- Requerimientos no-funcionales / de calidad:
  - Documentación (README + ejemplos de uso / Postman collection o OpenAPI/Swagger).
  - Pruebas automatizadas (al menos tests unitarios y 1 test de integración básico).
  - Manejo de dependencias y scripts de ejecución claros.
  - Estilo, estructura del proyecto y código legible.

- Criterios de evaluación (según la escala):
  - Funcionamiento (endpoints implementados y correctos).
  - Calidad del código (claridad, modularidad, manejo de errores).
  - Documentación y evidencia (README, instrucciones, ejemplos).
  - Tests y cobertura mínima (según rúbrica).

## Supuestos razonables (confirmar si es necesario)

1. El lenguaje y stack no están prescritos: propondré Node.js (Express) o Python (FastAPI) si no hay restricción. Indica preferencia y convertiré la plantilla.
2. La evaluación requiere un CRUD sobre una entidad simple (por ejemplo: usuarios, productos o tareas).
3. Se solicita un repositorio remoto en GitHub; inicialmente crearé el repo local y te daré pasos concretos para crear y vincular el remoto.

Si alguno de estos supuestos es incorrecto, indícalo y ajusto el plan.

## Entregables mínimos (primer sprint)

- Proyecto inicial con estructura de backend.
- README con requerimientos, cómo instalar y ejecutar, API doc mínima.
- Git repo con commit inicial y `.gitignore`.

## Estructura propuesta del repositorio

```
/ (repo)
├─ README.md
├─ .gitignore
├─ src/              # código fuente
├─ tests/            # pruebas automatizadas
├─ docs/             # documentación adicional (postman/openapi)
├─ package.json OR pyproject.toml
└─ .env.example
```

## Cómo continuar — pasos recomendados

1. Confirmar stack (Node.js/Express o Python/FastAPI/u otro).
2. Definir entidad/es y campos obligatorios.
3. Implementar endpoints y pruebas mínimas.
4. Documentar con OpenAPI o Postman.
5. Crear repo remoto en GitHub y configurar CI (GitHub Actions) para tests.

## Instrucciones para crear el repositorio remoto en GitHub (opciones)

Opción A — Usando la CLI de GitHub (`gh`):

1. Instalar y autenticar `gh` si no está instalado.
2. Desde la carpeta del proyecto ejecutar:

```powershell
cd "C:\Users\Ricardo\evaluacion backend"
gh repo create <nombre-repo> --public --source=. --remote=origin --push
```

Reemplaza `<nombre-repo>` por el nombre deseado. `--public` puede cambiar a `--private` si quieres repositorio privado.

Opción B — Web UI:

1. Crear un nuevo repositorio en https://github.com/new
2. No marques crear README (ya existe), y luego sigue las instrucciones para añadir el remote y push:

```powershell
cd "C:\Users\Ricardo\evaluacion backend"
git remote add origin https://github.com/<tu-usuario>/<nombre-repo>.git
git branch -M main
git push -u origin main
```

## Notas finales

- He inicializado el README y el `.gitignore` localmente y creado un commit inicial (ver historial de acciones).  
- Indícame qué stack prefieres y si quieres que cree la estructura de proyecto base con dependencias, ejemplos de endpoints y tests; puedo generarlo y ejecutar pruebas rápidamente.

---

Autor: Equipo de desarrollo (plantilla inicial)
Fecha: (commit inicial)
