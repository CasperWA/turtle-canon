# Turtle Canon

*It's turtles all the way down.*

![Codecov main](https://img.shields.io/codecov/c/github/CasperWA/turtle-canon/main)
![CI main](https://github.com/CasperWA/turtle-canon/actions/workflows/ci_tests.yml/badge.svg?branch=main)

A tool for canonizing Turtle (`.ttl`) ontology files.

The domain standardized tool for editing and creating ontologies is [Protégé](https://protege.stanford.edu/).
The Turtle (`.ttl`) file format is a format based on XML and OWL, which is considered one of the most readable formats for OWL ontology files.
However, Protégé writes the order of ontology entities differently depending on the version, this tool mitigates this by running the file through a canonizing parser that ensures the classes are sorted and listed in the same way, always.

The main use case for developing this tool is when developing ontologies utilizing versioning tools such as `git`, `svn` or similar, which are single character diff-sensitive.

## Install

The tool is written in Python 3.9, so one needs a Python 3.9 interpreter to run it at this stage.
The plan is to make a stand-alone executable for each of the major OS'.

Install via PyPI (stable version, recommended):

```shell
python3.9 -m pip install turtle-canon
```

Install via GitHub (development version):

```shell
python3.9 -m pip install git+https://github.com/CasperWA/turtle-canon#egg=turtle-canon
```

## Usage

To run the tool, simply run:

```shell
turtle-canon path/to/my_ontology_file.ttl
```

For more information about the tool and the options available, run `turtle-canon --help`.  
To check the version run `turtle-canon --version`.

The currently latest stable version is **0.0.1**.

## License & copyright

This tool is [MIT Licensed](LICENSE) and copyright &copy; 2021 Casper Welzel Andersen ([GitHub](https://github.com/CasperWA), [GitLab](https://gitlab.com/CasperWA), [website](https://casper.welzel.nu)) & SINTEF.
