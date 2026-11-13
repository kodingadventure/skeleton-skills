# skeleton-skills

Agent skills for working with a coding agent in plans and feature workspaces: start from a PRD, turn it into a workspace (`kickoff`), pause and resume across sessions, run a phased plan with a guardian reviewing every phase, and close the work out (`wrap-up`). Decisions that need you go to a short review page instead of a wall of chat.

- **PRD**: your request in your own words, a `PRD.md` file you write by hand or that `spin-off` seeds from a conversation for you to correct.
- **Workspace**: one git-ignored folder per feature or task, holding the PRD and three living documents (`CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`) that every later session reads first.
- **Guardian**: the main session when a plan runs through sub-agents: each phase goes to a sub-agent, and the guardian re-checks and commits its work.
- **Review page**: a short HTML page the agent writes and opens for you when it needs you to read or decide.

Most of it is common ground. The difference is control: skills run when you call them by name, and the agent hands you the decisions on a review page instead of making them. Three skills may also start on their own (see [Which skills start on their own](#which-skills-start-on-their-own)).

## Prerequisites

You need Node.js and an agent that reads skills. Skills are installed with the [`skills`](https://github.com/vercel-labs/skills) CLI, run through `npx` (nothing to install first). Claude Code is the best supported (the `phase-*` executor agents and the commit-reminder hook are Claude Code only).

The examples below use `-a claude-code`. With opencode, pass `-a opencode`; for other agents, `npx skills --help` lists the names.

Some skills depend on the [`mattpocock/skills`](https://github.com/mattpocock/skills) suite (MIT). It is not copied here: install it from its source, pinned to the ref this catalog was checked against.

```bash
npx skills add 'mattpocock/skills#4ae2317' -a claude-code --skill domain-modeling setup-matt-pocock-skills writing-for-agents grilling diagnosing-bugs code-review
```

Then run `/setup-matt-pocock-skills` once in each repo (without slash commands: ask the agent to use the setup-matt-pocock-skills skill). It writes `docs/agents/` (`domain.md`, `issue-tracker.md`, `triage-labels.md`) that several skills read.

| Skill from `mattpocock/skills` | Class                  | What it is for                                                          | Needed by                                                                                                        |
| ------------------------------ | ---------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `domain-modeling`              | required               | Writes ADRs (decision records) and the glossary                         | `wrap-up`, `execute-plan` and `review-phase` (when an ADR is due), `refine-docs`; `discuss` uses it if installed |
| `setup-matt-pocock-skills`     | required               | Creates `docs/agents/domain.md`, `issue-tracker.md`, `triage-labels.md` | `refine-docs`, `update-wiki`, `github-new-issue`, `github-spin-off`; `to-plan` and `execute-plan` carry on without it           |
| `writing-for-agents`           | required for one skill | How to write a skill well                                               | `skill-from-context`                                                                                             |
| `grilling`                     | recommended            | Stress-tests a plan or idea                                             | `discuss`, `skill-from-context`, `whatnext`                                                                      |
| `diagnosing-bugs`              | recommended            | Diagnosis loop when verify keeps failing                                | `execute-plan`                                                                                                   |
| `code-review`                  | recommended            | Full standards-and-spec review                                          | `review-phase`, `whatnext`                                                                                       |

A required skill is needed only by the skills in the last column. When it is missing, that skill stops with a message naming what to install; nothing else is affected. A recommended skill is used "if installed".

## Install

```bash
npx skills add kodingadventure/skeleton-skills
```

The CLI lists the skills and lets you pick, or pass names. To follow the whole flow (a workspace, then a plan), install the `workspace` and `workflow` groups:

```bash
npx skills add kodingadventure/skeleton-skills -a claude-code --skill \
  kickoff discuss tracker pause-here resume-here so-far spin-off wrap-up msg \
  to-plan writing-great-plan execute-plan review-phase guard-plan verify whatnext refine-docs update-wiki
```

Check the current flags with `npx skills --help`.

- **Folders.** The CLI flattens the groups: with Claude Code each skill lands in `.claude/skills/<skill>/`; with opencode and codex in `.agents/skills/<skill>/` (both share it). Installing one skill brings only that skill, so install a group's skills together when they refer to each other.
- **Claude Code plugin.** The same repo is a Claude Code marketplace: `claude plugin marketplace add kodingadventure/skeleton-skills`, then `claude plugin install workspace@skeleton-skills --scope project` (likewise `workflow`, `agent`, `github`).
- **Executor agents.** `guard-plan` dispatches `phase-s`, `phase-m`, `phase-l` and `phase-xl`. The `skills` CLI never installs agents. Install the `phase-agents` plugin once: `claude plugin install phase-agents@skeleton-skills --scope project` (the agents are then named `phase-agents:phase-s` and so on), or copy `plugins/phase-agents/agents/phase-*.md` into `.claude/agents/` (bare names). Without sub-agents, `execute-plan` with `review-phase` does the same job in one session.
- **Reminder hook.** `skills/workspace/hooks/workspace-reminder.mjs` is optional, Claude Code only, and installed by hand: see [skills/workspace/README.md](./skills/workspace/README.md).

### Calling a skill

| Where                                                  | How                                 |
| ------------------------------------------------------ | ----------------------------------- |
| Claude Code plugin                                     | `/workspace:kickoff` (group prefix) |
| Installed with the CLI                                 | `/kickoff` (plain name)             |
| Any other agent (opencode, codex) or no slash commands | "use the kickoff skill"             |

### Which skills start on their own

Only `pause-here`, `spin-off` and `kickoff`. They close a session, split a topic out, and turn a discussion into a workspace the moment you say so, without you typing the name. Every other workspace and GitHub skill runs only when you call it by name.

The Workflow and Agent skills are not manual-only: the agent may pick one when your request matches what it is for ("create a plan", "verify this"), and other skills or a fixed threshold reach them too: `to-plan` calls `writing-great-plan`, `execute-plan` calls `verify` and `review-phase`, `review-page` is used when there are two or more decisions, and `skill-from-context` only offers. They are different from the three above: you do not rely on them starting by themselves, and a skill that routes to another skill needs it to be visible to the agent.

## What is inside

| Group                                     | Skills | What it covers                                                            |
| ----------------------------------------- | ------ | ------------------------------------------------------------------------- |
| [workspace](./skills/workspace/README.md) | 9      | Feature workspaces: discuss, kickoff, pause and resume, spin-off, wrap-up |
| [workflow](./skills/workflow/README.md)   | 9      | Phased plans: write, execute, guard and verify them                       |
| [agent](./skills/agent/README.md)         | 3      | Review pages, skill capture and change explainers                         |
| [github](./skills/github/README.md)       | 3      | Announce, update and import GitHub issues (needs `workspace` and `gh`)    |

The `workflow` skills work alone; inside a feature workspace they also use the `workspace` group. The reverse does not hold: after `kickoff`, the next step is a plan, written by `to-plan` from the `workflow` group.

## Your first workspace

1. Write `.scratch/workspaces/<slug>/PRD.md`: what you want built, in your own words.
2. Discuss it with the agent until the open points are settled (optionally with `/grilling`).
3. Run `/kickoff <slug>`. On the first run it asks where workspaces live and checks the folder is git-ignored.
4. Run `/to-plan`, then `/execute-plan` (one session) or `/guard-plan` (sub-agents).
5. Stop with `/pause-here <slug>`; come back with `/resume-here <slug>`.

The full flow, with every other command, is in [skills/workspace/README.md](./skills/workspace/README.md#the-flow).

## Configuration

Two optional lines in the repo's `CLAUDE.md` or `AGENTS.md`; the skills ask once and write them for you.

```markdown
Workspace root: `.scratch/workspaces/`
Plan root: `.plans/`
```

`Workspace root:` is where feature workspaces live; `Plan root:` is where plans written outside a workspace live. Both defaults are shown above, and both folders must be git-ignored.

## Versions

The whole repo has one version, tracked in `CHANGELOG.md`, which records what changed. Pin to a tag if you want a fixed version: `npx skills add 'kodingadventure/skeleton-skills#v0.1.0' ...`.

## Contributing

Problem reports go to [GitHub Issues](https://github.com/kodingadventure/skeleton-skills/issues). To work on the skills themselves, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Credits

- [Matt Pocock](https://github.com/mattpocock/skills) (MIT) — the suite above is a dependency, not copied.
- [`caveman-commit`](https://github.com/JuliusBrussee/caveman) by JuliusBrussee — optional, for short commit messages; not part of this catalog.

## License

[MIT](./LICENSE)
