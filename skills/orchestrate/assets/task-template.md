# Task file template

Each task file is a self-contained context package: the worker sees only this file plus `architecture.md`. Do the research at write time (read the files to be touched, the spec, the contracts) and embed the findings — a pointer is not enough, **except for contracts**: those are cited by reference (`architecture.md §N`, spec section), never re-typed — a paraphrased contract can silently invert the original. Drop a section only if it genuinely doesn't apply.

Copy this into `.orchestrate/<slug>/tasks/NN-<slug>.md`:

```markdown
# Task NN — <short title>

- **Wave:** <n>
- **Depends on:** [<task ids>, or none]
- **Status:** todo            # todo → in-progress → done → verified
- **Executor:** <opus | sonnet | haiku | codex>

## Objective
One specific, self-contained goal — what this task delivers, in a sentence or two.

## Out of scope
Explicitly what this task must NOT touch. Name the files/modules other tasks own,
and any exclusive runtime resources (ports, servers, shared dirs) this task does
NOT own.

## Binding references (read before coding)
The contract and spec sections this task implements against, by reference —
`architecture.md §N`, spec §M, plus file:line anchors for the key existing code.
Implement against these verbatim; do not redesign. If a contract seems wrong or
unimplementable, STOP and report (see Escape hatch).

## Files to touch
For each file:
- `path/to/file` — CREATE | UPDATE | DELETE
  - UPDATE: current state / what changes / what must be preserved.
  - CREATE: what it contains and where it plugs in.

## Context & decisions
Non-obvious things the worker needs: relevant existing patterns, the library/approach to
use (and which NOT to use), edge cases, gotchas, lessons from earlier tasks that apply
here. Owner decisions relevant to this task are BINDING — cite them with their date.

## Executor constraints
What this executor can and cannot do (sandbox limits, no build/servers/commits, who
runs the first execution of anything it can't run itself). Omit for ordinary sub-agents.

## Escape hatch
If the contract is unimplementable, the task file contradicts the code, or a site
doesn't fit the prescribed treatment: STOP and report, or log it as NEEDS-ANALYSIS
with your evidence. Never guess, never redesign, never widen your own scope.

## Acceptance criteria
Concrete, checkable conditions for "done", including what must still work end-to-end.

## Test / verification strategy
Which tests to write or run, what command proves it works — and WHO runs it if the
executor can't (an artifact its author never executed is unvalidated by construction).

---
## Dev record (worker fills this in on completion)

### File List
Every file created / modified / deleted.

### Completion Notes
Key decisions, patterns established, and anything a dependent task needs to know.

### Deviations
Everything done differently from the brief, each with its justification. An empty
section is a claim, not an omission.

### Attack points
The weakest claims in this delivery — what a hostile reviewer should check first.
Self-declaring these is mandatory when cross-review is armed.
```
