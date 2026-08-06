---
name: codex-delegate
description: Delegate a bounded task to the OpenAI Codex CLI (GPT-5.x) by driving `codex exec` directly — an independent second opinion or adversarial review, a scoped implementation/fix, a diagnosis, an exploration, or a fleet of parallel workers. Use whenever Codex or GPT-5 is named ("ask Codex", "run codex on this", "demande à Codex", "délègue à Codex"), an independent take from another model is wanted, or several Codex workers should fan out and be tracked.
argument-hint: "[optional: what to delegate to Codex — omit to be asked]"
---

# codex-delegate — drive the Codex CLI as a sub-agent

Hand a bounded task to the Codex CLI (GPT-5.x) so it works independently, in parallel to your own reasoning.

**When it's the right call.** Not "when Codex is better" — frontier models across families sit within noise of each other on general capability. Reach for Codex when the task shape fits what it does well, or when you need a family that isn't yours:
- **Independence** — a counter-review, an adversarial pass, a diagnosis you want to cross-check. Different family, different failure modes; that's the whole value.
- **Persistent execution in an environment** — long-horizon work grinding across many files, running the tests, fixing, repeating; shell-heavy or tool-chaining work like migrations and build plumbing.
- **Capacity** — offloading a self-contained chunk while you do other work, at a lower cost per resolved task.

Keep for yourself (or another Claude) the judgment-heavy work: architecture, security review, cross-cutting reasoning, and anything where coherence over a long task matters more than throughput.

You drive `codex` directly — no wrapper. Return Codex's output as-is; if you want to trust it before acting, verify it yourself (read the cited code, run the build/tests) — that's your call as the caller.

## One-shot delegation

`codex exec` runs Codex non-interactively. The sandbox is the safety boundary — the one thing you must set deliberately:

```
codex exec -s read-only "PROMPT"           # inspect / diagnose / explain — touches nothing
codex exec -s workspace-write "PROMPT"      # let Codex edit files (scoped implementation/fix)
codex exec -s danger-full-access "PROMPT"   # no sandbox — last resort, see Sandbox capability limits
```

The intent (diagnose vs explain vs implement) lives in your prompt, not a flag — give Codex an objective, the relevant paths, the constraints, and the exact output you want.

**Clean output idiom.** Codex writes only the final message to stdout; banner, progress, and thinking go to stderr. So `2>/dev/null` gives a clean result; add `-o` when you want the final message as a file artifact (background runs, fleets):

```
codex exec -s read-only "PROMPT" </dev/null 2>/dev/null            # clean stdout
codex exec -s read-only -o /tmp/cx.md "PROMPT" </dev/null 2>&1     # + file artifact
```

The stderr banner prints `session id: <uuid>`, `model:`, `sandbox:` and `reasoning effort:` — the cheapest capture of the thread id and of what actually ran.

Gotchas worth baking into every call:
- `</dev/null` — Codex always reads stdin as additional input; left open, the call hangs forever (zero CPU, zero output).
- **Multiline or quote-heavy prompt → pass it as a file**: inline `"PROMPT"` breaks on shell quoting. Write it to a file and use `-` as the prompt: `codex exec -s read-only - < prompt.md` (`-` consumes stdin, so drop `</dev/null` on that form).
- `cd <abs> && …` or `-C <dir>` — background shells reset their cwd, and a `codex exec` launched from the wrong directory fails *silently*: the `-o`/JSONL files are never created. Check early that they exist and grow.
- In **read-only** mode Codex can't write files — the deliverable IS the final message, captured by `-o`.
- `--skip-git-repo-check` — Codex refuses to run outside a git repo; add this only when that's deliberate.

Other useful flags: `-m <model>`, `--add-dir <dir>` (extra writable dir), `--output-schema <file>` (JSON-Schema-shaped final response when you want to parse it).

**Config overrides (`-c`).** Two knobs, two different axes:

```
-c model_reasoning_effort="xhigh"   # reasoning depth — model-dependent
-c service_tier="fast"              # service speed — NOT a quality trade
```

A wrong effort value errors back with the model's supported list — use that rather than trusting any list written here. Naming differs by surface (the CLI and the app/IDE use different labels for the same rungs), and both knobs are version-dependent: **`--help` and the error message are ground truth**. The model/tier that *actually* ran is printed in the stderr banner (the `--json` stream doesn't carry it); defaults live in `~/.codex/config.toml`.

**Choosing model + effort.** Codex ships a tiered family (a flagship plus cheaper/faster tiers), so model and effort together are a real routing decision, not a detail:

