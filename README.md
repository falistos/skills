# skills

A collection of [Agent Skills](https://agentskills.io) for [Claude Code](https://claude.com/claude-code) (and other skill-aware agents like Codex).

Each skill is a self-contained folder with a `SKILL.md` — a set of instructions the
agent loads on demand when the task matches. They encode workflows worth doing the
same careful way every time, so you don't have to re-explain them.

## Install

Clone and run the installer. It copies every skill into each detected agent
(`~/.claude/skills` for Claude Code, `~/.agents/skills` for Codex and other skill-aware agents):

```sh
git clone https://github.com/falistos/skills.git
cd skills
./install.sh                     # every skill
./install.sh design-pipeline     # only the named ones
./install.sh --link              # symlink to the checkout instead: a pull updates every agent
```

Skills are plain folders — you can also copy any `skills/<name>/` directory by hand.

## Skills

| Skill | What it does |
|---|---|
| [design-pipeline](skills/design-pipeline) | Take a UI from a rough idea to a reviewed build: named art directions to pick from, the choice locked into a `DESIGN.md`, then build and review against it. Web, desktop and mobile. |
| [ui-sources](skills/ui-sources) | Source real UI building blocks instead of inventing them: component libraries, shadcn-compatible registries, AI interface kits, motion and shader tools, design tokens, public design systems. |

## How skills work

An agent sees each skill's `name` + `description` and consults the full `SKILL.md` only
when a task matches. Anything under a skill folder (templates in `assets/`, docs in
`references/`, scripts in `scripts/`) loads lazily from there. Keeping `SKILL.md` lean and
pushing detail into those files is deliberate — it's what keeps the always-on cost low.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
2. Put templates/docs/scripts alongside it as needed.
3. Add a row to the table above.
4. `./install.sh --link <name>` to try it locally.

## Related

Some tools live in their own repos when they're more than a skill (a CLI, a service):

- [term](https://github.com/mediavee/term) — persistent tmux-backed terminal sessions for agents.

## License

[MIT](LICENSE) © Mediavee
