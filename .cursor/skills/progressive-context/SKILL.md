---
name: Progressive context
description: >-
  Use at session start and before ending work in this repo: read and update
  current.md / contextmap.md so a new session does not lose follow-through.
---
# Progressive context (repo)

## Session start
1. Read `current.md`, then `contextmap.md`, before trusting the last chat or grepping the whole tree.
2. If `current.md` is missing or stale vs the open PR/branch, rewrite **Now** and **Next action** first.
3. Do the smallest next action named in `current.md`.

## Session end
1. Update **Now**, **Next action**, and **Known limitations** in `current.md`.
2. Add new material pointers to `contextmap.md`.
3. Append a dated line to `decisions.md` only if a real decision landed.
4. Tell the user state lives on disk (paths), not in chat memory.

## Four kinds of context
| Kind | File | Changes? |
|---|---|---|
| Stable rules | AGENTS.md / this skill | Rarely |
| Current state | current.md | Every meaningful session |
| Map | contextmap.md | When locations change |
| History | decisions.md / git / PR | Append-only |

## Reject
Giant prompt dumps; treating green CI as operator-true; leaving next action only in chat.
