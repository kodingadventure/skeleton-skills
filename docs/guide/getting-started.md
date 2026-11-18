# Getting started

This page answers one question: what do you do first, in a new project and in one that already has code, rules and docs?

## Before you start

Two things must be in place. Neither is repeated here.

1. The skills are installed. Commands and the pinned install line are in the [README](https://github.com/kodingadventure/skeleton-skills/blob/main/README.md#install) and its [Prerequisites](https://github.com/kodingadventure/skeleton-skills/blob/main/README.md#prerequisites). You can also paste one sentence to your agent and let it do the setup: see [Let your agent set it up](https://github.com/kodingadventure/skeleton-skills/blob/main/README.md#let-your-agent-set-it-up).
2. Your project is a git repository with at least one commit. Work on a branch or on `main`, as you like; `wrap-up` comes after the work is merged.

One more thing can wait: `/setup-matt-pocock-skills` (from the external `mattpocock/skills` suite; the README has the install line). It writes `docs/agents/` (`domain.md`, `issue-tracker.md`, `triage-labels.md`), which `refine-docs`, `update-wiki`, `github-new-issue` and `github-spin-off` read. You do not need it for your first workspace: `to-plan` and `execute-plan` carry on without it.

## Words used in this guide

- **Slug**: a short name for one piece of work, such as `double-pay`. It is also the workspace folder's name.
- **Weight**: a size label (S, M, L, XL) on each plan phase. It decides which executor agent and model run the phase. See [Model and effort](./model-and-effort.md).
- **Guardian**: the session that checks each phase and commits it, or prints the commit command when your rules leave commits to you.
- **`Review: guardian`**: a line in the plan header. Each phase is staged first, and you run `/review-phase` to check and commit it (under `/guard-plan`, the guardian does this itself).
- **Gate**: a build, lint or test command listed in `docs/agents/verify.md`, which `verify` runs.
- **ADR**: a short repo file recording a decision that is hard to reverse.
- **Docs Layout**: a block in `docs/agents/domain.md` that says where the repo keeps its docs.
- **`INDEX.md`**: the list at the workspace root, one row per workspace.

## In a new project

This expands "[Your first workspace](https://github.com/kodingadventure/skeleton-skills/blob/main/README.md#your-first-workspace)" in the README. Follow it in this order:

1. Get the idea down. Pick a slug, a short name for the work such as `login-page`. Either write `.scratch/workspaces/<slug>/PRD.md` yourself (create the folder if needed), in your own words, or skip the writing and talk the idea through with the agent (optionally with `/grilling`). When the idea came up in a session that already changed files for it, `/spin-off new <slug>` moves that thread into its own workspace instead.
2. Run `/kickoff <slug>`. Without a `PRD.md`, it writes one from the conversation, or from the words after the slug (`/kickoff login-page add a login page with email and password`). It needs two things in your own words, what you want changed and the result you expect, and asks for whichever is missing before it writes anything. Then it writes `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` and lays out the folder.
   - On the repo's first workspace it asks where workspaces live, unless `spin-off` already asked. The default is `.scratch/workspaces/`; if you wrote the PRD yourself and pick another folder, move it there.
   - It checks that folder is git-ignored. If it is not, it offers to add it to `.gitignore` and writes nothing until you answer.
   - It writes your answer as a `Workspace root:` line in `CLAUDE.md` or `AGENTS.md` and commits that line when your rules let the agent commit (asking first if they require confirmation); otherwise, or when that file already has uncommitted changes of yours, it leaves the commit to you.
3. Settle what the PRD left open: run `/discuss <slug>`, or just keep talking.
4. Run `/to-plan for the <slug> workspace` to turn it into a phased plan. Plans carry `Review: guardian` by default.
5. Run the plan with `/execute-plan` (this session, one item at a time) or `/guard-plan` (sub-agents that each do one phase). If unsure, start with `/execute-plan`. The difference is in [Skills that look alike](./skills-that-look-alike.md#execute-plan-and-guard-plan). Under `Review: guardian` each phase stops staged with "awaiting /review-phase": run `/review-phase` to check and commit it, then run `/execute-plan` again for the next phase. The first time, `verify` also creates `docs/agents/verify.md` and asks you one question (see below).
6. Stop for the day with `/pause-here <slug>`. Come back with `/resume-here <slug>`: it takes the first next step itself. If it stops, run step 5 again.
7. When the work is done, run `/wrap-up <slug>`. It moves what is worth keeping (decisions, terms, docs) into the repo and closes the workspace. See [Documentation and wrap-up](./documentation-and-wrap-up.md).

The same skill can be called in other ways; the [README](https://github.com/kodingadventure/skeleton-skills/blob/main/README.md#calling-a-skill) lists them.

## In an existing project

Most of the flow is the same. Four things differ.

- **Your rules win.** If `CLAUDE.md` or `AGENTS.md` already says who commits and when, the skills follow it. `review-phase` prints the commit command for you to run when the rules say nothing (and `execute-plan` does, when the plan has no `Review: guardian` line). If your rules forbid agent commits but you want `guard-plan` to commit its reviewed phases, add an exception to the rule, for example: `The agent never commits, except guard-plan, which commits each phase after its review.`
- **Missing gates are set up on first use.** If `docs/agents/verify.md` does not exist, `verify` creates it the first time it runs. It reads your build files and CI, runs each candidate command once, and asks you one question: may the agent start the app itself, or do you drive it. It then shows you the draft before writing it.
- **Missing doc layout is offered.** If `docs/agents/domain.md` exists but has no `## Docs Layout` block, `refine-docs` infers one, shows you the draft and writes it only after you correct it. If `domain.md` is missing, it stops and points you to `/setup-matt-pocock-skills`.
- **Teammates see nothing extra.** The workspace folder is git-ignored. They see ordinary commits and, once, the `Workspace root:` line (and a `Plan root:` line if you write a plan outside a workspace) and, if `kickoff` or `spin-off` added it, the `.gitignore` entry.

Do not document the whole codebase first. Start with one real feature or small fix, and let the docs grow from there.

## When you are lost

- `/whatnext` recommends the single next step and the skill to run.
- `/so-far <slug>` recaps a workspace on a page: what was done, what was decided, and what waits on you.

Next: [An example journey](./example-journey.md)
