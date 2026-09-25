# Non-React stacks

Most of the modern UI ecosystem assumes React + Tailwind + Motion. If the project is Django, Rails, Laravel, Spring, Astro, HTMX, Vue, Svelte or plain HTML, recommending Aceternity or Magic UI is useless. Use this instead.

## Want the shadcn look without React

**[Basecoat UI](https://basecoatui.com)** — recreates shadcn/ui with Tailwind classes and minimal vanilla JS. Compatible with shadcn themes, so a design token file is shared across stacks. Works with any backend: Laravel, Rails, Django, Flask, Astro, plain HTML. Covers buttons, forms, cards, alerts, nav, dialogs, dropdowns, tabs, accordions, toasts. Dark mode included.

This is the answer to "our app is server-rendered but I want it to look like everything else".

## Want components with zero JavaScript

**daisyUI** — semantic component classes on top of Tailwind, ships no JS to the browser. Framework-agnostic by construction, supports runtime CSS variables, P3 colours and RTL. More mature and broader than Basecoat; less visually identical to shadcn.

## Want headless primitives in Vue, Svelte or Solid

**Ark UI** (built on **Zag.js**) — the same accessible state machines compiled for React, Vue, Solid and Svelte. This is the only serious cross-framework answer for complex primitives (combobox, date picker, menu). **Park UI** is the styled layer on top, using Panda CSS.

## Want a token system without a framework

**Open Props** — 500+ CSS custom properties (easings, springs, shadows, masks, fluid type, gradients, noise). ~4 kB core, plain CSS. Drops into any stack including a Spring/Thymeleaf or Rails app.

Pair with **[Utopia](https://utopia.fyi)** for fluid type and space scales compiled to `clamp()`, and **Radix Colors** for the palette — both are plain CSS and framework-agnostic.

## Want isolated elements (buttons, toggles, loaders)

**Uiverse.io** — ~6 700 community elements, copyable as HTML/CSS, Tailwind, React or into Figma. Genuinely usable anywhere.

Two caveats worth stating out loud: quality is uneven because it is community-made, and these are isolated elements with no shared system. Taking five from different authors into one screen guarantees visual incoherence. Take **one**, then rebuild its siblings to match.

## Motion without React

GSAP for timelines and scroll choreography. Anime.js (~9 kB) for simple tweens. Or native CSS: `@keyframes`, `transition`, `scroll-timeline` and `view-transition` now cover a lot with zero JS and run on the compositor thread.

**[Kinetics](https://kinetics.colorion.co)** and **[CSS Springs](https://www.kvin.me/css-springs)** both output plain CSS, so they work regardless of stack.

## Ports of React-first libraries

Some sources publish official ports — check before assuming a library is React-only. React Bits has Vue and Svelte ports. Motion (ex-Framer Motion) now has first-class JavaScript and Vue support after absorbing Motion One.

## Native and desktop

For SwiftUI, Jetpack Compose, Flutter, React Native, JavaFX, WPF or Avalonia, this skill has nothing useful — the `ui-ux-pro-max` skill carries a database covering those stacks, and `impeccable` has iOS and Android references.
