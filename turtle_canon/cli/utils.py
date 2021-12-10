"""Utility functions for `turtle-canon` CLI."""
from pathlib import Path
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import List, Optional, Sequence, TextIO, Union


class Cache:
    """Small cache."""

    def __init__(self) -> None:
        self._errors: "List[Union[str, Exception]]" = []
        self._warnings: "List[Union[str, Exception]]" = []
        self._files: "List[Union[str, Path]]" = []

    @property
    def errors(self) -> "List[Union[str, Exception]]":
        """Get `errors` attribute."""
        return self._errors

    @property
    def warnings(self) -> "List[Union[str, Exception]]":
        """Get `warnings` attribute."""
        return self._warnings

    @property
    def files(self) -> "List[Union[str, Path]]":
        """Get `files` attribute."""
        return self._files

    def add_error(self, error: "Union[str, Exception]") -> None:
        """Add an error to the cache."""
        if not isinstance(error, (str, Exception)):
            raise TypeError("error must be either a str or Exception")
        self._errors.append(error)

    def add_warning(self, warning: "Union[str, Exception]") -> None:
        """Add a warning to the cache."""
        if not isinstance(warning, (str, Exception)):
            raise TypeError("warning must be either a str or Exception")
        self._warnings.append(warning)

    def add_file(self, file: "Union[str, Path]") -> None:
        """Add a file to the cache."""
        if not isinstance(file, (str, Path)):
            raise TypeError("file must be either a str or Exception")
        self._files.append(file)


def _print_message(
    message: str,
    target: "Optional[TextIO]" = None,
    prefix: "Optional[str]" = None,
    exit_after: bool = False,
) -> None:
    """Print a message to target.

    Parameters:
        message: The message to print.
        target: A file stream, defaults to STDOUT.
        prefix: String to prepend to message.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    target = target if target is not None else sys.stdout
    if prefix:
        message = prefix + message
    print(message, file=target, flush=True)
    if exit_after:
        sys.exit(1)


def print_error(message: "Union[str, Exception]", exit_after: bool = True) -> None:
    """Print an error message to the console.

    Parameters:
        message: The error message to print.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    res = f"Misfire !\n\n{message}"
    if isinstance(message, Exception):
        res += f"\n\nGeneral information about the exception: {message.__doc__}"
    _print_message(res, target=sys.stderr, prefix="ERROR: ", exit_after=exit_after)


def print_warning(message: "Union[str, Exception]", exit_after: bool = False) -> None:
    """Print a warnings message to the console.

    Parameters:
        message: The warning message to print.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    res = f"Don't come too close !\n\n{message}"
    if isinstance(message, Exception):
        res += f"\n\nGeneral information about the warning: {message.__doc__}"
    _print_message(res, target=sys.stderr, prefix="WARNING: ", exit_after=exit_after)


def print_summary(
    errors: "Optional[Sequence[Union[str, Exception]]]" = None,
    warnings: "Optional[Sequence[Union[str, Exception]]]" = None,
    exit_after: bool = False,
) -> None:
    """Print a summary, including of error and/or warning messages.

    Parameters:
        errors: List of error messages.
        warnings: List of warning messages.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    res = ""
    target = sys.stdout

    if errors or warnings:
        res += "The balls are stuck !\n\n"
        target = sys.stderr
    else:
        res += "Successful Fire !\n"

    if errors:
        res += "ERRORS:\n"
        for error in errors:
            res += f"* {error}\n"
            if isinstance(error, Exception):
                res += f"  General info: {error.__doc__}\n"

    if warnings:
        res += "WARNINGS:\n"
        for warning in warnings:
            res += f"* {warning}\n"
            if isinstance(warning, Exception):
                res += f"  General info: {warning.__doc__}\n"

    _print_message(res, target=target, prefix="", exit_after=exit_after)


def print_changed_files(
    files: "Sequence[Union[str, Path]]", exit_after: bool = False
) -> None:
    """Print list of changed files.

    Parameters:
        files: List of files with changes.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    res = "\nChanged files:\n"
    for file_ in files:
        res += f"{file_}\n"

    _print_message(res, target=sys.stdout, prefix="", exit_after=exit_after)
