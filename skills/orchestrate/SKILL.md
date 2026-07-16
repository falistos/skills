---
name: orchestrate
description: Orchestrate the end-to-end delivery of a substantial piece of work — a whole project, a sizeable feature, a migration or refactor too large for one linear pass — as a lead orchestrator; lock the spec, freeze contracts, dispatch sub-agents in dependency-ordered waves, verify, integrate. Use when the user wants to build or ship something spanning many files or several independent workstreams, or mentions orchestration, sub-agents, waves, or "spec then execute" ("orchestre", "gros chantier", "découpe en sous-agents", "monte-moi toute la feature"). Do NOT use for small or single-file changes where one linear pass is cheaper.
user-invocable: true
args: "[short description of what to build, or a path to an existing spec/plan — omit to start from an interview. Append 'no-fanout' to force a single-agent linear pass; 'assurance=max' to arm every assurance module; 'assurance=light' to force the baseline only.]"
---

# Orchestrate — build large work as a lead orchestrator

You are the **lead orchestrator**. Own the spine of the work — spec, architecture, interface contracts, integration — and delegate the leaves (independent, well-specified units) to sub-agents.

Sub-agents run in isolated context: a non-fork sub-agent sees none of this conversation, no files you read, no decisions made — only the prompt you hand it. So the two rules that hold everything together: **freeze the shared contracts before any fan-out**, and make **each task file a complete, self-contained context package**. The final integration pass is a first-class phase, not an afterthought — it's where semantic drift gets caught.

Third rule, for anything that outlives one sitting: **all state lives in files, not in your context**. The board, the decisions, the next action — if it matters after a crash or a `/clear`, it's written down the moment it happens.

## The gate: fan out, or not?

A multi-agent run costs ~15× the tokens of a linear pass, and every ambiguity in the decomposition propagates to every worker. Decide before spawning.

**Fan out only when all hold:** the work is genuinely large (many files / modules / a whole project); it has **independent workstreams** that can run in parallel once interfaces are fixed; the value justifies the token cost.

**Do a single linear pass instead when:** the change is small, single-file, or tightly sequential; the subtasks can't be cleanly separated (heavy shared state, one intricate algorithm); or specifying the split costs more than just doing it.

If `no-fanout` is passed or the gate says no: still do Phase 0 and Phase 1, then implement linearly yourself with checkpoints. Tell the user when fan-out isn't worth it.

Scale worker count to complexity: a couple of independent tasks → 2–4 workers; a large multi-module effort → more. Never swarm a small job.

## The assurance dial

Fan-out decides *how many agents*; assurance decides *how much verification*. They are sister decisions and both are set before dispatching — but assurance is not a global level. **Each heavy mechanism is armed by its own trigger, against a named risk.** When no trigger fires, you fall back to the baseline naturally, without having picked a "tier".

