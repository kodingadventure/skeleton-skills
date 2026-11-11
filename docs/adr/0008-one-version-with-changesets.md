# One version for the whole repo, managed with changesets

Status: accepted

## Context

People outside the owner's projects install these skills and may want a fixed version. A per-skill version would multiply bookkeeping for a small catalog.

## Decision

The whole repo has one version, starting at 0.x during the test period. Every change under `skills/` or `plugins/` ships with one changeset; documentation-only changes, including ADRs, need none. Versions are bumped only by the "version" pull request that a GitHub Action opens after a push to `main`; merging it tags the release. Nobody bumps the version by hand. The owner's own projects follow the latest version; outsiders may pin to a tag, as the README shows.

## Consequences

- Changeset text is merged into `CHANGELOG.md`, which is committed, so release notes survive even if history is squashed. Only the `v0.x` tags are lost when the repo is recreated.
- Do not move to per-skill versions, hand-edited version numbers, or skip the changeset for a skill change without a new ADR.
- Once outside users pin to tags, tags must not be rewritten or removed.
