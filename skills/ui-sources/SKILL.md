---
name: ui-sources
description: Source real UI building blocks instead of inventing them — component libraries, shadcn-compatible registries, AI/agent interface kits, shader and motion tools, design token systems, and public design systems to study. Use when a UI needs a concrete component (chat interface, command menu, data table, drag-and-drop, animated number, gradient background, dashboard shell), when picking a component library or design system for a new app, when the answer is "where do I get this from", or when building an AI/agent interface (chat, tool calls, reasoning, approvals, voice, workflow canvas). Not for design critique, layout review, or visual polish — that is `impeccable`.
user-invocable: true
argument-hint: "[what you need — e.g. 'chat UI', 'animated counter', 'non-react buttons', 'design system reference']"
---

# UI Sources

A catalogue of places to take real, working UI from. Browse it, pick what fits, ignore the rest.

## Routing

| Need | Load |
|---|---|
| Find a component, any component; browse registries | `reference/discovery.md` |
| Chat UI, tool calls, reasoning, approvals, voice, agent canvas | `reference/ai-interfaces.md` |
| Shaders, gradients, grain, motion, easing, tokens, type, colour | `reference/craft.md` |
| Study how a real design system is built; token architecture | `reference/design-systems.md` |
| Project is not React — Django, Rails, Laravel, Astro, plain HTML, Vue, Svelte | `reference/non-react.md` |

## Neighbouring skills

Don't duplicate what these already do: **`pick-ui-library`** (canonical React library per task — invoke it explicitly, it never self-triggers), **`baseline-ui`** (fast spacing/hierarchy/typography cleanup), **`emil-design-eng`** and **`review-animations`** (craft and motion judgement), **`impeccable`** (design direction, critique, polish).

## Two things worth respecting

- **Install components, don't rewrite them from memory.** Use the CLI, or fetch canonical markdown (see `reference/discovery.md`). Component galleries render their code through JS, so fetched HTML is not a reliable source.
- **Check the stack first.** Most of this ecosystem is React + Tailwind + Motion. If the project isn't, go to `reference/non-react.md` rather than proposing something unusable.

## The base layer

Unless a reason says otherwise the base is **shadcn/ui**, because nearly every source below distributes through its registry protocol:

```bash
pnpm dlx shadcn@latest init                 # once per project
pnpm dlx shadcn@latest add button           # official registry, no config
pnpm dlx shadcn@latest add @magicui/globe   # third-party, needs a namespace
```

Third-party namespaces are declared in `components.json`:

```json
{ "registries": { "@magicui": "https://magicui.design/r/{name}.json" } }
```

There is an official MCP server (`npx shadcn@latest mcp init --client claude`) that works with any shadcn-compatible registry. Worth suggesting when the user will be pulling components repeatedly in the same project.
