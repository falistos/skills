# Design systems — what to study and what to copy

For the question *how should this be structured*: naming, token layering, state coverage and documentation decide whether a UI stays coherent past week three.

## Galleries of real systems

- **[The Component Gallery](https://component.gallery)** — the same component across many systems, to compare anatomy. The most useful for a specific decision: how everyone handles a destructive confirm, a multi-select, a toast.
- **[Design Systems Surf](https://designsystems.surf)** — best-in-class systems from large product teams, plus 40+ public Figma files. Recent additions include Meta's Astryx.
- **[DesignSystems.one](https://www.designsystems.one/design-systems)** — 88 real systems with screenshots and token breakdowns (Polaris, Carbon, Material, Primer, shadcn).
- **[The Design System Guide](https://thedesignsystem.guide/public-design-systems-list)** — public systems and their documentation platforms.
- **[Figma Community open design systems](https://www.designsystems.com/open-design-systems/)** — downloadable files.

## Systems worth reading in full

| System | Read it for |
|---|---|
| **GOV.UK Design System** | Writing about components: the "when not to use this" sections are the gold standard |
| **Adobe Spectrum** | Token architecture and multi-platform scaling |
| **IBM Carbon** | Grid, motion specification, exhaustive state coverage |
| **Shopify Polaris** | UX copy guidance beside each component |
| **GitHub Primer** | Living inside a real, messy, long-lived product |
| **Atlassian Design System** | Accessibility documentation depth |

## Systems as installable code

- **`Better Design`** (registry.directory) — 85 complete design systems in one registry, each shipping the same 200+ components. The fastest way to try a whole visual language.
- **[ds.shadcn.com](https://ds.shadcn.com)** — shadcn's own under-promoted system for building design *tools* (Framer/Canva-class: canvases, panels, inspectors), a different problem from shadcn/ui.
- **`@usva`** — one React design language in three moods: atmospheric, dense, light.
- **`@zyeon`** — 353 components, each with live preview and full source.

## Token architecture

Three layers, in order. Skipping the middle one is the usual mistake:

1. **Primitive** — raw values, no meaning: `blue-500`, `space-4`.
2. **Semantic** — intent: `color-danger`, `surface-raised`, `space-inline-sm`. Components consume this layer.
3. **Component** — local overrides only where a component genuinely deviates: `button-radius`.

Components referencing primitives directly make rebranding and dark mode painful.

Implementation: **Open Props** without Tailwind, Tailwind v4's `@theme` with it, **Radix Colors** for colour scales in either case, **[Utopia](https://utopia.fyi)** for type and space scales.

## Before adopting a third-party system or registry

Check, in order: install works with your CLI; GitHub activity in the last quarter; TypeScript strictness; accessibility claims backed by APG patterns; React Server Component boundaries; bundle cost of its animation dependency, measured with a real build. A registry that pulls Framer Motion or GSAP into every component is a decision, not a detail.
