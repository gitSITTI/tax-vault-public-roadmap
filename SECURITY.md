# Security

Report security issues privately through GitHub security advisories when enabled.

## Public Repo Data Rule

This repo must never contain real DLP data. DLP data includes tax returns, bank statements, account numbers, SSNs, addresses, private financial values, private logs, extracted OCR from real documents, and embeddings derived from real documents.

## Required Security Checks

- Scan docs for accidental private names before publishing.
- Scan commits for private documents and database files.
- Use synthetic fixtures for parser tests.
- Treat document text as untrusted input.
- Do not add public examples containing real accounts, exact tax values, or private endpoints.
- Report accidental exposure as an incident, even if the data is quickly removed.
