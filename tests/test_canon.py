"""Test `turtle_canon.canon` module functions."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


def test_validate_turtle_no_file() -> None:
    """Ensure an exception is raised if file does not exist."""
    from pathlib import Path

    from turtle_canon.canon import validate_turtle
    from turtle_canon.utils.exceptions import TurtleFileNotFound

    non_existant_file = Path(__file__).resolve().parent / "non-existant.ttl"

    with pytest.raises(
        TurtleFileNotFound,
        match=f"Supplied file {non_existant_file.absolute()} not found.",
    ):
        validate_turtle(non_existant_file)


def test_validate_turtle_empty_file(tmp_dir: "Path") -> None:
    """Ensure a "warning" is raised if file is empty."""
    from turtle_canon.canon import validate_turtle
    from turtle_canon.utils.warnings import EmptyFile

    empty_file = tmp_dir / "empty.ttl"
    empty_file.touch()

    with pytest.raises(
        EmptyFile, match=f"The Turtle file {empty_file.absolute()} is empty."
    ):
        validate_turtle(empty_file)


def test_validate_turtle(simple_turtle_file: "Path") -> None:
    """Test `validate_turtle()` runs."""
    from turtle_canon.canon import validate_turtle

    assert validate_turtle(simple_turtle_file) == simple_turtle_file


def test_export_ontology_not_found() -> None:
    """Ensure an exception is raised if the export file does not already exist."""
    from pathlib import Path

    from rdflib import Graph

    from turtle_canon.canon import export_ontology
    from turtle_canon.utils.exceptions import TurtleFileNotFound

    non_existant_file = Path(__file__).resolve().parent / "non-existant.ttl"

    with pytest.raises(
        TurtleFileNotFound,
        match=f"File at {non_existant_file.absolute()} was unexpectedly not found !",
    ):
        export_ontology(ontology=Graph(), filename=non_existant_file)


def test_export_ontology_failed_export(tmp_dir: "Path") -> None:
    """Ensure an exception is raised if the export fails, i.e., if the generated file
    is empty."""
    from rdflib import Graph

    from turtle_canon.canon import export_ontology
    from turtle_canon.utils.exceptions import FailedExportToFile

    empty_file = tmp_dir / "empty.ttl"
    empty_file.touch()

    with pytest.raises(
        FailedExportToFile,
        match=f"Failed to properly save the loaded ontology from {empty_file.absolute()} to file.",
    ):
        export_ontology(ontology=Graph(), filename=empty_file)


def test_export_ontology(top_dir: "Path", tmp_dir: "Path") -> None:
    """Test `export_ontology()` runs."""
    import os
    import re
    import shutil

    from rdflib import __version__ as rdflib_version, Graph

    from turtle_canon.canon import export_ontology

    rdflib_canonized_dir = top_dir / "tests" / "static" / "rdflib_canonized"

    for rdflib_version_turtle_file in rdflib_canonized_dir.glob("*.ttl"):
        if re.match(fr".*_{rdflib_version}$", rdflib_version_turtle_file.stem):
            turtle_file = rdflib_version_turtle_file
            break
    else:
        pytest.fail(
            "Couldn't find a canonized turtle file for RDFlib version "
            f"{rdflib_version} in {rdflib_canonized_dir}\nContent:\n"
            f"{os.listdir(rdflib_canonized_dir)}"
        )

    editable_turtle_file = tmp_dir / turtle_file.name
    shutil.copy(turtle_file, editable_turtle_file)
    assert (
        editable_turtle_file.exists()
    ), f"Couldn't find the newly copied in turtle file at {editable_turtle_file} !"

    original_canonized_content = editable_turtle_file.read_text(encoding="utf8")

    ontology = Graph().parse(editable_turtle_file, format="turtle")

    export_ontology(ontology=ontology, filename=editable_turtle_file)

    assert (
        editable_turtle_file.exists()
    ), f"The file has unexpectedly been removed after running `export_ontology()` !"
    assert editable_turtle_file.read_text(encoding="utf8") == original_canonized_content
