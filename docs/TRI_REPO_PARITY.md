# Tri-Repo Parity Rule

## The rule

When a capability is reusable across domains, grow it in **all three** sibling
repositories with the same shape and the same shared core, so the repos evolve
together instead of drifting apart:

- `gitSITTI/tax-vault-public-roadmap` — tax-year readiness reporting.
- `gitSITTI/tradingview-codex-onboarding-agent` — strategy/backtest reporting.
- `gitSITTI/ConfluenceOS` — QA / operational readiness reporting.

A change that adds or improves a shared capability is not "done" until it has
been applied to whichever of the three repos it sensibly applies to.

## How parity is implemented

The portable core lives in a single file that is copied **verbatim** into each
repo:

- `provenance_report.py` — provenance-cited report core. Pure standard
  library, no network, treats all source text as untrusted data, fails closed
  when a value lacks a registered source.

Each repo then layers a thin, domain-specific module on top of the identical
core:

| Repo | Domain module | Report produced |
| --- | --- | --- |
| tax-vault | `taxvault/reconcile.py` | Tax-year readiness |
| tradingview | `tools/strategy_readiness.py` | Strategy / backtest readiness |
| ConfluenceOS | `tools/qa_readiness.py` | QA / docs readiness |

## Keeping the core in sync

The shared core file is byte-identical across the three repos. To verify:

```bash
# from a directory containing all three checkouts
sha256sum \
  tax-vault-public-roadmap/taxvault/provenance_report.py \
  tradingview-codex-onboarding-agent/tools/provenance_report.py \
  ConfluenceOS/tools/provenance_report.py
```

All three hashes must match. When you change the core in one repo, copy it to
the other two in the same change set and update each repo's domain module and
tests.

## Invariants the shared core must preserve

- Standard library only. No third-party dependencies. No network calls.
- Every reported value resolves to a registered source citation.
- Rendering fails closed (`ProvenanceError`) on any unregistered source.
- All source/document text is untrusted data, never executed as instructions.
- Logs are redacted: secret-like and identity-like tokens are masked.
