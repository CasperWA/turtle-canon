"""Pytest fixtures and setup functions."""
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import List


@pytest.fixture(scope="session")
def top_dir() -> Path:
    """Return `Path` object to the repository root directory."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def simple_turtle_file(top_dir: Path) -> Path:
    """Load and return `Path` object to a simple Turtle file."""
    import os
    from shutil import copy
    from tempfile import TemporaryDirectory

    turtle_file = top_dir / "tests" / "static" / "turtle_canon_tests.ttl"
    assert (
        turtle_file.exists()
    ), f"Test file {turtle_file.name} not found in {turtle_file.parent}!"
    tmpdir = TemporaryDirectory()
    try:
        yield Path(copy(turtle_file, Path(tmpdir.name) / turtle_file.name))
    finally:
        tmpdir.cleanup()
        assert not Path(
            tmpdir.name
        ).exists(), f"Failed to remove temporary directory at {tmpdir.name}. Content:\n{os.listdir(tmpdir.name)}"


@pytest.fixture
def single_turtle_permutations(top_dir: Path) -> "List[Path]":
    """Yield list of a single turtle file and permutations of it.

    The permutations are restructuring of the list of classes.
    """
    import os
    from shutil import copy
    from tempfile import TemporaryDirectory

    turtle_files = list((top_dir / "tests" / "static").glob("turtle_canon_tests*.ttl"))
    tmpdir = TemporaryDirectory()
    tmpdir_path = Path(tmpdir.name)
    try:
        res = []
        for turtle_file in turtle_files:
            copy(turtle_file, tmpdir_path / turtle_file.name)
            res.append(tmpdir_path / turtle_file.name)
        yield res
    finally:
        tmpdir.cleanup()
        assert not Path(tmpdir.name).exists(), (
            f"Failed to remove temporary directory at {tmpdir.name}. "
            f"Content:\n{os.listdir(tmpdir.name)}"
        )
