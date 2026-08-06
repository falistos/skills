# Assurance modules

All modules are OFF by default. A module is armed only by user decision at the Phase 1 gate — present each candidate with its named risk and its cost, and let the user arbitrate before the cost is paid. `assurance=max` arms everything; `assurance=light` forbids arming any.

Write the outcome as a 5-line **assurance plan** in `plan.md`: which modules, on what perimeter, why.

## The modules and their triggers

Propose a module only when its trigger is true — a named risk, not a vague "to be safe":

| Module | Propose when | Cost profile |
|---|---|---|
| Cross-review escalated to **per-delivery** (baseline is one Codex pass per wave) | a missed defect is expensive AND invisible to a quick read (concurrency, security, data loss, money) | one other-family reviewer + triage + corrective loop per in-scope delivery, instead of one per wave — this is the module most likely to make verification outgrow development, so scope it to the risky deliveries, not the whole wave |
| Double-reviewer (second family, fresh context) | a verdict lands in a **critical domain** you've named — per domain, not per task | one narrow extra review per critical verdict |
| Runtime harness as a wave-0 deliverable | the domain has a runtime static checks can't cover, and the project is long enough to amortize building it | the costliest module by far — wall-clock and infrastructure, not just tokens; gate it hardest. It's also the only layer that reliably catches what every review misses: when its trigger is true, it pays |
| Go/no-go spikes in the earliest wave | an architectural bet exists that could invalidate the design | one spike task per bet |
| Spec co-signed by a second model family | the spec itself is the risk (novel domain, hard external constraints) | one Codex pass over the spec |
| Wave-closure certification review | several tasks have intersecting perimeters — bugs live at the seams, and scoped reviews are structurally blind there | one cross-cutting review per closing wave; the wave closes as a unit |
| Exhaustive lead review | the user explicitly wants the lead model to read every diff itself | lead-model tokens per delivery — the expensive path Phase 3's verifier exists to avoid |
| Multi-session machinery (REPRISE, handoff) | the work won't fit one session | see `continuity.md` |
| Heterogeneous workers (Codex) | you need model independence or heavy capacity | see the `codex-delegate` skill |

Calibration examples: a standard feature → baseline, no modules; a production-sensitive change → + cross-review on the risky deliverables; a critical migration in a concurrent/stateful domain → everything, including harness and certification reviews.

## Running the armed modules (Phase 3 additions)

**Cross-review at per-delivery granularity:** same cycle as the baseline wave pass (`review-protocol.md`), applied per in-scope delivery, with the double-reviewer added on critical-domain verdicts.

**Runtime gates:** script the gates and commit the script to the repo (not a session scratchpad — those die with the session). **Gates evolve:** every defect found at runtime adds a scenario to the standard gate. "Fixed in code" and "proven at runtime" are different states — say which one you're in, and prove fixes by reproducing the exact failing path.

**Certification review:** at closure of a wave whose tasks had intersecting perimeters, a review that samples *across* the seams — designed for the intersections where scoped reviews are blind.
