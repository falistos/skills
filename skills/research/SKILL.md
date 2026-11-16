---
name: research
description: "Use for \"renseigne-toi sur\", \"fais des recherches\", \"research X\", \"how do serious projects do X\", non-UI library/tool comparisons, or API/version facts needing multiple lookups."
---

# Research

Record the bounded question, decision it informs and notes path. Research directly; delegate on request or for
a substantial independent investigation while the main thread progresses, subject to harness rules and
context/output cost. A worker does its assigned research itself.

1. Use primary docs, source, release notes, specs or first-party APIs. Blogs/answers are leads only. Clone a
   repository to study into a `mktemp -d` directory; pin readings to
   version/tag/commit.
2. Cite every claim with URL/section or `repo@sha:path:line`; mark uncited claims `assumed`.
3. Separate source statements, executed checks (command/output), open questions and contradictions.
4. Write one Markdown file: answer, evidence, then open questions.

## Notes path

- The location the project or its work tracker names for reports, if any.
- Otherwise: `research-<topic>.md` in session scratch (T3 scratch thread cwd, otherwise `/tmp`), outside
  repositories.

Done when the file exists, every claim is cited or `assumed`, and the reply gives path and a few-sentence
answer.
