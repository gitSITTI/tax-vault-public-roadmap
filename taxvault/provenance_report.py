"""Provenance-cited report core (tri-repo shared module).

This file is the shared, portable core of the "provenance-cited report"
capability. The SAME file is grown in parallel across the sibling repos
(see ``docs/TRI_REPO_PARITY.md``); keep changes in sync.

Design rules:
- Pure standard library. No network. No third-party dependencies.
- Every reported value resolves to a registered source citation. A report
  that references an unknown source fails closed (raises ``ProvenanceError``).
- All source/document text is treated as untrusted DATA, never as
  instructions. The module can flag likely prompt-injection text, but it
  never acts on it.
- Logs are redacted: secret-like and identity-like tokens are masked before
  they can reach a log line.

The module is deliberately domain-neutral. Each repo layers a domain module
on top (tax-year readiness, strategy readiness, QA readiness, ...).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional
import re

__all__ = [
    "ProvenanceError",
    "Source",
    "Fact",
    "Section",
    "Report",
    "redact",
    "injection_score",
    "is_probable_injection",
]


class ProvenanceError(ValueError):
    """Raised when a reported value does not resolve to a known source."""


# --------------------------------------------------------------------------
# Redaction + untrusted-text handling
# --------------------------------------------------------------------------

# Patterns for values that must never reach a log line in the clear. These are
# intentionally broad and err on the side of masking.
_REDACTION_PATTERNS = [
    # US SSN-like: 000-00-0000 or 000000000
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[redacted-ssn]"),
    # Long digit runs that look like account / card numbers (12+ digits)
    (re.compile(r"\b\d{12,}\b"), "[redacted-number]"),
    # API-key / token-like runs of base64/hex (24+ chars). Intentionally
    # aggressive: this may also mask benign long tokens (e.g. git SHAs). It
    # errs toward over-redaction so secrets never leak into a log line.
    (re.compile(r"\b[A-Za-z0-9_\-]{24,}\b"), "[redacted-token]"),
    # key=value secret assignments
    (re.compile(r"(?i)\b(api[_-]?key|secret|token|password|passphrase)\s*[:=]\s*\S+"),
     r"\1=[redacted]"),
]


def redact(text: str) -> str:
    """Return ``text`` with secret-like and identity-like tokens masked.

    Always call this before writing source-derived text to a log.
    """
    out = str(text)
    for pattern, replacement in _REDACTION_PATTERNS:
        out = pattern.sub(replacement, out)
    return out


# Phrases that commonly appear in prompt-injection payloads. Presence raises a
# score; it never changes control flow on its own.
_INJECTION_MARKERS = [
    "ignore previous instructions",
    "ignore all previous",
    "disregard the above",
    "disregard previous",
    "you are now",
    "system prompt",
    "reveal the api key",
    "read the api key",
    "include it in the answer",
    "upload this file",
    "exfiltrate",
    "send this to",
    "run the following command",
    "execute the following",
    "mark this document reviewed",
    "override the",
    "delete all",
]


def injection_score(text: str) -> int:
    """Count likely prompt-injection markers in ``text``.

    This is detection only. Callers store the score as evidence; they must
    not let untrusted text change workflow behavior.
    """
    lowered = str(text).lower()
    return sum(1 for marker in _INJECTION_MARKERS if marker in lowered)


def is_probable_injection(text: str) -> bool:
    """True when ``text`` contains at least one injection marker."""
    return injection_score(text) > 0


# --------------------------------------------------------------------------
# Core data model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Source:
    """A citable origin for a reported value.

    ``locator`` points inside the source (page, line, row, path). ``kind``
    records the source class (e.g. ``synthetic_w2``, ``fixture``, ``qa_scan``)
    so reports can prove they were built from synthetic / approved inputs.
    """

    id: str
    kind: str
    label: str
    locator: str = ""

    def citation(self) -> str:
        loc = f" — {self.locator}" if self.locator else ""
        return f"{self.label} ({self.kind}{loc})"


@dataclass(frozen=True)
class Fact:
    """A single reported value bound to a source id.

    ``value`` is data. It is rendered, never interpreted as an instruction.
    """

    name: str
    value: object
    source_id: str
    note: str = ""


@dataclass
class Section:
    title: str
    body: str = ""
    facts: List[Fact] = field(default_factory=list)

    def add(self, name: str, value: object, source_id: str, note: str = "") -> "Section":
        self.facts.append(Fact(name=name, value=value, source_id=source_id, note=note))
        return self


@dataclass
class Report:
    """A provenance-cited Markdown report.

    Register every source with :meth:`add_source`, add sections/facts, then
    call :meth:`render`. Rendering fails closed if any fact cites a source
    that was never registered.
    """

    title: str
    subtitle: str = ""
    sources: Dict[str, Source] = field(default_factory=dict)
    sections: List[Section] = field(default_factory=list)

    def add_source(self, source: Source) -> Source:
        if source.id in self.sources and self.sources[source.id] != source:
            raise ProvenanceError(f"conflicting source id: {source.id!r}")
        self.sources[source.id] = source
        return source

    def add_section(self, title: str, body: str = "") -> Section:
        section = Section(title=title, body=body)
        self.sections.append(section)
        return section

    def _ordered_used_sources(self) -> List[Source]:
        used: List[Source] = []
        seen = set()
        for section in self.sections:
            for fact in section.facts:
                if fact.source_id not in self.sources:
                    raise ProvenanceError(
                        f"fact {fact.name!r} cites unknown source {fact.source_id!r}"
                    )
                if fact.source_id not in seen:
                    seen.add(fact.source_id)
                    used.append(self.sources[fact.source_id])
        return used

    def validate(self) -> None:
        """Raise :class:`ProvenanceError` if any fact lacks a known source."""
        self._ordered_used_sources()

    def render(self) -> str:
        used = self._ordered_used_sources()
        # Stable citation index in first-use order.
        index = {src.id: n + 1 for n, src in enumerate(used)}

        lines: List[str] = [f"# {self.title}"]
        if self.subtitle:
            lines.append("")
            lines.append(f"_{self.subtitle}_")

        for section in self.sections:
            lines.append("")
            lines.append(f"## {section.title}")
            if section.body:
                lines.append("")
                lines.append(section.body)
            if section.facts:
                lines.append("")
                lines.append("| Field | Value | Source |")
                lines.append("| --- | --- | --- |")
                for fact in section.facts:
                    marker = f"[^{index[fact.source_id]}]"
                    value = _render_value(fact.value)
                    note = f" {fact.note}" if fact.note else ""
                    lines.append(f"| {fact.name} | {value}{note} | {marker} |")

        if used:
            lines.append("")
            lines.append("## Sources")
            lines.append("")
            for src in used:
                lines.append(f"[^{index[src.id]}]: {src.citation()}")

        lines.append("")
        return "\n".join(lines)


def _render_value(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    # Escape pipe and collapse newlines so untrusted text cannot break the
    # Markdown table layout.
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")
