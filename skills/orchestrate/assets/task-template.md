# Task file template

Each task file is a self-contained context package: the worker sees only this file plus `architecture.md`. Do the research at write time (read the files to be touched, the spec, the contracts) and embed the findings — a pointer is not enough. Drop a section only if it genuinely doesn't apply.

Copy this into `.orchestrate/<slug>/tasks/NN-<slug>.md`:

```markdown
# Task NN — <short title>

- **Wave:** <n>
- **Depends on:** [<task ids>, or none]
- **Status:** todo            # todo → in-progress → done → verified
- **Model:** <opus | sonnet | haiku>

## Objective
One specific, self-contained goal — what this task delivers, in a sentence or two.

## Out of scope
Explicitly what this task must NOT touch. Name the files/modules other tasks own.

## Interface contract
The exact signatures / types / DTOs / API shapes / schemas this task implements or
consumes, copied from architecture.md. Implement against these verbatim; do not redesign.

## Files to touch
For each file:
- `path/to/file` — CREATE | UPDATE | DELETE
  - UPDATE: current state / what changes / what must be preserved.
  - CREATE: what it contains and where it plugs in.

## Context & decisions
Non-obvious things the worker needs: relevant existing patterns, the library/approach to
use (and which NOT to use), edge cases, gotchas.

## Acceptance criteria
Concrete, checkable conditions for "done", including what must still work end-to-end.

## Test / verification strategy
Which tests to write or run, what command proves it works.

---
## Dev record (worker fills this in on completion)

### File List
Every file created / modified / deleted.

### Completion Notes
Key decisions, patterns established, deviations from the plan, and anything a dependent
task needs to know.
```
