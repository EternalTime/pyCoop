# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

- Development happens in a venv inside the clone (`python3 -m venv .venv`). This
  machine's Homebrew Python has no `pip` on PATH and refuses system-wide installs
  under PEP 668, so a bare `pip install -e .` fails twice over.
- Dependency groups live in `pyproject.toml`: `test` (pytest), `docs`
  (sphinx, sphinx-rtd-theme), `interactive` (ipywidgets).
- Supported range is Python 3.9-3.14; `pytest` from the repo root is the
  whole suite. `README.md` and `docs/getting_started.rst` both state the
  install and must agree with each other and with `pyproject.toml`.
- Docs are built with `sphinx-build -b html docs docs/_build` and published at
  https://damiansowinski.com/pyCoop/ by copying into the website repo.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
