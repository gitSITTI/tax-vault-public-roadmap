"""Tax-year readiness reconciliation over synthetic documents.

Loads synthetic source documents (W-2, 1099, 1040), reconciles income and
withholding against the return, finds missing expected forms, and records any
prompt-injection text found in document content. Everything resolves to a
source citation so the result can be rendered as a provenance-cited report.

Synthetic data only. Offline. Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import json

from .provenance_report import Report, Source, injection_score

# Cent tolerance for floating-point money comparisons.
TOLERANCE = 0.01

# Income line that each source-form kind contributes to the return total.
INCOME_FIELDS: Dict[str, str] = {
    "synthetic_w2": "wages",
    "synthetic_1099nec": "nonemployee_comp",
    "synthetic_1099int": "interest_income",
    "synthetic_1099div": "ordinary_dividends",
    "synthetic_1099misc": "other_income",
}

# Human labels for expected-but-missing forms.
FORM_LABELS: Dict[str, str] = {
    "synthetic_w2": "W-2",
    "synthetic_1099nec": "1099-NEC",
    "synthetic_1099int": "1099-INT",
    "synthetic_1099div": "1099-DIV",
    "synthetic_1099misc": "1099-MISC",
}

RETURN_KIND = "synthetic_1040"

# Location of the bundled synthetic fixtures.
FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic"
DEFAULT_FIXTURES_AVAILABLE = FIXTURES_DIR.is_dir() and any(FIXTURES_DIR.glob("*.json"))


@dataclass
class IncomeItem:
    doc_id: str
    kind: str
    label: str
    field_name: str
    amount: float
    locator: str


@dataclass
class InjectionFinding:
    doc_id: str
    label: str
    score: int
    excerpt: str


@dataclass
class ReconciliationResult:
    tax_year: Optional[int]
    income_items: List[IncomeItem] = field(default_factory=list)
    income_total: float = 0.0
    return_total_income: Optional[float] = None
    return_total_locator: str = ""
    income_reconciles: bool = False
    income_difference: float = 0.0
    withholding_sources_total: float = 0.0
    return_withholding: Optional[float] = None
    withholding_reconciles: bool = False
    missing_forms: List[str] = field(default_factory=list)
    injection_findings: List[InjectionFinding] = field(default_factory=list)
    documents: List[dict] = field(default_factory=list)

    @property
    def is_ready(self) -> bool:
        return (
            self.income_reconciles
            and self.withholding_reconciles
            and not self.missing_forms
        )


def load_documents(directory: str | Path) -> List[dict]:
    """Load and lightly validate every ``*.json`` document in ``directory``."""
    root = Path(directory)
    documents: List[dict] = []
    for path in sorted(root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "kind" not in data or "doc_id" not in data:
            raise ValueError(f"{path.name}: document needs 'doc_id' and 'kind'")
        data.setdefault("_path", str(path))
        documents.append(data)
    return documents


def _field(doc: dict, name: str) -> Optional[dict]:
    return (doc.get("fields") or {}).get(name)


def reconcile(documents: List[dict]) -> ReconciliationResult:
    """Reconcile synthetic source forms against the synthetic return."""
    returns = [d for d in documents if d.get("kind") == RETURN_KIND]
    if len(returns) > 1:
        raise ValueError("more than one return document supplied")
    ret = returns[0] if returns else None

    years = {doc["tax_year"] for doc in documents if doc.get("tax_year") is not None}
    if len(years) > 1:
        raise ValueError(f"documents span multiple tax years: {sorted(years)}")
    tax_year = next(iter(years)) if years else None

    result = ReconciliationResult(tax_year=tax_year, documents=documents)

    # Income items from every source form we understand.
    for doc in documents:
        income_field = INCOME_FIELDS.get(doc.get("kind", ""))
        if not income_field:
            continue
        field_data = _field(doc, income_field)
        if not field_data:
            continue
        amount = float(field_data["value"])
        result.income_items.append(
            IncomeItem(
                doc_id=doc["doc_id"],
                kind=doc["kind"],
                label=doc.get("label", doc["doc_id"]),
                field_name=income_field,
                amount=amount,
                locator=field_data.get("locator", ""),
            )
        )
    result.income_total = round(sum(i.amount for i in result.income_items), 2)

    # Withholding from source forms (any form may carry federal_withholding).
    wh_total = 0.0
    for doc in documents:
        if doc.get("kind") == RETURN_KIND:
            continue
        wh = _field(doc, "federal_withholding")
        if wh:
            wh_total += float(wh["value"])
    result.withholding_sources_total = round(wh_total, 2)

    # Compare to the return.
    if ret is not None:
        total = _field(ret, "total_income")
        if total:
            result.return_total_income = float(total["value"])
            result.return_total_locator = total.get("locator", "")
            result.income_difference = round(
                result.income_total - result.return_total_income, 2
            )
            result.income_reconciles = abs(result.income_difference) <= TOLERANCE

        ret_wh = _field(ret, "federal_withholding")
        if ret_wh:
            result.return_withholding = float(ret_wh["value"])
            result.withholding_reconciles = (
                abs(result.withholding_sources_total - result.return_withholding)
                <= TOLERANCE
            )

        # Missing expected forms -> readiness gaps.
        present_kinds = {d.get("kind") for d in documents}
        for expected in ret.get("expected_forms", []):
            if expected not in present_kinds:
                result.missing_forms.append(expected)

    # Prompt-injection scan over untrusted document text (evidence only).
    for doc in documents:
        text = doc.get("untrusted_text", "")
        score = injection_score(text)
        if score:
            result.injection_findings.append(
                InjectionFinding(
                    doc_id=doc["doc_id"],
                    label=doc.get("label", doc["doc_id"]),
                    score=score,
                    excerpt=str(text)[:120],
                )
            )

    return result


def build_report(result: ReconciliationResult) -> Report:
    """Render a reconciliation result as a provenance-cited report."""
    year = result.tax_year if result.tax_year is not None else "unknown"
    report = Report(
        title=f"Tax-Year Readiness Report — {year}",
        subtitle="Synthetic data only. Every value resolves to a source citation.",
    )

    # Register a source per source-form income item + the return.
    for item in result.income_items:
        report.add_source(
            Source(
                id=item.doc_id,
                kind=item.kind,
                label=item.label,
                locator=item.locator,
            )
        )
    ret = next((d for d in result.documents if d.get("kind") == RETURN_KIND), None)
    if ret is not None:
        report.add_source(
            Source(
                id=ret["doc_id"],
                kind=RETURN_KIND,
                label=ret.get("label", ret["doc_id"]),
                locator=result.return_total_locator,
            )
        )

    summary = report.add_section(
        "Readiness Summary",
        "READY" if result.is_ready else "NOT READY — see gaps below.",
    )
    if ret is not None:
        summary.add("Return total income", result.return_total_income, ret["doc_id"])
    for item in result.income_items:
        summary.add(
            f"{FORM_LABELS.get(item.kind, item.kind)} {item.field_name}",
            item.amount,
            item.doc_id,
        )

    if ret is not None:
        recon = report.add_section("Income Reconciliation")
        recon.add("Sum of source-form income", result.income_total, ret["doc_id"],
                  note="(computed)")
        recon.add("Return total income", result.return_total_income, ret["doc_id"])
        recon.add("Difference", result.income_difference, ret["doc_id"])
        recon.add("Income reconciles", result.income_reconciles, ret["doc_id"])
        if result.return_withholding is not None:
            recon.add("Withholding reconciles", result.withholding_reconciles,
                      ret["doc_id"])

    if result.missing_forms:
        gaps = report.add_section(
            "Readiness Gaps",
            "Expected forms that were not found in the catalog.",
        )
        if ret is not None:
            for kind in result.missing_forms:
                gaps.add("Missing form", FORM_LABELS.get(kind, kind), ret["doc_id"])

    if result.injection_findings:
        inj = report.add_section(
            "Untrusted-Content Findings",
            "Document text below is recorded as untrusted evidence only. "
            "It was not executed as an instruction.",
        )
        for finding in result.injection_findings:
            if finding.doc_id not in report.sources:
                report.add_source(
                    Source(id=finding.doc_id, kind="synthetic_document",
                           label=finding.label, locator="untrusted_text")
                )
            inj.add(
                f"Injection markers in {finding.doc_id}",
                finding.score,
                finding.doc_id,
                note=f"— quarantined excerpt: {finding.excerpt!r}",
            )

    return report
