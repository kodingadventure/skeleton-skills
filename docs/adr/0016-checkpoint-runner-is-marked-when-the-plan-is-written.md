# Who runs a manual test checkpoint is marked when the plan is written

Status: accepted

## Context

Some manual test checkpoints can be driven by an agent (a CLI, a bounded script, an endpoint), others need a person (a device, a visual judgement, a login). Someone has to decide which is which, and the guardian that runs the plan is the one tempted to decide on the fly, or to bend a scenario until an agent can run it.

## Decision

The plan writer marks every checkpoint `Runner: guardian` (an agent runs it) or `Runner: human`, with the same field items use, and the user changes the mark while reviewing the plan. A checkpoint with no `Runner:` line belongs to the person, the reverse of an item, so older plans keep stopping for the user. Scenarios are written the same way for both runners; only the wrapping differs.

At run time the guardian may adapt how a scenario is run to the code (a route name, a flag, a setup step) as a `Plan correction`. It may not weaken or drop a scenario, or change an expected result to match the code; when that seems needed, it stops and asks. A mark may move from agent to person when the agent cannot drive the surface, never the other way.

## Considered options

- **The guardian decides at run time.** Rejected: the user never sees the choice, and the runner who benefits from an easier scenario is the one choosing.
- **Ask at each checkpoint.** Rejected: one more pause in a run meant to go unattended; plan review is the one point the user is already there.
