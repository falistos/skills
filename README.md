# skills

A collection of [Agent Skills](https://agentskills.io) for [Claude Code](https://claude.com/claude-code) (and other skill-aware agents like Codex).

Each skill is a self-contained folder with a `SKILL.md` — a set of instructions the
agent loads on demand when the task matches. They encode workflows worth doing the
same careful way every time, so you don't have to re-explain them.

## Install

Clone and run the installer — it copies every skill into each detected agent
(`~/.claude/skills`, `~/.codex/skills`):

```sh
git clone https://github.com/falistos/skills.git
cd skills
./install.sh
```

Install only what you want:

```sh
./install.sh orchestrate
```

Skills are plain folders — you can also just copy any `skills/<name>/` directory into
`~/.claude/skills/` by hand.

## Skills

| Skill | What it does |
|---|---|
| [orchestrate](skills/orchestrate) | Build a large feature, project, or refactor as a lead orchestrator: lock the spec, freeze shared interface contracts, decompose into self-contained task files, dispatch sub-agents in dependency-ordered waves (one model per task), verify each wave, and run a final integration pass. |
| [step-by-step](skills/step-by-step) | Iterate through a list of findings (from a review, analysis, or audit) one item at a time: explain, propose approaches, wait for your go, implement, verify, optionally Codex-review, then make an atomic commit per item. |
| [codex-delegate](skills/codex-delegate) | Drive the OpenAI Codex CLI (`codex exec`) directly as a sub-agent for review, implementation, diagnosis, or research — including fanning out and tracking several Codex workers in parallel and managing their sessions. |

### orchestrate

For work too large for one linear pass. The agent acts as an orchestrator that owns the
*spine* — spec, architecture, frozen interface contracts, integration — and delegates the
*leaves* (independent, well-specified units) to sub-agents running in parallel waves,
picking the cheapest model that clears each task's bar. The design front-loads a shared
contract layer before any fan-out and treats the final coherence pass as a first-class
phase, which is how independent workers produce a result that's actually consistent.

It won't fan out for small changes — there's an explicit gate that falls back to a single
linear pass when parallelism isn't worth the token cost.

## How skills work

An agent sees each skill's `name` + `description` and consults the full `SKILL.md` only
when a task matches. Anything under a skill folder (templates in `assets/`, docs in
`references/`, scripts in `scripts/`) loads lazily from there. Keeping `SKILL.md` lean and
pushing detail into those files is deliberate — it's what keeps the always-on cost low.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
2. Put templates/docs/scripts alongside it as needed.
3. Add a row to the table above.
4. `./install.sh <name>` to install it locally.

## Related

Some tools live in their own repos when they're more than a skill (a CLI, a service):

- [term](https://github.com/mediavee/term) — persistent tmux-backed terminal sessions for agents.

## License

[MIT](LICENSE) © Mediavee
