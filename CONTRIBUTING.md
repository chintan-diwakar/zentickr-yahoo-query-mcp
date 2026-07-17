# Contributing to Zentickr

Thanks for helping improve Zentickr! Small, focused PRs merge fastest.

## Dev setup

```bash
git clone https://github.com/chintan-diwakar/zentickr-yahoo-query-mcp.git
cd zentickr-yahoo-query-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Run the server locally

`zentickr` (or `python -m zentickr`) starts a stdio MCP server. Pair it with an
MCP client — Claude Desktop/Claude Code (see README) or the inspector:
`npx @modelcontextprotocol/inspector .venv/bin/zentickr`.

## Tests and style

```bash
pytest                                # offline — tests must never hit the network
ruff check . && ruff format --check .
```

- Mock `zentickr.server.Ticker` in tests (see `tests/test_tools.py` for the stub pattern).
- Tool docstrings are the descriptions MCP clients show users — keep them accurate.
- Tools return clean `"<Title>: Error - ..."` strings on failure, never tracebacks.

## Adding a new tool

1. Add an async function in `src/zentickr/server.py` decorated with `@mcp.tool()`.
   If it maps to a plain yahooquery attribute, delegate:
   `return _get(symbols, "<yahooquery_attr>", "<Title>")`.
   Custom logic wraps its body in try/except returning `"<Title>: Error - {exc}"`.
2. Add the name to `EXPECTED_TOOLS` in `tests/test_tools.py` plus a behavior test.
3. Add it to the README tool catalog.
4. Verify once against live Yahoo Finance data before opening the PR.

## PR flow

- Branch from `main` (`feat/<short-name>`, `fix/<short-name>`).
- One change per PR; fill in the PR template; link the issue it closes.
- CI (ruff + pytest on Python 3.10 and 3.12) must be green.

## Bugs, features, security

Bugs and feature requests: GitHub issue forms.
Security problems: see [SECURITY.md](SECURITY.md) — please don't open a public issue.
