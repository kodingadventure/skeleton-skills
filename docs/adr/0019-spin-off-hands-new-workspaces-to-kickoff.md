# `spin-off` hands new workspaces to `kickoff`; no seeded stage

Status: accepted

## Context

`spin-off` and `github-spin-off` used to leave a new workspace "seeded": a `PRD.md`, an origin brief and minimal `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` with `TBD (kickoff)` fields, listed under `## Seeded` in `INDEX.md` until the user ran `/kickoff`. Once `kickoff` could write a `PRD.md` from the conversation itself, the half-set-up stage only added a step, and its readers (`kickoff`, `discuss`, `whatnext`, the index template) carried a second shape of workspace.

## Decision

For a new workspace, `spin-off` writes `PRD.md` and the origin brief from the slice only (`github-spin-off` from the issue), then runs `kickoff` on that folder, telling it to read those two files and not the conversation. The workspace is active at once, under `## Active`, with no parked status. Settled decisions travel in the brief's `## Decided` section. For an existing workspace, `spin-off` still writes a handoff. `## Seeded` and every reader of it are removed, with no compatibility path.

## Considered options

- **`kickoff` writes the PRD from the whole conversation.** Rejected: the other threads of the session would leak into the new workspace's PRD; the slice is `spin-off`'s job.
- **Keep the new workspace parked (`paused`) until someone works on it.** Rejected: `/whatnext` would stop recommending it, and backlog nobody is pointed at gets forgotten.
- **Keep the seeded stage (spin-off → discuss → kickoff).** Rejected: two shapes of workspace for one extra step, now that `kickoff` writes the PRD itself.

## Consequences

- A spun-off workspace asks `kickoff`'s question round (report audience and the rest) in the session that spun it off.
- Without `kickoff` installed, `spin-off` stops after `PRD.md` and the brief and writes no `INDEX.md` row.
