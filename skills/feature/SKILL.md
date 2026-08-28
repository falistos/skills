---
name: feature
description: Ship a feature, fix or refactor end to end through Orca — scope it, give it its own worktree, drive the coding agents, get it counter-reviewed, commit it. Use when the user asks to build or implement something and wants it run as a piece of work rather than edited in place. Triggers in French too — "dev cette feature", "implémente", "monte-moi", "on part sur", "ship ça".
argument-hint: "[what to build — omit to scope from the conversation. 'solo' = one worktree, no workers. 'on macmini' = run it on the paired runtime.]"
---

# Feature — run work through Orca

Orca owns the workspace: one worktree per unit of work, agents in its terminals, status visible on the card. You own the decisions. Never edit the user's checked-out branch in place for anything bigger than a one-liner.

Load the command surface from the binary, never from memory:
`orca skills get orca-cli` (worktrees, terminals, handoffs) and `orca skills get orchestration` (Run/Task/Dispatch, only for the supervised lane).

## 1. Pick the lane before doing anything

| | When | How |
|---|---|---|
| **solo** | one coherent change, sequential, you can hold it | `worktree create --agent claude`, or work in `current` |
| **supervised** | ≥3 genuinely independent units, contracts can be frozen first | Run + Tasks + `worker-start`, you coordinate |
| **handoff** | the user said "donne ça à un autre agent / worktree" | `worktree create --no-parent --agent <id> --prompt`, then stop |

Default to **solo**. Coding parallelizes badly — most of it is sequential and coherence-bound. Fan out only when the units are independent *and* their interfaces are already fixed; otherwise every ambiguity in the split multiplies. Fewer than 3 independent units → solo, and say so.

`handoff` means ownership transfer: do not monitor, do not poll the terminal, do not create lifecycle obligations.

## 2. Scope it (short)

Enough to write a brief a stranger could execute: the goal, what is explicitly *out*, the files or modules touched, the done-condition. Read the repo instead of asking whatever the repo answers. Ask only what changes what gets built, one question at a time, with your recommendation.

If the request rests on a bad premise or there is a better approach, say so before building — then build what was decided.

## 3. Place the work

```text
orca worktree create --repo id:<repoId> --name <kebab-task> --agent claude --prompt "<brief>" --json
orca worktree set --worktree active --workspace-status in-progress --json
```

- `--no-parent` for independent work; omit `--base-branch` so it forks the repo default, never the current feature branch, unless stacking was asked for.
- Use the `startupTerminal.handle` from the response as the only handle for that worker. Re-resolve with `terminal list` if it goes stale; never dual-send.
- To run on the Mac mini instead of this machine, add `--environment macmini` to every command. Cursor does not work there (locked keychain); Claude, Codex and Grok do.
- First launch in a fresh worktree stops on Claude Code's trust and bypass prompts — answer them with `terminal send`, or the worktree looks hung.

Update the card as state changes; that is what the user reads instead of asking:

```text
orca worktree set --worktree active --comment "repro done, fixing the resolver" --json
```

## 4. The worker brief

Workers see nothing of this conversation and do not inherit the user's config. Every brief is self-contained and carries the house rules verbatim:

> **Goal** — <what and why, one paragraph>
> **Scope** — touch only <paths>. Out of scope: <explicit list>.
> **Done when** — <observable condition>.
> **House rules**
> - Code, comments, config, commit messages in English.
> - No comments by default. Only a non-obvious *why*, one to three lines, no context from outside the code.
> - No backward compatibility, no migration path, unless explicitly asked.
> - No tests unless explicitly asked.
> - Prefer a well-maintained third-party library over reinventing it.
> - Java: never inline FQNs, always imports. Modern idioms (records, sealed, pattern-matching switch). IO/DB/saves async by default on virtual threads; block only where it is required, like shutdown. Fail fast internally, degrade gracefully at the user boundary. `Optional`/result types over exceptions; exceptions for genuinely exceptional cases.
> - Conventional Commits, English, subject line only unless the body adds a real *why*. Never an AI attribution footer. Never describe how the change was produced.
> - Verify against the source — dependency code, official docs, release notes — before asserting an API, a version or a behaviour. Mark what you assumed as assumed.
> - Report what you did not do, and why.

Append the repo's own conventions when they differ, and any interface the worker must not change.

## 5. Counter-review before commit

A same-family reviewer misses what the author missed. Run one pass from a different model family — Codex over Claude's work, or Claude over Codex's — on the diff only:

```text
orca terminal create --worktree active --command 'codex' --json
orca terminal send --terminal <handle> --text "Review the diff vs the base branch. Correctness, then the house rules in the worktree brief. Only findings you can point at a line for. No praise, no summary." --enter --json
```

Triage the findings yourself: fix what is real, drop what is noise, tell the user what you dropped. Do not hand the review back to the worker as a to-do list.

The `code-review`, `arch-review` and `python-review` skills go deeper when the change deserves it.

## 6. Land it

Conventional Commit, subject line only unless the body carries a *why*. Then:

```text
orca worktree set --worktree active --workspace-status in-review --json
```

Report to the user in French: what shipped, what you decided on their behalf, what you left out and why, and anything still unverified. Do not claim a check passed that you did not run.

## Guardrails

- Never commit or push unless asked. Never force-push. Branch before touching a default branch.
- To read an external repo, clone it under `/tmp` first, then search there.
- One worktree per unit of work. Do not let two agents write the same files; use `isolation`/separate worktrees instead of hoping.
- A worker that is quiet is not stuck: heartbeats and long silences are normal for coding tasks. Do not kill it because it has been 20 minutes.
- If Orca is not running (`orca status --json`), say so and fall back to plain git — do not invent Orca commands.
