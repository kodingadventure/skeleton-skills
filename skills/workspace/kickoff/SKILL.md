---
name: kickoff
description: Turn an idea or a PRD discussion into a feature workspace — writes `PRD.md` from the conversation when there is none, then CONTEXT.md, TRACKER.md and WHATNEXT.md in the PRD's language, and lays out the folder. Run mid-discussion or at its end; re-run to refresh. Also when the user says "turn this into a workspace" or "let's track this properly" (in any language).
argument-hint: "<feature-slug or workspace path> [idea]"
disable-model-invocation: false
---

# Kickoff

A **workspace** is one folder per feature or task, `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root. The user writes `PRD.md` there, or this skill writes it from the conversation, and the user discusses it with an agent; this skill turns that discussion into the three living documents every later agent works from:

- `CONTEXT.md`: the refined spec and the **workspace rules** (language, layout, conventions). Every agent reads it first.
- `TRACKER.md`: progress, decisions, questions, blockers, and the rules for progress reports.
- `WHATNEXT.md`: the short, always-current answer to "what do we do next?".

The workspace is **self-describing**: its rules live in its own files, so a plain prompt ("read CONTEXT.md, continue with WHATNEXT.md") works with or without the companion skills (`tracker`, `pause-here`, `resume-here`).

## Steps

### 1. Locate the workspace

From the argument (a slug or a path; any words after it are the idea's text, used in step 2), else the folder of the PRD discussed in this conversation, else a new `<root>/<slug>/`. A new slug is the one in the argument, or the idea in kebab-case: name it in step 2's question round so the user can correct it, or in your report when there is no round. Note whether `<path>/PRD.md` exists. On the repo's first workspace (no `Workspace root:` line in `CLAUDE.md` / `AGENTS.md`, and no `INDEX.md` at the root), ask the one root question from [`references/workspace-root.md`](references/workspace-root.md) — the default, or another folder — and write the answer as that line, then commit it as that file's "Asking once" says. Check the root is git-ignored (`git check-ignore <path>/x`); if it is not, **offer** to add the root to `.gitignore` and write nothing, in the repo or the workspace, until the user has answered. With no `PRD.md` yet, the root question and the `.gitignore` offer go in step 2's question round, and nothing is written (no folder, no `Workspace root:` line, no `.gitignore` change) until step 2 has settled that a PRD is written. If the root or its parent holds its own `.git`, it is a separate repository: say so in `### Layout`, with the two lines from `references/context-template.md` copied word for word, in English, never rewritten to match the repo's own notes rule. If it has none, tell the user once that `git init <root>` would keep a history of these notes, which are otherwise lost when a workspace is deleted — their call, not yours.

Done when: you have one workspace path, and you have noted whether it holds a `PRD.md`.

### 2. Write the PRD when there is none

If `<path>/PRD.md` exists, skip this step: the PRD is used as it is. Otherwise run `git log --oneline -20` and `git status --short`, then:

