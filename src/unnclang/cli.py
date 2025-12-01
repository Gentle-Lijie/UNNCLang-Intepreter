#!/usr/bin/env python3
"""Command-line interface for UNNCLang runner.

Provides the `uncl` entry point which reads a UNNCLang-style file, optionally
sets variables, and executes it via `run_uncl`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict

from .runner import run_uncl


def parse_set_vars(pairs: list[str]) -> Dict[str, object]:
    result: Dict[str, object] = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(f"Invalid --set-var value: {pair!r}. Use name=value")
        name, val = pair.split("=", 1)
        # simple literal parsing: try int, float, else keep string
        if val.isdigit():
            parsed: object = int(val)
        else:
            try:
                parsed = float(val)
            except Exception:
                parsed = val
        result[name] = parsed
    return result


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="uncl", description="Run UNNCLang-style file")
    parser.add_argument("file", help="Path to UNNCLang source file (e.g. demo.uncl)")
    parser.add_argument(
        "--set-var",
        "-s",
        action="append",
        default=[],
        help="Set a variable before execution (name=value). Can be used multiple times.",
    )

    ns = parser.parse_args(argv)
    p = Path(ns.file)
    if not p.exists():
        raise SystemExit(f"File not found: {p}")

    set_vars = parse_set_vars(ns.set_var)
    # run_uncl will raise NameError if variables (like `a`) are not defined — leave that behaviour
    run_uncl(p, set_vars=set_vars if set_vars else None)


if __name__ == "__main__":
    main()
