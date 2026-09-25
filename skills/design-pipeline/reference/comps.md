# Comps — making the three directions visible

The output of Phase 2 is something to look at. This file is how to produce it fast.

## Rules

- **Same screen, three times.** Identical content, identical information, three treatments. Different screens cannot be compared.
- **Real copy.** Never lorem ipsum, never "Card Title". Use the actual words from the brief — real feature names, real numbers, real labels. Half of what makes a direction feel right or wrong is how real text sits in it.
- **One screen only.** The most important one. Not a flow, not a set.
- **Static.** No framework, no build step, no dependencies. Hover states at most.
- **Make them genuinely different.** Three variations of the same grey card grid with different accent colours is not three directions. If the three comps could be swapped without anyone noticing, start over.
- **Under ten minutes each.** These are disposable. The build happens after the choice.

## The default: one HTML file

Three full-viewport sections in a single self-contained file, each with a fixed label showing the direction name. Inline CSS, system-fetched fonts, no assets that need to exist.

```
comps.html
├── section  A — <direction name>
├── section  B — <direction name>
└── section  C — <direction name>
```

Open it in the browser and let the user scroll between the three. Keep it in the scratchpad or at the project root as `comps.html` — it is throwaway; do not commit it.

For fonts, use Google Fonts or Fontshare links so the type is actually the type. Type is the single biggest carrier of direction — a comp with the wrong font tests nothing.

## What each comp must show

Enough for a direction to be judgeable, no more:

- The primary action, in its actual visual weight
- Real hierarchy: heading, body, secondary text — at the direction's actual sizes
- One instance of the dominant surface treatment (card, panel, bare, whatever the direction says)
- The accent colour doing its job at least once
- Whatever the screen's dense part is — a list, a table, a form — because that is where directions break

Leave out: nav chrome that isn't being decided, footers, settings, empty states.

## Where each direction breaks

Test the direction on the hardest part of the screen, not the easiest. A hero looks good in every direction; a fourteen-column table does not. If the brief's screen has a dense region, put it in the comp — that is the whole point of comping before building.

## Captions

Under or beside each comp:

```
A — <Name>
<one-line thesis>
Like: <product> — <url>
Bad at: <the honest cost>
```

## After the choice

Delete the comps or leave them in the scratchpad. Carry the chosen direction into `DESIGN.md` in Phase 3 — including anything the user said while choosing ("I like B but the accent is too loud"), because that is direction information and it will be lost otherwise.
