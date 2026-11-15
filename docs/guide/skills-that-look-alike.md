# Skills that look alike

This page answers one question: which of two similar skills do you call? Five pairs, each with a rule of thumb and a table.

"Starts on its own?" asks whether the agent may run a skill without you naming it. `pause-here`, `spin-off` and `kickoff` do, when you say so ("let's stop for today"). `execute-plan`, `guard-plan`, `refine-docs` and `update-wiki` are picked only when your request matches what they are for, so call them by name when it matters. The rest are manual-only. The rest of the story is in the [README](../../README.md#which-skills-start-on-their-own).

## `spin-off` and `kickoff`

Use `spin-off` to move one thread out of a running session. Use `kickoff` to turn a PRD discussion into a full workspace.

| | `spin-off` | `kickoff` |
| --- | --- | --- |
| Use it when | A long session wandered, and one topic deserves its own workspace | You have a `PRD.md` (yours, or seeded by `spin-off`), discussed it, and want to track the work |
| What it writes | In an existing workspace: a handoff, findings, and a next step in `WHATNEXT.md`. In a new one: `PRD.md`, an origin brief, and minimal `CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`. A new workspace is not live until `kickoff` runs | `CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`, the folder layout and the `INDEX.md` row |
| Starts on its own? | Yes, when you say so. You still confirm the slice and the destination | Yes, when you say so |

## `resume-here` and `discuss`

Use `resume-here` to do the next step. Use `discuss` to think about it first.

| | `resume-here` | `discuss` |
| --- | --- | --- |
| Use it when | A fresh session should pick up where the last one stopped | You want to talk a topic through before any work starts |
| What it writes | Whatever the next step produces. It first reads `WHATNEXT.md`, `CONTEXT.md` and the handoff `WHATNEXT.md` names, and checks them against git | No code, and no commits in your repo (it commits only the workspace notes, when your rules say so). Anything you settle is recorded in the workspace files |
| Starts on its own? | No (manual-only) | No (manual-only) |

## `execute-plan` and `guard-plan`

Use `execute-plan` to run a plan in this session. Use `guard-plan` to hand each phase to a sub-agent while this session checks the result.

| | `execute-plan` | `guard-plan` |
| --- | --- | --- |
| Use it when | You want the plan done in this session, one item at a time | You want each phase done by an executor agent, and this session to be the guardian |
| What it writes | The code, with the plan's boxes ticked. It stages and hands off, or commits, as the plan's `Review:` line and your repo's rules say. With `Review: guardian` it stops after staging each phase and waits for `/review-phase` | Each phase goes to the `phase-s`, `phase-m`, `phase-l` or `phase-xl` agent that matches its Weight. The guardian re-checks, fixes, and commits only if the run mode you chose when it started allows it. It does not push unless you ask, or your repo's rules require it |
| Starts on its own? | Maybe: the agent may pick it when your request matches | Maybe: the agent may pick it when your request matches |

`guard-plan` needs sub-agents and the `phase-*` agents, which means Claude Code. Install them as the "Executor agents" bullet under [Install](../../README.md#install) says. Without them, `execute-plan` with `review-phase` does the same job in one session.

## `refine-docs` and `update-wiki`

Use `refine-docs` for reference docs, glossaries and ADRs. Use `update-wiki` for flow pages and the feature index.

| | `refine-docs` | `update-wiki` |
| --- | --- | --- |
| Use it when | A pattern changed, a term needs recording, or a decision needs an ADR | A commit changed a business rule, a status, a route or a screen |
| What it writes | Architecture reference docs, glossary entries, ADRs, and the repo's `## Docs Layout` block | Flow pages that cross code units, the feature index, a `### Wiki` table in the Docs Layout, and a page of deliberately kept wrong behaviour when the repo has one |
| Starts on its own? | Maybe: the agent may pick it when your request matches | Maybe: the agent may pick it when your request matches |

Both read `docs/agents/domain.md`, which `/setup-matt-pocock-skills` creates.

## `pause-here` and `wrap-up`

Use `pause-here` to stop for now. Use `wrap-up` when the feature is finished.

| | `pause-here` | `wrap-up` |
| --- | --- | --- |
| Use it when | You stop for today, or `WHATNEXT.md` is stale | Every work item is done |
| What it writes | `WHATNEXT.md`, `TRACKER.md`, findings, questions, and a handoff when needed. The workspace stays live | The ADRs still owed, durable findings moved into the repo, a final report if the workspace has an audience, and the `INDEX.md` row moved to Shipped. You delete the folder yourself |
| Starts on its own? | Yes, when you say so | No (manual-only) |

The reason `wrap-up` exists is in [Documentation and wrap-up](./documentation-and-wrap-up.md).

Next: [What is in a workspace](./workspace-files.md)
