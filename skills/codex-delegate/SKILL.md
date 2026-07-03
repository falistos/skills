---
name: codex-delegate
description: Delegate a bounded task to the OpenAI Codex CLI as a sub-agent — a second-opinion code review or adversarial pass, a scoped implementation/fix, a root-cause diagnosis, or a codebase exploration — driven through a thin controllable wrapper over `codex exec`. Use whenever you want Codex (GPT-5.x) to independently work a task in parallel to your own reasoning: "ask Codex", "get a second opinion from Codex", "have Codex review this diff", "let Codex implement X", "run codex on this", "adversarial review with Codex", "what does GPT-5 think". This is the general, intentional way to drive Codex per task type (each type picks the right sandbox and invocation). For the reflexive "I'm stuck, hand it off" case, `codex:rescue` still applies. Triggers in French too: "demande à Codex", "deuxième avis de Codex", "fais reviewer par Codex", "délègue à Codex", "lance codex là-dessus".
user-invocable: true
args: "[optional: task type (review|implement|diagnose|research) and/or what to delegate — omit to be asked]"
---

# codex-delegate — drive Codex CLI as a sub-agent

Hand a bounded task to the Codex CLI (GPT-5.x) so it works independently, in parallel to your own reasoning. A second engine on the problem is worth most when you want an *independent* take (review, adversarial verification, a diagnosis you can cross-check) or when offloading a self-contained chunk while you do something else.

All invocations go through the wrapper, which picks the right sandbox and Codex sub-command per task type and returns a clean result:

```
scripts/codex-run <type> [options] "PROMPT"
```

**Output contract:** stdout is Codex's final message (clean); stderr is live progress. Return Codex's output to the user as-is — this skill does not second-guess it. If you want to trust it before acting, verify it yourself (read the cited code, run the build/tests) — that's your call as the caller, not something the wrapper does for you.

## Task types

Pick the type from what's being asked — it sets the sandbox, so it's also the safety boundary.

| Type | Sandbox | For |
|---|---|---|
| `review` | read-only | Review the working changes / a diff / a branch. Adversarial second pass on your own work. |
| `implement` | workspace-write | Write code for a scoped, well-specified task. Codex edits files in the workspace. |
| `diagnose` | read-only | Root-cause a bug, a failing test, a CI error. Returns analysis, touches nothing. |
| `research` | read-only | Explore and explain a module, an architecture, a behavior. |

Only `implement` can write. Everything else is read-only — reach for `implement` only when you actually want Codex editing files.

## Invoking

**Review the current changes** (Codex diffs the repo itself — no need to describe the change):
```
scripts/codex-run review --uncommitted "Adversarial review: find correctness bugs, edge cases, and regressions."
scripts/codex-run review --base main "Review this branch against main."
```

**Implement a scoped task:**
```
scripts/codex-run implement "Add input validation to src/api/users.ts per the existing pattern in src/api/auth.ts."
```

**Diagnose / research** (read-only):
```
scripts/codex-run diagnose "Tests in tests/payment_test.py fail with a KeyError since the last commit — find the root cause."
scripts/codex-run research "Explain how the event bus in src/core wires publishers to subscribers."
```

Write a good prompt: give Codex an objective, the relevant paths, and the output you want. A vague prompt gets a vague result. Use the `gpt-5-4-prompting` skill to tighten it before delegating if the task is non-trivial.

## Foreground vs background

- **Foreground** for a bounded task you're waiting on — you get the result back in the turn.
- **Background** for anything open-ended or long-running: run the Bash call with `run_in_background: true` and keep working; you'll be notified on completion. Don't block a whole turn on a long Codex run.

## Options worth knowing

- `-m, --model <M>` — leave unset by default (Codex uses its configured model). Set only when asked; pass model names through verbatim (e.g. `gpt-5.3-codex-spark`).
- `-C, --cd <DIR>` — run against another directory.
- `--add-dir <DIR>` — extra writable dir for `implement` (e.g. a sibling package).
- `--resume` / `--session <ID>` — continue a previous Codex session in this dir ("keep going", "apply the top fix", "dig deeper"). The prompt you pass is the follow-up.
- `--schema <FILE>` — a JSON Schema for a structured final response, when you want to parse Codex's output (e.g. review findings as JSON). stdout is then the JSON.
- `--json` — stream raw JSONL events instead of the final message (for live monitoring).
- `--` — everything after is passed to `codex` verbatim, for flags the wrapper doesn't wrap.

## Notes

- The wrapper needs `codex` on PATH and a logged-in Codex CLI (`codex login`). If it isn't set up, say so rather than guessing.
- `codex:rescue` still exists for the reflexive "I'm stuck, take over" handoff. This skill is for deliberate, typed delegation — prefer it when you know what kind of task you're handing off.
