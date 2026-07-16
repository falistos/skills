---
name: codex-delegate
description: Delegate a bounded task to the OpenAI Codex CLI (GPT-5.x) by driving `codex exec` directly — an independent second opinion or adversarial review, a scoped implementation/fix, a diagnosis, an exploration, or a fleet of parallel workers. Use whenever Codex or GPT-5 is named ("ask Codex", "run codex on this", "demande à Codex", "délègue à Codex"), an independent take from another model is wanted, or several Codex workers should fan out and be tracked.
user-invocable: true
args: "[optional: what to delegate to Codex — omit to be asked]"
---

# codex-delegate — drive the Codex CLI as a sub-agent

Hand a bounded task to the Codex CLI (GPT-5.x) so it works independently, in parallel to your own reasoning. Worth most when you want an *independent* take (review, adversarial verification, a diagnosis you can cross-check) or when offloading a self-contained chunk while you do other work.

You drive `codex` directly — no wrapper. This skill is the knowledge: the right invocation per intent, the output idiom, and how to run and track a fleet. Return Codex's output as-is; if you want to trust it before acting, verify it yourself (read the cited code, run the build/tests) — that's your call as the caller.

## One-shot delegation

`codex exec` runs Codex non-interactively. The sandbox is the safety boundary — it's the one thing you must set deliberately:

```
codex exec -s read-only "PROMPT"           # inspect / diagnose / explain — touches nothing
codex exec -s workspace-write "PROMPT"      # let Codex edit files (scoped implementation/fix)
codex exec -s danger-full-access "PROMPT"   # no sandbox — last resort, see Sandbox capability limits
```

The intent (diagnose vs explain vs implement) lives in your prompt, not a flag — give Codex an objective, the relevant paths, the constraints, and the exact output you want (format, location, level of detail).

**Clean output idiom.** In plain mode Codex mixes progress into stdout. To get just the final message, write it to a file with `-o` and read that:

```
codex exec -s read-only -o /tmp/cx.md "PROMPT" </dev/null >/dev/null 2>&1 && cat /tmp/cx.md
```

Gotchas worth baking into every call:
- `</dev/null` — close stdin so Codex never blocks waiting on it.
- `cd <abs> && …` or `-C <dir>` — background shells reset their cwd, and a `codex exec` launched from the wrong directory fails *silently*: the `-o`/JSONL files are never created. Check early that they exist and grow.
- In **read-only** mode Codex can't write files — the deliverable IS the final message, captured by `-o`.
- `--skip-git-repo-check` — Codex refuses to run outside a git repo; add this only when that's deliberate.

