"""UNNCLang macro helpers for CELEN086 teaching language."""
from __future__ import annotations

from .registry import export_macros, registered_macro_names, statement_macro
from . import macros as _macros  # noqa: F401  - ensure built-ins register on import
from .macros import *  # noqa: F401,F403 - re-export macros for convenience

__all__ = [
    "statement_macro",
    "export_macros",
    "registered_macro_names",
    *_macros.__all__,
]

__version__ = "0.1.0"


def load_macros(namespace=None, *, names=None, overwrite: bool = False):
    """Alias for :func:`export_macros` kept for a friendlier public API."""

    return export_macros(namespace, names=names, overwrite=overwrite)
