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
    import os
    from shutil import copy
    from tempfile import TemporaryDirectory

    ttl_file = top_dir / "tests" / "static" / "turtle_canon_tests.ttl"
    assert (
        ttl_file.exists()
    ), f"Test file {ttl_file.name} not found in {ttl_file.parent}!"
    tmpdir = TemporaryDirectory()
    yield Path(copy(ttl_file, Path(tmpdir.name) / ttl_file.name))
    tmpdir.cleanup()
    assert not Path(
        tmpdir.name
    ).exists(), f"Failed to remove temporary directory at {tmpdir.name}. Content:\n{os.listdir(tmpdir.name)}"
