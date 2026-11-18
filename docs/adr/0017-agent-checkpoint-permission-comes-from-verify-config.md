# What an agent may drive in a checkpoint comes from the verify config

Status: accepted

## Context

A checkpoint marked for an agent needs a source for "which surfaces may the agent drive itself, and how". The `verify` skill already reads that from `docs/agents/verify.md`: a `## Runtime policy` and a `## Surfaces` table, written once per repo.

## Decision

The plan writer reads the target repo's runtime policy and surfaces table, and marks a checkpoint `Runner: guardian` only when the policy lets the agent drive every surface its scenarios touch and the table says how. A repo with no `verify.md`, or no runtime policy, gets `Runner: human` on every checkpoint. No repo needs a separate manual-test document; a surface row may point to one when its setup is long (this repo points to `docs/agents/manual-test.md`).

## Considered options

- **A manual-test document required in every repo.** Rejected: a second source of "what the agent may drive" that drifts from the one `verify` uses.
