---
name: questionnaire
description: "Draft an async questionnaire in French for facts only a client, partner or server staff knows (\"prépare des questions pour le staff\")."
---

# Questionnaire

Extract the recipient's knowledge in one async pass. Ask the owner about the send (recipient and expected
result), not subject facts they lack.

## Steps

1. Establish role, technical level and relationship from context/spec/thread; ask for missing recipient facts
   in one message. Finish when what they know and the owner does not is explicit.
2. List needed facts/decisions and what each unblocks, using context first and one message for missing needs.
   Finish with a concrete list.
3. Write in French; every need gets a question.

Save it where the project's work tracker keeps reports, otherwise `questionnaire-<topic>.md` in session
scratch, and return its path.

## Format

Discord-pastable Markdown: headings and numbered questions, no tables. Most important first; group by theme
above five questions and number continuously so replies can say "3 : oui".

- Title; **Pourquoi** (decision depending on answers); **De / Pour**; intended use of answers.
- **Contexte:** one paragraph for an uninformed reader, in game/player terms, without code vocabulary.
- **Comment répondre:** deadline, rough effort, partial answers and « je ne sais pas » welcome.
- **Questions:** one idea each; closed with `a)`, `b)`, `autre :` when options are known, otherwise open.
  Explain player consequences and mark the recommended option; add a one-line _Pourquoi on demande_ only to
  prevent misreading/throwaway answers. Leave an empty `> ` answer line.
- **Autre chose ?** catch-all.
