"""CLI: build a tax-year readiness report from synthetic documents.

Usage:
    python -m taxvault.taxreport [--fixtures DIR] [--out FILE] [--json]

Defaults to the bundled synthetic fixtures. Offline, standard library only.
Exit code is non-zero when the tax year is NOT ready, so the command doubles
as a readiness gate in CI.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

from .provenance_report import redact
from .reconcile import build_report, load_documents, reconcile

DEFAULT_FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic"


def _result_to_dict(result) -> dict:
    return {
        "tax_year": result.tax_year,
        "ready": result.is_ready,
        "income_total": result.income_total,
        "return_total_income": result.return_total_income,
        "income_reconciles": result.income_reconciles,
        "income_difference": result.income_difference,
        "withholding_reconciles": result.withholding_reconciles,
        "missing_forms": result.missing_forms,
        "injection_findings": [
            {"doc_id": f.doc_id, "score": f.score} for f in result.injection_findings
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Tax-year readiness report (synthetic).")
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES),
                        help="directory of synthetic *.json documents")
    parser.add_argument("--out", default=None, help="write Markdown report to FILE")
    parser.add_argument("--json", action="store_true",
                        help="print a machine-readable summary instead of Markdown")
    args = parser.parse_args(argv)

    documents = load_documents(args.fixtures)
    result = reconcile(documents)

    if args.json:
        print(json.dumps(_result_to_dict(result), indent=2))
    else:
        report = build_report(result)
        report.validate()  # fail closed if any value lacks provenance
        markdown = report.render()
        if args.out:
            Path(args.out).write_text(markdown, encoding="utf-8")
            # Redact in case any source label carried sensitive-looking text.
            print(redact(f"Wrote report to {args.out}"))
        else:
            print(markdown)

    return 0 if result.is_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
