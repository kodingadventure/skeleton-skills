<!-- Copy of the kickoff skill's references/workspace-root.md; keep in sync. -->

# Choosing the workspace root

A repo names the folder that holds its workspaces with one line in `CLAUDE.md` or `AGENTS.md`, a path relative to the repo root:

```markdown
Workspace root: `.scratch/workspaces/`
```

Every workspace skill, and the commit reminder hook, reads that line. Without it the root is `.scratch/workspaces/`.

## Asking once

On the repo's first workspace — no `Workspace root:` line in `CLAUDE.md` / `AGENTS.md`, and no `.scratch/workspaces/INDEX.md` — ask the user one question: keep `.scratch/workspaces/` (the default) or name another folder.

- Check the answer is git-ignored (`git check-ignore <root>/x`). When it is not, say so and offer to add it to `.gitignore`; the notes must never be staged from the main repo.
- Write the answer as the `Workspace root:` line, even when it is the default, so the question is never asked again. Put it in `CLAUDE.md`, or in `AGENTS.md` when the repo keeps its agent rules there; near the repo's other workflow notes when there are any.
- That line is a repo change, and the skill that wrote it commits it at once:
  - Before writing the line, run `git diff HEAD --quiet -- <file>` (`<file>` is the `CLAUDE.md` or `AGENTS.md` you are about to edit). A non-zero exit means the file already holds uncommitted changes: write the line, commit nothing, and tell the user the file now mixes the line with their own changes, so they commit it themselves.
  - Otherwise commit under the repo's `CLAUDE.md` / `AGENTS.md`. If they let the agent commit, commit only that file, plus `.gitignore` when this run added the root to it, with explicit pathspecs and the message `chore: set the workspace root`. If they ask for confirmation, ask first. If they are silent or leave commits to the user, print the `git commit` command and go on.
  - A line left uncommitted is picked up by `wrap-up`, which commits it when it is the file's only change.

Later workspaces land in the same root and are never asked: one root keeps its `INDEX.md` the single place where every skill finds the live work.

## Moving a root

Move the folder, then edit the line. Nothing else names the path.

## Not the plan root

Plans written outside a workspace live under a different root, named by the `Plan root:` line (default `.plans/`; see the `writing-great-plan` skill's `references/plan-location.md`). The two roots are independent: asking for one never asks for the other, and a workspace's own plans stay in its `plans/NN-<name>/`.
