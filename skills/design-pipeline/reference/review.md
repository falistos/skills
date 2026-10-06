# Review — the exit passes

Run in order, then fix everything in **one batch**: build fully, inspect once, fix once, confirm once, stop.

## Pass 1 — Direction

Read `DESIGN.md` and answer in writing:

- Does the build match the locked direction, or drifted toward the average?
- Is anything from "Banned here" present?
- Is the reference still recognisable in the parts we said we'd take?

Look for drift specifically: a system font that crept in, a reappeared card grid, a second accent.

## Pass 2 — Density

Load `density.md` and run the deletion pass. It is mechanical, needs no taste, and improves a generated interface most.

## Pass 3 — Checklist

Invoke **`web-design-guidelines`**: 100+ concrete rules (focus handling, form semantics, `tabular-nums`, tap targets, `prefers-reduced-motion`, hover gating on touch, text-size adjust, contrast). Take its output as a defect list.

## Pass 4 — Motion

If anything animates, invoke **`review-animations`**. Rules it holds you to:

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

Hard ceiling under 300 ms. Exits about 20% faster than entrances. Larger elements move slower; duration scales with distance.

Common defects: starting from `scale(0)` (start near 0.8 so it reads as physical); missing `will-change: transform` on jittery elements; animating the parent on hover instead of the child (flicker); `transform-origin` not set to the trigger on popovers.

## Pass 5 — Cleanup

Invoke **`baseline-ui`** for spacing, hierarchy and typography.

## Pass 6 — See it

Passes 1–5 read code. Look at the render:

- **Paper** (`paper-desktop`) if running
- Otherwise screenshot the running app, desktop and mobile in one batch

Look for what no checklist catches: alignment off by a few pixels, a rhythm that breaks halfway down, an element louder than its importance, text that wraps badly at a real width.

## Stop condition

One inspection round, one fix batch, at most one confirmation round. Open-ended self-QA costs more than it improves and sands the character off a design that was working.
