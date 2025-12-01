"""Core registry utilities for defining UNNCLang statement-style macros."""
from __future__ import annotations

from dataclasses import dataclass
import inspect
from typing import Callable, Dict, Iterable, Iterator, Mapping, MutableMapping, Optional


@dataclass(frozen=True)
class StatementMacro:
    """Simple sentinel object that can live in Python source as a bare statement.

    The macro currently does not execute any runtime logic, but we keep a reference
    to the original handler to enable richer static transformations later on.
    """

    name: str
    handler: Optional[Callable[..., None]] = None
    doc: Optional[str] = None

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<UNNCLang statement '{self.name}'>"

    def __call__(self, *args, **kwargs):  # pragma: no cover - usage guard
        raise RuntimeError(
            f"UNNCLang statement '{self.name}' cannot be called like a function. "
            "Use it as a bare statement instead, e.g. just write the name on its own line."
        )


class MacroRegistry:
    """Holds onto every statement macro we register."""

    def __init__(self) -> None:
        self._macros: Dict[str, StatementMacro] = {}

    def register(self, macro: StatementMacro, *, overwrite: bool = False) -> None:
        if not overwrite and macro.name in self._macros:
            raise ValueError(f"Macro '{macro.name}' already exists. Pass overwrite=True to replace it.")
        self._macros[macro.name] = macro

    def get(self, name: str) -> StatementMacro:
        return self._macros[name]

    def items(self) -> Iterator[tuple[str, StatementMacro]]:
        return iter(self._macros.items())

    def as_dict(self, names: Optional[Iterable[str]] = None) -> Dict[str, StatementMacro]:
        if names is None:
            return dict(self._macros)
        return {name: self._macros[name] for name in names}


_registry = MacroRegistry()


def statement_macro(*, name: Optional[str] = None, doc: Optional[str] = None, overwrite: bool = False):
    """Decorator that turns a plain Python function into a UNNCLang statement macro."""

    def decorator(func: Callable[..., None]) -> StatementMacro:
        macro_name = name or func.__name__
        macro = StatementMacro(name=macro_name, handler=func, doc=doc or func.__doc__)
        _registry.register(macro, overwrite=overwrite)
        return macro

    return decorator


def export_macros(
    namespace: Optional[MutableMapping[str, object]] = None,
    *,
    names: Optional[Iterable[str]] = None,
    overwrite: bool = False,
) -> Mapping[str, StatementMacro]:
    """Inject all (or a subset of) macros into the provided namespace.

    If *namespace* is omitted we default to the caller's global scope so that
    `export_macros()` can be invoked directly inside user scripts.
    """

    if namespace is None:
        frame = inspect.currentframe()
        if frame is None or frame.f_back is None:  # pragma: no cover - safety net
            raise RuntimeError("Unable to determine caller frame for export_macros().")
        namespace = frame.f_back.f_globals

    selected = _registry.as_dict(names)
    for macro_name, macro in selected.items():
        if not overwrite and macro_name in namespace:
            continue
        namespace[macro_name] = macro
    return selected


def registered_macro_names() -> list[str]:
    return list(dict(_registry.items()).keys())


__all__ = [
    "StatementMacro",
    "MacroRegistry",
    "statement_macro",
    "export_macros",
    "registered_macro_names",
]
