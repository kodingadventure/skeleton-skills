# Getting started

This page answers one question: what do you do first, in a new project and in one that already has code, rules and docs?

## Before you start

Two things must be in place. Neither is repeated here.

1. The skills are installed. Commands and the pinned install line are in the [README](../../README.md#install) and its [Prerequisites](../../README.md#prerequisites).
2. `/setup-matt-pocock-skills` has run once in this repo. It writes `docs/agents/` (`domain.md`, `issue-tracker.md`, `triage-labels.md`), which `refine-docs` and `update-wiki` read. It comes from the external `mattpocock/skills` suite; see the README for the install line.

## In a new project

This expands "[Your first workspace](../../README.md#your-first-workspace)" in the README. Follow it in this order:

1. Write `.scratch/workspaces/<slug>/PRD.md` by hand: what you want built, in your own words.
2. Discuss the PRD with the agent until the open points are settled.
3. Run `/kickoff <slug>`. It writes `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` and lays out the folder.
   - On the repo's first workspace it asks where workspaces live. The default is `.scratch/workspaces/`.
   - It checks that folder is git-ignored. If it is not, it offers to add it to `.gitignore` and writes nothing until you answer.
   - It writes your answer as a `Workspace root:` line in `CLAUDE.md` or `AGENTS.md`. That line is a repo change, so you commit it.
4. Run `/to-plan` to turn the workspace into a phased plan.
5. Run the plan with `/execute-plan` (this session, one item at a time) or `/guard-plan` (sub-agents). The difference is in [Skills that look alike](./skills-that-look-alike.md#execute-plan-and-guard-plan).
6. Stop for the day with `/pause-here <slug>`. Come back with `/resume-here <slug>`, then repeat from step 5.
7. When the work is done, run `/wrap-up <slug>`. See [Documentation and wrap-up](./documentation-and-wrap-up.md).

The same skill can be called in other ways; the [README](../../README.md#calling-a-skill) lists them.

## In an existing project

Most of the flow is the same. Four things differ.

- **Your rules win.** If `CLAUDE.md` or `AGENTS.md` already says who commits and when, the skills follow it. `execute-plan` prints the commit command for you to run when the rules say nothing.
- **Missing gates are set up on first use.** If `docs/agents/verify.md` does not exist, `verify` creates it the first time it runs. It reads your build files and CI, runs each candidate command once, and asks you one question: may the agent start the app itself, or do you drive it.
- **Missing doc layout is offered.** If `docs/agents/domain.md` exists but has no `## Docs Layout` block, `refine-docs` infers one, shows you the draft and writes it only after you correct it. If `domain.md` is missing, it stops and points you to `/setup-matt-pocock-skills`.
- **Teammates see nothing extra.** The workspace folder is git-ignored. They see ordinary commits and, once, the `Workspace root:` line.

Do not document the whole codebase first. Start with one real feature or small fix, and let the docs grow from there.

## When you are lost

- `/whatnext` recommends the single next step and the skill to run.
- `/so-far <slug>` recaps a workspace on a page: what was done, what was decided, and what waits on you.

Next: [An example journey](./example-journey.md)
