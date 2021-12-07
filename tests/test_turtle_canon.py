"""General tests for Turtle Canon."""
from pathlib import Path


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
                assert (
                    simple_turtle_file_content
                    == (Path(tmp_dir) / turtle_file_copy).read_text()
                )
