# ACTIVE — Zentickr v0.1.0 release

**Goal:** Ship Zentickr v0.1.0 as a production-quality open-source MCP server (GitHub Release, no PyPI).

**Spec:** docs/superpowers/specs/2026-07-17-zentickr-v0.1.0-release-design.md
**Plan:** docs/superpowers/plans/2026-07-17-zentickr-v0.1.0-release.md
**Audit:** docs/audit/2026-07-17-v0.1.0-audit.md

## Acceptance criteria
- [ ] `pip install -e .` works; `zentickr` and `python -m zentickr` start the stdio server
- [ ] Every audit finding fixed or explicitly waived in the audit doc
- [ ] Offline pytest suite green; ruff clean; CI quality workflow green on the PR
- [ ] README rewritten (codex draft, Fable-verified): real captured outputs, client configs, full tool catalog
- [ ] Contributor kit present: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue/PR templates, CHANGELOG, AGENTS.md
- [ ] PR merged with green CI; tag v0.1.0 pushed; GitHub Release published

## Non-goals
PyPI, Docker, retries/rate-limiting, live-API tests in CI, new data tools.

## Progress log
- 2026-07-17: Spec approved, plan written, audit recorded.
