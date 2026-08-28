---
name: skillify
description: Turn the procedure that just worked in this session into a reusable skill. Use right after a painful problem is solved — an obscure format decoded, a flaky setup tamed, a multi-step fix that took several wrong turns — or when the user says "make that a skill", "garde ça", "on refera pareil", "skillify".
argument-hint: "[what to capture — omit to infer it from the session. Add a path to write somewhere other than the default skills directory.]"
---

# Skillify — capture what just worked

The value is not "write a skill about X". It is: **this session contains a procedure that cost real turns to discover, and next time it should cost none.** Capture the path that worked *and* the wrong turns that made it expensive.

## When it is worth it

Only when all three hold:

- The procedure is **repeatable** — it will come up again on this repo, this stack, or this machine.
- Getting it right took **more than one attempt**, or depended on something non-obvious you would not rediscover.
- A fresh agent with no memory of this session **could not** derive it from the code alone.

If it is a one-off, or the code already says it, say so and write nothing. A skill that fires on a case that never recurs is pure context tax.

If the knowledge belongs to a repo rather than to you, it is an `AGENTS.md`/`CLAUDE.md` line or a comment, not a skill. Say which and write that instead.

## What to extract

Reread the session, not your memory of it. From it, pull:

1. **The trigger** — what the situation looked like *before* anyone knew the answer. This becomes the description; it is the only part that decides whether the skill ever fires again.
2. **The procedure** — the steps that actually worked, in order, with the exact commands, paths, flags and version numbers used. Not a cleaned-up idealisation.
3. **The wrong turns** — what was tried first and why it failed. This is usually the most valuable part and the first thing a summary drops.
4. **The checks** — how you knew each step had worked.
5. **The boundary** — what this does *not* cover, and when the procedure stops applying.

Anything already written down elsewhere — a spec, an ADR, a service doc, a commit — is referenced by path, never copied.

## Writing it

Follow the `writing-great-skills` skill for the craft: invocation model, description phrasing, structure, what belongs in `references/` versus `SKILL.md`. Do not restate it here.

Two rules specific to captured procedures:

- **Keep it under one screen.** If the result is longer, it is two skills — one that diagnoses and reports, one that applies a named fix. A long skill makes the agent run the half it did not need.
- **Concrete over general.** Real paths, real commands, real error strings. The temptation is to generalise it into advice; advice is what the model already had, and it did not help.

Default location is the user's skills directory (`~/.claude/skills/<name>/`, or the repo's own skills folder when the procedure is repo-specific). Ask before writing anywhere else.

## Before finishing

- Reread the description alone and ask: six months from now, facing this problem again and having forgotten the skill exists, would that text fire? If not, rewrite it — that is the whole skill.
- Say plainly what you left out and why.
