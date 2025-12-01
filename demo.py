#!/usr/bin/env python3
"""Minimal entry script for students: run `python demo.py`.

This file intentionally keeps things tiny: it imports the package and calls
`run_uncl` on the accompanying `demo.uncl` file. Students don't need to know
about preprocessing details.
"""
from __future__ import annotations

import pathlib
import sys

# Ensure local `src/` is on sys.path so students can run this script without
# installing the package.
root = pathlib.Path(__file__).resolve().parent
srcdir = root / "src"
sys.path.insert(0, str(srcdir))

import unnclang


if __name__ == "__main__":
    demo = pathlib.Path(__file__).resolve().parent / "demo.uncl"
    # Do not inject a default `a` — if `a` is undefined the code should raise
    # a normal Python NameError as in real Python execution.
    unnclang.run_uncl(demo)
