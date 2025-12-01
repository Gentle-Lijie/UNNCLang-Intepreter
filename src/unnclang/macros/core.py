"""Default, built-in UNNCLang statement macros."""
from __future__ import annotations

from ..registry import statement_macro

__all__ = ["endif"]


@statement_macro(doc="Marks the end of a conditional block in UNNCLang-style code.")
def endif():
    """Placeholder macro used to emulate `endif` from the teaching language."""
    # There is intentionally no runtime logic here.
    # Having the symbol defined allows Python to parse scripts that close blocks
    # with `endif`, even though native Python relies solely on indentation.
    return None
