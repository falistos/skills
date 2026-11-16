---
name: overhaul
description: "Review a whole project on architecture, code, naming, performance, completeness and agent-readiness, then apply an owner-approved plan in proven lots."
disable-model-invocation: true
argument-hint: "[module or package to scope — omit for the whole project]"
---

# Overhaul

Fan out by area and axis group; each reviewer reads their area whole. Keep only findings with evidence and a
named harmed consumer, maintainer or hot path. Simplicity outranks completeness.

| Axis | Required evidence |
|---|---|
| Architecture | Module/package and broken boundary, cycle, ownership rule or coupling |
| Code | `file:line`: dead code (no repo/consumer callers), duplication, outdated idiom/dependency, workaround or swallowed error |
| Naming | Two meanings admitted by a catch-all/ambiguous name and a replacement admitting one |
| Performance | Measurement or complexity on a per-tick/request/player/event hot path |
| Completeness | Real consumers rebuilding/working around a missing capability/primitive; otherwise `speculative` |
| Agent-readiness | Fresh agent's observed failure on a real task involving docs/API/config |

## Steps

1. **Baseline:** read repo rules, decisions and conventions; run gate/benchmarks; find consumers (`gh search
   code --owner <org>`). Finish with gate result, benchmark numbers and every consumer/API recorded.
2. **Map by script:** module/package sizes, largest files, dependency cycles, public symbols without callers.
   Finish with areas each reviewer can read whole.
3. **Fan out:** briefs include rules, area, axes and finding format: axis, `file:line`, evidence, consequence,
   fix, S/M/L cost, affected consumers, breaking or not. For agent-readiness, give fresh agents only the entry
   doc and real consumer tasks; record stalls, invented APIs and workarounds. Finish with reports for every
   area/axis, including empty ones.
4. **Refute:** another reviewer tries to disprove each finding in code; use another model family when
   available, through the project's delegation procedure. Retain only surviving evidence.
5. **Plan:** deduplicate and rank by impact × consumers / cost. Each one-PR lot names goal, findings closed
   and test/benchmark/gate proof. Group breaking changes into one major with migration notes. For recurring
   classes add prevention (type/lint/architecture/CI). Present the plan and wait for owner approval.
6. **Apply in lots:** one lot/PR, green gate, review per lot; performance lots compare the same
   benchmark before/after.
