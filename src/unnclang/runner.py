"""Simple runner / preprocessor utilities for UNNCLang demo files.

This module is intentionally tiny: it performs small, line-oriented
transformations so teaching-style files (with `then:` / `otherwise` / `endif`)
can be executed as Python after a quick rewrite.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional


def _preprocess(text: str) -> str:
    out_lines: list[str] = []
    for raw in text.splitlines():
        stripped = raw.lstrip()
        indent = raw[: len(raw) - len(stripped)]
        # if ... then:  -> if ...:
        if stripped.startswith("if") and stripped.endswith("then:"):
            new = stripped[:-5].rstrip() + ":"
            out_lines.append(indent + new)
            continue
        # otherwise -> else:
        if stripped == "otherwise":
            out_lines.append(indent + "else:")
            continue
        # endif -> remove line
        if stripped == "endif":
            continue
        out_lines.append(raw)
    return "\n".join(out_lines)


def run_uncl(path: str | Path, *, set_vars: Optional[Dict[str, object]] = None) -> None:
    """Read a UNNCLang-style file, preprocess it and execute as Python.

    Parameters
    - path: path to the source file (relative or absolute)
    - set_vars: optional dict of variables to pre-populate in the execution namespace
    """
    p = Path(path)
    text = p.read_text(encoding="utf8")
    py = _preprocess(text)
    ns: dict = {"__name__": "__main__"}
    if set_vars:
        ns.update(set_vars)
    exec(py, ns)


__all__ = ["run_uncl"]
