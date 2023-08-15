#!/usr/bin/env bash

function test-unit() {
  python -m pytest tests/unit --verbose --junitxml tests/reports/unit_tests.xml
}

function test-integration() {
  python -m pytest tests/integration --verbose --junitxml tests/reports/unit_tests.xml
}

function test-e2e() {
  python -m pytest tests/e2e --verbose --junitxml tests/reports/unit_tests.xml
}

function test-coverage() {
  python -m pytest tests/unit \
    --cov-report html:tests/reports/coverage/htmlcov \
    --cov-report xml:tests/reports/coverage/cobertura-coverage.xml \
    --cov-report term \
    --cov=src
  sleep 1
  rm .coverage
}

function test-coverage-html() {
  test-coverage
  open tests/reports/coverage/htmlcov/index.html
}

function test() {
  test-unit && test-integration && test-e2e
}


function code-analysis() {
  pylint src --rcfile=.pylintrc --output-format=colorized
}

function build() {
  test-unit && code-analysis && export-api-reference
}
