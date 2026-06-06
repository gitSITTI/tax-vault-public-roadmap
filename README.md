# Tax Vault Public Roadmap

Public-safe roadmap for a local-first tax and financial-document catalog.

This repository intentionally contains no private data and no private implementation secrets. It exists so contributors can help design and build a community version of a source-cited financial document intelligence system.

## Goals

- Local-first financial document catalog.
- PDF extraction with provenance.
- SQL plus vector indexing.
- Tax-year readiness workflows.
- Prompt-injection-resistant document QA.
- Synthetic fixtures only.

## Non-Goals

- No real user tax files.
- No bank statements.
- No account numbers.
- No secrets.
- No private deployment details.

## Contribution Areas

- Synthetic tax document fixtures.
- PDF extraction benchmarks.
- Security review checklists.
- Prompt-injection test cases.
- Open-source library reviews.
- Documentation improvements.

## Project Rules

- Public artifacts must use synthetic examples only.
- Every extracted value in future code must resolve to a source citation.
- Every parser proposal must include a license and security review.
- Every AI workflow must treat document content as untrusted data.
- Every public issue should be reproducible without private documents.
- Any accidental private content must be removed immediately and treated as a security incident.
