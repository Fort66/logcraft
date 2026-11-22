"""Tests for module name abbreviation."""

from io import StringIO

import pytest

from logcraft import logger
from logcraft.formatters import abbreviate_name


@pytest.mark.parametrize(
    ("style", "expected"),
    [
        ("initials", "m.c.c.utils"),
        ("last", "utils"),
        ("last2", "core.utils"),
    ],
)
def test_abbreviate_styles(style: str, expected: str) -> None:
    assert abbreviate_name("my.company.core.utils", style=style) == expected


def test_abbreviate_single_part() -> None:
    assert abbreviate_name("utils") == "utils"


def test_abbreviate_unknown_style() -> None:
    with pytest.raises(ValueError):
        abbreviate_name("a.b", style="nope")


def test_add_abbreviate_kwarg() -> None:
    buffer = StringIO()
    handler_id = logger.add(
        buffer,
        format="{name} | {message}",
        abbreviate="initials",
        colorize=False,
    )
    logger.info("hello")
    logger.remove(handler_id)

    expected_name = abbreviate_name(__name__, style="initials")
    assert buffer.getvalue().startswith(f"{expected_name} | hello")