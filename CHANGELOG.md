# Changelog

All notable changes to this project are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-17

First release.

### Added
- MCP server exposing 23 Yahoo Finance tools via yahooquery: financial
  statements, price data, valuation, earnings, ownership, analyst
  recommendations, ESG scores, calendar events, historical prices, and
  symbol search.
- Installable package: `pip install -e .` provides the `zentickr` command
  (stdio MCP server); `python -m zentickr` also works.
- Offline test suite and GitHub Actions CI (ruff + pytest on Python 3.10/3.12).
- Contributor kit: CONTRIBUTING, code of conduct, security policy,
  issue forms, PR template.

### Fixed
- Packaging metadata was in `project.toml`, which pip ignores — the package
  was never installable and the declared console script never existed.
- Entry point crashed at launch (`asyncio.run` around the synchronous `mcp.run`).
- JSON serialization raised `ValueError` on array-like values.
- Tools now return clean error strings instead of leaking tracebacks.

[0.1.0]: https://github.com/chintan-diwakar/zentickr-yahoo-query-mcp/releases/tag/v0.1.0
