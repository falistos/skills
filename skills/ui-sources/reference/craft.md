# Craft — shaders, motion, tokens, type, colour

What separates a competent interface from one that looks made on purpose. Reach for these when the brief asks for character, not when it asks for a form.

## Shaders, gradients, grain

- **[Paper Shaders](https://shaders.paper.design)** — ~28 zero-dependency WebGL2 shaders: mesh gradients, grain, dither, liquid metal, paper texture, halftone. `@paper-design/shaders-react`. The strongest single source here.
- **[Canvas UI](https://canvasui.dev)** — WebGL effects applied *over live HTML* (fluid, glass, shatter). React/Vue/Svelte/vanilla via shadcn registry.
- **[ShaderGradient](https://www.shadergradient.co)** — animated 3D shader gradients, exportable.
- **[Colorflow](https://colorflow.ls.graphics)** — mesh gradients with WebGL effects.
- **[Pryzm](https://pryzm.design)** — gradient + glass + grain studio.
- **[backgrounds.supply](https://www.backgrounds.supply)** — 1 000+ ready backgrounds, plus a Gradient Lab exporting image/video/embed.
- **[Maxime Heckel's R3F lab](https://r3f.maximeheckel.com)** + [blog](https://blog.maximeheckel.com) — not a library. The shader reference to actually read when building something custom (SDF, blob tracking, frame differencing).
- **`@motion-menu`** — 598 registry items of scroll-driven WebGL, shader passes and spring choreography.

A shader is a bundle and a battery cost. Use one as a hero or a background, not on six surfaces.

## Motion

Pick by weight, not by reflex:

| Case | Take |
|---|---|
| Entrances, simple reveals, Tailwind project | Plain CSS, or `tailwindcss-motion` (~5 kB, zero JS) |
| React UI tied to state, gestures, mount/unmount | Motion (ex-Framer Motion), `AnimatePresence` |
| Complex scroll choreography, pinning, timelines, non-React | GSAP (~78 kB) |
| Lightweight tweens without scroll work | Anime.js (~9 kB) |

Tools: **[CSS Springs](https://www.kvin.me/css-springs)** generates real spring curves as CSS `linear()`. **[easing.dev](https://www.easing.dev)** is the playground. **[Kinetics](https://kinetics.colorion.co)** gives copy-paste spring CSS.

Learning: **[animations.dev](https://animations.dev)** — Emil Kowalski's course, theory then CSS then Motion, with walkthroughs of the Family drawer and Dynamic Island. It ships its own AI skills (`/animate`, `/review-animations`, `/debug-animation`).

Always respect `prefers-reduced-motion`.

## Tokens and type

- **[Open Props](https://open-props.style)** — 500+ CSS custom properties: easings including springs, shadows, masks, fluid type, gradients, noise. ~4 kB core, no framework. The best answer for a project that wants a token system without adopting Tailwind.
- **[Utopia](https://utopia.fyi)** — fluid type and space scales compiled to `clamp()`. Use it instead of accepting a default type scale.
- **[Tweakcn](https://tweakcn.com)** — visual editor for shadcn themes (colour, font, radius, background). The cure for shipping default zinc.

## Colour

- **Radix Colors** — scales built for UI states (hover, active, disabled, focus), coherent across light and dark. The default recommendation.
- **[oklch.com](https://oklch.com)** — OKLCH is perceptually uniform, so equal steps look equal. Use it to build tonal ramps.
- **[Huetone](https://huetone.ardov.me)** — ramps with contrast baked into the editing loop.
- **[Ramps](https://www.ramps.studio)** — colour ramps and tokens, WCAG-checked.
- **[Realtime Colors](https://www.realtimecolors.com)** — fast iteration on a live mock. Has **no contrast checker**; verify elsewhere before shipping.
- **[`<color-input>`](https://nerdy.dev/rfc-latest-color-input-concept)** — Adam Argyle's HDR/P3 picker web component with gamut mapping and contrast scores.

## Icons and lettering

`@svgl` (brand logos) · `pqoqubbw/icons` and `heroicons-animated` (animated) · [Morphicons](https://www.morphicons.com) (morph any stroke icon into another) · [Tegaki](https://gkurt.com/tegaki) (animated handwriting from any font).

## Vocabulary

**[index.how/to/articulate](https://index.how/to/articulate)** — names for what you are looking at in an interface. Without shared vocabulary a design critique is noise. Read it before arguing about a UI.
