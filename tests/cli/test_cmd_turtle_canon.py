"""Test `turtle_canon.cli.cmd_turtle_canon` aka. the `turtle-canon` CLI."""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from subprocess import CalledProcessError, CompletedProcess
    from typing import List, Union

    from .conftest import CLIOutput, CLIRunner

    CLIRunnerOutput = Union[CalledProcessError, CLIOutput, CompletedProcess]


def test_version(clirunner: "CLIRunner") -> None:
    """Test `--version`."""
    from turtle_canon import __version__

    output: "CLIRunnerOutput" = clirunner(["--version"])
    assert output.stdout == f"Turtle Canon version {__version__}\n"


def test_absolute_path(clirunner: "CLIRunner", simple_turtle_file: Path) -> None:
    """Simple test run with minimalistic Turtle file."""
    output: "CLIRunnerOutput" = clirunner([str(simple_turtle_file)])

    assertion_help = (
        f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\nRETURN_CODE: "
        f"{output.returncode}"
    )

    assert not output.stderr, assertion_help
    assert output.stdout, assertion_help
    assert output.returncode == 0, assertion_help
    assert "Successful" in output.stdout, assertion_help


def test_relative_path(clirunner: "CLIRunner", simple_turtle_file: Path) -> None:
    """Simple test run with minimalistic Turtle file."""
    relative_path = simple_turtle_file.relative_to("/tmp")
    assert str(relative_path) == str(
        Path(simple_turtle_file.parent.name) / simple_turtle_file.name
    )
    assert not relative_path.is_absolute()

    output: "CLIRunnerOutput" = clirunner([str(relative_path)], run_dir="/tmp")

    assertion_help = (
        f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\nRETURN_CODE: "
        f"{output.returncode}"
    )

    assert not output.stderr, assertion_help
    assert output.stdout, assertion_help
    assert output.returncode == 0, assertion_help
    assert "Successful" in output.stdout, assertion_help


def test_non_existant_file(clirunner: "CLIRunner") -> None:
    """Ensure an error is printed with error code != 0 if the passed file does not
    exist."""
    non_existant_file = Path(__file__).resolve().parent / "non-existant.ttl"
    assert (
        not non_existant_file.exists()
    ), f"{non_existant_file} was expected to not exist, but suprisingly it does !"

    error_substring = f"Supplied file {non_existant_file.absolute()} not found."

    output: "CLIRunnerOutput" = clirunner(
        [str(non_existant_file)], expected_error=error_substring
    )

    assertion_help = (
        f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\nRETURN_CODE: "
        f"{output.returncode}"
    )

    assert output.stderr, assertion_help
    assert (
        error_substring in output.stderr and error_substring not in output.stdout
    ), assertion_help
    assert output.returncode == 1, assertion_help
    assert "ERROR" in output.stderr, assertion_help
    assert "Successful" not in output.stdout, assertion_help


def test_empty_file(clirunner: "CLIRunner", tmp_dir: Path) -> None:
    """Ensure a warning is printed with error code != 0 if the passed file does not
    exist."""
    empty_file = tmp_dir / "empty.ttl"
    empty_file.touch()
    assert (
        empty_file.exists()
    ), f"{empty_file} was expected to exist, but suprisingly it does not !"
    assert (
        empty_file.read_text() == ""
    ), f"{empty_file} was expected to be empty, but suprisingly it is not !"

    warning_substring = f"The Turtle file {empty_file.absolute()} is empty."

    output: "CLIRunnerOutput" = clirunner([str(empty_file)])

    assertion_help = (
        f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\nRETURN_CODE: "
        f"{output.returncode}"
    )

    assert output.stderr, assertion_help
    assert (
        warning_substring in output.stderr and warning_substring not in output.stdout
    ), assertion_help
    assert output.returncode == 0
    assert "WARNING" in output.stderr, assertion_help
    assert "Successful" not in output.stdout, assertion_help


def test_multiple_files(
    clirunner: "CLIRunner", single_turtle_permutations: "List[Path]"
) -> None:
    """Ensure passing multiple files to the CLI works."""
    output: "CLIRunnerOutput" = clirunner([str(_) for _ in single_turtle_permutations])

    assertion_help = (
        f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\nRETURN_CODE: "
        f"{output.returncode}"
    )

    assert not output.stderr, assertion_help
    assert not output.stderr, assertion_help
    assert output.returncode == 0
    assert "Successful" in output.stdout, assertion_help


def test_fail_fast(
    clirunner: "CLIRunner", single_turtle_permutations: "List[Path]", tmp_dir: Path
) -> None:
    """Test `--fail-fast`."""
    warning_file = tmp_dir / "empty.ttl"
    warning_file.touch()
    assert (
        warning_file.exists()
    ), f"{warning_file} was expected to exist, but suprisingly it does not !"
    assert (
        warning_file.read_text() == ""
    ), f"{warning_file} was expected to be empty, but suprisingly it is not !"

    error_file = tmp_dir / "non_existant.ttl"
    assert (
        not error_file.exists()
    ), f"{error_file} was expected to not exist, but suprisingly it does !"

    assert len(single_turtle_permutations) == 3

    single_turtle_permutations.insert(1, error_file)
    single_turtle_permutations.insert(-1, warning_file)
    single_turtle_permutations.insert(-1, error_file)

    error_substring = f"Supplied file {error_file.absolute()} not found."

    output: "CLIRunnerOutput" = clirunner(
        [str(_) for _ in single_turtle_permutations],
        expected_error=error_substring,
    )

    assertion_help = (
        f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\nRETURN_CODE: "
        f"{output.returncode}"
    )

    assert output.stderr, assertion_help
    assert (
        error_substring in output.stderr and error_substring not in output.stdout
    ), assertion_help
    assert output.returncode == 1, assertion_help
    assert "ERROR" in output.stderr, assertion_help
    assert "*" in output.stderr, assertion_help
    assert not output.stdout, assertion_help
    assert "Successful" not in output.stdout, assertion_help

    output: "CLIRunnerOutput" = clirunner(
        ["--fail-fast"] + [str(_) for _ in single_turtle_permutations],
        expected_error=error_substring,
    )

    assertion_help = (
        f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\nRETURN_CODE: "
        f"{output.returncode}"
    )

    assert output.stderr, assertion_help
    assert (
        error_substring in output.stderr and error_substring not in output.stdout
    ), assertion_help
    assert output.returncode == 1, assertion_help
    assert "ERROR" in output.stderr, assertion_help
    assert "*" not in output.stderr, assertion_help
    assert not output.stdout, assertion_help
    assert "Successful" not in output.stdout, assertion_help
