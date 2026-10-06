# Discovery — finding a component without guessing

## How to use this

1. **Identify the task, not the library the user named.** "I need a dropdown" is a primitives task whatever they asked about.
2. **Check `package.json` first.** Use what already covers the need. If it is a competitor of what you'd recommend, say so once and leave the dependency alone.
3. **Recommend one thing.** A menu of five is a way of not deciding.
4. **Say when you leave the catalogue.** General knowledge is fine; passing it off as from here is not.

## Start here: registry.directory

An index of **82 shadcn-compatible registries** and ~28 000 components with machine-readable endpoints, so no component-gallery HTML.

```bash
curl -s https://registry.directory/directory.json   # all registries: name, namespace, registry_url
curl -s https://registry.directory/items.json       # every component across every registry
curl -s https://registry.directory/api/markdown/{owner}/{repo}/{slug}   # one component, as markdown
```

`items.json` is ~8 MB: filter it.

```bash
curl -s https://registry.directory/items.json \
  | jq -r '.items[] | select(.name|test("kanban";"i")) | "\(.registry.name)\t\(.name)\t\(.description)"'
```

Item pages also serve markdown: append `.md` to `https://registry.directory/{owner}/{repo}/{slug}`.

## The base and the big generalists

| Namespace | Source | Use it for |
|---|---|---|
| `@shadcn` | ui.shadcn.com | The base. ~470 items including blocks and charts |
| `@reui` | reui.io | Breadth (1 700 items), Radix and Base UI |
| `@kibo-ui` | kibo-ui.com | The **composites** shadcn omits: gantt, kanban, code editor, colour picker, dropzone |
| `@diceui` | diceui.com | Accessible complex primitives |
| `@intentui` | intentui.com | React Aria underneath: pick when accessibility is a hard requirement |
| `@coss` | Coss UI | Base UI rather than Radix |
| `@tailark` | tailark.com | Marketing/landing blocks |
| `@kokonutui` | kokonutui.com | 100+ Tailwind components |

## Specialist primitives — defer to `pick-ui-library`

For the canonical React pick per task (numbers, OTP inputs, command menus, toasts, charts, virtualisation, drag and drop, state, styling), invoke **`pick-ui-library`** explicitly: it is curated, one answer per task, and better maintained than a copy.

It does not cover:

| Need | Library | Note |
|---|---|---|
| Headless primitives outside React | [Ark UI](https://ark-ui.com) / [Zag.js](https://zagjs.com) | Same state machines for React, Vue, Solid, Svelte. [Park UI](https://park-ui.com) is the styled layer |
| A component nobody has curated | `registry.directory` above | 28 000 items, the fallback when curated lists come up empty |

## Character and aesthetic — when the brief is not "clean SaaS"

| Namespace | What |
|---|---|
| `@8bitcn` | 8-bit / pixel |
| `@retroui` | Neo-brutalism |
| `SMUI` | Nord-inspired terminal: monospace, zero radius |
| `@termcn` | Terminal UIs, 342 items |
| `@thegridcn` | Tron-inspired |
| `shadcn-glass-ui` | Glassmorphism |
| [Skiper UI](https://skiper-ui.com) | Deliberately uncommon: dynamic island, knockout brackets, kinetic inputs |
| [Rare UI](https://www.rareui.com) | Small set of unusual animated components, one file each |
| [FeralUI](https://feralui.dev) | Physics-driven: springs, proximity hover. Built for AI-product "handfeel" |
| [UI Layouts](https://www.ui-layouts.com) | Liquid glass, colour picker, drag primitives + a tools sibling for mesh/shadow/clip-path |

## Domain-specific registries

`@svgl` (brand logos) · `pqoqubbw/icons` and `heroicons-animated` (animated icons) · `@plate` (rich text editor) · `@supabase` and `@clerk` (auth flows) · `@better-upload` (S3 uploads) · `@trophy-ui` (streaks, achievements, leaderboards) · `@framecn` and `@remotionui` (video components) · `@payload-components` (Payload CMS blocks) · `@nuqs` (type-safe URL state).

## Common mismatches

Symptoms of rebuilding something that exists:

- **Hand-rolling a kanban, gantt, colour picker, file dropzone or code editor** → `@kibo-ui`, weeks of work each.
- **Writing a chat transcript, streaming message or tool-call card** → `reference/ai-interfaces.md`.
- **Reimplementing a combobox or date picker because the project isn't React** → Ark UI / Zag.js.
- **A full component library for one primitive** → install the single primitive.
- **Copying markup from a fetched inspiration page** → galleries render code through JS; what you fetched is not the component. Find it in a registry.
- **A second registry for something the base covers** → check `@shadcn` first; near-duplicates in another style are how a UI stops looking like one product.
- **The default zinc shadcn theme** → theme it (`tweakcn.com`) or it reads as unfinished.

## Inspiration, not code

These tell you what to build. Copy no code from them.

- [Godly](https://godly.website) — brutally curated, 3–5 sites a week
- [Refero](https://refero.design) and Mobbin — shipped product flows: onboarding, settings, pricing, search
- [SiteInspire](https://www.siteinspire.com) — editorial and typographic, best filtering
- [Land-book](https://land-book.com), Httpster, Lapa Ninja — landing pages
