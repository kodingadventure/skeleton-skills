# Contributing

## Reporting a problem

Open a [GitHub issue](https://github.com/kodingadventure/skeleton-skills/issues). One problem per issue, and put the steps that show the problem first: which skill, what you asked, what it did, what you expected. If an agent drafts the issue for you, keep it short and describe the problem rather than pasting a rewritten `SKILL.md`.

## Working on the skills

```bash
git clone git@github.com:kodingadventure/skeleton-skills.git
cd skeleton-skills
npm install
```

`npm install` also links every skill under `skills/` into this repo's `.claude/skills/`, and the executor agents into `.claude/agents/`, so a Claude Code session opened here runs the versions you are editing. The links stay inside this repo: your other projects keep the released versions they installed. Re-run `npm run link-skills` after adding, removing or renaming a skill. Never commit `.claude/skills/` or `.claude/agents/` (they are git-ignored): the `skills` CLI would install whatever it finds there ([ADR 0001](./docs/adr/0001-matt-pocock-suite-is-a-separate-dependency.md)).

Before you change a skill, read:

- [`CLAUDE.md`](./CLAUDE.md): the repo rules agents follow here.
- [`docs/agents/verify.md`](./docs/agents/verify.md): the checks to run for each kind of change (`npm run format:check` for `skills/` and `plugins/`).
- [`docs/agents/publish-skill.md`](./docs/agents/publish-skill.md): adding a new skill.
- [`docs/adr/`](./docs/adr/): decisions that look like bugs from inside the code but are deliberate.

Every change under `skills/` or `plugins/` needs one changeset: run `npx changeset`, pick `patch` for a fix or `minor` for new behavior, and write one or two lines for users (which skill, what is different). Documentation-only changes need none. Never bump the version by hand.
