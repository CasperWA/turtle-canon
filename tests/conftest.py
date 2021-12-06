"""Pytest fixtures and setup functions."""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def top_dir() -> Path:
    """Return `Path` object to the repository root directory."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def simple_ttl_file(top_dir: Path) -> Path:
    """Load and return `Path` object to a simple Turtle file."""
    res = top_dir / "tests" / "static" / "turtle_canon_tests.ttl"
    assert res.exists(), f"Test file {res.name} not found in {res.parent}!"
    return res
