# Checkpoint files

The files a manual test checkpoint leaves next to the plan. Same rules inside and outside a workspace.

## Location and names

- Folder: `<plan folder>/manual-tests/`. `<plan folder>` is the folder that holds `IMPLEMENTATION_PLAN.md`.
- `checkpoint-<NN>-prompt.md`: the handoff prompt. Written for `Runner: human` checkpoints only.
- `checkpoint-<NN>-result.md`: the result file.
- `<NN>` is the checkpoint's number in the plan, two digits.

## Git

Follow the same rule as the phase file in the guard-plan Commit step.

- Plan folder is git-ignored: do not stage the files.
- Plan folder is tracked by the repo: stage the files with the next commit the guardian makes.
- Plan folder lives in a notes repo whose rules ask for notes to be committed: commit there, following those rules.

Add no further ignore check.

## Result file format

Write it in the plan's language, one row at a time as each scenario ends, never all at the end. Scenario text, commands and quoted output stay literal.

```markdown
# Checkpoint <N> — <surface>

YYYY-MM-DD · runner: <guide session | companion> · repo: <absolute repo path> @ <short sha>

| Scenario                         | Result                | Expected          | Got                                                  |
| -------------------------------- | --------------------- | ----------------- | ---------------------------------------------------- |
| <scenario, as the plan words it> | pass / fail / not run | <expected result> | <what was observed, quoted; for not run, the reason> |

## Findings

- <anything odd that broke no scenario, or "none">
```

A re-run after a fix adds a `## Re-run <scenario> after fix` section with the same table and keeps the first record. A scenario the companion could not drive, handed to a person, adds a `## Re-run <scenario> by a person` section the same way.

## Waiting line

Written in the plan entry point's `## Baseline` before the guardian waits or stops, and deleted once its result is processed:

```markdown
Waiting: checkpoint <N> — prompt `<path>` · result `<path>` · HEAD <sha>
```
