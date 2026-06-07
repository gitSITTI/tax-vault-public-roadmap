# Roadmap

## Phase 0: Public Planning

Milestone goal: make it easy to contribute without private data.

Acceptance criteria:

- Public-safe requirements and contribution docs exist.
- Library review matrix exists.
- Synthetic fixture plan exists.
- Security checklist exists.
- Public data rules are explicit.
- Initial issue labels and contribution categories are defined.
- Parser review rubric exists.

Issue-ready tasks:

- Create synthetic W-2 fixture spec.
- Create synthetic bank statement fixture spec.
- Review one PDF text extraction library.
- Add prompt-injection fixture examples.

## Phase 1: Local Catalog Prototype

Milestone goal: catalog synthetic files and preserve provenance.

Acceptance criteria:

- Local document manifest records synthetic files.
- Synthetic PDF ingestion creates document and file records.
- SQL schema prototype stores documents, pages, chunks, and provenance.
- Provenance citation prototype resolves to synthetic source pages.
- Deterministic document fingerprinting identifies duplicates.
- Redacted log format is documented and tested.

Issue-ready tasks:

- Implement manifest JSON schema.
- Add duplicate synthetic fixture.
- Add citation URI parser.
- Add redacted logging tests.

## Phase 2: Search, Review, And Tools

Milestone goal: search synthetic evidence and expose safe read-only tooling.

Acceptance criteria:

- Vector index prototype stores synthetic chunks only.
- Dashboard prototype loads synthetic catalog and review queue.
- MCP read-only prototype exposes catalog search and citation resolution.
- Prompt-injection fixture suite fails closed.
- Review queue model supports open, accepted, rejected, and deferred states.
- Citation viewer contract opens synthetic source evidence.
- Export manifest contract lists included synthetic documents.

Issue-ready tasks:

- Implement vector metadata contract.
- Add read-only tool contract tests.
- Add browser smoke test with synthetic data.
- Add review state transition tests.

## Phase 3: Tax-Year Readiness With Synthetic Data

Milestone goal: demonstrate a full fake tax-year workflow.

Acceptance criteria:

- Synthetic W-2 reconciles to synthetic 1040.
- Missing synthetic 1099 creates readiness gap.
- Public benchmark reports compare extraction adapters.
- Contributor-maintained parser adapters follow review rubric.
- Multi-engine extraction comparison records disagreements.
- Rebuildable vector index proves orphan checks.
- Public docs quality gate blocks incomplete docs.

Issue-ready tasks:

- Add W-2 to 1040 reconciliation fixture.
- Add missing-form readiness fixture.
- Add parser benchmark report template.
- Add vector rebuild test.
