"""Test `turtle_canon.cli.cmd_turtle_canon` aka. the `turtle-canon` CLI."""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conftest import CLIRunner


def test_version(clirunner: "CLIRunner") -> None:
    """Test `--version`."""
    from turtle_canon import __version__

    output = clirunner(["--version"])
    assert output.stdout == f"Turtle Canon version {__version__}\n"


def test_simple_run(clirunner: "CLIRunner", simple_ttl_file: Path) -> None:
    """Simple test run with minimalistic Turtle file."""
    paths = [str(simple_ttl_file), f"../../static/{simple_ttl_file.name}"]

    for path in paths:
        output = clirunner([path])

        assert (
            "downloading" in output.stdout
        ), f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"
