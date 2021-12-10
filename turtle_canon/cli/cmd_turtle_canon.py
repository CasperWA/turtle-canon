"""Command line interface (CLI) for running `turtle-canon`."""
# pylint: disable=import-outside-toplevel
import argparse
import logging
from pathlib import Path
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from dataclasses import dataclass
    from typing import List

    @dataclass
    class CLIArgs:
        """CLI parsed arguments"""

        version: str
        log_level: str
        fail_fast: bool
        turtle_files: List[Path]


LOGGING_LEVELS = [logging.getLevelName(level).lower() for level in range(0, 51, 10)]


def main(args: "List[str]" = None) -> None:
    """Turtle Canon - It's turtles all the way down."""
    from turtle_canon import __version__
    from turtle_canon.canon import canonize
    from turtle_canon.cli.utils import print_error, print_summary, print_warning
    from turtle_canon.utils.exceptions import TurtleCanonException
    from turtle_canon.utils.warnings import TurtleCanonWarning

    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Show the version and exit.",
        version=f"Turtle Canon version {__version__}",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        help="Set the logging output level.",
        choices=LOGGING_LEVELS,
        default="info",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help=(
            "Exit the canonization immediately if an error occurs. E.g., if multiple "
            "files are given, Turtle Canon will exit immediately if an error occurs "
            "when canonization a single file. Otherwise, all files will be attempted "
            "to be canonized, and a summary will be printed at the end."
        ),
    )
    parser.add_argument(
        "turtle_files",
        action="extend",
        nargs="+",
        type=Path,
        help=(
            "Path to the Turtle file. Can be relative or absolute. Example: "
            "'../my_ontology.ttl'."
        ),
        metavar="TURTLE_FILE",
    )

    args: "CLIArgs" = parser.parse_args(args)  # type: ignore[assignment]

    errors = []
    warnings = []

    number_of_turtle_files = len(args.turtle_files)

    while args.turtle_files:
        turtle_file = args.turtle_files.pop()
        try:
            canonize(turtle_file)
        except TurtleCanonException as exception:
            if args.fail_fast:
                print_error(exception)
            else:
                errors.append(exception)
        except TurtleCanonWarning as warning:
            if number_of_turtle_files == 1:
                print_warning(warning)
            warnings.append(warning)

    if number_of_turtle_files == 1 and warnings:
        pass
    else:
        print_summary(errors=errors, warnings=warnings)

    sys.exit()
