# Where plans live, and which one runs

## Inside a workspace

`<workspace>/plans/<NN>-<name>/IMPLEMENTATION_PLAN.md` (+ `phases/`), `NN` the next free number. The workspace root is the `Workspace root:` line (see the `kickoff` skill's `references/workspace-root.md`); nothing below changes that layout.

## Outside a workspace: the plan root

A repo names the folder that holds its plans with one line in `CLAUDE.md` or `AGENTS.md`, a path relative to the repo root:

```markdown
Plan root: `.plans/`
```

Without the line the root is `.plans/`, except in a repo whose `docs/agents/domain.md` still has the older `Plan output` key: that key's folder stays in use, and nothing is asked.

### Asking once

On the repo's first plan outside a workspace — no `Plan root:` line, no `Plan output` key, no `.plans/` folder — ask the user one question: keep `.plans/` (the default) or name another folder.

- Check the answer is git-ignored (`git check-ignore <root>/x`). When it is not, say so and offer to add it to `.gitignore`: plans must never be staged by accident.
- Write the answer as the `Plan root:` line, even when it is the default, so the question is never asked again. Put it in `CLAUDE.md`, or in `AGENTS.md` when the repo keeps its agent rules there; create `CLAUDE.md` when the repo has neither.
- That line is a repo change: list it among the files you wrote.

### One folder per plan

Each plan is `<root>/<YYYY-MM-DD>-<slug>/IMPLEMENTATION_PLAN.md` (+ `phases/`). Never write into a plan folder that exists: a second plan with the same date and slug gets a `-2` suffix.

## Which plan runs

`**Status:**` is one of `pending`, `in-progress`, `done`, `abandoned`. `pending` and `in-progress` are _open_.

When the user gives no path, list the plan folders (in a workspace `plans/*`, otherwise `<root>/*`), read each `**Status:**` line, and

- exactly one open plan → use it, and name it in one line before starting;
- several open plans → ask which, listing each with its Status and first unchecked item;
- none → ask for a path.

No file marks the "active" plan: the plan already says whether it is open, and a second copy of that fact goes stale. A new plan never changes another plan's Status. Only the owner marks a plan `abandoned`.
