# Agent checkpoint

How the guardian runs a `Runner: guardian` checkpoint through a companion sub-agent, without stopping the run. The file rules are in `checkpoint-files.md`; the human route is in `manual-test-handoff.md`.

## Start the companion

- Claude Code: the Agent tool with the general-purpose sub-agent, with `model` and `effort` filled in. Other harnesses: the nearest equivalent that keeps its own context and accepts a follow-up.
- Default: Sonnet, effort medium. Effort high when the companion must drive a browser or diagnose output, beyond comparing it with the expected result.
- The guardian picks both; the plan never names them. This is a deliberate exception to "Weight is the only interface to the model", which holds for phase executors only: a companion is not a phase.
- Why a companion and not the guardian: the guardian is the expensive model and only checks. Driving an app and reading its output would swell its context in the middle of the plan.

## Fill the brief

- Scenarios and expected results: copied word for word from the checkpoint in the plan.
- How to drive each scenario: from the matching row of `## Surfaces` in the repo's `docs/agents/verify.md`, and from the document that row points to.
- Setup steps (install, start the app, seed data): derived from the phase's diff. Write "None" when there are none.
- Result file path: `checkpoint-<NN>-result.md`, per `checkpoint-files.md`.
- Result file format: the block in `checkpoint-files.md`, copied word for word, with `runner: companion`.
- Language: the plan's language for the result file.

## Brief template

Text outside `<…>` is literal; `<…>` holds fill-in instructions only.

```markdown
You run a manual test of a change in the repository at `<absolute repo path>`. You drive the scenarios yourself. You do not fix anything.

## Rules

- Change no file in the repository other than the result file. Never fix the code, a test or the plan, even when the fix looks obvious: record what you saw.
- After each scenario, write its row to the result file at once, quoting the output you observed.
- A scenario you cannot drive (a missing tool, a login you do not have, an app that will not start, a runtime policy that does not allow it) is `not run`. Write "could not drive: <what you tried, where you got stuck>" in the Got column. Go on to the next scenario.
- Drive the scenarios one at a time: start each test session after the previous one has ended.
- Delete every temporary folder you created.
- Report to the guardian one line per scenario: `<scenario> — pass | fail | not run`, then the result file path.

## Setup

<numbered setup steps, or "None">

## How to drive

<per scenario: the surface row from `docs/agents/verify.md` and the commands or steps it gives>

## Scenarios

<the checkpoint's scenarios and expected results, copied word for word from the plan>

## Result file

Write to `<absolute result file path>`, in this format:

<the format block from checkpoint-files.md, copied word for word, with `runner: companion`>
```

## After the report

- Read the result file, not the report, and match every row with the report's line. A row that differs from the report, or a scenario with no row, is not accepted: send the companion a follow-up (Claude Code: `SendMessage`) to finish or correct it.
- Re-test: after a fix, send a follow-up to the same companion naming the failed scenario and every other scenario the fix touched, and only those. The companion runs each of them once, one after another, adds a `## Re-run <scenario> after fix` section to the same result file and keeps the first record.
- Re-run budget: each scenario is a full session on the user's account, and a scenario that runs `guard-plan` starts its own executors too, so a few rounds of re-runs can reach the user's usage limit. Ask the user to decide before a third re-run round, and as soon as a re-run fails for a reason outside the change under test (the session misread a folder, a session ended early): fix again, accept the failure, or change the expectation as "Changing a scenario" in `SKILL.md` allows.
