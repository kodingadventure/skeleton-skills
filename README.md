# skeleton-skills

Agent skills for people who forget what they were doing yesterday. (Hi, that's me.)

Skills for working with a coding agent in plans and feature workspaces: start from a PRD, turn it into a workspace (`kickoff`), pause and resume across sessions, run a phased plan with a guardian reviewing every phase, and close the work out (`wrap-up`). Decisions that need you go to a short review page instead of a wall of chat.

- **PRD**: your request in your own words, a `PRD.md` file you write by hand or that `spin-off` seeds from a conversation for you to correct.
- **Workspace**: one git-ignored folder per feature or task, holding the PRD and three living documents (`CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`) that every later session reads first.
- **Guardian**: the main session when a plan runs through sub-agents: each phase goes to a sub-agent, and the guardian re-checks and commits its work.
- **Review page**: a short HTML page the agent writes and opens for you when it needs you to read or decide.

A short tour (about 90 seconds, shorter than your coffee break):

[![A short tour of skeleton-skills](https://img.youtube.com/vi/yoQ7tD5FEtE/maxresdefault.jpg)](https://youtu.be/yoQ7tD5FEtE)

Most of it is common ground. The difference is control, and you keep it: skills run when you call them by name, and the agent hands you the decisions on a review page instead of making them. A few may also start on their own (see [Which skills start on their own](#which-skills-start-on-their-own)).

## Guide

New here? Read the [guide](./docs/guide/README.md) first. It's shorter than this README, I promise 🤞 It covers how to start in a new or an existing project, one feature followed from PRD to wrap-up, how the look-alike skills differ, and an FAQ.

## Prerequisites

You need Node.js and an agent that reads skills. Skills are installed with the [`skills`](https://github.com/vercel-labs/skills) CLI, run through `npx` (nothing to install first). Claude Code is the best supported (the `phase-*` executor agents and the commit-reminder hook are Claude Code only).

The examples below use `-a claude-code`. With opencode, pass `-a opencode`; for other agents, `npx skills --help` lists the names.

Some skills depend on the [`mattpocock/skills`](https://github.com/mattpocock/skills) suite (MIT). It is not copied here: install it from its source, pinned to the ref this catalog was checked against.

```bash
npx skills add 'mattpocock/skills#4ae2317' -a claude-code --skill domain-modeling setup-matt-pocock-skills writing-for-agents grilling diagnosing-bugs code-review
```

Then run `/setup-matt-pocock-skills` once in each repo (without slash commands: ask the agent to use the setup-matt-pocock-skills skill). It writes `docs/agents/` (`domain.md`, `issue-tracker.md`, `triage-labels.md`) that several skills read.

| Skill from `mattpocock/skills` | Class                  | What it is for                                                          | Needed by                                                                                                             |
| ------------------------------ | ---------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `domain-modeling`              | required               | Writes ADRs (decision records) and the glossary                         | `wrap-up`, `execute-plan` and `review-phase` (when an ADR is due), `refine-docs`; `discuss` uses it if installed      |
| `setup-matt-pocock-skills`     | required               | Creates `docs/agents/domain.md`, `issue-tracker.md`, `triage-labels.md` | `refine-docs`, `update-wiki`, `github-new-issue`, `github-spin-off`; `to-plan` and `execute-plan` carry on without it |
| `writing-for-agents`           | required for one skill | How to write a skill well                                               | `skill-from-context`                                                                                                  |
| `grilling`                     | recommended            | Stress-tests a plan or idea                                             | `discuss`, `skill-from-context`, `whatnext`                                                                           |
| `diagnosing-bugs`              | recommended            | Diagnosis loop when verify keeps failing                                | `execute-plan`                                                                                                        |
| `code-review`                  | recommended            | Full standards-and-spec review                                          | `review-phase`, `whatnext`                                                                                            |

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
- **Reminder hook.** `skills/workspace/hooks/workspace-reminder.mjs` is optional, Claude Code only, and installed by hand: see [skills/workspace/README.md](./skills/workspace/README.md). When it helps, and how to check it is installed: [the FAQ](./docs/guide/faq.md#what-is-the-commit-reminder-hook-and-do-i-need-it).

### Calling a skill

| How you installed               | What you type                      |
| ------------------------------- | ---------------------------------- |
| Claude Code plugin              | `/workspace:kickoff` (group first) |
| `skills` CLI                    | `/kickoff` (plain name)            |
| An agent without slash commands | "use the kickoff skill"            |

The rest of this README uses plain names; add the group in front if you installed the plugin.

Asking in words only works for skills the agent may pick by itself. Most workspace and GitHub skills are manual-only on purpose, so in Claude Code they need the slash command: "use the discuss skill" gets you a confused agent, `/discuss` gets you a discussion.

### Which skills start on their own

Two kinds of skills can start without you typing the name:

- **Three workspace skills: `pause-here`, `spin-off` and `kickoff`.** They close a session, split a topic out, and turn a discussion into a workspace the moment you say so ("let's stop for today", "spin this off").
- **The Workflow and Agent skills.** The agent may pick one when your request matches what it is for ("create a plan", "verify this"), and some are called by other skills: `to-plan` calls `writing-great-plan`, `execute-plan` calls `verify` and `review-phase`, `review-page` steps in when there are two or more decisions, and `skill-from-context` only offers. Don't count on them starting by themselves, though: call them by name when it matters. A skill that calls another needs that one installed too.

Everything else (the other workspace skills and all GitHub skills) is manual-only: it runs only when you call it by name. That's on purpose: you stay in control.

## What is inside

| Group                                     | Skills | What it covers                                                            |
| ----------------------------------------- | ------ | ------------------------------------------------------------------------- |
| [workspace](./skills/workspace/README.md) | 9      | Feature workspaces: discuss, kickoff, pause and resume, spin-off, wrap-up |
| [workflow](./skills/workflow/README.md)   | 9      | Phased plans: write, execute, guard and verify them                       |
| [agent](./skills/agent/README.md)         | 3      | Review pages, skill capture and change explainers                         |
| [github](./skills/github/README.md)       | 3      | Announce, update and import GitHub issues (needs `workspace` and `gh`)    |

The `workflow` skills work alone; inside a feature workspace they also use the `workspace` group. The reverse does not hold: after `kickoff`, the next step is a plan, written by `to-plan` from the `workflow` group.

## Your first workspace

1. Get a PRD. Write `.scratch/workspaces/<slug>/PRD.md` yourself, in your own words, or skip the writing: talk the idea through with the agent (optionally with `/grilling`), then run `/spin-off new <slug>` and it drafts the PRD from the conversation.
2. Settle the open points: `/discuss <slug>` on a drafted PRD, or just keep talking about the one you wrote.
3. Run `/kickoff <slug>`. On the first run it asks where workspaces live and checks the folder is git-ignored.
4. Run `/to-plan`, then `/execute-plan` (one session) or `/guard-plan` (sub-agents).
5. Stop with `/pause-here <slug>`; come back with `/resume-here <slug>`. Lost? `/whatnext` tells you where you are.
6. Done? `/wrap-up <slug>` closes it out with a final report.

The full flow, with every other command, is in [skills/workspace/README.md](./skills/workspace/README.md#the-flow).

## Configuration

Two optional lines in the repo's `CLAUDE.md` or `AGENTS.md`; the skills ask once and write them for you.

```markdown
Workspace root: `.scratch/workspaces/`
Plan root: `.plans/`
```

`Workspace root:` is where feature workspaces live; `Plan root:` is where plans written outside a workspace live. Both defaults are shown above, and both folders must be git-ignored.

## Versions

The whole repo has one version, recorded in `CHANGELOG.md`. It is still before 1.0, so a skill's behavior can change between versions. If that makes you nervous (fair), pin to a tag: `npx skills add 'kodingadventure/skeleton-skills#vX.Y.Z' ...`, replacing `vX.Y.Z` with a tag from [the list of tags](https://github.com/kodingadventure/skeleton-skills/tags).

## Contributing

Found a bug? Something confusing? Tell me in [GitHub Issues](https://github.com/kodingadventure/skeleton-skills/issues). To work on the skills themselves, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Why this exists

I'm forgetful. Very. "Where are my keys" forgetful, and also "why did I decide this three weeks ago, and who approved it? Oh. Me." forgetful.

I started using [Matt Pocock's skills](https://github.com/mattpocock/skills) to manage my projects, and I learned a lot from them, especially about project documentation. Then I started bending them to fit how I actually work, and kept bending until skeleton-skills came out the other side.

The trick is that I don't have to remember. Each piece of work lives in its own workspace, with the decisions and the next step written down, so I can focus on one thing and safely forget the rest. A pile of unfinished work stops being scary when every pile knows where it left off, and `/whatnext` tells me what to do when I don't. I use it every day: grouping tasks into workspaces, writing plans that are easy to track and follow, and writing progress reports.

These skills lived in a private repo for a long time. I'm opening them up in case your brain leaks the same way mine does.

Thank you, Matt Pocock!

## Credits

- [Matt Pocock](https://github.com/mattpocock/skills) (MIT) — the suite above is a dependency, not copied.
- [`caveman-commit`](https://github.com/JuliusBrussee/caveman) by JuliusBrussee — optional, for short commit messages; not part of this catalog.

## License

[MIT](./LICENSE)
