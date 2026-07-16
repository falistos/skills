# Multi-session continuity protocol

Armed when the work won't fit one session. The doctrine: **all state lives in files, not in context** — a session must be resumable after a crash, a compaction, or a `/clear` with nothing but "resume from the handoff".

## During the session

- Update the `plan.md` board **at every transition**, not at milestones — it's the crash-recovery state. This is what makes a mid-session process crash a non-event.
- Write **future triggers into the board** the moment the user states them ("when wave N closes, do X") so they survive compaction.
- Scripts and tooling the process depends on (gate scripts, init scripts, harness drivers) go **in the repo**, never in the session scratchpad — scratchpads die with the session, and every re-creation costs a reprise.
- Heterogeneous worker threads (e.g. a persistent Codex thread) are part of the state: record the thread id and the exact resume command, with its known traps.

## At the session boundary (the handoff)

Seal the handoff only after the last in-flight verdict lands — a pending REQUEST-CHANGES belongs to this session, not the next.

1. **Rewrite the REPRISE section** at the top of `plan.md` — rewrite, don't append; incremental strata rot. Contents:
   - exact state (branch, HEAD, tree status, what's closed/certified);
   - the **next action**, down to the first task file to write and its number;
   - the **established process**, with exact commands (gates, dispatch syntax, worker threads) — nothing the next session must re-derive;
   - known traps (tooling gotchas discovered this session);
   - **owner decisions not to re-litigate**, each with its one-line rationale and date.
2. **Rewrite the project memory** (condensed state + "read the REPRISE first" pointer) — again a full rewrite, purging stale incremental updates.
3. Verify: clean tree, board consistent with reality, task reports up to date.
4. Optionally a dated `HANDOFF-<milestone>.md` for a heavyweight boundary — but the REPRISE is the mechanism; standalone handoff docs get absorbed into it and go stale.

## At resume

The next session's entire bootstrap: read project memory → read the REPRISE → `git status`/`log` to confirm the recorded state matches reality → go. Surgical reads of spec/reports as needed (grep sections, don't re-read wholesale). If the recorded state and the repo disagree, stop and reconcile before dispatching anything.

Budget: a well-maintained REPRISE makes a cold resume cost minutes, not an hour of re-exploration. That's the test of whether the handoff was done right.
