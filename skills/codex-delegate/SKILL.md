---
name: codex-delegate
description: Delegate a bounded task to the OpenAI Codex CLI as a sub-agent — a second-opinion code review or adversarial pass, a scoped implementation/fix, a root-cause diagnosis, or a codebase exploration — driven through a thin controllable wrapper over `codex exec`. Use whenever you want Codex (GPT-5.x) to independently work a task in parallel to your own reasoning: "ask Codex", "get a second opinion from Codex", "have Codex review this diff", "let Codex implement X", "run codex on this", "adversarial review with Codex", "what does GPT-5 think". This is the general, intentional way to drive Codex; the wrapper exposes primitive modes (read / write / review) and you write the prompt. For the reflexive "I'm stuck, hand it off" case, `codex:rescue` still applies. Triggers in French too: "demande à Codex", "deuxième avis de Codex", "fais reviewer par Codex", "délègue à Codex", "lance codex là-dessus".
user-invocable: true
args: "[optional: mode (read|write|review) and/or what to delegate — omit to be asked]"
---

# codex-delegate — drive Codex CLI as a sub-agent

Hand a bounded task to the Codex CLI (GPT-5.x) so it works independently, in parallel to your own reasoning. A second engine is worth most when you want an *independent* take (review, adversarial verification, a diagnosis you can cross-check) or when offloading a self-contained chunk while you do something else.

Everything goes through the wrapper:

```
scripts/codex-run <mode> [options] "PROMPT"
```

The wrapper is a **primitive**: a mode only sets the sandbox and the Codex invocation. It injects no prompt of its own — the framing is entirely yours. What makes this better than a blind forwarder is that *you* pick the right primitive and write a sharp prompt, rather than hoping Codex guesses the intent.

**Output contract:** stdout is Codex's final message (clean); stderr is live progress. Return Codex's output as-is — this skill does not second-guess it. If you want to trust it before acting, verify it yourself (read the cited code, run the build/tests); that's your call as the caller, not the wrapper's job.

## The three modes

Pick by what Codex needs to *do*, since the mode is also the safety boundary:

| Mode | Sandbox | Invocation | For |
|---|---|---|---|
| `read` | read-only | `codex exec -s read-only` | Anything that only inspects: diagnose a bug, explain a module, explore an architecture, answer a question about the code. |
| `write` | workspace-write | `codex exec -s workspace-write` | When you actually want Codex editing files: a scoped implementation or fix. |
| `review` | read-only | `codex exec review` | Review the working changes / a diff / a branch. Codex fetches the diff itself. |

`write` is the only mode that can change files — reach for it deliberately. `review` is separate from `read` because it's a distinct Codex sub-command that diffs the repo for you and unlocks the scoping flags below.

## Writing the prompt

The mode is mechanical; the prompt carries the intent. Give Codex an objective, the relevant paths, and the output you want — a vague prompt gets a vague result. Frame the intent explicitly since the tool won't:

```
# diagnose (read)
scripts/codex-run read "Root-cause why tests/payment_test.py fails with KeyError since HEAD~1. Trace it; don't propose fixes yet."

# explain (read)
scripts/codex-run read "Explain how the event bus in src/core wires publishers to subscribers."

# implement (write)
scripts/codex-run write "Add input validation to src/api/users.ts, following the existing pattern in src/api/auth.ts."

# review the current changes (review — no need to describe the diff)
scripts/codex-run review --uncommitted "Adversarial review: correctness bugs, edge cases, regressions."
scripts/codex-run review --base main "Review this branch against main."
```

For a non-trivial task, use the `gpt-5-4-prompting` skill to tighten the prompt before delegating.

## Foreground vs background

- **Foreground** for a bounded task you're waiting on — the result comes back in the turn.
- **Background** for anything open-ended or long: run the Bash call with `run_in_background: true` and keep working; you'll be notified on completion. Don't block a whole turn on a long Codex run.

## Options

- `-m, --model <M>` — leave unset by default (Codex uses its configured model). Set only when asked; pass names through verbatim (e.g. `gpt-5.3-codex-spark`).
- `-C, --cd <DIR>` — run against another directory.
- `--add-dir <DIR>` — extra writable dir for `write` (e.g. a sibling package).
- `--resume` / `--session <ID>` — continue a previous Codex session in this dir ("keep going", "apply the top fix", "dig deeper"). The prompt is the follow-up.
- `--schema <FILE>` — a JSON Schema for a structured final response, when you want to parse the output (e.g. review findings as JSON). stdout is then the JSON.
- `--json` — stream raw JSONL events instead of the final message.
- `--no-git` — allow running outside a git repository (Codex refuses by default).
- `--` — everything after is passed to `codex` verbatim.

## Notes

- Needs `codex` on PATH and a logged-in Codex CLI (`codex login`). If it isn't set up, say so rather than guessing.
- `codex:rescue` still exists for the reflexive "I'm stuck, take over" handoff. This skill is for deliberate delegation — prefer it when you know what you're handing off.
