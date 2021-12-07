"""The main `turtle-canon` module."""
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from rdflib import Graph

from turtle_canon.utils import exceptions, warnings


if TYPE_CHECKING:
    from typing import Union


def canonize(turtle_file: "Union[Path, str]") -> None:
    """The main function for running `turtle-canon`.

    Workflow:
    - Load Turtle file.
    - Read Turtle file.
    - Instantiate EMMOntoPy Ontology from Turtle file.
    - Export Ontology as Turtle file (overwriting loaded Turtle file as default).

    Parameters:
        turtle_file: An absolute path or `pathlib.Path` object representing the Turtle
            file location.

    """
    valid_turtle_file = validate_turtle(turtle_file)
    loaded_ontology = Graph().parse(location=str(turtle_file), format="turtle")
    export_ontology(loaded_ontology, valid_turtle_file)


def validate_turtle(turtle_file: "Union[Path, str]") -> Path:
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

    if not turtle_file.read_text(encoding="utf8"):
        raise warnings.EmptyFile(f"The Turtle file {turtle_file} is empty.")

    return turtle_file


def export_ontology(ontology: Graph, filename: Path) -> None:
    """Export an ontology as a Turtle file.

    Parameters:
        ontology: A loaded ontology.
        filename: The Turtle file's fully resolved path to export to.

    """
    if not filename.exists():
        raise exceptions.TurtleFileNotFound(
            f"File at {filename} was unexpectedly not found !"
        )

    with TemporaryDirectory() as tmp_dir:
        tmp_turtle_file = Path(tmp_dir) / "tmp_turtle_file.ttl"
        ontology.serialize(tmp_turtle_file, format="turtle")
        canonized_ttl = tmp_turtle_file.read_text(encoding="utf8")

    if not canonized_ttl:
        raise exceptions.FailedExportToFile(
            f"Failed to properly save the loaded ontology from {filename} to file."
        )

    filename.write_text(canonized_ttl, encoding="utf8")
