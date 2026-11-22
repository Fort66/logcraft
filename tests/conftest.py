"""Shared pytest fixtures."""

import pytest

from logcraft import logger


@pytest.fixture(autouse=True)
def _clean_logger():
    logger.remove()
    yield
    logger.remove()
