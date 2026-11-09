---
name: kickoff
description: Turn a PRD discussion into a feature workspace — writes CONTEXT.md, TRACKER.md and WHATNEXT.md in the PRD's language and lays out the folder. Run mid-discussion or at its end; re-run to refresh.
argument-hint: "<feature-slug or workspace path>"
disable-model-invocation: true
---

# Kickoff

A **workspace** is one folder per feature or task, `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root. The user writes `PRD.md` there and discusses it with an agent; this skill turns that discussion into the three living documents every later agent works from:

- `CONTEXT.md`: the refined spec and the **workspace rules** (language, layout, conventions). Every agent reads it first.
- `TRACKER.md`: progress, decisions, questions, blockers, and the rules for progress reports.
- `WHATNEXT.md`: the short, always-current answer to "what do we do next?".

The workspace is **self-describing**: its rules live in its own files, so a plain prompt ("read CONTEXT.md, continue with WHATNEXT.md") works with or without the companion skills (`tracker`, `pause-here`, `resume-here`).

## Steps

### 1. Locate the workspace

From the argument (a slug or a path), else the folder of the PRD discussed in this conversation. It must contain `PRD.md`; if there is none, ask the user for it and stop. On the repo's first workspace (no `Workspace root:` line in `CLAUDE.md` / `AGENTS.md`, and no `INDEX.md` at the root), confirm with the user that the folder holding the PRD's workspace is the root they want for every workspace, and write it as that line, per [`references/workspace-root.md`](references/workspace-root.md); that line is a repo change to commit. Check the root is git-ignored (`git check-ignore <path>`); if it is not, tell the user before writing. If the root or its parent holds its own `.git`, it is a separate repository: say so in `### Layout` — never staged from the main repo, and no git commands inside it unless the user asks. If it has none, tell the user once that `git init <root>` would keep a history of these notes, which are otherwise lost when a workspace is deleted — their call, not yours.

Done when: you have one workspace path holding a `PRD.md`.

### 2. Detect the languages

- **Workspace language**: the language of the PRD's prose (ignore code blocks and quoted UI text). It is the language for talking with the user and for every document in the workspace.
- **Report language**: English, always.
- **Repo language**: whatever the repo's own rules say for code, commits and committed docs.

On a re-run, keep the languages already recorded in `CONTEXT.md`, exceptions included.

Done when: all three are named.

### 3. Fill the gaps

Collect from the PRD, the conversation, and the origin brief when `spin-off` seeded this folder (`docs/*-origin.md`: what was already tried, learned and left open; its minimal `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` already hold the decisions made since, and say `TBD (kickoff)` where an answer is owed): the feature summary, decisions settled, open questions (and who answers each), the **report audience** (name, role, how technical), the **baseline %** (work done before the tracker exists, default 0), the work items with weights, and the **areas** this work will touch (the modules, apps or paths) for the index row. Ask the user, in one round, only for what the conversation does not already answer.

Done when: every placeholder in the three templates has a value or is deliberately left empty.

### 4. Lay out the folder

Create the folders from the layout in `references/context-template.md` (`plans/`, `findings/`, `questions/`, `handoffs/`, `reports/`, `docs/`; `logs/` only when the work involves manual tests). Move loose input files (mockups, sample data, notes, anything that is not `PRD.md` or one of the three living documents) into `docs/`. List each move in your final report.

Done when: the workspace root holds only `PRD.md`, the three living documents and the folders.

### 5. Write the three documents

Write each from its template, translated into the workspace language (headings included). Keep literal: file and folder names, status tokens (`todo`, `in-progress`, `done`, `blocked`), checkboxes, code, UI strings.

- `CONTEXT.md` ← `references/context-template.md`. Every entry in `## Decisions` gets its `ADR:` tag; the criteria are in the template's `### Conventions`.
- `TRACKER.md` ← `references/tracker-template.md`. Weights of all work items sum to `100 − baseline`. Every row is unticked.
- One file per open question in `questions/`, with its tracker row and index line ← `references/question-template.md`.
- One file per finding in an origin brief, in `findings/`, with its `scope:` line in `## Findings`.
- `WHATNEXT.md` ← `references/whatnext-template.md`. The next step is usually to finish the PRD discussion, or to write the first plan with the repo's plan skill into `plans/01-<name>/`.
- `INDEX.md` at the **root above the workspace** ← `references/index-template.md`: this workspace's row under `## Active`, moved from `## Seeded` when `spin-off` left one there (goal in one line, `active`, progress = the baseline, today's date, who is being waited on, the areas). Its rows are in English whatever the workspace language, since it is read across workspaces. Create the file if it is missing; never touch another workspace's row. Any other workspace folder already under the root that has no row gets one too, read from its own `WHATNEXT.md`.

**Re-run** (the documents already exist): update in place. Merge new decisions, questions and work items; keep existing rows, ticks, Report History, and the weight of every item already `done`; keep existing prose unless the user asked to change it. **A seed from `spin-off`** is a re-run with two exceptions: replace every `TBD (kickoff)` with its real value, and replace the placeholder work item `Refine the PRD, then run /kickoff` with the real work items (weights sum to `100 − baseline`). Refresh this workspace's `INDEX.md` row and leave every other row alone.

Done when: the three files exist, every template section is filled or removed on purpose, and the tracker's weights add up.

### 6. Report

In the workspace language: the files written or updated (the index row included), the moves, the three languages, the baseline and weight total, and the resume line:

```
/resume-here <slug>   (or: "read <path>/CONTEXT.md, then continue with <path>/WHATNEXT.md")
```
