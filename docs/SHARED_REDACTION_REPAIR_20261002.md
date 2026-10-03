# Shared report redaction repair

Status: implemented; independently validated by Sol (linked below). Source finding APP-07 in gitSITTI/tradingview-codex-onboarding-agent code audit 2026-10-02.

The core now masks nested structured secret fields before JSON serialization and quoted/escaped text assignments, URL credentials and token queries. Numeric metrics remain typed. `redact_object(..., mask_identifiers=False)` preserves ordinary repository paths and identifiers while masking explicit secrets. This bounded filter is not a general PII or tax-document admission certification.

The core is copied byte-identically across TradingView `tools/provenance_report.py`, tax-vault `taxvault/provenance_report.py`, and ConfluenceOS `tools/provenance_report.py`. The existing tax readiness consumer and its tests remain part of verification.

Run `python -m pytest -q -p no:cacheprovider tests/test_shared_redaction_regression.py`.

Independent validation: [Sol re-observation](../reports/shared-redaction/2026-10-02/sol-validation-root.md), with [raw test evidence](../reports/shared-redaction/2026-10-02/sol-validation-root-tests.json). Exact-path staging excludes generated caches. This completes the shared-redaction subset; it does not claim the other TradingView audit repairs are delivered here.
