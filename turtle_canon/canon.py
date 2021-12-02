"""The main `turtle-canon` module."""
from contextlib import redirect_stdout
from os import devnull as DEVNULL
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from turtle_canon.utils import exceptions, warnings

# Avoid printing Owlready2 warnings to console
with open(DEVNULL, "w") as handle:
    with redirect_stdout(handle):
        import ontopy

if TYPE_CHECKING:
    from typing import Union


def canonize(ttl_file: "Union[Path, str]") -> None:
    """The main function for running `turtle-canon`.

    Workflow:
    - Load Turtle file.
    - Read Turtle file.
    - Instantiate EMMOntoPy Ontology from Turtle file.
    - Export Ontology as Turtle file (overwriting loaded Turtle file as default).

    Parameters:
        ttl_file: An absolute path or `pathlib.Path` object representing the Turtle
            file location.

    """
    valid_ttl_file = validate_turtle(ttl_file)
    loaded_ontology = ontopy.get_ontology(str(valid_ttl_file)).load(format="turtle")
    export_ontology(loaded_ontology, valid_ttl_file)


def validate_turtle(ttl_file: "Union[Path, str]") -> Path:
    """Validate a Turtle file.

    Parameters:
        ttl_file: An absolute path or `pathlib.Path` object representing the Turtle
            file location.

    Returns:
        A `pathlib.Path` object representing a validated Turtle file.

    """
    ttl_file = Path(ttl_file).resolve()

    if not ttl_file.exists():
        raise exceptions.TurtleFileNotFound(f"Supplied file {ttl_file} not found.")

    if not ttl_file.read_text(encoding="utf8"):
        raise warnings.EmptyFile(f"The Turtle file {ttl_file} is empty.")

    return ttl_file


def export_ontology(ontology: ontopy.ontology.Ontology, filename: Path) -> None:
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
        tmp_ttl_file = Path(tmp_dir) / "tmp_ttl_file.ttl"
        ontology.save(tmp_ttl_file, format="turtle")
        canonized_ttl = tmp_ttl_file.read_text(encoding="utf8")

    if not canonized_ttl:
        raise exceptions.FailedExportToFile(
            f"Failed to properly save the loaded ontology from {filename} to file."
        )

    filename.write_text(canonized_ttl, encoding="utf8")
