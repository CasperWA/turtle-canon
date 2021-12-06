"""Test `turtle_canon.cli.cmd_turtle_canon` aka. the `turtle-canon` CLI."""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from subprocess import CalledProcessError, CompletedProcess
    from typing import Union

    from .conftest import CLIOutput, CLIRunner


def test_version(clirunner: "CLIRunner") -> None:
    """Test `--version`."""
    from turtle_canon import __version__

    output = clirunner(["--version"])
    assert output.stdout == f"Turtle Canon version {__version__}\n"


def test_absolute_path(clirunner: "CLIRunner", simple_ttl_file: Path) -> None:
    """Simple test run with minimalistic Turtle file."""
    output: "Union[CalledProcessError, CLIOutput, CompletedProcess]" = clirunner(
        [str(simple_ttl_file)]
    )

    assert (
        output.stdout == output.stderr == ""
    ), f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"


def test_relative_path(clirunner: "CLIRunner", simple_ttl_file: Path) -> None:
    """Simple test run with minimalistic Turtle file."""
    relative_path = simple_ttl_file.relative_to("/tmp")
    assert str(relative_path) == str(
        Path(simple_ttl_file.parent.name) / simple_ttl_file.name
    )
    assert not relative_path.is_absolute()

    output: "Union[CalledProcessError, CLIOutput, CompletedProcess]" = clirunner(
        [str(relative_path)], run_dir="/tmp"
    )

    assert (
        output.stdout == output.stderr == ""
    ), f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"
