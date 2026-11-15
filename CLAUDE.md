## Agent skills

### Language Policy

- All project code, comments, docs, commit messages — must be in English only.

### Commits

The agent commits its own reviewed work (the guardian commits each phase after review). It never pushes, merges, opens or closes a pull request, or changes repo settings or visibility: those need the owner's permission, one at a time.

### Issue tracker

Issues live in GitHub Issues `kodingadventure/skeleton-skills`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage roles, label string equal to the role name. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Adding or changing a skill

Gates and sequencing: `docs/agents/verify.md`. Steps for a new skill (group, manifest, README bullet, invocation choice): `docs/agents/publish-skill.md`. Known failure modes: `docs/agents/failure-modes.md`. Manual test of a skill change (a plan checkpoint, a re-test after a fix, a new skill): `docs/agents/manual-test.md`.

### Skills in this repo's own sessions

`npm install` (and `npm run link-skills`) links `skills/*/*` and the phase agents into `.claude/skills/` and `.claude/agents/`, so sessions here run the working copy. Re-run `npm run link-skills` after adding, removing or renaming a skill. Never commit those two folders (`docs/adr/0001`).

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
