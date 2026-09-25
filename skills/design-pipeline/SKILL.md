---
name: design-pipeline
description: Run a UI design from intent to reviewed build. Use when the user wants to design or redesign an interface, app, page or screen and has only a rough idea — "je veux designer une app de X", "propose-moi des directions", "design me a dashboard", "refais cette page", "j'ai besoin d'une UI pour". Presents named art directions to choose from rather than guessing, locks the choice into a DESIGN.md, then builds and reviews against it. Covers web, desktop and mobile surfaces. Not for reviewing an existing UI without designing anything — that is `web-design-guidelines`.
user-invocable: true
argument-hint: "[what you're designing — e.g. 'a dashboard for X', 'landing page', or nothing at all]"
---

# Design Pipeline

The user does not have to arrive with a visual idea. The pipeline's job is to produce one, show it, and let them choose — then hold that choice for the rest of the build.

Two constraints stand for every phase, without being asked:

- **No slop.** See the banned defaults in `reference/directions.md`. Sameness is the failure mode, not ugliness.
- **No overload.** See `reference/density.md`. An interface that says everything says nothing.

## Phase 1 — Brief

Ask at most six questions, in one message, and offer a default for each so the user can answer "va comme tu veux" to any of them:

1. What is it and who uses it? (one sentence)
2. The one thing a user must be able to do on the main screen
3. Surface: web / desktop / mobile / native
4. Stack, if it already exists — check `package.json` before asking
5. Any product whose look they'd point at and say "like that"
6. Anything forbidden — existing brand, palette, an aesthetic they hate

If the user says "surprise me", skip straight to Phase 2 and infer from the domain.

**Never start building at the end of Phase 1.** A brief is not a direction.

## Phase 2 — Directions, shown not described

Three named directions, never one. **Always produce something to look at.** A written description of a direction is unjudgeable by anyone who is not already a designer — and the person asking usually isn't, which is why they asked.

**Build the comps first, then write the text.** Pick the single most important screen from the brief and render *the same screen, with the same real content*, three times. Comparing identical content across three treatments is what makes the choice possible; three different screens are not comparable.

Route by what is available, in this order:

1. **Paper** (`paper-desktop`) if it is running — comps on the canvas, iterate there.
2. **The `design` skill** — a multi-artboard canvas Artifact, one artboard per direction, pan and zoom to compare. Best when there is no project to build in yet.
3. **A single self-contained HTML file** — three sections, one per direction, same screen each time, opened in the browser. No dependencies, no build step, fastest path. Use this as the default when in doubt.

Keep comps cheap: static, one screen, real copy, no interactivity beyond hover. They are for choosing a direction, not for shipping.

Alongside the comps, give each direction a short caption:

- Name and one-line thesis
- A reference product **with its URL**, so the real thing can be looked at
- **What it is bad at** — every direction costs something, say what

Load `reference/comps.md` for how to build them and `reference/directions.md` for the catalogue and the rules that keep each one from reading as pastiche.

Then ask: pick one, or remix — "the type of A with the depth of C" is a valid and common answer. Offer three more if none land, and say what you changed about the search.

## Phase 3 — Lock

Write `DESIGN.md` at the project root, derived from the chosen direction, not invented:

```markdown
# Design
Direction: <name> — <one-line thesis>
Reference: <product> — what we take from it, what we don't

## Tokens
Type: <families, scale, the 3 sizes in use>
Colour: <surface, text, one accent — with contrast ratios>
Depth: <how elevation is expressed>
Radius / spacing: <scale>

## Motion
<easing rules and duration bands — see review.md>

## Density budget
<from density.md, filled in for this surface>

## Banned here
<the specific things this project must never do>
```

Add one line to `CLAUDE.md` or `AGENTS.md`: `Always read DESIGN.md before touching UI.`

This file is the memory that skills do not have. Without it, direction resets every session.

## Phase 4 — Build

Route by surface:

- **Canvas exploration** — Paper (`paper-desktop`) if running; it is the visual loop. Iterate shapes there before committing to code.
- **Code** — build against `DESIGN.md`. Source components through the `ui-sources` skill; use `pick-ui-library` for the canonical React library per task.
- **Static artefact or mock** — the `design` skill's canvas.

Build the main screen **fully** before starting a second one. A half-finished set of screens cannot be judged.

## Phase 5 — Review

Never ship the build straight out of Phase 4. Load `reference/review.md` and run the passes it lists — a checklist pass, a density pass, a motion pass — then fix in one batch.
