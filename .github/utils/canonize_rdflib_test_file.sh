#!/usr/bin/env bash

if [ -z "${CI}" ]; then
    echo "This script is intended to be run in a GitHub Actions environment."
    exit 1
else
    echo "Running in CI environment"
    echo "GITHUB_WORKSPACE: ${GITHUB_WORKSPACE}"
    echo "GITHUB_ACTOR: ${GITHUB_ACTOR}"
fi

# Only run if the PR is from dependabot
if [ "${GITHUB_ACTOR}" != "dependabot[bot]" ]; then
    echo "This PR is not from dependabot, exiting early..."
    exit 0
fi

pip install --upgrade pip
pip install -U setuptools wheel
pip install -U ${GITHUB_WORKSPACE}

RDFLIB_VERSION="$(python -c 'import rdflib; print(rdflib.__version__)')"
CANONIZED_FILENAME="turtle_canon_tests_canonized_${RDFLIB_VERSION}.ttl"
CANONIZED_FILEPATH="${GITHUB_WORKSPACE}/tests/static/rdflib_canonized/${CANONIZED_FILENAME}"
CORE_TEST_ONTOLOGY_FILE="${GITHUB_WORKSPACE}/tests/static/turtle_canon_tests.ttl"

if [ -f "${CANONIZED_FILEPATH}" ]; then
    echo "Canonized test file for RDFlib version ${RDFLIB_VERSION} already exists, checking contents..."

    # Copy core test ontology file into a temporary file and canonize it
    TEMP_FILEPATH="/tmp/${CANONIZED_FILENAME}.ttl"
    cp "${CORE_TEST_ONTOLOGY_FILE}" "${TEMP_FILEPATH}"
    turtle-canon "${TEMP_FILEPATH}"

    if [ "$(diff "${TEMP_FILEPATH}" "${CANONIZED_FILEPATH}")" ]; then
        echo "The existing canonized test file for RDFlib version ${RDFLIB_VERSION} differs from the currently generated one using the same version !"
        rm -f "${TEMP_FILEPATH}"
        exit 1
    else
        echo "Canonized test file for RDFlib version ${RDFLIB_VERSION} is up-to-date, nothing to do."
        rm -f "${TEMP_FILEPATH}"
        exit 0
    fi
else
    echo "No canonized test file for RDFlib version ${RDFLIB_VERSION} found, creating it..."

    cp "${CORE_TEST_ONTOLOGY_FILE}" "${CANONIZED_FILEPATH}"
    turtle-canon "${CANONIZED_FILEPATH}"
    exit 0
fi
