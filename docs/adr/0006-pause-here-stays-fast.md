# `pause-here` stays fast

Status: accepted

## Context

`pause-here` is used when a session must close soon: it brings the workspace's next-step file, tracker and open questions up to date. A suggestion to add a longer check to it, for example running the project's verification, came up and was rejected.

## Decision

`pause-here` only writes the handoff. It does not call slow checks such as `verify`, a test run or a full audit. If something needs checking, it records that as the next step for the next session.

## Consequences

- Do not make `pause-here` run or wait for a long command, and do not chain another skill into it that does.
- A stale or unverified state is recorded in the handoff, not resolved during the pause.
