# Plans outside a workspace live in a repo-named plan root, and no file marks the active plan

Status: accepted

## Context

Plan-writing skills used one fixed output path per feature, so a second plan for the same feature overwrote the first, and nothing said which of several plans a skill should run. Tools that keep an "active plan" marker file showed the same weakness in testing: the marker drifted from the plan files, and a new plan displaced the active one without closing it.

## Decision

The plan root is named once, by a `Plan root:` line in `CLAUDE.md` or `AGENTS.md`. It is asked for when the repo's first plan is written outside a workspace, and checked to be git-ignored. Every plan is a dated subfolder, so no plan overwrites another.

Skills choose the plan to run from its `**Status:**` line: exactly one open plan runs, several are asked about. A new plan never changes an older plan's Status; only the owner marks one `abandoned`. A repo's older plan-output key keeps working as a fallback.

## Considered options

- Reusing the workspace root: rejected. A plan without a workspace's overview would mix with workspaces.
- A marker file for the active plan: rejected. It is a second copy of a fact the plan already holds, and it drifts.
- A new plan closing the old one: rejected. A half-done plan is lost without the owner noticing.

## Consequences

- Do not add an active-plan marker, and do not let a new plan edit another plan's Status.
- Someone who runs two plans on purpose is asked which one every time.
