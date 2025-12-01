"""Smoke tests for the UNNCLang macro helpers."""
from __future__ import annotations

import textwrap

import pytest


def test_endif_macro_allows_block_closure():
    """A tiny script using `endif` should execute without syntax/runtime errors."""

    script = textwrap.dedent(
        """
        from unnclang import load_macros

        load_macros(globals())

        value = 5
        if value > 0:
            message = "positive"
        endif
        """
    )
    local_vars: dict[str, object] = {}
    exec(script, {}, local_vars)
    assert local_vars["message"] == "positive"


def test_load_macros_can_scope_exports():
    from unnclang import load_macros, registered_macro_names

    namespace: dict[str, object] = {}
    load_macros(namespace, names=["endif"])

    assert "endif" in namespace
    assert set(namespace) == {"endif"}
    assert "endif" in registered_macro_names()
