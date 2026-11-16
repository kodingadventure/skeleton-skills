# Where plans live, and which one runs

## Inside a workspace

`<workspace>/plans/<NN>-<name>/IMPLEMENTATION_PLAN.md` (+ `phases/`), `NN` the next free number. The workspace root is the `Workspace root:` line (see the `kickoff` skill's `references/workspace-root.md`); nothing below changes that layout.

## Outside a workspace: the plan root

A repo names the folder that holds its plans with one line in `CLAUDE.md` or `AGENTS.md`, a path relative to the repo root:

```markdown
Plan root: `.scratch/plans/`
```

Without the line the root is `.scratch/plans/`, next to the default workspace root (`.scratch/workspaces/`), except in a repo whose `docs/agents/domain.md` still has the older `Plan output` key: that key's folder stays in use, and nothing is asked.

### Asking once

On the repo's first plan outside a workspace — no `Plan root:` line, no `Plan output` key, no `.scratch/plans/` folder — ask the user one question: keep the default or name another folder. The default is `.scratch/plans/`, with two exceptions read from the `Workspace root:` line:

- It names a `workspaces/` folder inside a notes folder (for example `_local/workspaces/`): the default is its sibling (`_local/plans/`), so all local notes stay in one folder.
- It names the older `.scratch/plan/`: the default is `.plans/`, because `.scratch/plan/` and `.scratch/plans/` side by side differ by one letter.

Then:

- Compare the answer with the workspace root (the `Workspace root:` line, or `.scratch/workspaces/` without one) before anything else, path against path. When the answer is that folder, or starts with it (`_local/plans/` starts with `_local/`), it is inside the workspace root and plan folders would mix with workspace folders: write no line and no plan there, tell the user that in one sentence that names both paths, and ask again. With nobody to answer, use `.scratch/plans/`.
- Check the answer is git-ignored (`git check-ignore <root>/x`). When it is not, say so and offer to add it to `.gitignore`: plans must never be staged by accident.
- Write the answer as the `Plan root:` line, even when it is the default, so the question is never asked again. Put it in `CLAUDE.md`, or in `AGENTS.md` when the repo keeps its agent rules there; create `CLAUDE.md` when the repo has neither.
- That line is a repo change, and the skill that wrote it commits it at once:
  - Before writing the line, run `git diff HEAD --quiet -- <file>` (`<file>` is the `CLAUDE.md` or `AGENTS.md` you are about to edit; skip this for a `CLAUDE.md` you create). A non-zero exit means the file already holds uncommitted changes: write the line, commit nothing, and tell the user the file now mixes the line with their own changes, so they commit it themselves.
  - Otherwise commit under the repo's `CLAUDE.md` / `AGENTS.md`. If they let the agent commit, commit only that file, plus `.gitignore` when this run added the root to it, with explicit pathspecs and the message `chore: set the plan root`. If they ask for confirmation, ask first. If they are silent or leave commits to the user, print the `git commit` command and go on.
  - A line left uncommitted is picked up by `wrap-up`, which commits it when it is the file's only change.

### One folder per plan

Each plan is `<root>/<YYYY-MM-DD>-<slug>/IMPLEMENTATION_PLAN.md` (+ `phases/`). Never write into a plan folder that exists: a second plan with the same date and slug gets a `-2` suffix.

## Which plan runs

`**Status:**` is one of `pending`, `in-progress`, `done`, `abandoned`; nothing else. Progress text goes on a separate `**Progress:**` line, so reading `Status` stays exact. `pending` and `in-progress` are _open_.

When the user gives no path, list the plan folders (in a workspace `plans/*`, otherwise `<root>/*`), read each `**Status:**` line, and

- exactly one open plan → use it, and name it in one line before starting;
- several open plans → ask which, listing each with its Status and first unchecked item;
- none → ask for a path.

No file marks the "active" plan: the plan already says whether it is open, and a second copy of that fact goes stale. A new plan never changes another plan's Status. Only the owner marks a plan `abandoned`.
