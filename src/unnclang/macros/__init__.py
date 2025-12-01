"""Collection of built-in UNNCLang macros."""
from __future__ import annotations

from . import core as _core
from .core import *  # noqa: F401,F403 - re-export user-facing macros

__all__ = list(_core.__all__)
