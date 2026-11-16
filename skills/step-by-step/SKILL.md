---
name: step-by-step
description: "Use for \"step by step\", \"point par point\", or \"go\" on review findings, with user validation and a commit per item."
---

# Step-by-step

Use the user-selected review/audit/list first, otherwise the latest list in this conversation. Without one,
ask for a list or whether to analyze first.

## Per item

1. Announce **Point N/Total: [title]**, problem and impact/risk concisely.
2. Via the question tool, offer approaches (or go/skip for an obvious one), skip and free choice; wait for
   validation before coding.
3. Implement the chosen solution.
4. Run a relevant existing fast build/type/lint/test check before commit; skip only if none is quick. Add no
   tests.
5. Offer commit / Codex review then commit / discard via the question tool; review is opt-in.
6. Make one atomic conventional commit and advance.

## Opt-in Codex review

1. Stage this item's files; run `codex exec review --uncommitted` in a fresh thread, with what/why and a
   request for correctness, edge cases and regressions: pass/warn/fail, `file:line`, suggested fixes.
2. Verify each finding in code; retain only real issues introduced within scope and lower exaggerated
   severity. All invalid means pass.
3. Show verified findings and counts discarded.
4. Pass/no verified findings → commit. Warn/fail → ask fix (then re-review or commit), ignore (commit as-is),
   or discard. Wait for validation before review fixes.

Skip/pass/next advances without coding; stop/done/enough ends. For already fixed/irrelevant items, explain and
ask to skip. Avoid repeating the original list.
