---
name: arch-review
description: "Review Java architecture or modernize its design (\"review archi\"), with alternatives and a refactoring plan."
user-invocable: true
argument-hint: "[package or module path to scope the review — omit for full project. Append 'fast' to skip Codex parallel analysis.]"
---

# Java architecture review

Review design only; write no code. Bugs, security, performance, naming, formatting, tests and dead code are
outside scope.

## 1. Discover

1. Read build files (Java, modules, frameworks, plugin manifests), README, repo rules and docs for
   intent, standards and stage. Map Java packages and public entry points, handlers, APIs and config schema;
   honor the requested scope.
2. Read entry points, a key class per package, domain models, abstractions, wiring and 1–2
   input-to-persistence slices. Delegate independent areas only when their context/output cost is justified.
3. Write a 2–3 sentence synthesis: purpose, components, dominant style, maturity and appropriate rigor. Every
   claim must trace to code read before findings begin.

For thousands of files, select 3–5 central modules after mapping layout/public surface; state which, why and
that the review is sampled. Report recurring patterns with counts.

## 2. Analyze

Use two axes: **Standards** cites a documented rule; **Spec** cites stated intent (README, spec, decisions).
Catalog smells are **Judgement**, subordinate to repo standards and recorded exceptions.

Calibrate to scale, stage and purpose: a small utility needs little architecture; greenfield and public
libraries warrant more design investment; projects on an in-house framework reuse its primitives. Raise DDD, CQRS, event sourcing,
hexagonal architecture or microservices only for concrete benefit. Drop findings that cannot explain harm
here; personal preference is a Suggestion at most.

### Independent analysis

Unless `fast` was requested, run Codex read-only in the background with `codex exec -s read-only`, using a
prompt file. Its brief includes:

- Scope, project context and calibration above; design choices only, with the same exclusions.
- Responsibilities, abstractions, domain, API/extensibility, state ownership, error strategy and Java 21+
  modeling gains.
- Findings ordered by severity then impact, each grounded in a read class/package: severity, tier, title,
  location, problem, project-specific impact, root cause and concrete proposed fix.
- Deferable findings are Minor or omitted; finish with solid design decisions.

If Codex is missing or logged out, report it and continue the local analysis alone.

### Local analysis, in parallel

Read each tier's reference before writing findings:

| Tier | Inspect | Reference under `references/` |
|---|---|---|
| 1. Architecture | Responsibility, layering, cycles, hidden/static coupling | `anti-patterns.md` |
| 2. Domain | Invariants, primitive obsession, contracts, leaky/speculative abstractions | `anti-patterns.md` |
| 3. Patterns | Inheritance, dispatch, factories/builders, Visitor, speculative generality | `patterns-catalog.md` |
| 4. API | Minimal hard-to-misuse contracts, hidden internals, real extension points | `patterns-catalog.md` |
| 5. State | Ownership, immutability, shared-state contracts, IO and virtual threads | `modern-java-design.md` |
| 6. Errors | Consistent vocabulary/strategy, expected outcomes, swallowed failures | `anti-patterns.md` |
| 7. Modern Java | Records, sealed types, exhaustive dispatch, payloads, text blocks | `modern-java-design.md` |

Modernization must visibly improve modeling, exhaustiveness or immutability; syntax alone is insufficient.
When the repo or an installed skill documents its framework's architecture conventions, read them before findings.

## 3. Reconcile and report

Wait for Codex. Both sources: `[Claude + Codex]`; local only: `[Claude]`; Codex only: verify in code before
retaining `[Codex]`; disagreement: `[Disputed]` with both views. Deduplicate, keep the clearer explanation,
and repeat the project-fit calibration.

**Critical** prevents maintainability/extensibility required by stated goals; **Major** causes increasing pain
worth addressing soon; **Minor** is worth fixing when touching the area. Distinguish clear mistakes from
strong opinions and acknowledge possibly deliberate choices.

Report:

- Verdict (3–5 sentences), project type, Java version, 3–5 shaping dependencies, stage and dominant style.
- Dependency overview: components, critical paths and problematic directions.
- Findings by tiers 1–7, then severity: title, source, concrete classes/packages/methods, axis with citation,
  problem, project-specific impact and root cause.
- What's good: 2–5 specific decisions.
- Proposed architecture for every Critical/Major: named target classes/packages/interfaces, moves, new
  abstractions, deletions/merges and reasons.
- Ordered atomic refactoring steps, independently committable, dependencies before consumers; mark high-risk
  steps for manual verification.

End with: "Run `/step-by-step` to start implementing this plan."
