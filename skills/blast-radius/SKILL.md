---
name: blast-radius
description: "Check a small diff before merge: \"blast radius\", \"qu'est-ce que ça peut casser\", \"what could this break\", or a small change you do not trust; not a lot review."
---

# Blast radius

Prove the fact that makes the change safe, including breakage a caller search cannot reveal. A full review of a
change belongs to the project's review procedure.

## Evidence ladder

1. **Asserted**: insufficient alone.
2. **Cited**: `file:line` or dependency source at the pinned version.
3. **Walked**: failure path traced and ruled out.
4. **Executed**: real-code script/test fails loudly if the fact is false.
5. **Reproduced**: boot gate, dev server or real CLI.

Push each safety claim as far down the ladder as cheap; state where it stopped.

## Steps

1. Read the diff, all changed/added/deleted symbols and implicit changes (defaults, order, timing). Read the
   PR and history (`gh pr view`, `git log -L`) for intent. Finish with one sentence naming the behavior
   change.
2. Name the **keystone**: the single fact that clears most risks if true. Focus proof effort there.
3. Check beyond callers:
   - Code named in text: manifest commands/permissions, YAML config/message keys, reflection, service lookups,
     other plugins' listeners.
   - Stored/wire formats: columns/migrations, PDC/NBT, JSON, consumers in another language.
   - Other repos' public API/event consumers: `gh search code --owner <org> <symbol>`.
   - Timing: main/async, Folia region/global, enable/disable/reload, `depend`/`softdepend`.
   - Dependency source at the pinned version, including shaded/relocated copies.
   Finish when every category has an affected or checked citation; quote commands for empty searches.
4. Rate each confirmed risk: failure mechanism, `file:line`, likelihood and cost; separate cleared risks.
5. Prove the keystone at rung 4 or 5 with a real-code script, JShell, test or gate scenario; retain output.
6. For a wide change, obtain another model family's independent analysis through the project's
   delegation procedure, then reconcile it.

## Reply

State what changed, keystone and rung, proof command/output (or `unproven`), risks with checks, and cleared
paths with reasons. Supply the cheapest pre-merge repro/test as a written script.
