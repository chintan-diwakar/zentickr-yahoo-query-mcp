# ACTIVE — Zentickr v0.1.0 release

**Goal:** Ship Zentickr v0.1.0 as a production-quality open-source MCP server (GitHub Release, no PyPI).

**Spec:** docs/superpowers/specs/2026-07-17-zentickr-v0.1.0-release-design.md
**Plan:** docs/superpowers/plans/2026-07-17-zentickr-v0.1.0-release.md
**Audit:** docs/audit/2026-07-17-v0.1.0-audit.md

## Acceptance criteria
- [x] `pip install -e .` works; `zentickr` and `python -m zentickr` start the stdio server
- [x] Every audit finding fixed or explicitly waived in the audit doc
- [x] Offline pytest suite green; ruff clean; CI quality workflow green on the PR
- [x] README rewritten (codex draft, Fable-verified): real captured outputs, client configs, full tool catalog
- [x] Contributor kit present: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue/PR templates, CHANGELOG, AGENTS.md
- [x] PR merged with green CI; tag v0.1.0 pushed; GitHub Release published

## Non-goals
PyPI, Docker, retries/rate-limiting, live-API tests in CI, new data tools.

## Progress log
- 2026-07-17: Spec approved, plan written, audit recorded.
- 2026-07-17: e2e smoke passed (23 tools live); PR ready for merge.
- 2026-07-17: v0.1.0 released — PR #2 squash-merged (b9ffe2f), tag pushed, GitHub Release published.
  Post-release fast-follows from final review: NaN cells inside DataFrame/Series records escape
  NaN→null conversion; get_historical_prices swallows per-symbol dict errors; search_symbols title
  varies by path; frequency arg unvalidated; local gate omits ruff format --check; blocking I/O in
  async tools serializes concurrent calls.
