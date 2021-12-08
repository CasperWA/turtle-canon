"""PyTest fixtures for the CLI (`turtle_canon.cli`)."""
from collections import namedtuple
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

CLIOutput = namedtuple("CLIOutput", ["stdout", "stderr"])

if TYPE_CHECKING:
    from subprocess import CalledProcessError, CompletedProcess
    from typing import Callable, List, Optional, Union

    from pytest import FixtureRequest

    CLIRunner = Callable[
        [
            Optional[List[str]],
            Optional[str],
            Optional[Union[Path, str]],
            bool,
        ],
        Union[CalledProcessError, CLIOutput, CompletedProcess],
    ]


@pytest.fixture(scope="session", params=[True, False])
def clirunner(request: "FixtureRequest") -> "CLIRunner":
    """Call the `turtle-canon` CLI."""
    from contextlib import redirect_stderr, redirect_stdout
    import os
    from subprocess import run, CalledProcessError
    from tempfile import TemporaryDirectory

    def _clirunner(
        options: "Optional[List[str]]" = None,
        expected_error: "Optional[str]" = None,
        run_dir: "Optional[Union[Path, str]]" = None,
        use_subprocess: bool = request.param,
    ) -> "Union[CalledProcessError, CLIOutput, CompletedProcess]":
        """Call the `turtle-canon` CLI.

        Parameters:
            options: Options with which to call `cli`, e.g., `--version`.
            expected_error: Sub-string expected in error output, if an error is
                expected.
            run_dir: The directory to use as current work directory when
                running the CLI.
            use_subprocess: Whether or not to run the CLI through a
                `subprocess.run()` call or instead import and call
                `turtle_canon.cli.cmd_turtle_canon.main()` directly.
                Will be forcefully set to `request.param` - cannot be overwritten.

        Returns:
            The return class for a successful call to `subprocess.run()` or the
            captured response from importing and running the `main()` function
            directly.

        """
        options = options or []
        use_subprocess = request.param

        if not isinstance(options, list):
            try:
                options = list(options)
            except TypeError as exc:
                raise TypeError("options must be a list of strings.") from exc

        if run_dir is None:
            run_dir = TemporaryDirectory()
        elif isinstance(run_dir, Path):
            run_dir = run_dir.resolve()
        else:
            try:
                run_dir = Path(run_dir).resolve()
            except TypeError as exc:
                raise TypeError(f"{run_dir} is not a valid path.") from exc

        if use_subprocess:
            try:
                output = run(
                    args=["turtle-canon"] + options,
                    capture_output=True,
                    check=True,
                    cwd=run_dir.name
                    if isinstance(run_dir, TemporaryDirectory)
                    else run_dir,
                    text=True,
                )
                if expected_error:
                    pytest.fail(
                        "Expected the CLI call to fail with an error "
                        f"containing the sub-string: {expected_error}"
                    )
            except CalledProcessError as error:
                if expected_error:
                    if expected_error in error.stdout or expected_error in error.stderr:
                        # Expected error, found expected sub-string as well.
                        return error

                    pytest.fail(
                        "The CLI call failed as expected, but the expected "
                        "error sub-string could not be found in stdout or "
                        f"stderr. Sub-string: {expected_error}\nSTDOUT: "
                        f"{error.stdout}\nSTDERR: {error.stderr}"
                    )
                else:
                    pytest.fail(
                        "The CLI call failed when it didn't expect to.\n"
                        f"STDOUT: {error.stdout}\nSTDERR: {error.stderr}"
                    )
            else:
                return output
            finally:
                if isinstance(run_dir, TemporaryDirectory):
                    run_dir.cleanup()
        else:
            from turtle_canon.cli.cmd_turtle_canon import main as cli

            with TemporaryDirectory() as tmpdir:
                stdout_path = Path(tmpdir) / "out.txt"
                stderr_path = Path(tmpdir) / "err.txt"
                original_cwd = os.getcwd()
                try:
                    os.chdir(
                        run_dir.name
                        if isinstance(run_dir, TemporaryDirectory)
                        else run_dir
                    )
                    with open(stdout_path, "w") as stdout, open(
                        stderr_path, "w"
                    ) as stderr:
                        with redirect_stdout(stdout), redirect_stderr(stderr):
                            cli(options if options else None)
                    output = CLIOutput(stdout_path.read_text(), stderr_path.read_text())
                except SystemExit as exc:
                    output = CLIOutput(stdout_path.read_text(), stderr_path.read_text())
                    if exc.code:
                        pytest.fail(
                            "The CLI call failed when it didn't expect to.\n"
                            f"Exit code: {exc.code}\n"
                            f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"
                        )
                    return output
                except Exception:  # pylint: disable=broad-except
                    output = CLIOutput(stdout_path.read_text(), stderr_path.read_text())
                    if expected_error:
                        if (
                            expected_error in output.stdout
                            or expected_error in output.stderr
                        ):
                            # Expected error, found expected sub-string as well.
                            return output

                        pytest.fail(
                            "The CLI call failed as expected, but the expected "
                            "error sub-string could not be found in stdout or "
                            f"stderr. Sub-string: {expected_error}\nSTDOUT: "
                            f"{output.stdout}\nSTDERR: {output.stderr}"
                        )
                    else:
                        pytest.fail(
                            "The CLI call failed when it didn't expect to.\n"
                            f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"
                        )
                else:
                    return output
                finally:
                    os.chdir(original_cwd)
                    if isinstance(run_dir, TemporaryDirectory):
                        run_dir.cleanup()

    return _clirunner
