---
name: clean-copy
description: "Use when writing or reviewing user-facing strings, labels, hints, empty states, toasts or confirmations, or asked to clean up / tighten copy."
---

# Clean copy

Decide whether a string belongs on screen before improving its wording. Read it beside the actual label, value
and controls.

## Deletion ladder

Stop at the first matching rung:

1. **Unprompted question**: remove copy about something the user would never wonder about; reassurance can
   create the doubt it answers.
2. **Redundant label**: remove captions already expressed by the label, field or adjacent value. Keep units
   that make a bare value meaningful.
3. **Defending implementation**: remove bug-fix history, design justifications, permission slips and hedges
   about normal behavior. A fixed bug earns a fix, not a caption.
4. **Empty remainder**: cut offending clauses; if nothing useful remains, delete the element/prop rather than
   leaving an empty hint or stub.

## Keep

- A consequence the user cannot infer, at the decision point (for example unsynced data loss).
- Invisible compatibility or scope requirements that determine applicability.
- The meaning of an empty state and its next action.
- Units, scale and format for bare values.

Keep only the necessary consequence, without telling users when they are allowed to press an available button.
Move rare-state explanations into that state where possible.

## Review output

For each failing string: `file:line`, current text, rewrite or `cut`, and the failed rung. Cut whole clauses
before trimming words; leave passing copy alone.
