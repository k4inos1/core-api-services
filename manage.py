#!/usr/bin/env python
import os
import sys
import importlib
import importlib.util
import pkgutil

if not hasattr(pkgutil, "find_loader"):
    from typing import Optional
    from importlib.machinery import ModuleSpec

    def _find_loader(name: str) -> Optional[ModuleSpec]:
        return importlib.util.find_spec(name)

    setattr(pkgutil, "find_loader", _find_loader)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'inventario_escolar.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError() from exc

    try:
        from django.template.context import BaseContext

        def _basecontext_copy_safe(self):
            duplicate = self.__class__.__new__(self.__class__)
            if hasattr(self, '__dict__'):
                duplicate.__dict__.update(self.__dict__)
            if hasattr(self, 'dicts'):
                duplicate.dicts = list(self.dicts)
            return duplicate

        try:
            BaseContext.__copy__ = _basecontext_copy_safe
        except Exception:
            pass
    except Exception:
        pass
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
