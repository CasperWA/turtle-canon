"""Setup file for installing the `turtle-canon` package."""
from pathlib import Path
import re

from setuptools import setup, find_packages


TOP_DIR = Path(__file__).parent.resolve()

with open(TOP_DIR / "turtle_canon/__init__.py", "r", encoding="utf8") as handle:
    VERSION = AUTHOR = AUTHOR_EMAIL = None
    for line in handle.readlines():
        VERSION_match = re.match(r'__version__ = (\'|")(?P<version>.+)(\'|")', line)
        AUTHOR_match = re.match(r'__author__ = (\'|")(?P<author>.+)(\'|")', line)
        AUTHOR_EMAIL_match = re.match(
            r'__author_email__ = (\'|")(?P<email>.+)(\'|")', line
        )

        if VERSION_match is not None:
            VERSION = VERSION_match
        if AUTHOR_match is not None:
            AUTHOR = AUTHOR_match
        if AUTHOR_EMAIL_match is not None:
            AUTHOR_EMAIL = AUTHOR_EMAIL_match

    for info, value in {
        "version": VERSION,
        "author": AUTHOR,
        "author email": AUTHOR_EMAIL,
    }.items():
        if value is None:
            raise RuntimeError(
                f"Could not determine {info} from "
                f"{TOP_DIR / 'turtle_canon/__init__.py'} !"
            )
    VERSION = VERSION.group("version")  # type: ignore[union-attr]
    AUTHOR = AUTHOR.group("author")  # type: ignore[union-attr]
    AUTHOR_EMAIL = AUTHOR_EMAIL.group("email")  # type: ignore[union-attr]

with open(TOP_DIR / "requirements.txt", "r", encoding="utf8") as handle:
    BASE = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

with open(TOP_DIR / "requirements_docs.txt", "r", encoding="utf8") as handle:
    DOCS = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

with open(TOP_DIR / "requirements_dev.txt", "r", encoding="utf8") as handle:
    DEV = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ] + DOCS

setup(
    name="turtle-canon",
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url="https://github.com/CasperWA/turtle-canon",
    description="A tool for canonizing Turtle (`.ttl`) ontology files.",
    long_description=(TOP_DIR / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=BASE,
    extras_require={"dev": DEV, "docs": DOCS},
    keywords="ontology turtle",
    entry_points={
        "console_scripts": [
            "turtle-canon = turtle_canon.cli.cmd_turtle_canon:main",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Version Control",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
