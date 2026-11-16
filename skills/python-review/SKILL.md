---
name: python-review
description: "Review Python code or modernization (\"is this Pythonic?\"), including bugs, async, security, design and Python 3.12+ idioms."
---

# Python review

Review what static tools miss: design, async, API and hidden runtime bugs. Input is a root/subpackage/file,
default cwd; ask if a supplied path is missing. Weight user-named concerns.

## Method

1. Read `pyproject.toml` (backend, Python target, tool config, dependencies), layout, entry points
   (`[project.scripts]`, `__main__.py`), lockfiles, README, repo rules/ADRs, module tree and public API.
   Respect pinned versions; 3.12+ is the modernization baseline when compatible with repo intent.
2. Identify tooling: ruff `B/SIM/UP/RUF/ASYNC/PTH/S/LOG/DTZ` covers style smells; recommend missing categories
   instead of duplicate findings. Strict CI mypy/pyright shifts focus to type design, Protocol/ABC and public
   Any leakage. No static tooling is Major and expands manual coverage.
3. Walk every tier below. Time-box by skipping tiers 6–8 only when 1–4 already give a long list, and disclose
   the skip.
4. Report only findings grounded in read lines, with severity, `file:line`, impact and fix.

**Axes:** Standards cites repo rules/tool config; Spec cites request/README/issue/docstring intent; reference
smells are Judgement, overridden by documented policies and intentional choices.

| Tier | Focus | Read under `references/` before findings |
|---|---|---|
| 1. Correctness | Output/crashes, invariants, races, errors, resources | `checklist.md` |
| 2. Security | Actual injection/deserialization/secrets/TLS/path exposure | `checklist.md` |
| 3. Design | Boundaries, API/import coupling, abstractions, migrations, config/errors, test seams | `checklist.md` |
| 4. Async | Task lifetime, blocking, cancellation, TaskGroup/gather, timeout/wait_for | `async-correctness.md` |
| 5. Types | Public signatures, Any, Protocol/generics, override, ignores | `checklist.md` |
| 6. Modernization | Supported-version gains, deprecations, Pydantic v1 remnants | `modern-idioms.md` |
| 7. Performance | Visible complexity/waste, sync IO on async paths | `checklist.md` |
| 8. Polish | Names, log levels, actionable errors, dead code beyond linters | `checklist.md` |

## Calibration

- Internal tool/script: bugs, security, async, basic modernization; skip `__all__`, `py.typed` and public API.
- PyPI library: full public API, hints and semver bar.
- Service/app: architecture, config and async; public API is not the focus.
- Tutorial/example: light review, identify production differences.
- If unsure, ask which project type/production bar to use.

Three substantive findings beat many nitpicks. Unchosen style is outside scope; preference is Suggestion at
most, a clear error at least Major. Missing call-site context is a valid finding.
For thousands of files, map layout/API, select 3–5 central modules, explain selection and sampled scope, and
count recurring patterns.

## Report

- Verdict (2–4 sentences): health, main concerns and modernization tier.
- Context: layout, Python target or `unspecified`, tooling (none/basic ruff/strict), build and 3–5 shaping
  dependencies.
- Findings grouped by tiers 1–8, Critical → Major → Minor → Suggestion; include axis and its rule/intent
  citation.
- Below strict tooling: concrete `pyproject.toml` recommendations, not bare rule names.
- 2–5 specific good decisions when code is decent; prioritized first/next/later actions.

Done when every tier is covered or explicitly skipped under the time-box rule, and every finding cites a read
line.