**Baseline (always on — it's nearly free):** validated spec, frozen contracts, self-contained task files, live `plan.md` board, orchestrator verification of every deliverable (read the diff, run build/tests), final integration pass, and the worker-brief safety clauses (STOP/NEEDS-ANALYSIS, deviations). This is enough for an ordinary feature.

**Modules — arm each one only when its trigger is true:**

| Module | Arm when |
|---|---|
| Adversarial cross-review per delivery | a missed defect is expensive AND invisible to a quick read (concurrency, security, data loss, money) |
| Double-reviewer (second family, fresh context) | a verdict lands in a **critical domain** you've named — per domain, not per task |
| Runtime harness as a wave-0 deliverable | the domain has a runtime that static checks can't cover, and the project is long enough to amortize building it |
| Go/no-go spikes in the earliest wave | an architectural bet exists that could invalidate the design |
| Spec co-signed by a second model family | the spec itself is the risk (novel domain, hard external constraints) |
| Wave-closure certification review | several tasks have intersecting perimeters (bugs live at the seams — scoped reviews miss them) |
| Multi-session machinery (REPRISE, handoff) | the work won't fit one session |
| Heterogeneous workers (Codex) | you need model independence or heavy capacity — see Phase 2 |

Write the outcome as a 5-line **assurance plan** in `plan.md` (which modules, on what perimeter, why) and validate it with the wave plan at the Phase 1 gate — the user arbitrates cost there, before it's paid. `assurance=max` in args arms everything; `assurance=light` forces the baseline. The costliest module by far is the runtime harness (wall-clock and infrastructure, not just tokens) — gate it hardest; it's also the only layer that reliably catches what every review misses, so when its trigger is true, it pays.

Calibration examples: a standard feature → baseline; a production-sensitive change → + cross-review on risky deliverables; a critical migration in a concurrent/stateful domain → everything, including harness and certification reviews.

## Phase 0 — Lock the spec

Interview the user one question at a time, walking the decision tree and resolving dependencies between decisions as you go. For each question give your recommended answer with a short rationale. If a question is answerable by reading the repo, read it instead of asking.

Cover: goal and success criteria; scope boundaries (explicitly what's *out*); constraints (stack, deps, performance, compatibility); integration with what exists; done-conditions; **and the assurance target — "what does a missed defect cost here?"**. "It has to be perfect" is an answer: it means `assurance=max`.

Stop on explicit sign-off. If `args` holds a spec or a path to one, read it and confirm the gaps rather than re-interviewing. Write the agreed spec to `spec.md`. A frozen spec is not immutable — it's amendable through an explicit process (a recorded amendment round, re-signed), never silently by a worker.

## Phase 1 — Architecture, contracts, decomposition

Do this yourself, on the strongest model.

**1. Set up the hidden workspace** at the repo root:

```
.orchestrate/<feature-slug>/
├── spec.md          # validated spec
├── architecture.md  # design + FROZEN interface contracts + conventions — shared source of truth
├── plan.md          # task index: waves, dependency graph, status board, assurance plan, decision log
├── spikes/          # spike findings and shared reference artifacts workers cite instead of re-deriving
└── tasks/
    └── NN-<slug>.md      # task file; the worker's report/dev-record accretes alongside
```

Keep it uncommitted without touching tracked files: in a git repo, append `.orchestrate/` to `.git/info/exclude`. Otherwise add it to `.gitignore` and say so, or just create the folder if not a git repo.

**2. Design and FREEZE the contracts** in `architecture.md`, before any task file exists:
- The design: components, responsibilities, data flow, key patterns and abstractions (introduce an abstraction only where it earns its place).
- **The interface contracts** — the seams between what different workers build: public signatures / types / DTOs / API shapes / schemas / event formats, and their file paths. Workers implement *against* these; they never redefine them.
- **The conventions** every worker follows: naming, error handling, structure, logging, testing. Anchor to what the codebase already does (read recent commits and the files you'll touch).
- **The exclusive resources** — anything single-writer at runtime: ports, dev servers, test databases, shared directories. Name them and assign ownership per task; collisions here waste hours and produce false test results (a "0 failures" run against a server that never booted validates nothing).

**3. Decompose into task units.** A task is a unit of independent, deliverable work — which may span several files, not "one file per task". Build the dependency graph; group independent tasks into **waves** that run in order. Any remaining contract/schema-defining work goes in the earliest wave, gated by your review before dependents start. If a spike or harness module is armed, it IS an earliest-wave task.

Write each task with `assets/task-template.md` (read it now) as a self-contained package: the worker needs only its task file plus `architecture.md`. For each file a task touches, document current state / what changes / what to preserve. **Point at contracts, never paraphrase them** — a hand-retyped contract in a task file can invert the original (it has happened); cite `architecture.md §N` or the spec section instead. Record waves, dependency graph, status board, and the assurance plan in `plan.md` (source of truth: `todo → in-progress → done → verified`). Update the board at every transition, not at the end — it's your crash-recovery state, and future triggers ("when X closes, do Y") get written into it so they survive anything.

**Gate:** present the wave plan, frozen contracts, and assurance plan to the user before dispatching. Pause specifically for architecture, API-contract, schema, and security-sensitive decisions.

## Phase 2 — Dispatch in waves

Per wave, spawn one sub-agent per task **in a single message** (parallel calls). Each worker prompt gives it an **objective**, an **output format**, **tool/boundary guidance**, and **explicit scope limits**:

- Read `.orchestrate/<slug>/architecture.md` and `.orchestrate/<slug>/tasks/NN-*.md` — everything you need is there. Implement exactly that task. Respect the frozen contracts verbatim; follow the conventions.
- **Boundaries:** touch only the files your task lists. Do not modify or "improve" files outside your scope — another agent owns them. If a listed exclusive resource is involved, you own it for the duration or you don't touch it.
- **STOP clause:** if a contract seems wrong or unimplementable, or the task file contradicts the code, STOP and report it (or log the site as NEEDS-ANALYSIS) instead of guessing or redesigning. This clause catches real inventory errors — include it verbatim.
- **No background children:** workers must not spawn background sub-agents — their results route to the main conversation, not back to the worker, which then waits forever. Research needed mid-task is done inline.
- **Chained context:** for each task this one depends on, paste in that task file's *Completion Notes* and *File List*.
- **Output:** fill in your task file's *Dev record* — File List, Completion Notes, **deviations** (what you did differently and why), and **self-declared attack points** (the weakest claims a reviewer should hit first) — then return a terse summary. Keep verbose reasoning and test output out of the return.

**Escalation (AUTHORIZED protocol):** when a worker stops on a contract problem, adjudicate yourself, then resume *that worker* with an explicit, narrow grant — "AUTHORIZED: <the specific change>, with these constraints" — rather than silently widening its scope or patching around it.

**Keep the pump running:** a pending user decision (AskUserQuestion) must not freeze dispatch — keep processing deliveries and reviews for everything that doesn't depend on the answer.

### Model routing

Pick the executor per task. Rule of thumb: the orchestrator stays on the strongest model; each worker gets the cheapest executor that clears its bar, judged on reasoning-left-after-the-task-file, ambiguity, and cost-of-a-wrong-answer.

| Executor | Reach for it when | Typical tasks |
|---|---|---|
| `fable` (you) | orchestration only — rarely a worker | spec, contracts, decomposition, adjudication, integration, commits |
| `opus` | ambiguity or cross-cutting reasoning left after the brief | hard design, tricky debugging, research/spikes, diagnosis agents, **adversarial reviews** |
| `sonnet` | the default for well-specified production work | implementation against a tight brief, standard refactors, tests |
| `haiku` | mechanical, high-volume, low-ambiguity | renames, sweeps, boilerplate, config, simple CRUD |
| Codex CLI (GPT-5.x, high effort — via the `codex-delegate` skill) | HEAVY/XL implementation or deep audits; or you need a **different model family** | keystone modules, large field-by-field audits, spec co-signing, **counter-reviews in a fresh thread** |

Codex-specific rules (mechanics and sandbox limits live in `codex-delegate` — read it before the first dispatch):
- **Persistent thread for continuity, fresh thread for independence**: one resumed thread accumulates the project context across tasks and sessions (open each dispatch with the delta since its last task); a second opinion or counter-review gets a fresh thread.
- **Sandbox division of labor**: Codex delivers into the working tree; *you* own build, gates, and commits. An artifact its author couldn't execute is unvalidated by construction — route its first run to whoever owns the runtime.

Two routing rules that hold for every executor: a read-only reviewer can run one tier below the worker it checks, except for adversarial passes (and reviewer + implementer come from **different model families** when cross-review is armed); and routing drifts over long sessions — re-check it against the plan at every wave boundary.

## Phase 3 — Verify each wave before the next

As each worker returns, verify — don't trust the summary, and don't trust exit codes either: judge the deliverable itself (the diff, the report, the artifact on disk).

**Baseline verification (every task):** check output against the task's acceptance criteria and the frozen contracts (did it drift from the agreed signature?). **System-integrity rule:** the change must leave the system working end-to-end, not merely satisfy stated criteria. Run the stack's real checks — build, typecheck, lint, tests — after each wave, especially at wave boundaries where independent parts first meet.

**Adversarial cross-review (when armed):** for each delivery in scope, run the cycle in `assets/review-protocol.md` — read it at the first armed delivery. Shape: fresh other-family reviewer → graded verdict → corrective split (MINOR = you, BLOCKING = the original worker) → re-review by the same reviewer → double-reviewer on critical-domain verdicts. Residual findings route to a collector task: nothing lost, nothing blocking.

**Runtime gates (when armed):** static review never catches everything — the harness run is a separate rung, and historically the only one that catches the blocking bugs. Script the gates and commit the script to the repo (not a session scratchpad — those die with the session). **Gates evolve:** every defect found at runtime adds a scenario to the standard gate. "Fixed in code" and "proven at runtime" are different states — say which one you're in, and prove fixes by reproducing the exact failing path.

**Wave closure:** on a defect, re-dispatch a corrective task rather than patching it yourself (unless trivial), so task files stay the accurate record. Update `plan.md`. Start a wave only once its dependencies are `verified`, not merely `done`. When tasks in the wave had intersecting perimeters, close with a **certification review** that samples *across* the seams — scoped reviews miss the bugs living at intersections. Commit per task (or per wave) only after review verdicts and gates are green; if two tasks co-modified a file, split by hunks rather than smearing one commit.

## Phase 4 — Integration and final coherence pass

Do this yourself. Non-negotiable.
- **Wire the seams** workers couldn't own: composition roots, DI, routing, config, feature flags.
- **Hunt duplication and divergence:** the same helper written twice, inconsistent naming or error handling, two valid-but-different readings of one requirement. Consolidate.
- **Verify against the spec**, not just the tasks — does the assembled whole deliver what Phase 0 agreed?
- Full build + full test suite green; run the feature for real where feasible.
- Clean up dead scaffolding, stray TODOs, debug leftovers.

Report to the user: what was built, how it maps to the spec, deviations and why, what's left. If the user asked for a final deliverable report, it's a task like any other — spec it early and feed it from the board as decisions happen, don't reconstruct it at the end. Offer to clean up or keep `.orchestrate/<slug>/`.

Semantic drift on ambiguous requirements has no automated fix — tight contracts plus this pass are the only defense. Stay alert for it.

## Multi-session continuity (when armed)

Continuity is a deliverable, not an afterthought: all state lives in files — the board updated at every transition, future triggers written into it, process scripts in the repo. At each session boundary run the handoff protocol in `assets/continuity.md` (read it at the first boundary); the next session's whole bootstrap is memory → REPRISE → go.

## Operational hygiene

Hard-won rules — each one has burned a real run:
- **Absolute paths in every Bash call** (`cd <abs> && …` or `git -C`): background shells reset their cwd between calls, and a dispatch launched from the wrong cwd fails *silently* (its output file is simply never created). Check early that expected output files exist and grow.
- **Monitor every task longer than ~10 minutes**: heartbeat + liveness (file mtime / log freshness), and monitors must cover failure states, not just success markers. Never a detached `nohup … &` without a monitor. Silent deaths otherwise get discovered by the user, not by you.
- **Size timeouts to the task** — a default timeout kills long salvos at the deadline and can orphan child processes (which then squat ports and poison the next run).
- **Exit codes lie in both directions**: a worker can exit non-zero with a perfect deliverable, and a green run against a half-booted environment validates nothing. Judge artifacts.
- Prefer measuring over asserting when the user asks about behavior/perf — and measure only what changes a decision, not what fills a table.