Other useful flags: `-m <model>` (leave unset to use Codex's configured model; set only when asked), `--add-dir <dir>` (extra writable dir), `--output-schema <file>` (force a JSON-Schema-shaped final response when you want to parse it).

**Config overrides (`-c`).** Two knobs, two different axes:

```
-c model_reasoning_effort="xhigh"   # reasoning depth (minimal|low|medium|high|xhigh)
-c service_tier="fast"              # service speed — NOT a quality trade
```

`low` effort is enough for a one-line follow-up on an existing thread. The model/tier that *actually* ran is in the run's JSONL events — read it there when asked; defaults live in `~/.codex/config.toml`, and both knobs are version-dependent (`--help` is ground truth).

## Review mode

For reviewing changes, `codex exec review` is purpose-built — Codex fetches the diff itself, so you don't describe it:

```
codex exec review --uncommitted -o /tmp/rev.md "Adversarial review: correctness bugs, edge cases, regressions." </dev/null
codex exec review --base main "Review this branch against main."
codex exec review --commit <sha> "..."
```

## Foreground vs background

- **Foreground** for a bounded task you're waiting on — the result comes back in the turn.
- **Background** for anything open-ended or long, and always when running several at once: launch each with your Bash tool in background mode and keep working. You're re-invoked when each finishes, so don't block a turn on a long run. No default timeout on a long run — it kills the worker at the deadline mid-task; size it to the job or rely on a monitor.

## Spawning and tracking a fleet

To run several Codex workers at once, launch each as a background process writing to its own files, then track them. Keep the outputs in a gitignored dir (e.g. `.codex/`):

```
# one worker, launched in the background:
codex exec --json -s read-only -o .codex/w1.msg "PROMPT" </dev/null >.codex/w1.jsonl 2>&1
```

- `--json` streams structured events to `w1.jsonl`; `-o` still writes the clean final message to `w1.msg`. You get both.
- The **session id** is the first event: `{"type":"thread.started","thread_id":"019f…"}` — `head -1 .codex/w1.jsonl` gives it. Capture it per worker.

Tracking, without a wrapper — and **judge the artifacts, never the exit code**: a worker can exit non-zero with a complete, correct deliverable, and a "clean" launch may have produced nothing (the silent-cwd failure above).
- **Completion** — you're notified as each background process exits; react rather than busy-poll. Done = `turn.completed` in the JSONL (with token usage) + the final answer in `.msg`.
- **Liveness** — `stat` the `.jsonl`: recent mtime and growing size = alive; a stale file = dead or never started.
- **Progress / status** — count `item.completed` events; parse the last `agent_message` for a relayable "what's it doing".
- **Follow up** — resume by captured id: `codex exec resume <thread_id> "next instruction"`. (`--last` is ambiguous with a fleet — always resume by id.)

**Parallelism caution.** Read-only workers fan out freely. But several `workspace-write` workers on the same working tree will collide on files — give each its own directory or git worktree, or run the writers serially. This is the same coherence trap as any multi-agent build: freeze who-owns-what before fanning out.

Scale to the task: a handful of workers with clear, non-overlapping scopes — not a swarm. Each `codex exec` is a full GPT-5.x agent; they're expensive and heavy.

## Sessions

- `codex exec resume --last "..."` — continue the most recent session in this dir (serial follow-up: "keep going", "apply the top fix").
- `codex exec resume <id> "..."` — continue a specific session (use the captured `thread_id`).
- `codex resume` / `codex fork` — interactive picker / branch a session (human-driven).
- `codex exec --ephemeral ...` — don't persist the session at all.

**Resume gotchas** (both have burned real runs; `--help` if the CLI has changed): global flags (`--json`, `-o`, `-c …`) go **before** the `resume` subcommand — after it, the call errors out; and the **sandbox is inherited from the thread** (`resume` takes no sandbox flag) — pick it at creation, it's for life.

**Persistent vs fresh thread — a doctrine, not a mechanic.** One thread resumed across tasks accumulates project context — the continuity worker of a long build (record the id, it outlives your own sessions; open each dispatch with the delta since its last task). But an independent opinion — counter-review, adversarial pass — must run in a **fresh thread**: resuming contaminates exactly the independence you're paying for. And when a worker stops on a blocker, resume *its* thread with a bounded grant ("AUTHORIZED: <the specific change>, with these constraints") rather than restating the task or silently widening scope.

## Sandbox capability limits

`workspace-write` cuts off more than file writes. Establish the division of labor up front (verified on this setup; re-probe if the environment changes):
- **Build daemons**: Gradle wants its daemon and locks in `~/.gradle` — outside the sandbox. Either you own compilation (Codex delivers uncompiled, you build and feed errors back), or give it `GRADLE_USER_HOME` inside the workspace + `--no-daemon` so it can self-verify.
- **Network/DNS is cut**: clones and downloads fail — pre-stage pinned checkouts/vendored deps and point at them.
- **`.git` is effectively read-only**: Codex never commits — you own commits, which conveniently forces your review/gates to run pre-commit.
- **No servers or long-running processes in the sandbox** — the runtime owner runs them. Corollary: a test Codex couldn't execute is unvalidated by construction; route its first run to whoever owns the runtime.

**Escape valve — `-s danger-full-access`.** When a limit has no workaround (a build that truly needs global caches, a task that must reach the network) and pre-staging doesn't fit, drop the sandbox deliberately rather than contorting the task. The safety boundary is gone, so compensate in the prompt: scope it to exactly the commands and paths needed, and prefer a discardable fresh thread. The sandbox being thread-for-life, an existing thread can't be upgraded — create a new one. (`--dangerously-bypass-approvals-and-sandbox` also skips approvals; meant only for environments that are already externally sandboxed.)

## Notes

- Needs `codex` on PATH and a logged-in CLI (`codex login`). If it isn't set up, say so rather than guessing.
