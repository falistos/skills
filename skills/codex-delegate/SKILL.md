---
name: codex-delegate
description: Delegate a bounded task to the OpenAI Codex CLI as a sub-agent — a second-opinion code review or adversarial pass, a scoped implementation/fix, a root-cause diagnosis, or a codebase exploration — by driving `codex exec` directly. Use whenever you want Codex (GPT-5.x) to independently work a task in parallel to your own reasoning: "ask Codex", "get a second opinion from Codex", "have Codex review this diff", "let Codex implement X", "run codex on this", "adversarial review with Codex", "what does GPT-5 think", or when you want to fan out several Codex workers and track them. For the reflexive "I'm stuck, hand it off" case, `codex:rescue` still applies. Triggers in French too: "demande à Codex", "deuxième avis de Codex", "fais reviewer par Codex", "délègue à Codex", "lance codex là-dessus", "plusieurs codex en parallèle".
user-invocable: true
args: "[optional: what to delegate to Codex — omit to be asked]"
---

# codex-delegate — drive the Codex CLI as a sub-agent

Hand a bounded task to the Codex CLI (GPT-5.x) so it works independently, in parallel to your own reasoning. Worth most when you want an *independent* take (review, adversarial verification, a diagnosis you can cross-check) or when offloading a self-contained chunk while you do other work.

You drive `codex` directly — no wrapper. This skill is the knowledge: the right invocation per intent, the output idiom, and how to run and track a fleet. Return Codex's output as-is; if you want to trust it before acting, verify it yourself (read the cited code, run the build/tests) — that's your call as the caller.

## One-shot delegation

`codex exec` runs Codex non-interactively. The sandbox is the safety boundary — it's the one thing you must set deliberately:

```
codex exec -s read-only "PROMPT"        # inspect / diagnose / explain — touches nothing
codex exec -s workspace-write "PROMPT"   # let Codex edit files (scoped implementation/fix)
```

The intent (diagnose vs explain vs implement) lives in your prompt, not a flag — give Codex an objective, the relevant paths, and the output you want. A vague prompt gets a vague result. For a non-trivial task, tighten it with the `gpt-5-4-prompting` skill first.

**Clean output idiom.** In plain mode Codex mixes progress into stdout. To get just the final message, write it to a file with `-o` and read that:

```
codex exec -s read-only -o /tmp/cx.md "PROMPT" </dev/null >/dev/null 2>&1 && cat /tmp/cx.md
```

Two gotchas worth baking into every call:
- `</dev/null` — close stdin so Codex never blocks waiting on it.
- `--skip-git-repo-check` — Codex refuses to run outside a git repo; add this only when you deliberately run somewhere that isn't one.

Other useful flags: `-m <model>` (leave unset to use Codex's configured model; set only when asked), `-C <dir>` (working root), `--add-dir <dir>` (extra writable dir), `--output-schema <file>` (force a JSON-Schema-shaped final response when you want to parse it).

## Review mode

For reviewing changes, `codex exec review` is purpose-built — Codex fetches the diff itself, so you don't describe it:

```
codex exec review --uncommitted -o /tmp/rev.md "Adversarial review: correctness bugs, edge cases, regressions." </dev/null
codex exec review --base main "Review this branch against main."
codex exec review --commit <sha> "..."
```

## Foreground vs background

- **Foreground** for a bounded task you're waiting on — the result comes back in the turn.
- **Background** for anything open-ended or long, and always when running several at once: launch each with your Bash tool in background mode and keep working. You're re-invoked when each finishes, so don't block a turn on a long run.

## Spawning and tracking a fleet

To run several Codex workers at once, launch each as a background process writing to its own files, then track them. Keep the outputs in a gitignored dir (e.g. `.codex/`):

```
# one worker, launched in the background:
codex exec --json -s read-only -o .codex/w1.msg "PROMPT" </dev/null >.codex/w1.jsonl 2>&1
```

- `--json` streams structured events to `w1.jsonl`; `-o` still writes the clean final message to `w1.msg`. You get both.
- The **session id** is the first event: `{"type":"thread.started","thread_id":"019f…"}` — `head -1 .codex/w1.jsonl` gives it. Capture it per worker.
- `{"type":"turn.completed",...}` at the end of the JSONL marks that worker done (with token usage); the final answer is in `w1.msg`.

Tracking, without a wrapper:
- **Completion** — you're notified as each background process exits; react to those rather than busy-polling. To check mid-flight, use your background-task tooling (list running tasks, read a task's output, stop one) or just read the worker's `.jsonl`/`.msg` files — they're yours, safe to read.
- **Follow up on a specific worker** — resume by its captured id: `codex exec resume <thread_id> "next instruction"`. (`--last` only works when a single session is in play; with a fleet it's ambiguous — always resume by id.)

**Parallelism caution.** Read-only workers fan out freely. But several `workspace-write` workers on the same working tree will collide on files — give each its own directory or git worktree, or run the writers serially. This is the same coherence trap as any multi-agent build: freeze who-owns-what before fanning out.

Scale to the task: a handful of workers with clear, non-overlapping scopes — not a swarm. Each `codex exec` is a full GPT-5.x agent; they're expensive and heavy.

## Sessions

- `codex exec resume --last "..."` — continue the most recent session in this dir (serial follow-up: "keep going", "apply the top fix").
- `codex exec resume <id> "..."` — continue a specific session (use the captured `thread_id`).
- `codex resume` / `codex fork` — interactive picker / branch a session (human-driven).
- `codex exec --ephemeral ...` — don't persist the session at all.

## Notes

- Needs `codex` on PATH and a logged-in CLI (`codex login`). If it isn't set up, say so rather than guessing.
- `codex:rescue` still exists for the reflexive "I'm stuck, take over" handoff. This skill is for deliberate delegation and fan-out — prefer it when you know what you're handing off.
