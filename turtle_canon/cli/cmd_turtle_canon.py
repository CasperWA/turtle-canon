"""Command line interface (CLI) for running `turtle-canon`."""
# pylint: disable=import-outside-toplevel
import argparse
import logging
from pathlib import Path
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from collections import namedtuple
    from typing import List

    CLIArgs = namedtuple("CLIArgs", ["version", "log_level", "TURTLE_FILE"])

LOGGING_LEVELS = [logging.getLevelName(level).lower() for level in range(0, 51, 10)]


def main(args: "List[str]" = None) -> None:
    """Turtle Canon - It's turtles all the way down."""
    from turtle_canon import __version__
    from turtle_canon.canon import canonize
    from turtle_canon.cli.utils import print_error, print_warning
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
        "TURTLE_FILE",
        action="extend",
        nargs="+",
        type=Path,
        help=(
            "Path to the Turtle file. Can be relative or absolute. Example: "
            "'../my_ontology.ttl'."
        ),
    )

    args: "CLIArgs" = parser.parse_args(args)  # type: ignore[assignment]

    try:
        for turtle_file in args.TURTLE_FILE:
            canonize(turtle_file)
    except TurtleCanonException as exception:
        print_error(exception)
    except TurtleCanonWarning as warning:
        print_warning(warning)
    sys.exit()
