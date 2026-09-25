# Density — the discipline against overloaded interfaces

Generated UI is overloaded by default. The model has no cost function for attention, so it answers every requirement with another visible element: another card, another badge, another icon, another toggle. Nothing is ever *not* shown. The result reads as busy and undecided even when every individual element is fine.

This is a budget, not a taste question. Apply it whether or not anyone asked.

## The budget, per screen

- **One primary action.** Exactly one thing is the brightest, largest or most saturated. Everything else is quieter. If two things compete, the screen has no answer to "what do I do here".
- **Three type sizes in use.** Not seven. Hierarchy comes from large jumps between few sizes.
- **One accent colour.** State colours (error, success) are not accents; they are exceptions and appear rarely.
- **One elevation level for content.** Cards inside cards inside panels is the single most common generated-UI failure.
- **Icons carry information or they go.** An icon next to a label that repeats the label is noise.
- **Empty space is a decision.** If a region has nothing to say, leave it empty rather than filling it with a stat nobody asked for.

## The deletion pass — run it every time

After the first build, before any review, go through the screen and remove:

- Every card that wraps a single value. It is a number with a border.
- Every "kicker" — the small all-caps label above a heading. The heading is the label.
- Every decorative icon.
- Every count, badge or metadata line the user did not ask for.
- Every divider that separates things already separated by space.
- Every gradient that is not the one deliberate expensive thing.
- The light/dark toggle, unless it was a requirement.

Ask, per element: **what breaks if this disappears?** If the answer is "nothing", it goes. Expect to cut 20–30% of the first version. That is normal, not a failure of the first pass.

## Progressive disclosure

When a requirement genuinely needs everything to be reachable, reachable is not the same as visible:

- Secondary actions live in a menu, not in the toolbar
- Detail lives one click down, not in a sidebar that is always open
- Advanced settings live behind a disclosure, not in the main form
- Rare states (errors, empty, loading) are designed but not simultaneously present

## Density by direction

The budget is not uniform. Read it against the chosen direction:

| Direction | Density |
|---|---|
| Editorial, Warm print, Soft depth | **Low.** Few elements, large. Soft depth *requires* low density to remain legible |
| Atmospheric | **Low foreground**, rich background. The expense is behind, not in front |
| High contrast | **Medium.** Fewer elements but louder ones |
| Dense technical | **High — and only here.** Density is the point; compensate with hairline borders, `tabular-nums`, tight consistent rhythm, and zero ornament |

Dense technical is the only direction where a busy screen is correct. Everywhere else, busy means unfinished.

## Signals that a screen is overloaded

- You cannot say in one sentence what the screen is for
- More than one element is fighting to be looked at first
- Explaining the layout takes longer than using it
- Removing a random element improves it
- It looks fine as a screenshot and is exhausting to actually use
