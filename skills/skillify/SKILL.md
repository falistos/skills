---
name: skillify
description: "Capture a hard-won, reusable procedure after a painful multi-attempt fix, or for \"make that a skill\", \"garde ça\", \"on refera pareil\", \"skillify\"."
argument-hint: "[what to capture — omit to infer it from the session. Add a path to write somewhere other than the default skills directory.]"
---

# Skillify

Capture the successful path and costly wrong turns only if all hold:

- **Repeatable:** recurs on this repo, stack or machine.
- **Non-obvious:** needed multiple attempts or knowledge not readily rediscovered.
- **Underivable:** a fresh agent cannot recover it from code alone.

Otherwise explain and write no skill. Repo knowledge belongs in an AGENTS.md/CLAUDE.md line or comment; name
that home and write there instead.

## Extract from the session

1. Trigger before the answer was known → description.
2. Successful ordered procedure with exact commands, paths, flags and versions, not an idealized rewrite.
3. Wrong turns and reasons they failed.
4. Each step's success check.
5. Boundary and when the procedure stops applying.

Reference existing specs/ADRs/service docs/commits by path rather than copying.

## Write and finish

Load `writing-for-agents` when installed; follow the target repo's authoring rules, with folder-matching `name`.
Keep under one screen; longer procedures split diagnosis/report from a named fix. Use concrete
commands/paths/error strings rather than generic advice.

Locations: shared → the skills repo it belongs to, through a PR; repo-specific → `.agents/skills/<name>/`
plus a Claude `.claude/skills/<name>` symlink.
Honor an explicit path; ask before another location.

Done when the description would trigger for the original problem six months later, and omissions/reasons are
stated.
