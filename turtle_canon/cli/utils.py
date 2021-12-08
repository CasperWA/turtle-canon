"""Utility functions for `turtle-canon` CLI."""
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional, TextIO, Union


def _print_message(
    message: str, target: "Optional[TextIO]" = None, prefix: "Optional[str]" = None
) -> None:
    """Print a message to target.

    Parameters:
        message: The message to print.
        target: A file stream, defaults to STDOUT.
        prefix: String to prepend to message.

    """
    target = target if target is not None else sys.stdout
    if prefix:
        message = prefix + message
    print(message, file=target, flush=True)


def print_error(message: "Union[str, Exception]", exit_after: bool = True) -> None:
    """Print an error message to the console.

    Parameters:
        message: The error message to print.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    res = f"Misfire !\n\n{message}"
    if isinstance(message, Exception):
        res += f"\n\nGeneral information about the exception: {message.__doc__}"
    _print_message(res, target=sys.stderr, prefix="ERROR: ")
    if exit_after:
        sys.exit(1)


def print_warning(message: "Union[str, Exception]", exit_after: bool = False) -> None:
    """Print a warnings message to the console.

    Parameters:
        message: The warning message to print.
        exit_after: Whether or not to call `sys.exit(1)` after printing the message.

    """
    res = f"Don't come too close !\n\n{message}"
    if isinstance(message, Exception):
        res += f"\n\nGeneral information about the warning: {message.__doc__}"
    _print_message(res, target=sys.stderr, prefix="WARNING: ")
    if exit_after:
        sys.exit(1)
