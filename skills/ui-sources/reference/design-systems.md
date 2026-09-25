# Design systems — what to study and what to copy

Use these when the question is *how should this be structured*, not *where is the button*. A design system answers naming, token layering, state coverage and documentation — the parts that decide whether a UI stays coherent past week three.

## Galleries of real systems

- **[The Component Gallery](https://component.gallery)** — indexes the same component across many design systems so you can compare anatomy. The most useful of the three when you have a specific decision to make: how does everyone else handle a destructive confirm, a multi-select, a toast.
- **[Design Systems Surf](https://designsystems.surf)** — best-in-class systems from large product teams, plus 40+ public Figma files. Recent additions include Meta's Astryx.
- **[DesignSystems.one](https://www.designsystems.one/design-systems)** — 88 real systems with screenshots and token breakdowns (Polaris, Carbon, Material, Primer, shadcn).
- **[The Design System Guide](https://thedesignsystem.guide/public-design-systems-list)** — list of public systems and their documentation platforms.
- **[Figma Community open design systems](https://www.designsystems.com/open-design-systems/)** — downloadable files.

## Systems worth reading in full

Each is strong at a different thing:

| System | Read it for |
|---|---|
| **GOV.UK Design System** | Writing about components — the "when not to use this" sections are the gold standard |
| **Adobe Spectrum** | Token architecture and multi-platform scaling |
| **IBM Carbon** | Grid, motion specification, exhaustive state coverage |
| **Shopify Polaris** | UX copy guidance sitting next to each component |
| **GitHub Primer** | Living inside a real, messy, long-lived product |
| **Atlassian Design System** | Accessibility documentation depth |

## Systems as installable code

- **`Better Design`** (registry.directory) — 85 complete design systems in one registry, each shipping the same 200+ components. The fastest way to try a whole visual language rather than one component.
- **[ds.shadcn.com](https://ds.shadcn.com)** — shadcn's own under-promoted system, aimed at building design *tools* (Framer/Canva-class: canvases, panels, inspectors). Different problem from shadcn/ui.
- **`@usva`** — one React design language shipped in three moods: atmospheric, dense, light.
- **`@zyeon`** — 353 components, each with live preview and full source.

## Token architecture

Three layers, in this order. Skipping the middle one is the usual mistake:

1. **Primitive** — raw values. `blue-500`, `space-4`. No meaning attached.
2. **Semantic** — intent. `color-danger`, `surface-raised`, `space-inline-sm`. This is the layer components consume.
3. **Component** — local overrides only where a component genuinely deviates. `button-radius`.

Components referencing primitives directly is what makes rebranding and dark mode painful later.

For implementation: **Open Props** if there is no Tailwind, Tailwind v4's `@theme` if there is, and **Radix Colors** for the colour scales in either case. **[Utopia](https://utopia.fyi)** for the type and space scales.

## Before adopting any third-party system or registry

Check, in this order: installation actually works with your CLI; GitHub activity in the last quarter; TypeScript strictness; accessibility claims backed by APG patterns; React Server Component boundaries; and the bundle cost of its animation dependency. Measure with a real build — a registry that pulls Framer Motion or GSAP into every component is a decision, not a detail.
