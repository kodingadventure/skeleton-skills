# Workspace and GitHub skills are invoked by name

Status: superseded by ADR 0018

## Context

A skill description can be written so the agent starts the skill on its own when the conversation seems to match. That is convenient, but it starts work the user did not ask for, and the skills here change files, stage commits and write handoffs.

## Decision

Workspace and GitHub skills run only when the user names them (`disable-model-invocation: true`). A skill there that does not start on its own is intended, so control stays with the user. The only exceptions are `pause-here`, `spin-off` and `kickoff`: they close a session, split a topic out and turn a discussion into a workspace the moment the user says so, without typing the name. They are listed in the README.

Workflow and Agent skills deliberately carry no such flag: other skills hand off to them (`to-plan` to `writing-great-plan`, `execute-plan` to `verify`), and the agent may open a `review-page` when a decision calls for one. They change nothing the user has not asked for without a confirmation step.

## Considered options

- Auto-trigger hooks that start a skill from a keyword or a tool event: rejected. They run at moments the user did not choose, and a false match costs a wrong edit or a noisy handoff.
- Broad descriptions that make every skill match loosely: rejected for the same reason.

## Consequences

- Do not add auto-trigger hooks or widen descriptions to make a skill start by itself. "Fixing" a skill that did not start on its own is not a bug fix.
- Do not add `disable-model-invocation` to Workflow or Agent skills, or remove it from Workspace and GitHub skills, without a new ADR.
- Adding a skill to the exception list needs a new ADR and a README change.
