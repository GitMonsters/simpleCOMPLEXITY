"""
Import restriction hooks for Worm Python
"""

from .import_restrictions import (
    install_import_restrictions,
    is_module_allowed,
    get_blocked_modules,
    WormImportError,
)

__all__ = [
    'install_import_restrictions',
    'is_module_allowed',
    'get_blocked_modules',
    'WormImportError',
]
