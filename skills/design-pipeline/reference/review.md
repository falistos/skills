# Review — the exit passes

Run these after the build, in this order, then fix everything in **one batch**. Do not loop: build fully, inspect once, fix once, confirm once, stop.

## Pass 1 — Direction

Read `DESIGN.md` and answer honestly, in writing:

- Does the build match the direction that was locked, or did it drift back toward the average?
- Is anything from the "Banned here" list present?
- Is the reference product still recognisable in the result — the parts we said we'd take?

Drift back toward the default is the expected failure. Look for it specifically: a system font that crept in, a card grid that reappeared, a second accent colour.

## Pass 2 — Density

Load `density.md` and run the deletion pass. This is the one that most improves a generated interface, and it is mechanical — it needs no taste, only the checklist.

## Pass 3 — Checklist

Invoke **`web-design-guidelines`**. It reviews the code against 100+ concrete rules: focus handling, form semantics, `tabular-nums`, tap targets, `prefers-reduced-motion`, hover gating on touch, text-size adjust, contrast. None of it requires judgement, all of it requires checking.

It reviews; it does not design. Take its output as a defect list.

## Pass 4 — Motion

If anything animates, invoke **`review-animations`**. It flags by default and approval is earned.

The rules it holds you to, worth knowing without loading it:

| Case | Easing |
|---|---|
| Entering / exiting | `ease-out` |
| Moving or morphing on screen | `ease-in-out` |
| Hover | `ease` |
| Constant motion | `linear` |

| Kind | Duration |
|---|---|
| Micro-interactions | 100–150 ms |
| Standard UI | 150–250 ms |
| Modals, drawers | 200–300 ms |

Hard ceiling under 300 ms. Exits run about 20% faster than entrances. Larger elements move slower; duration scales with distance travelled.

Common defects: starting from `scale(0)` — elements should start around 0.8 so they read as physical, not as materialising from nothing; missing `will-change: transform` on jittery elements; animating the parent on hover instead of the child, which causes flicker; `transform-origin` not set to the trigger on popovers.

## Pass 5 — Cleanup

Invoke **`baseline-ui`** for a mechanical pass on spacing, hierarchy and typography.

## Pass 6 — See it

Everything above reads code. None of it sees the rendered result.

- **Paper** (`paper-desktop`) if it is running — this is the visual loop
- Otherwise screenshot the running app and look at it: desktop and mobile in one batch

Look for what no checklist catches: alignment that is off by a few pixels, a rhythm that breaks halfway down, one element that is visually louder than its importance, text that wraps badly at a real width.

## Stop condition

One inspection round, one batch of fixes, at most one confirmation round. Then stop. Open-ended self-QA costs more than it improves and tends to sand the character off a design that was working.
