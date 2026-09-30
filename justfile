python := env_var_or_default("PYTHON", "python3")

# List all available recipes
_default:
    @just --list

# Install the package and development tools in editable mode
install:
    {{python}} -m pip install --editable ".[dev]"

# Format Python files and apply safe lint fixes
format:
    {{python}} -m ruff format .
    {{python}} -m ruff check . --fix

# Check lint rules and formatting without changing files
lint:
    {{python}} -m ruff check .
    {{python}} -m ruff format --check .

# Run the test suite
test:
    {{python}} -m pytest

# Build the source and wheel distributions
build:
    {{python}} -m build

# Validate built distribution metadata
dist-check: build
    {{python}} -m twine check dist/*

# Run all static checks and tests
check: lint test

# Run checks, tests, build, and distribution validation
all: check dist-check
