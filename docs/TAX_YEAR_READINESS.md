# Tax-Year Readiness Report

A local-first, offline prototype that proves the Tax Vault architecture using
synthetic data only. It reconciles synthetic source forms against a synthetic
return, finds missing expected forms, and renders a provenance-cited Markdown
report where every value resolves to a source citation.

## What it does

- Loads synthetic documents (`fixtures/synthetic/*.json`).
- Reconciles income: the sum of source-form income must equal the return's
  total income line.
- Reconciles federal withholding across source forms versus the return.
- Detects readiness gaps: forms the return expects that are absent from the
  catalog (for example a missing 1099-INT).
- Records untrusted-content findings: prompt-injection text inside a document
  is stored as evidence and cited, but never executed as an instruction.
- Fails closed: a report referencing an unregistered source raises
  `ProvenanceError` instead of emitting an uncited value.

## Run it

```bash
# Human-readable report (exit code 1 when NOT ready — usable as a CI gate)
python -m taxvault.taxreport

# Write the report to a file
python -m taxvault.taxreport --out readiness.md

# Machine-readable summary
python -m taxvault.taxreport --json

# Tests
python -m unittest discover -s tests
```

## Document fixture format

Each synthetic document is a JSON object:

```json
{
  "doc_id": "syn-w2-0001",
  "kind": "synthetic_w2",
  "label": "Synthetic W-2 (ACME SYNTHETIC LLC)",
  "tax_year": 2025,
  "fields": {
    "wages": { "value": 72000.0, "locator": "Box 1 wages" }
  },
  "untrusted_text": "any document text — treated as untrusted data"
}
```

- `kind` maps to an income line via `INCOME_FIELDS` in `taxvault/reconcile.py`.
- The return document (`synthetic_1040`) lists `expected_forms`; any expected
  kind that is absent becomes a readiness gap.
- `locator` is the in-document citation (box, line, row) shown in the report.

## Safety properties

- Standard library only. No network. No third-party dependencies.
- Synthetic data only — see `SECURITY.md` and `CONTRIBUTING.md`.
- All document text is untrusted: `injection_score()` flags likely
  prompt-injection payloads but the workflow never acts on document content.
- `redact()` masks identity-like and secret-like tokens before logging.

## Module map

| File | Responsibility |
| --- | --- |
| `taxvault/provenance_report.py` | Shared report core (see `docs/TRI_REPO_PARITY.md`). |
| `taxvault/reconcile.py` | Tax-year reconciliation and report assembly. |
| `taxvault/taxreport.py` | CLI entry point and readiness gate. |
| `fixtures/synthetic/` | Synthetic W-2, 1099-NEC, and 1040 documents. |
| `tests/` | Unit tests for the core and reconciliation. |
