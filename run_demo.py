#!/usr/bin/env python3
"""Runner for the minimal four-line UNNCLang demo (`demo.uncl`).

This script:
- inserts `src` into sys.path so `import unnclang` works without installation
- reads `demo.uncl`, applies tiny transformations:
  - converts `then:` after an if into `:`
  - removes `endif` lines
  (keeps indentation)
- sets `a = 2` in the execution namespace so the demo prints `1`
"""
from __future__ import annotations

import sys
from pathlib import Path


def add_src_to_path():
    root = Path(__file__).resolve().parent
    src = root / "src"
    sys.path.insert(0, str(src))


def preprocess(src: str) -> str:
    out: list[str] = []
    for raw in src.splitlines():
        stripped = raw.lstrip()
        indent = raw[: len(raw) - len(stripped)]
        # convert `if ... then:` -> `if ...:`
        if stripped.startswith("if") and stripped.endswith("then:"):
            new = stripped[:-5].rstrip() + ":"
            out.append(indent + new)
            continue
        # drop `endif`
        if stripped == "endif":
            continue
        out.append(raw)
    return "\n".join(out)


def main():
    add_src_to_path()
    demo_path = Path(__file__).resolve().parent / "demo.uncl"
    src = demo_path.read_text(encoding="utf8")
    py = preprocess(src)

    print("--- Transformed code ---")
    print(py)
    print("------------------------")

    ns: dict = {"__name__": "__main__"}
    # set a so the demo condition is true
    ns["a"] = 2
    exec(py, ns)


if __name__ == "__main__":
    main()
