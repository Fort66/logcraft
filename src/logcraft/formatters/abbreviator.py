"""Abbreviation of long module names (Loguru issue #1400)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

STYLES = ("initials", "last", "last2")


def abbreviate_name(name: str, style: str = "initials") -> str:
    """
    Shorten a dotted module path.

    Styles:
        initials: "my.company.core.utils" -> "m.c.c.utils"
        last:     "my.company.core.utils" -> "utils"
        last2:    "my.company.core.utils" -> "core.utils"
    """
    if style not in STYLES:
        raise ValueError(f"Unknown abbreviate style {style!r}, expected one of {STYLES}")

    parts = [p for p in name.split(".") if p]
    if not parts:
        return name
    if style == "last":
        return parts[-1]
    if style == "last2":
        return ".".join(parts[-2:])
    if len(parts) == 1:
        return parts[0]
    return ".".join([p[0] for p in parts[:-1]] + [parts[-1]])


def make_abbrev_patcher(style: str = "initials") -> Callable[[dict[str, Any]], None]:
    """Return a patcher that rewrites record['name'] to its abbreviated form."""

    def patcher(record: dict[str, Any]) -> None:
        record["name"] = abbreviate_name(record["name"], style=style)

    return patcher