- **Flagship + medium effort** is the sensible default for ordinary work; raise to the top effort rungs for hard debugging, large refactors, and deep audits. `low` is enough for a one-line follow-up on an existing thread.
- **Be wary of the cheaper tiers.** Optimize cost per *resolved* task, not price per token: a weaker tier burns more tokens circling the problem and fails more often, and measured comparisons have shown a half-price tier costing more per resolved task than the flagship. Reach for a cheap tier only for genuinely simple, repeatable work.
- Leave `-m` unset to take the configured default when you have no reason to override; set it deliberately when the task is hard (raise) or trivially mechanical (lower).

## Review mode

For reviewing changes, `codex exec review` is purpose-built — Codex fetches the diff itself, so you don't describe it:

```
codex exec review --uncommitted -o /tmp/rev.md "Adversarial review: correctness bugs, edge cases, regressions." </dev/null
codex exec review --base main "Review this branch against main."
codex exec review --commit <sha> "..."
```

A Codex review is worth running as a matter of course on any substantial change — a different family sees what yours structurally cannot, and it spends a separate quota. Its cost isn't the review, it's the filtering it obliges: the output is **high-recall and low-precision**, with roughly two findings in three not actionable on production PRs, plus real nitpick volume. So pair every review with a filter — triage the findings against the cited code (a cheap read-only agent does this well), then adjudicate what survives. Never auto-apply a review's sketched fixes; validate each against the code first, since a sketch can be wrong in ways that create new bugs.

## Foreground vs background

- **Foreground** for a bounded task you're waiting on — the result comes back in the turn.
- **Background** for anything open-ended or long, and always when running several at once: launch each with your Bash tool in background mode and keep working. You're re-invoked when each finishes, so don't block a turn on a long run. No default timeout on a long run — it kills the worker at the deadline mid-task; size it to the effort (low ≈3 min, medium ≈10, high ≈20, xhigh ≈30+) or rely on a monitor.

To run and track **several workers at once**, read `references/fleet.md` — per-worker output files, thread-id capture, liveness/hang recovery, and the parallel-write collision trap.

## Threads

A thread is the resumable Codex conversation (the CLI also says "session" — same thing).

- `codex exec resume --last "..."` — continue the most recent thread in this dir (serial follow-up: "keep going", "apply the top fix").
- `codex exec resume <id> "..."` — continue a specific thread (use the captured `thread_id`).
- `codex resume` / `codex fork` — interactive picker / branch a thread (human-driven).
- `codex exec --ephemeral ...` — don't persist the thread at all.

**Resume gotchas** (`--help` is ground truth): recent CLIs accept `--json`/`-o`/`-c` after the `resume` subcommand, older ones only before it — before works everywhere; and the **sandbox mode is inherited from the thread** (`resume` takes no sandbox flag) — pick it at creation.

**Persistent vs fresh thread — a doctrine, not a mechanic.** One thread resumed across tasks accumulates project context — the continuity worker of a long build (record the id, it outlives your own sessions; open each dispatch with the delta since its last task). But an independent opinion — counter-review, adversarial pass — must run in a **fresh thread**: resuming contaminates exactly the independence you're paying for. And when a worker stops on a blocker, resume *its* thread with a bounded grant ("AUTHORIZED: <the specific change>, with these constraints") rather than restating the task or silently widening scope.

## Sandbox capability limits

`workspace-write` cuts off more than file writes. Establish the division of labor up front (verified on this setup; re-probe if the environment changes):
- **Build daemons**: Gradle wants its daemon and locks in `~/.gradle` — outside the sandbox. Either you own compilation (Codex delivers uncompiled, you build and feed errors back), or give it `GRADLE_USER_HOME` inside the workspace + `--no-daemon` so it can self-verify.
- **Network/DNS is cut**: clones and downloads fail — pre-stage pinned checkouts/vendored deps and point at them.
- **`.git` is effectively read-only**: Codex never commits — you own commits, which conveniently forces your review/gates to run pre-commit.
- **No servers or long-running processes in the sandbox** — the runtime owner runs them. Corollary: a test Codex couldn't execute is unvalidated by construction; route its first run to whoever owns the runtime.

**Escape valve — `-s danger-full-access`.** When a limit has no workaround (a build that truly needs global caches, a task that must reach the network) and pre-staging doesn't fit, drop the sandbox deliberately rather than contorting the task. The safety boundary is gone, so compensate in the prompt: scope it to exactly the commands and paths needed, and prefer a discardable fresh thread. A thread can't *switch* sandbox modes — resume with `--dangerously-bypass-approvals-and-sandbox` (all-or-nothing: it also skips approvals; meant for environments that are already externally sandboxed) or create a fresh thread.

## Notes

- Needs `codex` on PATH and a logged-in CLI (`codex login`). If it isn't set up, say so rather than guessing.
