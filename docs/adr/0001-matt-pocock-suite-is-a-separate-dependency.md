# The Matt Pocock suite is a separate dependency, not copied here

Status: accepted

## Context

Several skills here hand off to skills from [`mattpocock/skills`](https://github.com/mattpocock/skills) (MIT), such as `domain-modeling`, `grilling` and `setup-matt-pocock-skills`. This catalog once republished copies of them. A consumer that installed a copy got a lockfile entry crediting this repo as the `source`, and `skills update` pulled the suite from our copy instead of from its author. The `source` field is written by the CLI from where a skill was installed, so no manifest note can correct it.

## Decision

The suite is installed separately, from its own source, pinned to the ref this catalog was checked against. This repo does not list, vendor or commit any of its skills. Skills here that need one keep naming it, the way they name any optional skill. The README lists each needed skill, whether it is required or optional, and which skills use it.

## Consequences

- A skill that needs a suite skill stops with a clear message before it changes anything when that skill is missing.
- The README table of needed suite skills and the pinned ref are kept in step with what the skills actually call.
- Do not add suite skills to a manifest or commit copies of them. The `skills` CLI discovers skills under a source repo's `.claude/skills/` whatever a manifest lists, so such a folder must not be committed either. A change here needs a new ADR.
