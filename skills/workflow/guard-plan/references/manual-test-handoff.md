# Manual test handoff

How the guardian hands a `Runner: human` checkpoint to a guide session. The file rules are in `checkpoint-files.md`.

## Fill the prompt

- Scenarios and expected results: copied word for word from the checkpoint in the plan.
- Setup steps (install, start the app, seed data): derived from the phase's diff and from `## Surfaces` in the repo's `docs/agents/verify.md`. Write "None" when there are none.
- What the agent already tried: fill only for a fallback from an agent checkpoint (`agent-checkpoint.md`); otherwise delete the section.
- Result file for a fallback: the file already holds the companion's rows. Replace the Result file section's first line with "Append to `<absolute result file path>` a `## Re-run <scenario> by a person` section with the table below; keep everything already in the file."
- Result file format: the block in `checkpoint-files.md`, copied word for word.
- Language: the user's language in the guardian session. In a workspace, the workspace language from `CONTEXT.md`.
- Plan language: the language the plan's files are written in.

## Prompt template

Write it to `checkpoint-<NN>-prompt.md`. Text outside `<…>` is literal; `<…>` holds fill-in instructions only.

```markdown
# Manual test — checkpoint <N>: <surface>

You guide a person through a manual test of a change in the repository at `<absolute repo path>`. You do not run the test yourself and you do not fix anything.

## Language

Every message to the person is in <language>: each step, question and summary. The result file is written in <plan language>; scenario text, commands and quoted output stay literal.

## Rules

- One step per message: say exactly what to run or click and what to look at, then wait for the person's report. Name where each command runs: "in a separate terminal, in `<absolute repo path>`", not in this session; the guide session never runs the test commands itself.
- After each scenario, write its row to the result file at once, quoting what the person reported.
- Change no file other than the result file. Never fix the code, a test or the plan, even when the fix looks obvious: record what you saw.
- A scenario the person cannot run (a missing tool, a login, a crash before it starts) is `not run`, with the reason in the Got column. Go on to the next one.
- When every scenario has a row, tell the person: go back to the guard-plan session and say "done"; if that session was closed, start a new one in `<absolute repo path>` and run `/guard-plan <plan path>`.

## Setup

<numbered setup steps, or "None">

## What the agent already tried

<only when this handoff is the fallback from an agent checkpoint: quote the `not run` row from the companion's result file, its "could not drive" text included. Otherwise delete this whole section>

## Scenarios

<the checkpoint's scenarios and expected results, copied word for word from the plan>

## Result file

Write to `<absolute result file path>`, in this format:

<the format block from checkpoint-files.md, copied word for word>
```

## The command

Print one line for the user:

```
cd <absolute repo path> && claude --model <model> --effort <effort> "Read <absolute prompt path> and follow it."
```

- Default: `--model sonnet --effort medium`.
- `--effort high` only when the scenarios make the guide read logs or diagnose output, beyond comparing it with the expected result.
- The guardian picks both. The plan never names them. `claude --help` lists the flags.

## Wait or stop

Suggest one, with one sentence of reason. The user chooses; the guardian never decides.

- Wait when the scenarios are short: a few commands, one or two screens.
- Stop when the test is long, needs a device, or the guardian's context is already large (several phases guarded in this session).
