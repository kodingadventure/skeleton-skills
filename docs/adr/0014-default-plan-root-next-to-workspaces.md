# The default plan root is `.scratch/plans/`, next to the workspace root

Status: accepted

## Context

The default workspace root is `.scratch/workspaces/` (see 0004), but the default plan root was `.plans/`, alone at the repo root. The README now shows how to keep every local note in one folder, with the two roots side by side (`_local/workspaces/` and `_local/plans/`), yet the defaults themselves split the notes across two top-level folders. A user who gives `.scratch/` its own git repository kept a history of their workspaces but not of their plans. No repo used `.plans/` when this was decided.

## Decision

The default plan root is `.scratch/plans/`. When a repo's `Workspace root:` line names a `workspaces/` folder inside another folder (`_local/workspaces/`), the default is its sibling (`_local/plans/`). The plan root stays a separate folder from the workspace root, never the same folder nor one inside it (see 0002). When a repo's workspace root is the older `.scratch/plan/`, the plan root question offers `.plans/` instead, because `.scratch/plan/` and `.scratch/plans/` side by side are the one-letter mix-up 0004 removed.

## Considered options

- **Move the workspace root to `.workspaces/` to match `.plans/`.** Rejected: `.scratch/` is where the `mattpocock/skills` suite keeps local issues and specs, `code-review` looks for specs there, and `.scratch/` as one parent folder is what lets one git repository hold all the notes.
- **One `Notes root:` line that derives both roots.** Rejected: every workspace skill and the reminder hook would change, for a question asked once per repo.

## Consequences

- No fallback for an existing `.plans/` folder: a repo that has one names it with a `Plan root:` line.
- Keep the two default roots under one parent folder; a different default needs a new ADR.
