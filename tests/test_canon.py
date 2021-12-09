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


def test_validate_turtle_binary_file(tmp_dir: "Path") -> None:
    """Ensure an exception is raised when the file cannot be decoded as UTF-8."""
    from turtle_canon.canon import validate_turtle
    from turtle_canon.utils.exceptions import FailedReadingFile

    binary_file = tmp_dir / "binary_file.ttl"
    binary_file.write_bytes(bytes("æøå", "latin-1"))
    assert (
        binary_file.exists()
    ), f"Binary test file {binary_file} expected to exist, but it does not !"
    assert binary_file.read_text(
        encoding="latin-1"
    ), f"Binary test file {binary_file} expected to be non-empty, but it was empty !"

    with pytest.raises(
        FailedReadingFile,
        match=f"The Turtle file {binary_file.absolute()} could not be opened and read \(using UTF-8 encoding\).",
    ):
        validate_turtle(binary_file)


def test_validate_turtle_no_rw_file(tmp_dir: "Path") -> None:
    """Ensure an exception is raised when the file cannot be read or written to."""
    import os

    from turtle_canon.canon import validate_turtle
    from turtle_canon.utils.exceptions import FailedReadingFile

    no_rw_file = tmp_dir / "unreadable_unwriteable.ttl"
    no_rw_file.write_text("test")

    assert (
        no_rw_file.exists()
    ), f"No rw test file {no_rw_file} expected to exist, but it does not !"
    assert (
        no_rw_file.read_text()
    ), f"No rw test file {no_rw_file} expected to be non-empty, but it was empty !"

    try:
        os.chmod(no_rw_file, 0o000)  # none

        with pytest.raises(
            FailedReadingFile,
            match=f"The Turtle file {no_rw_file.absolute()} could not be opened and read \(using UTF-8 encoding\).",
        ):
            validate_turtle(str(no_rw_file))
    finally:
        os.chmod(no_rw_file, 0o644)
        assert no_rw_file.read_text()


def test_validate_turtle_no_w_file(tmp_dir: "Path") -> None:
    """Ensure an exception is raised when the file cannot be read or written to."""
    import os

    from turtle_canon.canon import validate_turtle
    from turtle_canon.utils.exceptions import FailedReadingFile

    no_w_file = tmp_dir / "unwriteable.ttl"
    no_w_file.write_text("test")

    assert (
        no_w_file.exists()
    ), f"No w test file {no_w_file} expected to exist, but it does not !"
    assert (
        no_w_file.read_text()
    ), f"No w test file {no_w_file} expected to be non-empty, but it was empty !"

    try:
        os.chmod(no_w_file, 0o444)  # read only

        with pytest.raises(
            FailedReadingFile,
            match=(
                f"The Turtle file {no_w_file.absolute()} could not be opened and "
                "written to \(using UTF-8 encoding\)."
            ),
        ):
            validate_turtle(str(no_w_file))
    finally:
        os.chmod(no_w_file, 0o644)
        assert no_w_file.read_text()
        assert no_w_file.write_text("test again")


def test_sort_ontology(simple_turtle_file: "Path") -> None:
    """Test `sort_ontology()` runs."""
    from rdflib import Graph

    from turtle_canon.canon import sort_ontology

    ontology = sort_ontology(simple_turtle_file)
    assert isinstance(ontology, Graph)


def test_sort_ontology_no_triples(tmp_dir: "Path") -> None:
    """Ensure a warning is raised (as an exception) if there are no triples.

    While the Turtle file in this test _is_ empty, this is not checked in
    `sort_ontology()`, since a "validated" Turtle file is expected (where this is
    checked).
    """
    from turtle_canon.canon import sort_ontology
    from turtle_canon.utils.warnings import NoTriples

    empty_file = tmp_dir / "empty_file.ttl"
    empty_file.write_text("\n")

    with pytest.raises(
        NoTriples,
        match=(
            "No triples found in the parsed non-empty Turtle file at "
            f"{empty_file.absolute()}"
        ),
    ):
        sort_ontology(empty_file)


def test_sort_ontology_unparseable_file(tmp_dir: "Path") -> None:
    """Ensure exceptions from RDFlib during parsing an unparseable Turtle file are
    wrapped as Turtle Canon exceptions."""
    import os

    from turtle_canon.canon import sort_ontology
    from turtle_canon.utils.exceptions import FailedParsingFile

    unparseable_file = tmp_dir / "unparseable_file.ttl"
    unparseable_file.write_text("test")

    try:
        os.chmod(unparseable_file, 0o000)  # none

        with pytest.raises(
            FailedParsingFile,
            match=(
                "Failed to properly parse the Turtle file at "
                f"{unparseable_file.absolute()}"
            ),
        ):
            sort_ontology(unparseable_file)
    finally:
        os.chmod(unparseable_file, 0o644)
        assert unparseable_file.read_text()
