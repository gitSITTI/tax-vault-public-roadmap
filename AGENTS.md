# Agent Guidance

## Script-First Implementation

- When a task can be made repeatable, create the best-fit script, CLI command, skill, or workflow for the job instead of leaving only prose instructions.
- Choose the implementation language by use case and surrounding repo conventions. Prefer Python for automation, data processing, repo maintenance, and local CLIs unless another runtime is clearly better.
- Skills may include scripts, templates, examples, and workflow files when they make the skill executable or easier to validate.
- Documentation should explain how to run the script or workflow, but the runnable artifact should come first when practical.

## Tri-Repo Parity Rule

- Reusable capabilities are grown across all three sibling repos
  (`tax-vault-public-roadmap`, `tradingview-codex-onboarding-agent`,
  `ConfluenceOS`) with the same shared core and the same shape.
- The shared report core (`taxvault/provenance_report.py` here) is kept
  byte-identical across the repos; each repo layers a domain module on top.
- A shared-capability change is not done until it has been applied to every
  repo it sensibly applies to. See `docs/TRI_REPO_PARITY.md`.
