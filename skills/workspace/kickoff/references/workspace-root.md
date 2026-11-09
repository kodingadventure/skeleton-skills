# Choosing the workspace root

A repo names the folder that holds its workspaces with one line in `CLAUDE.md` or `AGENTS.md`, a path relative to the repo root:

```markdown
Workspace root: `.scratch/workspaces/`
```

Every workspace skill, and the commit reminder hook, reads that line. Without it the root is `.scratch/workspaces/`.

Older versions defaulted to `.scratch/plan/`. A repo that still keeps its workspaces there without a `Workspace root:` line needs `Workspace root: .scratch/plan/` added, or its workspaces are no longer found.

## Asking once

On the repo's first workspace — no `Workspace root:` line in `CLAUDE.md` / `AGENTS.md`, and no `.scratch/workspaces/INDEX.md` — ask the user one question: keep `.scratch/workspaces/` (the default) or name another folder.

- Check the answer is git-ignored (`git check-ignore <root>/x`). When it is not, say so and offer to add it to `.gitignore`; the notes must never be staged from the main repo.
- Write the answer as the `Workspace root:` line, even when it is the default, so the question is never asked again. Put it in `CLAUDE.md`, or in `AGENTS.md` when the repo keeps its agent rules there; near the repo's other workflow notes when there are any.
- That line is a repo change. List it among the files you wrote, to be committed under the repo's rules.

Later workspaces land in the same root and are never asked: one root keeps its `INDEX.md` the single place where every skill finds the live work.

## Moving a root

Move the folder, then edit the line. Nothing else names the path.

## Not the plan root

Plans written outside a workspace live under a different root, named by the `Plan root:` line (default `.plans/`; see the `writing-great-plan` skill's `references/plan-location.md`). The two roots are independent: asking for one never asks for the other, and a workspace's own plans stay in its `plans/NN-<name>/`.
