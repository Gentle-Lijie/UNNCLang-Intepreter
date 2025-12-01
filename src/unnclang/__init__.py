"""UNNCLang macro helpers for CELEN086 teaching language."""
from __future__ import annotations

from .registry import export_macros, registered_macro_names, statement_macro
from . import macros as _macros  # noqa: F401  - ensure built-ins register on import
from .macros import *  # noqa: F401,F403 - re-export macros for convenience
from .runner import run_uncl
import builtins

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


# Convenience export so students can call `unnclang.run_uncl("demo.uncl")`.
__all__.append("run_uncl")


# By default, inject statement macros into the builtins namespace so that
# scripts which `import unnclang` can use bare statement names like `endif`
# as expression-statements without needing to call `load_macros(globals())`.
# This is convenient in teaching environments; call `disable_builtin_macros()`
# to remove the injected names if you need a cleaner global scope.
def _inject_macros_into_builtins():
    try:
        export_macros(builtins.__dict__)
    except Exception:
        # Be permissive: don't make import fail if injection isn't possible.
        pass


def disable_builtin_macros():
    """Remove known macro names from the builtins namespace.

    Use this if you need to avoid any side-effects from importing `unnclang`.
    """
    for name in registered_macro_names():
        if hasattr(builtins, name):
            try:
                delattr(builtins, name)
            except Exception:
                # best-effort removal
                try:
                    del builtins.__dict__[name]
                except Exception:
                    pass


# Perform the injection at import time (convenient for students).
_inject_macros_into_builtins()
