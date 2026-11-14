# FAQ

This page answers seven common questions about the skills.

## Is the Matt Pocock suite required?

Only for the skills in the "Needed by" column of the Prerequisites table in the [root README](../../README.md#prerequisites). A skill that needs a missing one stops with a message that names what to install. Every other skill is unaffected. A "recommended" skill is used only if it is installed.

## Is the workspace folder committed?

Not by the main repo. The workspace root (`.scratch/workspaces/` by default) must be ignored by git. You can give the folder above it its own git repository (`git init .scratch`) to keep a history of your notes after a workspace is deleted. That is optional.

The skills never run git in that repository unless your repo's instructions tell them to. To have the agent commit your notes, add a rule like this to `CLAUDE.local.md` (Claude Code; kept out of git, so it is yours alone) or to `AGENTS.md` / `CLAUDE.md` when the whole team keeps notes this way:

```markdown
## Workspace notes

`.scratch/` is its own git repository. After you create or change files under `.scratch/workspaces/`, commit them there: `git -C .scratch add <explicit paths>`, then `git -C .scratch commit -m "docs: <summary>"`. Never stage `.scratch/` from the main repo, and leave out changes you did not make.
```

With that rule, a skill that writes notes (`kickoff`, `discuss`, `pause-here`, `spin-off`, `wrap-up`) commits only the files it wrote and names the commit in its report. Without it, nothing changes: the notes stay uncommitted until you commit them.

## What are tracker, so-far and msg for when nobody receives reports?

Progress reports are optional. `kickoff` asks whether anyone receives them, and the default is no audience.

- `tracker` is still the work log: item status, weights and the Action Log. With no audience, `tracker report` and `tracker sent` decline, and `wrap-up` skips the final report.
- `so-far` is for you, not for a reader. It opens a recap page that tells you what was done and decided, and why the next step is next. It only reads.
- `msg` drafts a chat message to a teammate, such as a question or a short update. If you work alone, you never need it.

## What does a good PRD look like?

A PRD is `.scratch/workspaces/<slug>/PRD.md`, in plain prose. You can write it yourself, or let `spin-off` seed it from a conversation; either way you correct it before `kickoff`. `kickoff` reads it, so these are worth having in it, as far as you know them:

- What the feature is.
- Decisions already made.
- Open questions, and who can answer each one.
- Whether anyone receives progress reports, and in which language.
- How much is already done, if any.
- The work items, and which modules or paths they touch.

You do not need all of it. `kickoff` asks for the missing parts in one round. Put mockups and sample data next to the PRD; `kickoff` moves them into the workspace's `docs/` folder. The language of the PRD's prose becomes the workspace language.

## What is a review page?

It is a short HTML page that an agent writes to your temp folder and opens in your browser, so you can decide several things in a few minutes. It has plain-word text, diagrams, a recommended option for each decision, and an answer box at the end. You copy the answer and paste it back into the conversation. There is no server and nothing is saved in the browser, so the page never changes behind your back. The Explain button works the same way: it copies a question for you to paste into the conversation, and the agent answers there. The reasons are in [ADR 0007](../adr/0007-review-page-answers-by-copy-paste.md). The skill is `review-page`.

## What do I do when I am lost?

Run one of these, depending on what you lost:

- `/whatnext` names the single next step and the skill to call.
- `/so-far <slug>` recaps a workspace for you: what was done, what was decided, and what comes next.
- `/resume-here <slug>` starts a fresh session on a workspace and takes the next step from `WHATNEXT.md`.

## Does guard-plan save tokens?

Probably, but it has not been measured, so this guide gives no number. Each phase runs in an agent with a fresh context, on a model chosen from the phase's Weight, and the main session only checks the result instead of doing the work. See [Model and effort](./model-and-effort.md) for the Weight table.

Back to [Start here](./README.md)
