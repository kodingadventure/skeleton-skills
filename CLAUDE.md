## Agent skills

### Language Policy

- All project code, comments, docs, commit messages — must be in English only.

### Issue tracker

Issues live in GitHub Issues `kodingadventure/skeleton-skills`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage roles, label string equal to the role name. See `docs/agents/triage-labels.md`.

### Adding or changing a skill

Gates and sequencing: `docs/agents/verify.md`. Steps for a new skill (group, manifest, README bullet, invocation choice): `docs/agents/publish-skill.md`. Known failure modes: `docs/agents/failure-modes.md`.

### Decisions

Architecture decisions: `docs/adr/`. Read the matching ADR before changing a behavior it records.

### Versioning

Every change under `skills/` or `plugins/` ships with one changeset (`npx changeset`): `patch` for a fix, `minor` for new behavior. Write it for the user: which skill, and what is different. Documentation-only changes need no changeset. Never bump the version by hand; the "chore: version skills" pull request from the release Action does it.

### Feature workspaces

Workspace root: `_local/workspaces/`

`_local/` is gitignored and holds its own git repository — never stage it from this repo.

### Plan root

Plans written outside a workspace go under the root below.

Plan root: `_local/plans/`
