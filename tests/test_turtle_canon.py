"""General tests for Turtle Canon."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    pass


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


def test_permutated_files(single_turtle_permutations: list[Path]) -> None:
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


def test_extra_whitespace(simple_turtle_file: Path) -> None:
    """Add random valid whitespace to a turtle file and ensure canonizing it doesn't
    change."""
    from random import randrange

    from turtle_canon.canon import canonize

    SPACE = " "
    multi_line_start_end = (
        'rdfs:comment """Test ontology file.',
        "owl:versionInfo",
    )

    canonize(simple_turtle_file)
    original_canonized_content = simple_turtle_file.read_text(encoding="utf8")

    whitespaced_content_lines = original_canonized_content.splitlines()

    assertion_fail_msg = "Failed after implementing the following changes:\n"
    for number, change in enumerate(
        (
            "End-of-line whitespace",
            "Extra empty lines",
            "Extra empty lines full of whitespace",
        )
    ):
        comment_start_line_number = comment_end_line_number = None
        for index, line in enumerate(whitespaced_content_lines):
            if multi_line_start_end[0] in line:
                comment_start_line_number = index
            elif multi_line_start_end[1] in line:
                comment_end_line_number = index
            if (
                comment_start_line_number is not None
                and comment_end_line_number is not None
            ):
                break
        else:
            if (
                comment_start_line_number is not None
                and comment_end_line_number is None
            ):
                msg = (
                    f"Could not find the {multi_line_start_end[1]!r} line in the test "
                    "Turtle file !"
                )
            elif (
                comment_start_line_number is None
                and comment_end_line_number is not None
            ):
                msg = (
                    f"Could not find the {multi_line_start_end[0]!r} line in the test "
                    "Turtle file !"
                )
            else:
                msg = (
                    f"Could neither find the {multi_line_start_end[0]!r} line or the "
                    f"{multi_line_start_end[1]!r} line in the test Turtle file !"
                )
            pytest.fail(msg + f"\n\nCanonized file:\n\n{original_canonized_content}")
        comment_range_index = range(comment_start_line_number, comment_end_line_number)

        random_line_number_cache = []
        for _ in range(randrange(5, 10)):
            random_line_number = randrange(0, len(whitespaced_content_lines))
            while (
                random_line_number in comment_range_index
                or random_line_number in random_line_number_cache
            ):
                random_line_number = randrange(0, len(whitespaced_content_lines))
            random_line_number_cache.append(random_line_number)

            if change == "End-of-line whitespace":
                whitespaced_content_lines[random_line_number] += (
                    randrange(1, 20) * SPACE
                )
            elif change == "Extra empty lines":
                whitespaced_content_lines.insert(random_line_number, "")
                if random_line_number < comment_start_line_number:
                    comment_start_line_number += 1
                    comment_end_line_number += 1
                    comment_range_index = range(
                        comment_start_line_number, comment_end_line_number
                    )
            elif change == "Extra empty lines full of whitespace":
                whitespaced_content_lines.insert(
                    random_line_number, randrange(1, 20) * SPACE
                )
                if random_line_number < comment_start_line_number:
                    comment_start_line_number += 1
                    comment_end_line_number += 1
                    comment_range_index = range(
                        comment_start_line_number, comment_end_line_number
                    )
            else:
                pytest.fail("Failure in spelling hard-coded change (descriptions) !")

        assertion_fail_msg += f"  {number + 1}) {change}.\n"

        changes = Path(simple_turtle_file.parent / f"changes_{number}.ttl")
        changes.write_text("\n".join(whitespaced_content_lines) + "\n", encoding="utf8")
        canonize(changes)
        assert (
            changes.read_text(encoding="utf8") == original_canonized_content
        ), assertion_fail_msg


def test_different_sources(different_sources_ontologies: list[Path]) -> None:
    """Test that the canonization is true only to the given set of triples."""
    import re

    from turtle_canon.canon import canonize

    source_regex = r"^turtle_canon_tests_(?P<source>.*)\.ttl$"

    for turtle_file in different_sources_ontologies:
        source_match = re.match(source_regex, turtle_file.name)
        if source_match:
            source = source_match.group("source")
        else:
            pytest.fail(f"Couldn't determine source from {turtle_file.name!r} !")

        try:
            canonize(turtle_file)
        except Exception as exc:
            pytest.fail(
                f"Failed canonizing file from source {source}.\n\nException:\n{exc}"
            )
