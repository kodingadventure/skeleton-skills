# `guard-plan` derives its commit mode from the repo's rules

Status: accepted

## Context

`guard-plan` asked at preflight how to run: commit each phase or print the command, go on automatically or stop after each phase. The point of `guard-plan` is a plan that runs without someone watching each phase, so the question was friction, and the repo's commit rules already answer it: in a repo that forbids agent commits, going on automatically is impossible, because the next phase would pile onto uncommitted changes and the per-phase diffs would mix.

## Decision

`guard-plan` asks nothing. It greps `CLAUDE.md`, `CLAUDE.local.md` and `AGENTS.md` for commit rules, announces one of three commit modes and records it under the plan's `## Baseline`, re-derived every session:

- `commit` — no commit rule, or one that lets the agent commit: commit each phase and go on.
- `confirm` — a rule that asks for confirmation, or an ambiguous one ("Commit only when the user asks"): show the diff summary, ask, commit when approved, go on.
- `print` — a rule that forbids agent commits: stage, print the commit command, wait, and check the commit exists before going on.

It never pushes unless the user asks or the repo's rules require it.

## Considered options

- **Keep asking the run mode.** Rejected: a question whose answer the repo already holds.
- **Commit even when the repo forbids it, because the user invoked `guard-plan`.** Rejected: the skill would contradict the repo's rules, and the rule may be someone else's team policy. A user who wants it adds an exception for `guard-plan` to their rule (the guide shows how).
- **Ambiguous rules read as permission.** Rejected: misreading a prohibition as permission commits in a repo that forbids it; the opposite mistake costs one question per phase.

## Consequences

- There is no "stop after each phase" option any more; a user who wants to look at each phase writes a confirmation rule.
