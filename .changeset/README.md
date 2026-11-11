# Changesets

Run `npx changeset` to record a change: pick `patch` for a fix or `minor` for new behavior, and write one or two lines for the user (which skill, what is different). Every change under `skills/` or `plugins/` needs one changeset; documentation-only changes do not. Never bump the version by hand: the "chore: version skills" pull request from the release Action does it.
