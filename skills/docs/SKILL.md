---
name: docs
description: "Write or regenerate operator-facing project or plugin docs/wiki in wiki/, covering setup, configuration, commands, permissions and features with examples."
user-invocable: true
argument-hint: "[specific section to regenerate — omit for full documentation]"
---

# Operator documentation

Write root `wiki/` pages for installers/admins, at the standard of EssentialsX, LuckPerms or Citizens. With an
argument, regenerate only that section while reading enough context to verify it.

## 1. Inventory

Read build metadata/dependencies, all admin resources (manifest, config, messages) and Java code, using
parallel Explore agents. Finish with a complete inventory:

- Commands/subcommands, arguments, flags, permissions and descriptions.
- Every config key traced from YAML to Java usage.
- Permission nodes and grants.
- Features, PlaceholderAPI placeholders, exposed events/hooks, dependencies and soft dependencies.

## 2. Write

| Page | Content |
|---|---|
| `Home.md` | Plain opening paragraph, features, links, requirements (server, framework, etc.) |
| `Getting-Started.md` | Installation and shortest zero-to-working path |
| `Configuration.md` | File locations/reload, then sections with purpose, realistic commented YAML, non-obvious options, valid values and gotchas; complete file for directory-scanned configs |
| `Commands.md` | Base command and `Command / Description / Permission` table; complex commands also get syntax (`<required> [optional] [--flag]`) and examples explaining flags |
| `Permissions.md` | `Permission / Description / Default` (`op`/`true`/`false`) and wildcards/grouping |
| `{Feature}.md` | Major systems only: purpose, setup (config/commands), complete working example, scenarios/FAQ |
| `_Sidebar.md` | Bold plugin name, links to every page, `---` before feature pages |

Scale page count/detail to the project. Use operator language, real values (`Lobby`, `30`, `DIAMOND_SWORD`)
and examples before prose. Omit marketing, meta introductions, class names/internal calls and explanations of
self-evident keys.

## 3. Verify

Compare registrations and code permissions against command/permission pages, all resource config sections
against Configuration, examples against implemented syntax, and every internal link against an existing page.
Fix every missing command, key, permission or broken link before finishing.