- **One idea only.** The PRD is written from one idea, never from the whole conversation. An argument that points to exactly one idea (a slug such as `kickoff-without-prd`, or the idea's text) is used as it is. With no argument, or one that matches more than one idea, name the ideas and ask which one in the question round. A guess drawn from a vague argument is named in that round so the user can correct it.
- **Enough?** From the user's own words (the conversation and the argument text both count) you must be able to take (a) the problem or goal, what is to change, and (b) the expected result. Anything else (why it matters, the areas, the scope) may be written as open in the PRD. Wrong: `/kickoff dark-mode` with no conversation has neither, so it is not enough. Right: `/kickoff dark-mode add a dark mode switch to the settings page` is enough (change: the UI has no dark mode; result: a switch in settings).
- **One question round.** What is missing (which idea, the problem, the result, the slug guess), the root question and `.gitignore` offer of step 1, and the questions of step 4 (report audience, and whatever the conversation does not answer) go in **one round**, in the user's language. Step 4 then asks nothing more, and there is no second round.
- **Work already done.** When the chosen idea already has commits or changed files in this session (`git log`, `git status --short`), `kickoff` only picks the idea and does not cut a slice. In the question round, suggest `/spin-off new <slug>`, which carries those commits and files into the workspace brief. With no answer, carry on and repeat the suggestion in the report. Name `/spin-off` only when it is in your list of available skills.
- **Stop.** Only when the user will not explain after being asked: write nothing (no folder, no `PRD.md`, no `Workspace root:` line, no `.gitignore` change), say what is needed, and stop.
- **Write, no draft.** When it is enough, write `PRD.md` at once, with no draft for review: a doubt was settled in the round, and the rest goes into the PRD's open section for `/discuss` later. First do what step 1 held back (the `Workspace root:` line and its commit, the `.gitignore` change), then create the folder. The PRD is in the user's language from the conversation. Its first line is, literally, `Written by /kickoff on YYYY-MM-DD from the conversation. The user owns it from here.` with today's date. Its sections: the problem, why it matters, the expected result, what is known, what is still open, out of scope. What is not known is written as open, never guessed.

Done when: the workspace has a `PRD.md` (found, or written by this step), or the user would not explain and nothing was written.

### 3. Detect the languages

- **Workspace language**: the language of the PRD's prose (ignore code blocks and quoted UI text). A PRD written by step 2 is in the user's language, so the workspace language follows it. It is the language for talking with the user and for every document in the workspace.
- **Report language**: the `Language:` line of `TRACKER.md` `## Report rules`, set in step 4 (default English).
- **Repo language**: whatever the repo's own rules say for code, commits and committed docs.

On a re-run, keep the languages already recorded in `CONTEXT.md` and `TRACKER.md`, exceptions included.

Done when: the workspace and repo languages are named.

### 4. Fill the gaps

Collect from the PRD, the conversation, and the origin brief when `spin-off` seeded this folder (`docs/*-origin.md`: what was already tried, learned and left open; its minimal `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` already hold the decisions made since, and say `TBD (kickoff)` where an answer is owed): the feature summary, decisions settled, open questions (and who answers each), whether anyone receives progress reports (see below), the **baseline %** (work done before the tracker exists, default 0), the work items with weights, and the **areas** this work will touch (the modules, apps or paths) for the index row. Ask the user, in one round, only for what the conversation does not already answer; when step 2 already asked, that round is used, so ask nothing more.

**Report audience.** Ask: "Does anyone receive progress reports on this work? If so, who, and in which language?" Record the answer on the `Audience:` and `Language:` lines of `TRACKER.md` `## Report rules`. The defaults are `Audience: none` and `Language: English`. Ask for the audience's name, role and how technical they are only when there is an audience. With `Audience: none` the tracker is still the work log (status, weights, Action Log); `tracker report` and `tracker sent` decline, and `wrap-up` skips the final report. Other skills read these two lines and never assume a report language.

Done when: every placeholder in the three templates has a value or is deliberately left empty.

### 5. Lay out the folder

Create the folders from the layout in `references/context-template.md` (`plans/`, `findings/`, `questions/`, `handoffs/`, `reports/`, `docs/`; `logs/` only when the work involves manual tests). Move loose input files (mockups, sample data, notes, anything that is not `PRD.md` or one of the three living documents) into `docs/`. List each move in your final report.

Done when: the workspace root holds only `PRD.md`, the three living documents and the folders.

### 6. Write the three documents

Write each from its template, translated into the workspace language (headings included). Keep literal: file and folder names, status tokens (`todo`, `in-progress`, `done`, `blocked`), checkboxes, code, UI strings, and the two separate-repository lines of `### Layout` (English, word for word).

- `CONTEXT.md` ← `references/context-template.md`. Every entry in `## Decisions` gets its `ADR:` tag; the criteria are in the template's `### Conventions`.
- `TRACKER.md` ← `references/tracker-template.md`. Weights of all work items sum to `100 − baseline`. Every row is unticked.
- One file per open question in `questions/`, with its tracker row and index line ← `references/question-template.md`.
- One file per finding in an origin brief, in `findings/`, with its `scope:` line in `## Findings`.
- `WHATNEXT.md` ← `references/whatnext-template.md`. The next step is usually to finish the PRD discussion, or to write the first plan into `plans/01-<name>/` with a plan skill (`to-plan` from the workflow group, when installed).
- `INDEX.md` at the **root above the workspace** ← `references/index-template.md`: this workspace's row under `## Active`, moved from `## Seeded` when `spin-off` left one there (goal in one line, `active`, progress = the baseline, today's date, who is being waited on, the areas). Its rows are in English whatever the workspace language, since it is read across workspaces. Create the file if it is missing; never touch another workspace's row. Any other workspace folder already under the root that has no row gets one too, read from its own `WHATNEXT.md`.

**Re-run** (the documents already exist): update in place. Merge new decisions, questions and work items; keep existing rows, ticks, Report History, and the weight of every item already `done`; keep existing prose unless the user asked to change it. **A seed from `spin-off`** is a re-run with two exceptions: replace every `TBD (kickoff)` with its real value, and replace the placeholder work item `Refine the PRD, then run /kickoff` with the real work items (weights sum to `100 − baseline`). Refresh this workspace's `INDEX.md` row and leave every other row alone.

Never stage anything under the workspace root from the main repo. When the root, or a folder above it, has its own git repository, run git there only when the repo's instructions (`CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`) say to commit the workspace notes: then commit in that repository only the files this run wrote, with explicit paths and a short message, leave out every change this run did not make, and name those in your report. Without such an instruction, run no git there.

Done when: the three files exist, every template section is filled or removed on purpose, and the tracker's weights add up.

### 7. Report

In the workspace language: the `PRD.md` this skill wrote (its path), each idea left out of it (it stays in the session, one line per idea), the `/spin-off` suggestion when step 2 made one and it was not answered, the files written or updated (the index row included), the moves, the three languages, the baseline and weight total, the notes commit hash (or "notes not committed" and why), and the resume line:

```
/resume-here <slug>   (or: "read <path>/CONTEXT.md, then continue with <path>/WHATNEXT.md")
```

The resume line goes in this report only; later replies in this conversation do not repeat it.
