# Workflow

Plan-driven delivery: turn a spec into a phased plan, run it, and check every phase before it is committed. The workflow skills work alone; inside a feature workspace they also use the workspace group.

- **[to-plan](./to-plan/SKILL.md)** — Turns a spec, issue or conversation into a phased `IMPLEMENTATION_PLAN.md`. Use it when there is something to build and nothing yet says in what order.
- **[writing-great-plan](./writing-great-plan/SKILL.md)** — The rules a plan follows (weights, atomic checkboxes, splitting, required sections). Called by `to-plan`; not meant to be started by hand.
- **[execute-plan](./execute-plan/SKILL.md)** — Works through the unchecked items one at a time, staging or committing per the plan's `Review:` line. Use it for a plan you want to run in this session.
- **[review-phase](./review-phase/SKILL.md)** — Reviews one staged phase before it is committed: re-runs its checks, fixes what is wrong, prepares the commit. Use it after `execute-plan` under `Review: guardian`.
- **[guard-plan](./guard-plan/SKILL.md)** — Runs a multi-file plan with the session as guardian and one executor sub-agent per phase. Use it when the agent can start sub-agents and you want to save tokens.
- **[verify](./verify/SKILL.md)** — Runs the project's gates for the paths a change touches, then drives the change where it runs. Called by `execute-plan`; also usable before any commit.
- **[whatnext](./whatnext/SKILL.md)** — Reads the workspace, plans and git state and names the single next step and the skill for it. Use it when unsure what to do.
- **[refine-docs](./refine-docs/SKILL.md)** — Keeps architecture docs, glossaries and ADRs current in the layout the repo declares in `docs/agents/domain.md`. Use it when a pattern or decision should be written down.
- **[update-wiki](./update-wiki/SKILL.md)** — Writes the wiki: flow pages across code units, the feature index and, if kept, the preserved-behaviour page, from committed changes. Use it after a commit that changed what the system does.

## Running a plan

| Situation                        | Skills                                            |
| -------------------------------- | ------------------------------------------------- |
| No sub-agents                    | `execute-plan`                                    |
| No sub-agents, review each phase | `execute-plan` with `review-phase`                |
| Sub-agents available             | `guard-plan` (dispatches the `phase-*` executors) |

From idea to commit: discuss or write the spec, `to-plan`, one of the rows above, `verify`, commit. `whatnext` names the step when you lose the thread.

## Keeping the docs current

Four parts, all reading the doc map in `docs/agents/domain.md`:

- `to-plan` ends a feature plan that changes behaviour with a docs phase: one item per installed documentation skill, reviewed and committed like the code (`writing-great-plan` holds the rule).
- `refine-docs` writes the doc map; its `### Wiki` table says where the flow pages, the index and the optional preserved-behaviour page live. It commits under the repo's rules, except inside a plan phase.
- `update-wiki` writes the wiki pages from commits, and commits them when the repo's rules let the agent commit; inside a plan phase the plan runner commits.
- `whatnext` suggests the docs step once after a plan's last phase, or right away for a commit outside a plan, and stays quiet once a docs phase or a later commit has touched the docs; without `update-wiki` it suggests `refine-docs`.

All need `docs/agents/domain.md` from `setup-matt-pocock-skills` (`mattpocock/skills`). A repo without a wiki gets a docs phase only when there is something to write, through `refine-docs`.

## Stand-alone and paired

`to-plan` needs `writing-great-plan`, and `execute-plan` uses `verify` and `review-phase`; install those together. `guard-plan` needs the `phase-*` agents below. `update-wiki` is installed with `refine-docs`. The rest stand alone.

Plans written outside a workspace go under the `Plan root:` line of `CLAUDE.md` / `AGENTS.md` (default `.scratch/plans/`, next to the default workspace root); inside a workspace they go to `plans/NN-<name>/`.

## Executor agents

`guard-plan` dispatches `phase-s`, `phase-m`, `phase-l` and `phase-xl`, chosen by each phase's Weight. The `skills` CLI never installs agents. Two ways to get them:

- The `phase-agents` Claude Code plugin: `claude plugin marketplace add kodingadventure/skeleton-skills`, then `claude plugin install phase-agents@skeleton-skills --scope project`. The agents are named `phase-agents:phase-s` and so on; a bare `phase-s` is rejected.
- Copy `plugins/phase-agents/agents/phase-*.md` into `.claude/agents/`; the names stay bare.

`guard-plan` asks the agent which names exist and uses them as listed.

## Which skills start on their own

These are not manual-only: the agent may pick one when your request matches what it is for ("create a plan", "execute the plan"), and a skill or a fixed threshold may reach them without you typing the name: `writing-great-plan` is called by `to-plan`; `verify` and `review-phase` by `execute-plan`; `review-page` (agent group) when there are two or more decisions. `skill-from-context` only offers. That differs from the three workspace skills that start on their own (`kickoff`, `pause-here`, `spin-off`), which exist so you need not type the name mid-discussion.

## Dependencies

`refine-docs` and `update-wiki` need `docs/agents/domain.md` from `setup-matt-pocock-skills` and stop with a message naming it when missing. `to-plan` and `execute-plan` carry on without it, using `GLOSSARY.md` and `docs/adr/` at the repo root when they exist. `execute-plan` and `review-phase` need `domain-modeling` only when an ADR is due; `diagnosing-bugs` and `code-review` are used if installed. All come from [`mattpocock/skills`](https://github.com/mattpocock/skills); see the [root README](../../README.md) for the table and the pinned command.
