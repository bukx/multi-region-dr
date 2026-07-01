# Contributing

## Local setup

1. Create a virtual environment with Python 3.12 or newer.
2. Install the project and dev tooling with `python -m pip install -e .[dev]`.
3. Run checks before opening a pull request:
   - `PYTHONPATH=src python -m unittest discover -s tests`
   - `python -m ruff check .`
   - `python -m mypy src tests`

## Pull requests

- Keep infrastructure and application behavior changes small and reviewable.
- Add or update tests whenever orchestration behavior changes.
- Make sure CI is green before requesting review.
