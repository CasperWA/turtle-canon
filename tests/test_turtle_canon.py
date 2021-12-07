"""General tests for Turtle Canon."""
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import List


def test_repetitivity(simple_turtle_file: Path) -> None:
    """Ensure firing the Turtle Canon multiple times renders the same result."""
    from os import listdir
    from shutil import copy

    from turtle_canon.canon import canonize

    tmp_dir = simple_turtle_file.parent

    for i in range(5):
        simple_turtle_file_content = simple_turtle_file.read_text(encoding="utf8")
        canonize(simple_turtle_file)
        if i:
            assert simple_turtle_file_content == simple_turtle_file.read_text(
                encoding="utf8"
            )

        copy(
            simple_turtle_file,
            simple_turtle_file.with_stem(f"{simple_turtle_file.stem}_{i}"),
        )
        for j in range(i - 1):
            canonize(simple_turtle_file.with_stem(f"{simple_turtle_file.stem}_{j}"))
            for turtle_file_copy in listdir(tmp_dir):
                assert simple_turtle_file_content == (
                    Path(tmp_dir) / turtle_file_copy
                ).read_text(encoding="utf8")


def test_permutated_files(single_turtle_permutations: "List[Path]") -> None:
    """Ensure firing the Turtle Canon for a single file with content permutations
    renders the same result."""
    from turtle_canon.canon import canonize

    for turtle_file in single_turtle_permutations:
        canonize(turtle_file)

    for turtle_file in single_turtle_permutations:
        for other_turtle_file in single_turtle_permutations:
            if other_turtle_file == turtle_file:
                continue
            assert turtle_file.read_text(
                encoding="utf8"
            ) == other_turtle_file.read_text(encoding="utf8")


def test_rdflib_consistency(top_dir: Path) -> None:
    """Test canonized versions of the `turtle_canon_tests.ttl` file with supported
    RDFlib versions."""
    import re

    version_from_file_regex = r".*_(?P<version>[0-9]+(\.[0-9]+){2})\.ttl$"
    all_rdflib_turtle_files = list(
        (top_dir / "tests" / "static" / "rdflib_canonized").glob("*.ttl")
    )
    if len(all_rdflib_turtle_files) <= 1:
        pytest.skip(
            "Not enough supported RDFlib versions to compare canonization consistency."
        )

    for turtle_file in all_rdflib_turtle_files:
        version_match = re.match(version_from_file_regex, turtle_file.name)
        if version_match:
            rdflib_version = version_match.group("version")
        else:
            pytest.fail(
                f"Couldn't determine the RDFlib version from the file {turtle_file} !"
            )

        for other_turtle_file in all_rdflib_turtle_files:
            if other_turtle_file == turtle_file:
                continue
            version_match = re.match(version_from_file_regex, other_turtle_file.name)
            if version_match:
                other_rdflib_version = version_match.group("version")
            else:
                pytest.fail(
                    "Couldn't determine the RDFlib version from the file "
                    f"{other_turtle_file} !"
                )

            assert turtle_file.read_text(
                encoding="utf8"
            ) == other_turtle_file.read_text(encoding="utf8"), (
                f"The canonized files when using RDFlib versions {rdflib_version} and "
                f"{other_rdflib_version} are not the same !"
            )
