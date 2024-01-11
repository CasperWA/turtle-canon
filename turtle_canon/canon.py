"""The main `turtle-canon` module."""
from __future__ import annotations

import re
from pathlib import Path
from tempfile import TemporaryDirectory

from rdflib import Graph
from rdflib.exceptions import Error as RDFlibError
from rdflib.exceptions import ParserError

from turtle_canon.utils import exceptions, warnings


def canonize(turtle_file: Path | str) -> Path | None:
    """The main function for running `turtle-canon`.

    Workflow:
    - **Validate** Turtle file.
      Check the file integrity, readability, writeability and content.
    - **Parse** and **sort** Turtle file's triples.
      Parse Turtle file using RDFlib.
      Retrieve triples, sort them, and generate a new RDFlib `Graph` from the sorted
      triples.
    - **Export** ontology as Turtle file.
      Overwriting loaded Turtle file, i.e., overall the canonization is done in-place.

    Parameters:
        turtle_file: An absolute path or `pathlib.Path` object representing the Turtle
            file location.

    Returns:
        If the file has been changed during the canonization, the Turtle file's
        location will be returned, otherwise `None` will be returned.

    """
    valid_turtle_file = validate_turtle(turtle_file)
    sorted_ontology = sort_ontology(valid_turtle_file)
    changed_file = export_ontology(sorted_ontology, valid_turtle_file)

    return Path(turtle_file) if changed_file else None


def validate_turtle(turtle_file: Path | str) -> Path:
    """Validate a Turtle file.

    Parameters:
        turtle_file: An absolute path or `pathlib.Path` object representing the Turtle
            file location.

    Returns:
        A `pathlib.Path` object representing a validated Turtle file.

    """
    turtle_file = Path(turtle_file).resolve()

    if not turtle_file.exists():
        raise exceptions.TurtleFileNotFound(f"Supplied file {turtle_file} not found.")

    try:
        content = turtle_file.read_text(encoding="utf8")
    except (OSError, UnicodeDecodeError) as exc:
        raise exceptions.FailedReadingFile(
            f"The Turtle file {turtle_file} could not be opened and read (using UTF-8 "
            "encoding)."
        ) from exc

    try:
        turtle_file.write_text(content, encoding="utf8")
    except (OSError, UnicodeDecodeError) as exc:
        raise exceptions.FailedReadingFile(
            f"The Turtle file {turtle_file} could not be opened and written to (using "
            "UTF-8 encoding)."
        ) from exc

    if not content:
        raise warnings.EmptyFile(f"The Turtle file {turtle_file} is empty.")

    return turtle_file


def sort_ontology(turtle_file: Path) -> Graph:
    """Load and sort triples in ontology.

    A validated Turtle file is expected, hence there are no "unnecessary" sanity checks
    in this function.

    Parameters:
        turtle_file: A valid `pathlib.Path` object representing the (unsorted) Turtle
            file.

    """
    try:
        ontology = Graph().parse(location=str(turtle_file), format="turtle")
    except (SyntaxError, ParserError, RDFlibError) as exc:
        raise exceptions.FailedParsingFile(
            f"Failed to properly parse the Turtle file at {turtle_file}"
        ) from exc

    triples = sorted(ontology)

    if not triples:
        raise warnings.NoTriples(
            f"No triples found in the parsed non-empty Turtle file at {turtle_file}"
        )

    sorted_ontology = Graph(
        namespace_manager=ontology.namespace_manager, base=ontology.base
    )
    try:
        for triple in triples:
            sorted_ontology.add(triple)
    except (AssertionError, RDFlibError) as exc:
        raise exceptions.FailedCreatingOntology(
            "Failed to properly create a sorted ontology from the triples in the "
            f"Turtle file at {turtle_file}"
        ) from exc

    if set(ontology) - set(sorted_ontology) or len(ontology) != len(sorted_ontology):
        raise exceptions.InconsistencyError(
            f"After sorting the ontology triples from the Turtle file at {turtle_file}"
            " and re-creating the ontology, inconsistencies were found !"
        )

    return sorted_ontology


def export_ontology(ontology: Graph, filename: Path) -> bool:
    """Export an ontology as a Turtle file.

    Parameters:
        ontology: A loaded ontology.
        filename: The Turtle file's fully resolved path to export to.

    Returns:
        Whether or not the exported ontology changed the file at `filename` or not.

    """
    if not filename.exists():
        raise exceptions.TurtleFileNotFound(
            f"File at {filename} was unexpectedly not found !"
        )

    with TemporaryDirectory() as tmp_dir:
        tmp_turtle_file = Path(tmp_dir) / "tmp_turtle_file.ttl"
        try:
            ontology.serialize(tmp_turtle_file, format="turtle")
        except (ValueError, RDFlibError) as exc:
            raise exceptions.FailedExportToFile(
                f"Failed to properly save the loaded ontology from {filename} to file."
            ) from exc

        canonized_ttl = tmp_turtle_file.read_text(encoding="utf8")

    if not canonized_ttl or re.match(r"^\s$", canonized_ttl):
        raise exceptions.FailedExportToFile(
            f"Failed to properly save the loaded ontology from {filename} to file."
        )

    changed = filename.read_text() != canonized_ttl

    filename.write_text(canonized_ttl, encoding="utf8")

    return changed
