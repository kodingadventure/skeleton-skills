# skeleton-skills

A catalog of agent skills that take a feature from discussion to a reviewed commit: workspaces, plans, guarded execution and documentation.

## Language

**Commit mode**:
How the guardian treats each guarded phase — commit it (`commit`), ask before committing it (`confirm`), or stage it and wait for the user's commit (`print`) — derived from the repo's own commit rules.
_Avoid_: Run mode

**Manual Test Checkpoint**:
A point in a plan, after a named phase, where the changed behaviour is driven at its real surface and its observed result compared with the expected one.
_Avoid_: Smoke test, QA step

**Runner**:
Who carries out a plan item or a Manual Test Checkpoint that is not the executor's: the guardian (an agent) or a human.
_Avoid_: Owner, actor
