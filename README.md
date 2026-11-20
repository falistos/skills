# skills

My agent stack: the [Agent Skills](https://agentskills.io) I write, plus the third-party skills I follow.
They work with Claude Code, Codex, Grok and any agent that reads `~/.agents/skills`.

An agent sees each skill's `name` and `description` and reads the full `SKILL.md` only when a task
matches; files beside it (`references/`, `assets/`, scripts) load from there on demand.

## Install

```sh
git clone https://github.com/falistos/skills.git
cd skills
./install.sh --link              # link every skill to this checkout and add external.txt
./install.sh design-pipeline     # copy only the named skills
```

`--link` makes the checkout the live source: a `git pull` or an edit here reaches every agent at once.
`external.txt` is the complete list of npx skills: applied when it changes, it uninstalls any other npx skill,
so every machine has the same set;
`npx skills update -g` keeps them current.

## My skills

| Skill | What it does |
|---|---|
| [arch-review](skills/arch-review) | Review a Java project's architecture, with alternatives and a refactoring plan |
| [clean-copy](skills/clean-copy) | Write or tighten user-facing strings |
| [correct](skills/correct) | Turn a repeated mistake or a retrospective into a rule or a check that prevents it, or a hard-won procedure into a skill |
| [design-pipeline](skills/design-pipeline) | Take a UI from a rough idea to named art directions, a `DESIGN.md`, a build and a review |
| [diagnosing-bugs](skills/diagnosing-bugs) | Reproduce, explain and fix a bug, crash, failing test or performance regression |
| [docs](skills/docs) | Write operator-facing docs: setup, configuration, commands, permissions, features |
| [overhaul](skills/overhaul) | Review a whole project on six axes, then apply an approved plan in proven lots (invoked by hand) |
| [questionnaire](skills/questionnaire) | Draft an async questionnaire for facts only someone else knows |
| [research](skills/research) | Compare how serious projects solve a problem, or check API and version facts at the source |
| [step-by-step](skills/step-by-step) | Walk review findings one by one, with validation and a commit each |
| [ui-sources](skills/ui-sources) | Source real UI components, registries, kits, tokens and design systems |

## Third-party skills

[`external.txt`](external.txt) lists them, one source per line: Matt Pocock's `codebase-design`,
`grilling` and `writing-for-agents`; `term`; `impeccable`; `shadcn`;
the BeautifulRust `rust-best-practices` and `rust-review`; and Emil Kowalski's design-engineering, animation, worst-case and mobile skills.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with `name` (the folder's name) and a `description` that says when to load it.
2. Put references, templates or scripts beside it.
3. Add a row to the table above.
4. `./install.sh --link <name>` to try it.

A third-party skill is one line in `external.txt`, then `./install.sh`.

## License

[MIT](LICENSE) © Mediavee. [diagnosing-bugs](skills/diagnosing-bugs/NOTICE) and [questionnaire](skills/questionnaire/NOTICE) credit the work they adapt.
