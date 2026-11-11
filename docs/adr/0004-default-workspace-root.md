# The default workspace root is `.scratch/workspaces/`

Status: accepted

## Context

Feature workspaces used to default to `.scratch/plan/`, while plans written outside a workspace go under `.scratch/plans/` (see 0002). The two names differ by one letter, so people and agents put files in the wrong one.

## Decision

The default workspace root is `.scratch/workspaces/`. A repo may choose any folder with a `Workspace root:` line in `CLAUDE.md` or `AGENTS.md`. Repos that already keep workspaces under `.scratch/plan/` add the line `Workspace root: .scratch/plan/` instead of moving anything.

## Consequences

- Do not change the default back to a name close to the plan root's. A different default needs a new ADR.
- Skills read the root from the `Workspace root:` line first and fall back to the default only when it is absent.
- Both roots must be git-ignored.
