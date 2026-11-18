# skeleton-skills

A catalog of agent skills that take a feature from discussion to a reviewed commit: workspaces, plans, guarded execution and documentation.

## Language

**Commit mode**:
How the guardian treats each guarded phase — commit it (`commit`), ask before committing it (`confirm`), or stage it and wait for the user's commit (`print`) — derived from the repo's own commit rules.
_Avoid_: Run mode
