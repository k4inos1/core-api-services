# AGENTS.md — core-api-services guidance

Purpose
-------
Concise, actionable guidance for AI coding agents working in this repo.

Project layout
--------------
- Django project: core_api/
- Domain apps: api/, core_users/, core_notifications/, core_audit/, entregables/, equipos/

Key entry points
----------------
- README: ../README.md
- Django settings: ../core_api/settings.py
- URL config: ../core_api/urls.py
- Manage script: ../manage.py

Common commands (verify README before running)
---------------------------------------------
- Run server: python manage.py runserver
- Run tests: python -m pytest

Testing notes
-------------
- Pytest configuration: ../pytest.ini
- Tests live under ../tests/ and app-level tests.py files.
