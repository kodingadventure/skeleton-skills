# Question files

One file per question that someone outside the session must answer (a stakeholder, the team, a vendor). The file is the **single home of the question's detail**: context, options, answer and consequences. The other two places only point at it:

- `TRACKER.md` `## Open Questions`: one row, the question in one plain sentence, its `File` column naming this file. The row carries the reporting checkbox.
- `CONTEXT.md` `## Open questions`: one index line per open question, `<who>: <one line> — questions/<file>.md`. Answered questions leave the index; their outcome lives in `## Decisions`.

File name: `questions/YYYY-MM-DD-<topic>.md`, the date it was raised. Written in the workspace language.

## Shape

```markdown
# <The question, one line>

Raised: YYYY-MM-DD · For: <who answers> · Status: open | answered | withdrawn | merged into <file>
Asked: YYYY-MM-DD via <channel> (once sent, written by /msg; ", follow-up YYYY-MM-DD" for reminders)
Answered: YYYY-MM-DD by <who> (once answered)

## Question

<The question in full, in words the person who answers it follows.>

## Context

<Why it is asked now: what was found, what is blocked. Point to findings rather than copying them.>

## Options

1. <option> — <consequences>. (Recommended: <why>)
2. <option> — <consequences>.

## Answer

<The answer, quoted or closely paraphrased, with its date.>

## Consequences

- Decision: <what was decided, also in CONTEXT.md ## Decisions>
- Unblocks: <work items, blockers>
- Follow-up: <new questions, plan changes>
```

Omit `## Options` when the question is open-ended, and `## Answer` / `## Consequences` until it is answered.

## Monitoring

`grep -l "Status: open" questions/*.md` lists every question still waiting.
