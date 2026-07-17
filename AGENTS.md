# AGENTS.md

Zentickr — Yahoo Finance MCP server. Python ≥3.10, FastMCP (`mcp`), yahooquery, pandas.

## Commands
- Setup: `python -m venv .venv && .venv/bin/pip install -e ".[dev]"`
- Test: `.venv/bin/pytest` (offline; never add tests that hit the network)
- Lint: `.venv/bin/ruff check . && .venv/bin/ruff format --check .`
- Run: `.venv/bin/zentickr` (stdio MCP server)

## Layout
- `src/zentickr/server.py` — all MCP tools; plain yahooquery attributes go through `_get()`
- `tests/` — offline unit tests; mock `zentickr.server.Ticker` (stub pattern in `tests/test_tools.py`)
- `pyproject.toml` — single source of deps/metadata (there is no requirements.txt)

## Hard constraints
- Tool docstrings are user-facing MCP descriptions — keep them accurate.
- Tools return `"<Title>: Error - ..."` strings on failure, never tracebacks.
- CI (`.github/workflows/quality.yml`: ruff + pytest, py3.10/3.12) must stay green.
- Design docs live in `docs/superpowers/`; contributor docs in CONTRIBUTING.md — link, don't restate.
