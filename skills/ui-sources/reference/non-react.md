# Non-React stacks

The modern UI ecosystem assumes React + Tailwind + Motion. For Django, Rails, Laravel, Spring, Astro, HTMX, Vue, Svelte or plain HTML, Aceternity or Magic UI are useless; use this.

## The shadcn look without React

**[Basecoat UI](https://basecoatui.com)** — shadcn/ui recreated with Tailwind classes and minimal vanilla JS. Compatible with shadcn themes, so a token file is shared across stacks. Any backend (Laravel, Rails, Django, Flask, Astro, plain HTML). Buttons, forms, cards, alerts, nav, dialogs, dropdowns, tabs, accordions, toasts; dark mode included.

The answer to "our app is server-rendered but should look like everything else".

## Components with zero JavaScript

**daisyUI** — semantic component classes on Tailwind, no JS shipped. Framework-agnostic, runtime CSS variables, P3 colours, RTL. Broader and more mature than Basecoat, less visually identical to shadcn.

## Headless primitives in Vue, Svelte or Solid

**Ark UI** (on **Zag.js**) — the same accessible state machines compiled for React, Vue, Solid and Svelte. The only serious cross-framework answer for complex primitives (combobox, date picker, menu). **Park UI** is the styled layer, using Panda CSS.

## A token system without a framework

**Open Props** — 500+ CSS custom properties (easings, springs, shadows, masks, fluid type, gradients, noise), ~4 kB core, plain CSS. Fits any stack, including Spring/Thymeleaf or Rails.

Pair with **[Utopia](https://utopia.fyi)** (fluid type and space scales compiled to `clamp()`) and **Radix Colors**: both plain CSS.

## Isolated elements (buttons, toggles, loaders)

**Uiverse.io** — ~6 700 community elements, copyable as HTML/CSS, Tailwind, React or into Figma. Usable anywhere.

Quality is uneven, and the elements share no system: five from different authors on one screen guarantees incoherence. Take **one**, then rebuild its siblings to match.

## Motion without React

GSAP for timelines and scroll choreography; Anime.js (~9 kB) for simple tweens; native CSS (`@keyframes`, `transition`, `scroll-timeline`, `view-transition`) covers a lot with zero JS, on the compositor thread.

**[Kinetics](https://kinetics.colorion.co)** and **[CSS Springs](https://www.kvin.me/css-springs)** output plain CSS.

## Ports of React-first libraries

Check for official ports before assuming React-only. React Bits has Vue and Svelte ports. Motion (ex-Framer Motion) has first-class JavaScript and Vue support after absorbing Motion One.

## Native and desktop

For SwiftUI, Jetpack Compose, Flutter, React Native, JavaFX, WPF or Avalonia this skill has nothing: `ui-ux-pro-max` carries a database for those stacks, and `impeccable` has iOS and Android references.
