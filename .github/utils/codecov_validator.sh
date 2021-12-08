#!/usr/bin/env bash
set -e

if [ -n "${CI}" ]; then
    echo "Not checking codecov configuration file when CI is true."
    exit 0
fi

CODECOV_FILE=.codecov.yml
CODECOV_TMP_OUTPUT=/tmp/codecov_validator.txt

curl -s --data-binary @${CODECOV_FILE} https://codecov.io/validate > ${CODECOV_TMP_OUTPUT}

cat ${CODECOV_TMP_OUTPUT} | grep "Valid!" && rm -f ${CODECOV_TMP_OUTPUT} || (cat ${CODECOV_TMP_OUTPUT} ; rm -f ${CODECOV_TMP_OUTPUT} ; exit 1)
