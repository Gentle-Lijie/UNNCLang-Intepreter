#!/usr/bin/env python3
"""Bump the version in pyproject.toml.

Usage:
  python3 scripts/bump_version.py [patch|minor|major] [--file pyproject.toml] [--dry-run]

Default level is 'patch'. By default performs a dry-run; pass --no-dry-run to write changes.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys


SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("level", nargs="?", choices=["patch", "minor", "major"], default="patch")
    p.add_argument("--file", default="pyproject.toml", help="Path to pyproject.toml")
    p.add_argument("--dry-run", dest="dry_run", action="store_true", default=True, help="Do not write changes; show what would change")
    p.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Write changes to file")
    return p.parse_args()


def bump_version_tuple(major: int, minor: int, patch: int, level: str):
    if level == "patch":
        patch += 1
    elif level == "minor":
        minor += 1
        patch = 0
    elif level == "major":
        major += 1
        minor = 0
        patch = 0
    return major, minor, patch


def find_project_version(lines: list[str]):
    """Return (index, old_version_str) where index is the line index of version= under [project]."""
    in_project = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"
            continue
        if in_project:
            # match lines like: version = "0.1.3"
            m = re.match(r"^version\s*=\s*\"([0-9]+\.[0-9]+\.[0-9]+)\"", stripped)
            if m:
                return i, m.group(1)
    return None, None


def main():
    args = parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(2)

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    idx, old = find_project_version(lines)
    if idx is None:
        print("Could not find version under [project] in", args.file, file=sys.stderr)
        sys.exit(3)

    m = SEMVER_RE.match(old)
    if not m:
        print("Found version, but it's not in simple X.Y.Z format:", old, file=sys.stderr)
        sys.exit(4)

    major, minor, patch = map(int, m.groups())
    new_major, new_minor, new_patch = bump_version_tuple(major, minor, patch, args.level)
    new_version = f"{new_major}.{new_minor}.{new_patch}"

    print(f"Detected current version: {old}")
    print(f"Recommended bump: {args.level} -> new version: {new_version}")

    old_line = lines[idx]
    new_line = re.sub(r"(version\s*=\s*)\"[0-9]+\.[0-9]+\.[0-9]+\"", rf"\1\"{new_version}\"", old_line)

    print("\nOld line:")
    print(old_line)
    print("\nNew line:")
    print(new_line)

    if args.dry_run:
        print("\nDry run: no files modified. To apply the change, re-run with --no-dry-run")
        return

    lines[idx] = new_line
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote new version to {path}: {old} -> {new_version}")


if __name__ == "__main__":
    main()
