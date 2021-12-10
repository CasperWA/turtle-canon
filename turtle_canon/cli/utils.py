"""Utility functions for `turtle-canon` CLI."""
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional, Sequence, TextIO, Union


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
    exit_after: bool = True,
) -> None:
    """Print a summary, including of error and/or warning messages.

    Parameters:
        errors: List of error messages.
        warnings: List of warning messages.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    exit_after = bool(errors)

    res = ""
    target = sys.stdout

    if errors or warnings:
        res += "The balls are stuck !\n\n"
        target = sys.stderr
    else:
        res += "Successful Fire !"

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
