---
name: step-by-step
description: Iterate through a list of items previously identified by Claude (issues, improvements, suggestions from an analysis or review). For each item, explain the problem, propose solutions, wait for validation, implement, and commit. Use when user says "step by step", "point par point", "one by one", "on les traite", "go", or wants to iterate through findings.
user-invocable: true
---

# Step-by-Step Implementation Workflow

You are now in **step-by-step mode**. Iterate through a list of items you previously identified (from a review, analysis, audit, etc.) and process each one with user validation.

## Finding the List

Iterate on the most recent list of items in scope. In order of preference: a list the user just pointed at (a file — analysis doc, handoff, `improve` output — or a pasted set), then the most recent list you produced earlier in the conversation (issues, improvements, suggestions, etc.).

If there's no list anywhere, ask: "I don't have a list to iterate on. Want me to analyze something first, or do you have a list to give me?"

## Cycle per Item

For **each item** in the list, follow this exact sequence:

1. **Announce** — "**Point N/Total: [title]**"
2. **Explain** — Concisely explain the problem/issue and why it matters (impact, risk, etc.).
3. **Propose** — Present one or more solution approaches. Use `AskUserQuestion` to let the user pick an approach, skip this item, or suggest their own. If only one obvious approach exists, present it and ask for go/skip.
4. **Wait** — Do NOT code until the user validates.
5. **Implement** — Code the validated solution.
6. **Verify** — If the project has a fast check that covers this change (build, typecheck, lint, or a relevant existing test), run it to confirm the change holds before committing. Don't write new tests. Skip if there's nothing quick to run.
7. **Codex Review (optional)** — After implementation, offer the user a Codex review before committing. Use `AskUserQuestion` with options: commit, review (Codex review then commit), or discard. If the user picks review, follow the **Codex Review** section below.
8. **Commit** — Atomic conventional commit for this item only.
9. **Next** — Move to the next item and repeat.

## Codex Review

When the user requests a Codex review on the current item:

1. **Stage changes** — `git add` the files touched by this item.
2. **Launch review** — Use the `codex:codex-rescue` subagent with a review prompt targeting the staged diff. Follow the `gpt-5-4-prompting` skill to structure the prompt. The prompt must:
   - Include the item context (what was changed and why).
   - Ask Codex to review the staged diff for correctness, edge cases, and regressions.
   - Request a structured output: verdict (pass/warn/fail), findings with file:line references, and suggested fixes if any.
3. **Verify findings** — Before presenting anything to the user, independently verify each Codex finding. For every reported issue:
   - Read the actual code at the referenced file:line.
   - Check if the issue is real (not a hallucination or misunderstanding of context).
   - Check if it's relevant to the current change (not a pre-existing issue outside scope).
   - Drop any finding that doesn't hold up. Downgrade severity if Codex overstated the risk.
   - If all findings are invalid, treat as pass.
4. **Present verified findings** — Follow the `codex:codex-result-handling` skill. Show only the verified findings to the user. If you dropped or downgraded findings, briefly mention it (e.g. "Codex flagged 3 issues, 1 confirmed after verification").
5. **Act on findings:**
   - If **pass** or no verified findings: proceed to commit.
   - If **warn/fail**: present findings and use `AskUserQuestion` to let the user choose: fix (apply fixes then re-review or commit), ignore (commit as-is), or discard (undo changes for this item).
6. **Do NOT auto-fix.** Never apply fixes from a review without user validation.

## Rules

- **The user can skip.** If they say skip/pass/next, move to the next item without coding.
- **The user can stop.** If they say stop/done/enough, end the workflow.
- **If an item is already fixed or irrelevant**, say so and ask whether to skip.
- **Stay concise.** Short explanations, don't repeat what was already said in the original list.
- **Codex review is opt-in.** Never launch a Codex review without the user asking for it.
