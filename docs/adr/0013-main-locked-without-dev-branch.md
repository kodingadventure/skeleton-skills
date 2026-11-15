# `main` is locked by a ruleset and there is no `dev` branch

Status: accepted

## Context

The repo became public with `main` as the branch people install from. Installing without a pin takes the latest `main`. Work reaches `main` through a feature branch and a pull request, and the changeset Action then opens a "chore: version skills" pull request whose merge is the release and the tag (see 0008).

## Decision

`main` is protected by a GitHub ruleset: it cannot be deleted, force pushes are blocked, and every change goes through a pull request (zero required approvals, no required status checks, because no CI runs on pull requests). Repository admins may bypass the ruleset through a pull request only. There is no `dev` branch: feature branches open pull requests straight into `main`, and the changeset flow is unchanged.

## Considered options

- **A `dev` branch that merges into `main` at release.** Rejected: every change needs two pull requests, a fix needed in the maintainer's own projects waits for the merge to `main`, the changeset workflow and the "default branch" assumptions in `wrap-up` and `pause-here` would need changes, and `dev` and `main` can drift apart when a merge is forgotten. For one maintainer, the only gain is that `main` moves at release time.
- **Required approvals or required status checks.** Rejected for now: a sole maintainer would lock themselves out, and a required check with no workflow behind it blocks every pull request.

## Consequences

- `main` can hold changes whose changeset is not released yet. Someone who installs without a pin gets them; someone who wants a stable version pins to a release tag (the README shows the pin with a placeholder, `#vX.Y.Z`).
- The ruleset is easy to change in the repo settings. If CI is added for pull requests, add it as a required check then.
- Agents never push, merge or change repo settings (see `CLAUDE.md`): the owner merges the pull request.
