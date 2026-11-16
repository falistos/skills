---
name: ux-review
description: "Review Java plugin/tool feature gaps and operator use cases (\"qu'est-ce qui manque\", \"complétude fonctionnelle\"), cross-checked with Codex; excludes UI design."
user-invocable: true
argument-hint: "[package or module path to scope the review — omit for full project]"
---

# Functional completeness review

Report operator gaps only; write no code. Suggest concrete commands, keys, flags and behaviors for real
scenarios, including half-done features and uncontrolled side effects. Code quality and architecture are
outside scope.

## 1. Discover

Read build, manifests/permissions, all resource YAML/JSON, messages/locales and scoped Java, with parallel
Explore agents. Read README, AGENTS.md and spec for intent; documented non-goals are not gaps.

Finish with today's commands, configurable versus hardcoded behavior, triggers and managed state enumerated.

## 2. Analyze in parallel

Run background read-only Codex (`codex exec -s read-only`) from a prompt file. Brief it with scope/exclusions,
concrete operational scenarios, and the six angles below. Require each suggestion to cite read
code/config/commands and check that it is absent; return type, severity, title, context, scenario and specific
suggestion, plus well-covered areas. If Codex is missing/logged out, report it and continue local analysis
alone.

Local angles:

1. **Operations:** create/modify/inspect/delete/list for each entity; internal-only admin operations; bulk
   variants.
2. **Side effects:** logical deletion versus physical cleanup, reset keep/loss choices, controllable cascades.
3. **Config:** constants, thresholds, durations, cooldowns, limits, messages, materials/sounds, feature
   toggles and changes without restart.
4. **Use cases:** initial setup, daily management, mid-event changes/emergencies/rollback/correction, seasonal
   reset/migration/archive/cleanup, empty/overflow/concurrent/partial-failure states.
5. **Half-done features:** missing options, scope/customization and natural extensions such as leaderboard
   reset/filter/export.
6. **Integrations:** useful PlaceholderAPI, events, config actions/conditions.

## 3. Reconcile and report

Wait for Codex. Both → `[Claude + Codex]` (high confidence); local only → `[Claude]`; Codex only → reread code
to verify absence before `[Codex]`; disagreement → `[Disputed]` with both views. Deduplicate and reread before
claiming anything missing.

Severity: **BLOCKING** makes a realistic use case impossible without code changes; **GAP** is a noticeable
omission most operators expect; **IMPROVEMENT** extends something workable. Types: `FEATURE`, `CONFIG`,
`COMMAND`, `FLAG`, `PERMISSION`.

Report one-sentence completeness verdict, specific well-covered areas, then suggestions ordered by
severity/type. Each gives severity/title/source/type, concrete gap/context, real operator scenario, and named
key/command syntax/feature behavior. End with numbered action groups: quick wins, new commands/operations, new
features.

Apply operator judgment: not every edge needs a command or everything config; this is an operations wishlist.
Say plainly if only the happy path is covered.

End with: "Run `/step-by-step` to start implementing these changes."
