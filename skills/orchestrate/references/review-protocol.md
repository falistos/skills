# Adversarial cross-review protocol

Used when the cross-review module is armed. The reviewer's job is to **break the delivery**, not to approve it politely — a review briefed as "check this" finds style nits; a review briefed as "reverse this" finds the data-loss bug.

## Reviewer selection

- Fresh, read-only agent, from a **different model family than the implementer** (Claude delivery → Codex counter-check where warranted; Codex delivery → Claude reviewer).
- One tier below the worker is acceptable for routine checks — never for adversarial passes.
- Independence is structural: a counter-review never resumes the implementer's thread or reuses its context.

## The reviewer brief

Include, in this order:
1. **Reading order**: task file → the delivery report (including the worker's self-declared attack points) → the binding spec/contract sections → the sources themselves.
2. **Named attack axes**, numbered, tailored by you — put the most fragile claim first. "Audit by omission" claims ("no other site needs this") are attacked by sampling: impose quotas ("check AT LEAST 10 call sites / 12 mutators").
3. **Verification duty**: re-verify the worker's citations against the sources — don't take file:line claims on faith. Re-run cheap gates (build) independently where possible.
4. **Scope guard**: the reviewer touches no sources; it writes only into the review section of the task report. Tell it explicitly which unrelated changes may be sitting in the working tree ("IGNORE everything outside <paths> — a concurrent task owns it"), or perimeter false-positives will pollute the verdict.
5. **Verdict format** (mandatory): `APPROVE` or `REQUEST-CHANGES`, then findings `F1..Fn`, each graded **BLOCKING / MAJOR / MINOR / NOTE** with file:line, a concrete failure scenario (inputs/interleaving → wrong outcome), and a minimal fix sketch. Terse.

## The corrective loop

1. **Adjudicate the findings yourself** before routing them — reviewers produce false positives and mis-graded findings too; a finding you can refute gets closed with the refutation on record.
2. **Split the correctives**: MINOR with a pre-validated fix → apply yourself, logged in the task report (`## Corrective pass (orchestrator)` with per-finding status: FIXED / ACCEPTED-DOCUMENTED / ROUTED). BLOCKING or substantial → re-dispatch to the **original worker**, findings re-framed and pre-adjudicated ("F2 is a false positive, don't touch it").
3. Never apply a reviewer's sketched fix blind — sketches can be wrong in ways that create new bugs. Validate the idea against the code first.
4. **Re-review by the same reviewer** (resume it): scope = the fixes only. Its retained context makes this a fraction of the initial review's cost.
5. **Double-reviewer** on critical-domain verdicts (the domains named in the assurance plan): a second, fresh, other-family reviewer with a NARROW scope — the two or three load-bearing claims only. Its purpose is to reverse false APPROVEs; treat a reversal as normal operation, not an anomaly.
6. **Residual findings** (NOTE/MINOR not worth blocking on) are routed to a designated collector task, recorded in the board. Nothing is lost, nothing blocks.

## The task report as accretive record

Everything lands in the task's report file, in order: delivery (with deviations + attack points) → `## Cross-review` → `## Corrective pass` → `### Re-review` → `## Orchestrator resolution` (verdict recorded, findings accepted/refuted/routed). One file per task tells the whole story to any future session.

## What review cannot do

Static review — even adversarial, even doubled — does not catch everything; runtime gates are a separate rung, not a substitute. A wave whose tasks had intersecting perimeters additionally needs a **certification review** at closure: cross-cutting sampling designed for the seams, where scoped reviews are structurally blind.
