---
name: pause-here
description: Brings a workspace's WHATNEXT.md, TRACKER.md, findings and questions up to date, with a handoff when needed. Use when the user stops for now ("udahan dulu", "lanjut besok", "stop for today"), or when WHATNEXT.md is stale because work happened without it ("phase 4 sudah selesai", "update WHATNEXT").
argument-hint: "<workspace> [what happened, or what the next session will focus on]"
disable-model-invocation: false
---

# Pause Here

Leave the **workspace** (a feature folder set up by `kickoff`, `.scratch/plan/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root) so that a fresh agent picks up exactly where the work stands by reading `CONTEXT.md` and `WHATNEXT.md`, and nothing else unless a step needs it.

Two cases, same steps:

- **Pause**: the user is stopping mid-session. The conversation is the main source: what was tried, what happened, what is half-done, what the user said comes next.
- **Sync**: `WHATNEXT.md` fell behind, because work happened in a session that never opened the workspace or never paused. The conversation knows little, so the repo and the workspace files are the source.

## Steps

### 1. Locate and read

Resolve the workspace in the same order as every workspace skill: the slug or path in the argument (in any position); else the workspace this conversation has already been working in; else `INDEX.md` at the workspace root, the only row under `## Active` (no `INDEX.md` → the only `*/WHATNEXT.md` under the root); else ask, listing the `## Active` rows. Never pick between two live workspaces, and name the one you resolved in one line (`Workspace: <slug>`) before writing anything.

Read `CONTEXT.md` (`## Workspace rules` names the languages and the layout), `TRACKER.md` and `WHATNEXT.md`.

Capture the repo state, read-only: `git branch --show-current`, `git status --short`, and `git log --oneline <last commit in WHATNEXT's state>..HEAD` (or `-10` when it names none).

Done when: you know the workspace, its languages, the branch, the uncommitted files and every commit since the last WHATNEXT.

### 2. Reconcile what happened

Collect every piece of work since `WHATNEXT.md` was written, from all sources:

- this conversation;
- the commits since the recorded commit;
- checkboxes ticked in the plans under `plans/` since then;
- what the user says in the argument ("phase 4 sudah selesai").

Map each to the next steps in `WHATNEXT.md` and to the work items in `TRACKER.md`: done, partly done (and what remains), or not started. A step you cannot place with confidence becomes a question to the user, asked before step 6.

Done when: every current next step is marked done, partly done or untouched, and every new piece of work is mapped.

### 3. Log in `TRACKER.md`

Its `## How this tracker works` binds this step and wins where it differs. For everything step 2 found — the same procedure as `/tracker log`:

- one Action Log row per meaningful action, today's date, in the tracker's language and in plain words the report audience follows;
- the status of every work item whose work moved (`done` only when finished and verified);
- new decisions, blockers and report notes as new rows, and the Answer / Resolved column of the rows that were settled.

Tick nothing: only `/tracker sent` ticks.

Done when: every action, status change and settled question has its row.

### 4. Record findings and questions

- A **finding** is a discovery a later agent must not re-learn the hard way: a test result, a root cause, a dead end and why it failed, a tool or device gotcha. Each new one gets `findings/YYYY-MM-DD-<topic>.md` (what was observed, the evidence such as log lines or commands, what it means, what follows from it) and a one-line entry in `CONTEXT.md` `## Findings` carrying its `scope:` tag (`scope: workspace`, or `repo: <path>` once its content has moved into the repo). An existing finding that moved gets updated in place.
- A **question** someone outside this session must answer gets its file in `questions/`, its tracker row and its index line, in the format of the files already in `questions/` (an empty folder → `.claude/skills/kickoff/references/question-template.md`). A question settled in this session gets its file updated (status, answer, consequences).
- Decisions settled in this session go into `CONTEXT.md` `## Decisions`, each with its `ADR:` tag (the criteria are in `### Conventions` there). A `candidate` whose code has already landed and that still has no ADR becomes a next step in `WHATNEXT.md` — written with `domain-modeling` in the next session, not left to `/wrap-up` when the reasoning has gone cold.

Done when: every discovery lives in exactly one finding file, every open question in exactly one question file, and `CONTEXT.md` lists both.

### 5. Decide on a handoff

`WHATNEXT.md` holds a short state and the next steps. Write a **handoff** too when the next session needs more than that:

- uncommitted work, and why it is not committed yet;
- a test, debugging run or procedure in progress, with its exact commands and setup;
- approaches tried that the next agent must not repeat (each linked to its finding);
- context the user gave in the conversation that lives nowhere else.

Write it to `handoffs/YYYY-MM-DD-<topic>.md`. Sections: state now; what was done and learned (point to findings, questions, commits and plans rather than copying them); the plan, with branches ("if it passes … / if it fails …"); pitfalls. Handoffs are written once: a new pause writes a new file. A sync rarely needs one.

Done when: either a handoff exists that covers every bullet above that applies, or none applies.

### 6. Rewrite `WHATNEXT.md`

Overwrite it, keeping its section headings (the shape is in `.claude/skills/kickoff/references/whatnext-template.md`). Fill:

- **How to resume**: the reading order, naming the new handoff if one was written. Mark an older handoff whose plan is finished as not needed.
- **State now**: progress %, the items in progress, branch, last commit, uncommitted files and why.
- **Next steps**: numbered, concrete, each naming who acts (the agent or the user), with branches for outcomes still unknown. Done steps are gone; a partly done step keeps only what remains. Step 1 is what the next session starts with. Shape it around the argument when the user passed one.
- **Waiting on**: people and what they owe, each linked to its question file.
- **Guardrails**: what the next agent keeps doing or holds back on, stated as the target behaviour.

**Every work item `done`** → next step 1 is `/wrap-up <slug>`: the ADRs still owed, durable findings and vocabulary into the repo, the final report, then the user deleting the folder.

Keep it under about 40 lines; detail belongs in the handoff, a finding or a question.

Then refresh this workspace's row in the root `INDEX.md`: status (`active` / `paused` / `blocked`), progress, today's date, who is being waited on, and the areas if they grew. Other sessions read that row before they read anything else here; leave every other row alone.

Done when: a fresh agent reading `CONTEXT.md` and this file knows the first action and has every caveat it needs to take it.

### 7. Report

Reply in the workspace language: the files written or updated (the index row included), the steps marked done, one line on the next step, and the resume line:

```
/resume-here <slug>   (or: "read <path>/CONTEXT.md, then continue with <path>/WHATNEXT.md")
```

Commit nothing: the workspace is git-ignored, and code changes are committed by the work itself, under the repo's rules.

Leave secrets (keys, passwords, tokens, personal data) out of every file; refer to where they are kept.
