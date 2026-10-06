# Directions — art directions that read as intentional

Present three, adapted to the brief, each with its cost.

## The banned defaults

What an unguided model converges on. Not ugly: *average*, which reads as machine-made.

**Typography** — Inter, Roboto, Arial, system-ui as the headline face. Second-order trap: with Inter banned, models converge on Space Grotesk. Ban that too.

**Colour** — purple or indigo gradient on white; evenly distributed palettes where nothing dominates.

**Layout** — three or four cards in a row as the answer to everything; nested cards; all-caps kickers above every heading; decorative icons; an unrequested light/dark toggle.

**Depth** — flat everything, or drop shadows on every surface at the same elevation.

**Motion** — none, or a fade-in on every element.

## The catalogue

### 1. Editorial

**Thesis.** The type does the work; almost nothing else is allowed to.

Reference: Stripe docs, Vercel's writing surfaces, Basecamp.

Type-led with a real serif or distinctive grotesk, one sparing accent, generous whitespace, depth through spacing not shadow, motion limited to page transitions. Body measure capped near 65ch.

**Bad at** — dense data. A 14-column table kills it.

### 2. Dense technical

**Thesis.** Information-dense, monospaced, zero ornament. Speed is the aesthetic.

Reference: Linear, Vercel dashboard, Raycast.

Tight or no radii, monospace for numerals and identifiers, `tabular-nums` wherever numbers align, one accent for state, depth by hairline borders, motion under 150 ms and functional only.

**Bad at** — consumer-facing or emotional products. Reads as a tool, never as a product someone loves.

Source: `@termcn`, `SMUI`, Base UI primitives.

### 3. Soft depth (hybrid neumorphism)

**Thesis.** Physical surfaces and tactile controls, without real neumorphism's accessibility disaster.

Reference: iOS control centre, Apple Home, hi-fi and instrument UIs.

**Read before proposing.** Classic neumorphism gives elements the background colour and defines them with two shadows only. That is a structural WCAG failure: text under the 4.5:1 minimum, non-text UI under 3:1, buttons indistinguishable from static surfaces, focus rings vanishing into the glow. Polish cannot fix it, because the look *depends* on low contrast.

The 2026 way to keep the mood:

- Soft shadows for **surfaces only**, never the sole boundary of an interactive element
- Every control also has a visible border or accent fill
- Text contrast **7:1**, not the 4.5:1 floor
- Focus is a visible ring or border, never a soft glow
- Reserve for **low-density, single-purpose screens** (player, calculator, thermostat, settings panel), never a data-dense dashboard

**Bad at** — density, text-heavy screens, anything a stranger must learn fast. Expensive to build correctly.

### 4. Atmospheric

**Thesis.** A generated background does the emotional work; the foreground stays quiet.

Reference: Linear's marketing site, Paper, modern AI product landing pages.

Layered gradients, mesh, grain, dither or a shader as background. Foreground restrained to two type sizes and one accent. Motion ambient and slow, or scroll-driven.

**Bad at** — battery and bundle (one hero surface, not six); ages fast.

Source: Paper Shaders, Canvas UI, `@motion-menu` — see `ui-sources/reference/craft.md`.

### 5. High contrast / brutal

**Thesis.** Hard edges, extreme type weights, colour that commits.

Reference: Gumroad, Figma's marketing, indie tools.

Weight extremes (100/200 against 800/900), 3x+ size jumps between levels, one dominant colour with a sharp accent, visible borders, snappy motion with slight overshoot.

**Bad at** — long-form reading, enterprise contexts, anything that must feel calm.

Source: `@retroui`, `@8bitcn` for the extreme end.

### 6. Warm print

**Thesis.** Paper, ink and restraint. The opposite of a SaaS template.

Reference: independent magazines, Readwise, Craft.

Off-white or cream surfaces, a text serif, muted ink colours, illustration or texture over icons, motion nearly absent.

**Bad at** — dashboards, real-time data, anything that must feel fast.

## Avoiding pastiche

- **One dominant colour.** An evenly distributed palette is the signature of indecision.
- **Three type sizes**, large jumps.
- **One place to be expensive** (a background, a chart, one transition); everything else cheap and quiet.
- **Delete after the first pass.** "A lot of design is deleting."
- **State the reference in `DESIGN.md`**, including what you are *not* taking from it.
