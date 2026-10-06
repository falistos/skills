# Comps — making the three directions visible

## Rules

- **Same screen, three times**: identical content and information, three treatments.
- **Real copy**: the actual feature names, numbers and labels from the brief. Real text sitting in a treatment is half of what makes a direction feel right or wrong.
- **One screen**, the most important one.
- **Static**: no framework, build step or dependency. Hover states at most.
- **Genuinely different**: if the three comps could be swapped unnoticed, start over. Three grey card grids with different accents are one direction.
- **Under ten minutes each**: disposable, the build comes after the choice.

## The default: one HTML file

Three full-viewport sections in one self-contained file, each with a fixed label showing the direction name, inline CSS, no assets that must exist:

```
comps.html
├── section  A — <direction name>
├── section  B — <direction name>
└── section  C — <direction name>
```

Open it in the browser. Keep it in the scratchpad or at the project root as `comps.html`, uncommitted.

Load fonts from Google Fonts or Fontshare: type is the biggest carrier of direction, and a comp with the wrong font tests nothing.

## What each comp shows

- The primary action at its actual visual weight
- Real hierarchy (heading, body, secondary text) at the direction's actual sizes
- One instance of the dominant surface treatment (card, panel, bare…)
- The accent doing its job at least once
- The screen's dense part (list, table, form): directions break there. A hero looks good in every direction, a fourteen-column table does not.

Leave out nav chrome that isn't being decided, footers, settings, empty states.

## Captions

Under or beside each comp:

```
A — <Name>
<one-line thesis>
Like: <product> — <url>
Bad at: <the honest cost>
```

## After the choice

Delete the comps or leave them in the scratchpad. Carry the choice into `DESIGN.md`, including remarks made while choosing ("I like B but the accent is too loud").
