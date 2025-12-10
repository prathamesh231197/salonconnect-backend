# Contributing to SalonConnect Backend

Thank you for contributing! Please follow these steps:

## Branching

- Work from `develop` branch.
- Create feature branches using `feature/<short-description>` or `bugfix/<short>`.
- Keep commits small & focused.

## Code style

- Run `ruff check .` and `black .` before committing.
- Python: follow PEP8.

## Commit messages

Use conventional style:

- `feat:`, `fix:`, `chore:`, `docs:`, `test:`.

## Pull requests

- Target branch: `develop`
- Add a description, testing steps, and mark related issues.
- Ensure CI passes (lint/tests) before merging.

## Adding tests

Add pytest tests in the `tests/` folder.
