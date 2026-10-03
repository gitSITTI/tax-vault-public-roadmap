# Independent Sol validation of root operations and parity repairs

Validator: GPT-5.6 Sol
Producer under review: Codex root
Mode: read-only source challenge and independent offline re-observation
Repair checkout: `C:\Users\edsos\.codex\worktrees\code-audit-repairs\tradingview-codex-onboarding-agent`

The validator made no source fixes in the producer's ownership. Two parity
handoff defects were sent back to the producer: malformed Markdown task tables
and generated Python caches inside the new Confluence `tools/` tree. The
producer corrected both task tables and committed to exact-path staging that
excludes caches. This report validates source and tests; final staged-path and
commit contents remain a delivery gate for root.

## Verdicts

| Finding | Verdict | Independent basis |
|---|---|---|
| OPS-01 | **CONFIRMED** | Packing requires a new direct outbox child, validates key/source/age before creating output, stages into a fresh owned directory, and never replaces an existing destination. Sentinel, missing-source/key, and duplicate cases pass. |
| OPS-02 | **CONFIRMED** | Verification covers signature, schema, age, exact allowlist/required set, duplicate paths, size and hash before promotion. Promotion copies a complete generation, re-verifies it, and atomically changes one pointer. The consumer receives the returned immutable input root. Corrupt-last-entry and omitted-optional regressions pass. |
| OPS-03 | **CONFIRMED** | Session JSONL is folded chronologically with incremental offsets and a retained partial-line offset. New starts supersede old completions; aborted/failed/waiting/unknown states are distinct. The payload and rendered heading explicitly limit coverage to recent local lifecycle records and disclose unavailable cloud-only chats. |
| OPS-04 | **CONFIRMED** | HTTP reachability, readiness and identity are distinct. HTTP errors remain unready, 401/403 are identified separately, and service-specific Hermes/receiver/dashboard/CDP signatures are required. Mocked 503/auth/unrelated-service cases pass. |
| OPS-05 | **CONFIRMED** | Fast-forward eligibility requires a fresh fetch object with return code zero and no timeout. Apply with no fetch or failed/timed-out fetch never calls merge and reports the blocking state. |
| OPS-06 | **CONFIRMED** | Repository inspection is redacted structurally and the JSON/Markdown writer applies the redaction boundary again. Dummy HTTPS userinfo, token queries and echoed error URLs do not survive; ordinary SSH remotes remain readable. |
| APP-07 | **CONFIRMED** | Recursive secret-key masking, quoted/escaped assignment masking, Authorization/query/userinfo handling and non-mutation pass in all three repositories. The result is correctly bounded as secret-field filtering, not general PII/DLP coverage. |

## Tri-repository parity

The shared core is byte-identical in all three locations: 10,567 bytes and
SHA-256 `8fd7c3e34f1f89c62fb9bbe6386988381bb8ea7291125f49805f825bc8112785`.

| Repository | Observed base | Remote | Independent result |
|---|---|---|---|
| tradingview-codex-onboarding-agent | repair branch based on `f99d95251c6e26b598ad0a2f38ce1d24a828ee94` | repository under repair | Root focused suite: 40 passed. |
| tax-vault-public-roadmap | `f453164e1f03be0a56f98ed275c32024ac440948` | `https://github.com/gitSITTI/tax-vault-public-roadmap.git` | 22 passed across provenance, reconciliation, and shared-redaction tests. |
| ConfluenceOS | `e20083854b16daaceb7bfadc58214c63c734a66f` | `https://github.com/gitSITTI/ConfluenceOS.git` | 3 shared-redaction tests passed. The report does not claim a pre-existing Confluence domain integration. |

The two parity task files now contain valid contiguous Markdown tables and
remain `in_progress` until final delivery. Generated `__pycache__` files are
present locally under the untracked Confluence `tools/` directory after tests;
they are outside the approved exact staging list. A validator must inspect the
actual index or commit before confirming their exclusion.

## Counts and boundaries

Independent reruns observed 40 + 22 + 3 = 65 passing tests for this producer
scope. The commands and raw summaries are recorded in
`sol-validation-root-tests.json`. The number is evidence only for the listed
offline contracts.

No live stack, broker, TradingView, CDP, Cloudflare, remote merge, deployment,
or destructive snapshot action was exercised. The health repair proves
classification logic through fake responses; it does not assert that any
service is currently up. Repository-refresh tests use mocked Git and do not
prove remote freshness. Final staging, commits, pushes, checks, and PR state
are outside this validator pass.

## Validator conclusion

The seven root repairs are **CONFIRMED** at source and focused-test level. The
tri-repo shared core and focused tests are **CONFIRMED**. Final delivery remains
conditional on an exact staged/committed path review that excludes generated
caches and includes both parity docs, task files, tests, and core paths.
