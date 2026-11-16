---
name: correct
description: "Use after an owner correction (\"encore la même erreur\"), for a retrospective (\"retro\"), or when closing a piece of work with lessons, to prevent repeated mistakes."
---

# Correct

Make the shortest path a fresh agent copies the right one; prose advises, mechanisms fail loudly. Successful
procedures belong to `skillify`.

## 1. Collect

Read owner corrections (Claude JSONL in `~/.claude/projects/`, T3 via `t3_thread_read`), reviews, reverts,
`fix:` commits and workaround comments. At the close of a tracked piece of work, include its reports and
recorded lessons.

Group mistake classes: two occurrences, or one owner correction, qualifies. Finish when every input has a
class or a reason for exclusion.

## 2. Diagnose what allowed it

- **Navigation**: missing pointer caused a long search.
- **Checks**: inspect gate/CI first; an existing unwired/skipped/broken check is the finding, not grounds for
  another. No gate is its own finding.
- **Access**: unavailable logs, state or service.
- **Tool economy**: unnecessarily expensive/noisy calls.
- **Steering sediment**: no-op, contradictory or unenforced instructions.

## 3. Choose and prove a mechanism

Prevent with the smallest effective mechanism, in this order (architecture/API → type → lint/CI/gate
→ judgement rule → skill):

- Architecture/API: one state owner, one supported path, hidden internals and one source of truth; remove
  obsolete examples agents would copy.
- Checks name the replacement file/type/function; ratchet existing widespread violations by rejecting only new
  ones. Shell bans belong in the agents' command guard; build-checkable rules in the build's checks.
- Judgement rules go in repo AGENTS.md, the diff review brief, or the always-on rules file for every session;
  skills serve reusable judgement procedures.
- A broken pre-existing rule must move up a level in this change.

One commit per class, most frequent first. For each check, replay the mistake on a scratch branch or offending
snippet and capture red output; run the same command green locally and in CI. Keep exceptions on the offending
line with a reason. Delete rules made unnecessary by the mechanism.

Done when every class has a ready-to-merge change or an explicit reason it remains open.

## Reply

One row per class: evidence (links, lines, lesson), level and why the higher level did not work, change,
red/green proof. Then list pruned rules.
