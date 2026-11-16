---
name: kill-slop
description: "Use when implementing, fixing or cleaning up code, writing docstrings, or reviewing comment quality, to keep changes minimal."
---

# Kill slop

Apply the scope, simplicity and comment rules of the always-on instructions, if any; the checks below
decide file shape and diff size.

## File shape

Edit the owning file; split only when all three hold:

1. **Pain now**: already hard to navigate (~300–400 lines or unrelated concerns), worsened by this change.
2. **One unit**: cohesive piece with a clear name.
3. **Local fit**: follows a nearby pattern, otherwise sits beside the caller.

Cohesion alone does not justify a split. Keep splits in the same directory, fix imports and add no convenience
re-exports. Use `utils/`, `helpers/`, `common/` only where established; greenfield stays flat under one root
until navigation hurts.

Match validated project patterns. Remove imports/variables made unused by the change, complete required error
paths, and replace names that need explanatory comments with clearer names.

## Diff budget

Before writing, state goal (user-visible change), smallest touch list and non-goals. For a small task
exceeding ~5 files, reduce the plan. Explicit requests for structure, dependencies, tests or scaffolding
prevail; on ambiguity choose minimal scope and report omissions.

## Comments/docstrings

- Imperative docstring summary with a period; blank line before a body.
- Update stale comments alongside code.
- Use neutral vocabulary in neutral layers; vendor/CLI names only for their own behavior.
- Fuse related clauses with `;`, keep one example, cut filler.

## Finish

Every changed line serves the goal; every new file passes the split rule or an explicit request; no
unexplained addition remains. Report changes and deliberate omissions.
