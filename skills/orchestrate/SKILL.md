---
name: orchestrate
description: Orchestrate the end-to-end delivery of a substantial piece of work — a new project, a sizeable feature, or a large refactor/migration — as a lead orchestrator that locks the spec with the user, freezes shared interface contracts, decomposes the work into self-contained task files in a hidden folder, then dispatches sub-agents in dependency-ordered waves (picking the right model per task), verifies their output, and runs a final integration pass so the result is coherent, complete, and clean. Use this whenever the user wants to build or ship a whole feature or project, tackle a big multi-file / multi-module change, a migration, or a refactor too large for one linear pass — especially when they mention orchestration, sub-agents, parallelizing the work, waves, or "spec then execute". Prefer it over ad-hoc coding for anything spanning many files or several independent workstreams. Do NOT use it for small, single-file, or quick targeted changes where a single linear pass is cheaper. Triggers in French too: "orchestre", "gros chantier", "découpe en sous-agents", "lance des vagues", "spec puis exécution", "monte-moi toute la feature".
user-invocable: true
args: "[short description of what to build, or a path to an existing spec/plan — omit to start from an interview. Append 'no-fanout' to force a single-agent linear pass.]"
---

# Orchestrate — build large work as a lead orchestrator

You are the **lead orchestrator**. Own the spine of the work — spec, architecture, interface contracts, integration — and delegate the leaves (independent, well-specified units) to sub-agents.

Sub-agents run in isolated context: a non-fork sub-agent sees none of this conversation, no files you read, no decisions made — only the prompt you hand it. So the two rules that hold everything together: **freeze the shared contracts before any fan-out**, and make **each task file a complete, self-contained context package**. The final integration pass is a first-class phase, not an afterthought — it's where semantic drift gets caught.

## The gate: fan out, or not?

A multi-agent run costs ~15× the tokens of a linear pass, and every ambiguity in the decomposition propagates to every worker. Decide before spawning.

**Fan out only when all hold:** the work is genuinely large (many files / modules / a whole project); it has **independent workstreams** that can run in parallel once interfaces are fixed; the value justifies the token cost.

**Do a single linear pass instead when:** the change is small, single-file, or tightly sequential; the subtasks can't be cleanly separated (heavy shared state, one intricate algorithm); or specifying the split costs more than just doing it.

If `no-fanout` is passed or the gate says no: still do Phase 0 and Phase 1, then implement linearly yourself with checkpoints. Tell the user when fan-out isn't worth it.

Scale worker count to complexity: a couple of independent tasks → 2–4 workers; a large multi-module effort → more. Never swarm a small job.

## Phase 0 — Lock the spec

Interview the user one question at a time, walking the decision tree and resolving dependencies between decisions as you go. For each question give your recommended answer with a short rationale. If a question is answerable by reading the repo, read it instead of asking.

