# Directions — art directions that read as intentional

Present three of these, adapted to the brief. Never present a direction without its cost.

## The banned defaults

These are what an unguided model converges on. They are not ugly; they are *the average*, which is why they read as machine-made.

**Typography** — Inter, Roboto, Arial, system-ui as the headline face. Also the second-order trap: once Inter is banned, models converge on Space Grotesk. Ban the new default too.

**Colour** — purple or indigo gradient on white. Evenly distributed palettes where nothing dominates.

**Layout** — three or four cards in a row as the answer to every problem. Cards nested inside cards. All-caps kickers above every heading. Decorative icons that carry no information. A light/dark toggle nobody asked for.

**Depth** — flat everything, or drop shadows on every surface at the same elevation.

**Motion** — none at all, or a fade-in on every element.

## The catalogue

### 1. Editorial

**Thesis.** The type does the work; almost nothing else is allowed to.

Reference: Stripe docs, Vercel's writing surfaces, Basecamp.

Type-led with a real serif or a distinctive grotesk, one accent colour used sparingly, generous whitespace, depth expressed through spacing rather than shadow, motion limited to page transitions. Body measure capped near 65ch.

**Bad at** — dense data. A table with 14 columns kills it.

### 2. Dense technical

**Thesis.** Information-dense, monospaced, zero ornament. Speed is the aesthetic.

Reference: Linear, Vercel dashboard, Raycast.

Tight radii or none at all, monospace for numerals and identifiers, `tabular-nums` everywhere numbers align, one accent for state, depth by hairline borders rather than shadow, motion under 150 ms and functional only.

**Bad at** — anything consumer-facing or emotional. Reads as a tool, never as a product someone loves.

Source: `@termcn`, `SMUI`, Base UI primitives.

### 3. Soft depth (hybrid neumorphism)

**Thesis.** Physical surfaces and tactile controls, without the accessibility disaster of real neumorphism.

Reference: iOS control centre, Apple Home, hi-fi and instrument UIs.

**Read this before proposing it.** Classic neumorphism gives elements the same colour as the background and defines them with two shadows only. That is a structural WCAG failure: text lands under the 4.5:1 minimum, non-text UI under the 3:1 minimum, buttons are indistinguishable from static surfaces, and focus rings vanish into the glow. No amount of polish fixes it, because the look *depends* on low contrast.

The 2026 way to keep the mood without the failure:

- Soft shadows for **surfaces only** — never as the sole boundary of an interactive element
- Every control also carries a visible border or an accent fill
- Text contrast pushed to **7:1**, not the 4.5:1 floor
- Focus = a visible ring or border, never a soft glow
- Reserve it for **low-density, single-purpose screens**: a player, a calculator, a thermostat, a settings panel. Never a data-dense dashboard.

**Bad at** — density, text-heavy screens, anything a stranger must learn fast. Also expensive to build correctly.

### 4. Atmospheric

**Thesis.** A generated background does the emotional work; the foreground stays quiet.

Reference: Linear's marketing site, Paper, modern AI product landing pages.

Layered gradients, mesh, grain, dither or a shader as the background layer. Foreground restrained to two type sizes and one accent. Motion is ambient and slow, or driven by scroll.

**Bad at** — battery and bundle. One hero surface, not six. Also ages fast; it will date.

Source: Paper Shaders, Canvas UI, `@motion-menu` — see `ui-sources/reference/craft.md`.

### 5. High contrast / brutal

**Thesis.** Hard edges, extreme type weights, colour that commits.

Reference: Gumroad, Figma's marketing, indie tools.

Weight extremes (100/200 against 800/900), 3x+ size jumps between levels, one dominant colour with a sharp accent rather than a timid spread, borders that are actually visible, motion snappy and slightly overshooting.

**Bad at** — long-form reading, enterprise contexts, anything that must feel calm.

Source: `@retroui`, `@8bitcn` for the extreme end.

### 6. Warm print

**Thesis.** Paper, ink and restraint. The opposite of a SaaS template.

Reference: independent magazines, Readwise, Craft.

Off-white or cream surfaces rather than pure white, a text serif, muted ink colours, illustration or texture over icons, motion nearly absent.

**Bad at** — dashboards, real-time data, anything that must feel fast.

## Making any of them not read as a pastiche

- **Commit to one dominant colour.** An evenly distributed palette is the visual signature of indecision.
- **Use three type sizes.** Not seven. The hierarchy comes from the jumps being large.
- **Pick one place to be expensive** — a background, a chart, one transition — and make everything else cheap and quiet.
- **Delete after the first pass.** "A lot of design is deleting." The first version always has too much.
- **State the reference explicitly in `DESIGN.md`**, including what you are *not* taking from it.
