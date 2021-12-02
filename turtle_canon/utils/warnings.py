"""Warnings for general usage by the Turtle Canon tool.

!!! note
    These warnings are *not* like regular Python `Warning`s.
    Instead, they are `Exception`s that will be caught and treated specially by the CLI.

"""


class TurtleCanonWarning(Exception):
    """Base Warning for the Turtle Canon tool."""


class EmptyFile(TurtleCanonWarning):
    """A file's content is empty."""