Cover: goal and success criteria; scope boundaries (explicitly what's *out*); constraints (stack, deps, performance, compatibility); integration with what exists; done-conditions. Surface ambiguous parts early.

Stop on explicit sign-off. If `args` holds a spec or a path to one, read it and confirm the gaps rather than re-interviewing. Write the agreed spec to `spec.md`.

## Phase 1 — Architecture, contracts, decomposition

Do this yourself, on the strongest model.

**1. Set up the hidden workspace** at the repo root:

```
.orchestrate/<feature-slug>/
├── spec.md          # validated spec
├── architecture.md  # design + FROZEN interface contracts + conventions — shared source of truth
├── plan.md          # task index: waves, dependency graph, status board
└── tasks/
    └── NN-<slug>.md
```

Keep it uncommitted without touching tracked files: in a git repo, append `.orchestrate/` to `.git/info/exclude`. Otherwise add it to `.gitignore` and say so, or just create the folder if not a git repo.

**2. Design and FREEZE the contracts** in `architecture.md`, before any task file exists:
- The design: components, responsibilities, data flow, key patterns and abstractions (introduce an abstraction only where it earns its place).
- **The interface contracts** — the seams between what different workers build: public signatures / types / DTOs / API shapes / schemas / event formats, and their file paths. Workers implement *against* these; they never redefine them.
- **The conventions** every worker follows: naming, error handling, structure, logging, testing. Anchor to what the codebase already does (read recent commits and the files you'll touch).

**3. Decompose into task units.** A task is a unit of independent, deliverable work — which may span several files, not "one file per task". Build the dependency graph; group independent tasks into **waves** that run in order. Any remaining contract/schema-defining work goes in the earliest wave, gated by your review before dependents start.

Write each task with `assets/task-template.md` (read it now) as a self-contained package: the worker needs only its task file plus `architecture.md`. For each file a task touches, document current state / what changes / what to preserve. Record waves, dependency graph, and status board in `plan.md` (source of truth: `todo → in-progress → done → verified`).

**Gate:** present the wave plan and frozen contracts to the user before dispatching. Pause specifically for architecture, API-contract, schema, and security-sensitive decisions.

## Phase 2 — Dispatch in waves

Per wave, spawn one sub-agent per task **in a single message** (parallel calls). Each worker prompt gives it an **objective**, an **output format**, **tool/boundary guidance**, and **explicit scope limits**:

- Read `.orchestrate/<slug>/architecture.md` and `.orchestrate/<slug>/tasks/NN-*.md` — everything you need is there. Implement exactly that task. Respect the frozen contracts verbatim; follow the conventions.
- **Boundaries:** touch only the files your task lists. Do not modify or "improve" files outside your scope — another agent owns them.
- **Chained context:** for each task this one depends on, paste in that task file's *Completion Notes* and *File List*.
- **Output:** fill in your task file's *File List* and *Completion Notes*, then return a terse summary — files changed, key decisions, deviations, follow-ups. Keep verbose reasoning and test output out of the return.

**Pick the model per task via the Agent tool's `model` param** (aliases: `opus` / `sonnet` / `haiku` / `fable`). Rule: the orchestrator stays on the strongest model; each worker gets the cheapest model that clears its bar. Decide per task on reasoning-left-after-the-task-file, ambiguity, and cost-of-a-wrong-answer:
- `opus` — hard design, ambiguous/cross-cutting tasks, tricky debugging, high blast radius.
- `sonnet` — the default: well-specified production coding, standard refactors, tests.
- `haiku` — mechanical, high-volume, low-ambiguity: renames/format sweeps, boilerplate, config, simple CRUD.
- `fable` — only for a uniquely hard reasoning worker; usually overkill.
- A read-only reviewer can run one tier below the worker it checks, except for adversarial regression passes.

## Phase 3 — Verify each wave before the next

As each worker returns, verify — don't trust the summary.
- Check output against the task's acceptance criteria and the frozen contracts (did it drift from the agreed signature?).
- **System-integrity rule:** the change must leave the system working end-to-end, not merely satisfy stated criteria. If a behavior is needed for the feature to work in the existing system, it's required whether the task spelled it out or not.
- Run the stack's real checks — build, typecheck, lint, tests — after each wave, especially at wave boundaries where independent parts first meet.
- On a defect, **re-dispatch** a corrective task rather than patching it yourself (unless trivial), so task files stay the accurate record.
- Update `plan.md`. Start a wave only once its dependencies are `verified`, not merely `done`. For heavy or adversarial checks, spawn a dedicated read-only reviewer.

## Phase 4 — Integration and final coherence pass

Do this yourself. Non-negotiable.
- **Wire the seams** workers couldn't own: composition roots, DI, routing, config, feature flags.
- **Hunt duplication and divergence:** the same helper written twice, inconsistent naming or error handling, two valid-but-different readings of one requirement. Consolidate.
- **Verify against the spec**, not just the tasks — does the assembled whole deliver what Phase 0 agreed?
- Full build + full test suite green; run the feature for real where feasible.
- Clean up dead scaffolding, stray TODOs, debug leftovers.

Report to the user: what was built, how it maps to the spec, deviations and why, what's left. Offer to clean up or keep `.orchestrate/<slug>/`.

Semantic drift on ambiguous requirements has no automated fix — tight contracts plus this pass are the only defense. Stay alert for it.
