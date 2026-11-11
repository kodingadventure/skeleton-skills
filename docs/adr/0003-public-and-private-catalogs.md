# General skills live in the public catalog; project-specific skills stay private

Status: accepted

## Context

Skills useful to anyone and skills tied to one team's projects were kept in one catalog. Releasing the general ones meant deciding where they are edited, and what happens to consumers that already pull from the old location.

## Decision

Released skills are edited only in the public repo; this is the single place to edit them. Project-specific skills stay in a private catalog. One project may install from both sources. A copy of a released skill left in the private catalog is retired and deleted, and only after every consumer that uses it has installed from the public repo.

When the public repo takes a name an existing repo already uses, the existing repo is renamed first and its consumers are repointed to the new name before the public repo is created. A rename redirect stops working as soon as a new repo takes the old name, and consumers would then pull silently from the new repo and lose the project-specific skills.

## Consequences

- Do not edit a released skill in the private catalog, and do not move a project-specific skill into the public repo without an explicit decision.
- A consumer's lockfile `source` shows which catalog a skill came from; a skill installed from the wrong one is a drift to fix, not a style choice.
- Reusing an old repo name for a different repo breaks consumers that still point at it. Repoint them first.
