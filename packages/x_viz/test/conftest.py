"""Configuration of pytest."""

import pytest
from path import Path


@pytest.fixture(scope="session")
def data_dir() -> Path:
    """Return the data directory path."""
    return Path(__file__).parent.parent.parent.parent / "data"
