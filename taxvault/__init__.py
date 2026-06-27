"""Tax Vault public prototype (synthetic data only).

Local-first, offline, standard-library tax-year readiness tooling. Every
reported value resolves to a source citation; all document text is treated as
untrusted data. See ``docs/TAX_YEAR_READINESS.md``.
"""

from .provenance_report import (
    Fact,
    ProvenanceError,
    Report,
    Section,
    Source,
    injection_score,
    is_probable_injection,
    redact,
)

__all__ = [
    "Fact",
    "ProvenanceError",
    "Report",
    "Section",
    "Source",
    "injection_score",
    "is_probable_injection",
    "redact",
]
