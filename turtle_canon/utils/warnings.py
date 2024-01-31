"""Warnings for general usage by the Turtle Canon tool.

!!! note
    These warnings are *not* like regular Python `Warning`s.
    Instead, they are `Exception`s that will be caught and treated specially by the CLI.

"""

from __future__ import annotations


class TurtleCanonWarning(Exception):
    """Base Warning for the Turtle Canon tool."""


class EmptyFile(TurtleCanonWarning):
    """A file's content is empty."""


class NoTriples(TurtleCanonWarning):
    """No triples found in the parsed ontology."""
