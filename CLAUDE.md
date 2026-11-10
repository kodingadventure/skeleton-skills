## Agent skills

### Language Policy

- All project code, comments, docs, commit messages — must be in English only.

### Issue tracker

Issues and specs live as markdown files under `.scratch/<feature-slug>/` (gitignored).

### Adding or changing a skill

Gates and sequencing: `docs/agents/verify.md`. Steps for a new skill (group, manifest, README bullet, invocation choice): `docs/agents/publish-skill.md`. Known failure modes: `docs/agents/failure-modes.md`.

### Feature workspaces

Workspace root: `_local/workspaces/`

`_local/` is gitignored and holds its own git repository — never stage it from this repo.

### Plan root

Plans written outside a workspace go under the root below.

Plan root: `_local/plans/`
