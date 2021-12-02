"""Exceptions for general usage by the Turtle Canon tool."""


class TurtleCanonException(Exception):
    """Base Exception for the Turtle Canon tool."""


class TurtleFileNotFound(TurtleCanonException):
    """A Turtle file cannot be found."""


class FailedExportToFile(TurtleCanonException):
    """Failed to export an ontology to file."""
