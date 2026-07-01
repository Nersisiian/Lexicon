# Contributing to Lexicon

## How to Contribute
1. Fork the repository and create your branch from `main`.
2. If you added code, add tests.
3. Ensure the test suite passes (`make test`).
4. Make sure your code lints (`make lint`).
5. Open a pull request with a clear title and description.

## Development Setup
- Install prerequisites: Python 3.12, Poetry, Docker Desktop.
- Run `docker compose -f deploy/docker-compose/docker-compose.test.yml up -d` to start the local environment.
- Refer to the README for more details.

## Code Style
We follow PEP 8 with a 120-character line limit. All public methods must have docstrings.

## Reporting Bugs
Open an issue using the bug report template. Include steps to reproduce, expected vs actual behavior, and environment details.

## Suggesting Enhancements
Open an issue using the feature request template. Explain why the enhancement would be useful.

## Code Review
All submissions require at least one approving review from the owning team (see CODEOWNERS).
