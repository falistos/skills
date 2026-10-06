# Density — the discipline against overloaded interfaces

Generated UI is overloaded by default: the model has no cost function for attention, so it answers every requirement with another visible element. The result reads busy and undecided even when each element is fine. Treat this as a budget, applied unasked.

## The budget, per screen

- **One primary action**: exactly one thing is brightest, largest or most saturated. Two competing means the screen has no answer to "what do I do here".
- **Three type sizes in use**, with large jumps between them.
- **One accent colour.** State colours (error, success) are rare exceptions, not accents.
- **One elevation level for content.** Cards inside cards inside panels is the most common generated-UI failure.
- **Icons carry information or go.** An icon repeating its label is noise.
- **Empty space is a decision.** A region with nothing to say stays empty, not filled with an unrequested stat.

## The deletion pass — every time

After the first build, before any review, remove:

- Every card wrapping a single value (a number with a border)
- Every kicker, the small all-caps label above a heading
- Every decorative icon
- Every count, badge or metadata line the user did not ask for
- Every divider between things already separated by space
- Every gradient that is not the one deliberate expensive thing
- The light/dark toggle, unless required

Per element ask **what breaks if this disappears?** "Nothing" means it goes. Expect to cut 20–30% of the first version.

## Progressive disclosure

When everything must be reachable, reachable is not visible:

- Secondary actions in a menu, not the toolbar
- Detail one click down, not in an always-open sidebar
- Advanced settings behind a disclosure
- Rare states (error, empty, loading) designed but not simultaneously present

## Density by direction

| Direction | Density |
|---|---|
| Editorial, Warm print, Soft depth | **Low.** Few, large elements. Soft depth *requires* it to stay legible |
| Atmospheric | **Low foreground**, rich background: the expense is behind |
| High contrast | **Medium.** Fewer but louder elements |
| Dense technical | **High — only here.** Compensate with hairline borders, `tabular-nums`, tight consistent rhythm, zero ornament |

Everywhere but Dense technical, busy means unfinished.

## Signals of overload

- One sentence cannot say what the screen is for
- More than one element fights to be looked at first
- Explaining the layout takes longer than using it
- Removing a random element improves it
- Fine as a screenshot, exhausting to use
