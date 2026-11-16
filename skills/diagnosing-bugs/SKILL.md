---
name: diagnosing-bugs
description: "Diagnose code bugs, crashes, failing tests or performance regressions (\"ça marche pas\", \"c’est lent\") and fix rounds; a live service incident where code is not suspected starts with operations, not here."
---

# Diagnosing bugs

Follow phases in order; justify any skip explicitly. Read repo AGENTS.md and `docs/decisions.md` for the
affected modules and decisions.

## Evidence hygiene

Redact secrets as `<REDACTED>` before showing commands, output or artifacts. Credentials stay in environment
variables; quote only relevant artifact lines because captures may contain auth headers. If redaction removes
necessary evidence, explain and ask the user.

## 1. Build a tight, red-capable loop

Spend the effort here before forming a theory. Find a rerunnable pass/fail signal for the user's exact
symptom, not merely "no crash". Prefer, in order:

1. Failing unit/integration/E2E test, through the repo's own test conventions and harness when it has them.
2. Curl/HTTP script against dev.
3. CLI fixture with stdout diff against a known-good snapshot.
4. Headless Playwright/Puppeteer DOM/console/network assertion.
5. Captured request/payload/event replay through the path in isolation.
6. Throwaway minimal service harness with mocked dependencies.
7. Property/fuzz loop (for example 1000 inputs).
8. Automated known-state bisection (`git bisect run`).
9. Differential old/new version or config outputs.
10. Structured human loop as last resort: numbered steps, exact values to report, one hypothesis per round.

Tighten setup/scope, assert the specific symptom, and control time, RNG, filesystem and network. Aim for
seconds; server boot gates are the accepted exception. For nondeterminism raise and pin reproduction rate
(100× trigger, stress, parallelism, timing windows/sleeps) until debuggable; a 1% rate is inadequate.

**Gate:** name one already-run command and show redacted invocation/output. It must reach the real bug path,
catch the exact symptom, be deterministic (or have a pinned high repro rate), fast, and unattended except for
a structured human loop. No such command means no phase 2; code reading to construct the loop is not a license
to theorize.

If no loop can be built, stop, list attempts and request missing environment access, a redacted
HAR/log/core/timestamped recording, or permission for temporary production instrumentation. Do not hypothesize
without the loop.

## 2. Reproduce and minimize

Observe the user's failure, repeatedly or at a high enough rate, and capture its exact error/output/timing.
Remove inputs, callers, config, data and steps one at a time, rerunning after each cut. Finish only when each
remaining element is load-bearing: removing any makes the loop green.

## 3. Rank hypotheses

Write 3–5 before testing any, each with a falsifiable prediction: "If X causes this, changing Y
removes/worsens it." Discard or sharpen unfalsifiable claims. Show the ranked list to the user before testing;
continue with your ranking if they are absent.

## 4. Instrument

Map each probe to one prediction; change one variable. Prefer debugger/REPL, then targeted boundary logs. Give
every debug log a unique prefix such as `[DEBUG-a4f2]` so cleanup is searchable.

For performance, read `references/performance.md` before trusting, reporting or acting on any
baseline/speedup/regression number; logs alone are usually insufficient.

## 5. Fix at the correct seam

Before the fix, convert the minimal repro into a regression test only where it exercises the real call-site
pattern (including multiple callers or the triggering chain). A shallow test is false confidence. If no
correct seam exists, report that architectural finding.

1. Run the regression test red. If red was forced by code/fixture mutation, diff a pristine copy to prove the
   mutation landed.
2. Apply the fix and run it green.
3. Replay the original, unminimized phase 1 scenario.

**After two fixes sharing a premise fail the same loop**, write that premise and test it directly before a
third. Use a rerunnable observation that differs if it is false; inspect failure distribution across
inputs/threads/platforms/runs. If contradicted, return to phase 3 with what the failures share; if confirmed,
ask the next why because fixes treated a consequence. Remove the causing condition rather than compensating
for it. No further fix until the premise is written and tested.

## 6. Finish

- Original loop no longer reproduces.
- Regression passes, or missing correct seam is documented.
- Search confirms all uniquely prefixed debug instrumentation removed.
- Throwaway prototypes deleted or moved to an explicitly marked debug location.
- Commit/PR states the confirmed cause for the next debugger.
