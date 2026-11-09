---
name: spin-off
description: Carves one thread out of the current session and hands it to a feature workspace, an existing one or a new one seeded for /kickoff. Use when the user wants a thread moved out of this session ("spin this off", "pisahin ke workspace"), or asks to keep a settled design for later in its own workspace.
argument-hint: "[<workspace> | new <slug>] [topic]"
---

# Spin Off

A long session wandered through many things, and one of them deserves its own focus. This skill moves that **thread** into a **workspace** (a feature folder set up by `kickoff`, `.scratch/plan/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root), so a later agent can pick it up from the workspace's files alone, without this conversation.

The thread is a **slice**: only what belongs to it moves. The rest of the session stays out of the workspace, and out of its tracker and the reports built from it.

Two destinations:

- **Existing workspace**: the thread lands as an inbound handoff plus a next step in its `WHATNEXT.md`.
- **New workspace**: the thread becomes a seeded `PRD.md`, an origin brief and minimal `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md`, so decisions made before `/kickoff` already have a home; `/kickoff` completes them.

## Steps

### 1. Carve out the thread

From the topic in the argument, or, with none, from what the conversation was last focused on, propose the slice to the user in one message:

- **The thread**, in one or two lines: the problem as it now stands.
- **In**: what was found, decided, tried (and how it went), and changed — commits by hash, files touched, uncommitted files.
- **Out**: the other things this session dealt with, named in a few words each, so the user sees the boundary.
- **Open**: what is still unknown or undecided.

Read the repo for the "changed" part rather than relying on memory: `git log --oneline` for this session's commits, `git status --short` for uncommitted files. When the conversation was summarized and the early detail is thin, say which parts come from the summary and the repo, and ask the user for what is missing.

Done when: the user has confirmed the slice, every commit and file listed under **In** is checked against the repo, and every uncommitted file is assigned to the thread or to the rest of the session.

### 2. Choose the destination

The argument names it: a workspace slug or path, or `new <slug>`. Otherwise read `INDEX.md` at the workspace root, match the thread against each row's Goal and Areas, and propose one destination — an existing workspace, or `new <slug>` with a slug you suggest — for the user to confirm.

The destination is always the user's choice. The usual fallback of the other workspace skills (the only `## Active` row) is deliberately absent here: this session usually belongs to no workspace, and the only active one is rarely where a side thread belongs.

Confirmed, name it in one line before writing anything: `Workspace: <slug>` or `New workspace: <slug>`.

### 3. Hand off to an existing workspace

Read `CONTEXT.md` (`## Workspace rules` sets the language of everything you write there) and `WHATNEXT.md`. Grep the thread's key words across `## Decisions`, `## Findings`, `findings/` and `questions/`: a thread the workspace already knows extends those files rather than duplicating them.

Write, in the workspace language and the format of the files already there:

- **The brief** as `handoffs/YYYY-MM-DD-<topic>.md` (shape below).
- **Findings** → one `findings/YYYY-MM-DD-<topic>.md` per discovery, with its one-line `scope:` entry in `CONTEXT.md` `## Findings`.
- **Questions** for someone outside the session → their file in `questions/`, their `TRACKER.md` row and their `CONTEXT.md` index line (format: the files already in `questions/`, else `.claude/skills/kickoff/references/question-template.md`).
- **Decisions** the session settled for this feature → `CONTEXT.md` `## Decisions` with their `ADR:` tag, plus a Decision row in `TRACKER.md`.
- **Commits** from the slice that already moved this feature's work → Action Log rows under the tracker's `## How this tracker works`. Work from the rest of the session gets no row: the Action Log feeds the stakeholder's report.
- **A new work item** only when the user says yes, its weight set by the tracker's own rules.
- **`WHATNEXT.md`**: insert the thread as a numbered next step that points at the brief — after the current step 1 unless the user says it comes first — and name the brief under "How to resume". Update the `Updated:` line; the other steps, the state and the guardrails stay as they are.
- **`INDEX.md`**: this workspace's row — today's date, and the areas when the thread adds one.

Tick no checkbox: only `/tracker sent` does that.

Done when: a fresh agent reading `CONTEXT.md`, `WHATNEXT.md` and the brief can take the thread up with no access to this conversation, and every finding, question and decision lives in exactly one file.

### 4. Seed a new workspace

**First workspace in this repo** (no `Workspace root:` line in `CLAUDE.md` / `AGENTS.md`, and no `.scratch/plan/INDEX.md`): ask the user once where workspaces live — `.scratch/plan/` (the default) or a folder they name — and write the answer as that line, per `.claude/skills/kickoff/references/workspace-root.md`. List the instructions-file edit among the files written: it is a repo change to commit.

Create `<root>/<slug>/` and check it is git-ignored (`git check-ignore`). Write in the language the user speaks in this conversation: `kickoff` takes the workspace language from the PRD's prose.

- **`PRD.md`**: the seed — the problem, why it matters, what is known, what is open, what is out of scope. First line: `Seeded by /spin-off on YYYY-MM-DD from a session about <one line>. Refine before /kickoff.` The user owns it from here.
- **The brief** as `docs/YYYY-MM-DD-<topic>-origin.md` (shape below). Findings and questions stay inside it: `kickoff` turns them into files.
- **`INDEX.md`**: a row under `## Seeded` — slug, goal in one line, today's date, areas — in English. Create the section above `## Shipped` when it is missing; a missing `INDEX.md` starts from `.claude/skills/kickoff/references/index-template.md`. Before writing, compare the areas with every `## Active` row and tell the user about any overlap.

- **`CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`** in minimal form, from `.claude/skills/kickoff/references/`, so that `/discuss` has somewhere to record. Fill what the thread already answers and write `TBD (kickoff)` for what is the user's to answer; never guess it.
  - `CONTEXT.md`: `## Workspace rules` complete (the language of this conversation; exceptions the user stated; the layout, with the root's own-repository note when it applies); `## Summary` = `TBD (kickoff)` plus a pointer to `PRD.md` and the brief; `## Decisions` = the decisions the thread settled, each with its `ADR:` tag; the other sections empty.
  - `TRACKER.md`: baseline 0; report audience `TBD (kickoff)`; one **placeholder work item** of weight 100, `Refine the PRD, then run /kickoff`, status `todo`; a Decision row per decision above; every row unticked.
  - `WHATNEXT.md`: next steps `1.` the user shapes the PRD with `/discuss <slug>`, `2.` `/kickoff <slug>` fills the `TBD (kickoff)` fields and replaces the placeholder work item; waiting on the user.

  Create `findings/` and `questions/` too, so `/discuss` can write there; `kickoff` lays out the rest of the folders.

  The seed is not a live workspace yet: its `INDEX.md` row stays under `## Seeded` until `/kickoff`, and no report is built from it.

Done when: the folder holds `PRD.md`, the brief and the three minimal documents, `INDEX.md` lists it under `## Seeded`, and the PRD reads as a request someone who never saw this session could discuss.

### 5. Close the thread here

Reply in the language of this conversation:

- the files written (paths), and any area overlap found;
- uncommitted files that belong to the thread, still in the working tree — commit them under the repo's rules before this session moves on, or leave them as the brief records;
- one line: `<thread> now lives in <workspace>`;
- the line to continue with: `/resume-here <slug>` or `/discuss <slug> <topic>` for an existing workspace; `/discuss` the seeded PRD, then `/kickoff <slug>`, for a new one.

From here on in this session, the thread belongs to the workspace: when the user returns to it, point at the workspace and its continue line, and carry on with whatever else they bring.

Commit nothing in this step, and run no git inside the workspace root when it has its own repository. Secrets (keys, tokens, passwords, personal data) stay out of every file; refer to where they are kept.

## The brief

One file, written once, never edited. It must stand alone: the reader has the repo and the workspace, never this conversation.

```markdown
# <Thread, one line>

Spun off: YYYY-MM-DD · From: <what the session was about, one line> · Branch: <branch>

## The thread

<the problem as it now stands, and why it needs its own focus>

## What changed

<commits by hash and subject; files touched; uncommitted files and why they are not committed>

## What was tried and learned

<each attempt and its outcome; dead ends and why they failed, linked to their finding files when there are any>

## Open

<what is still unknown or undecided; questions, linked to their files when there are any>

## Suggested first step

<one concrete step, and who takes it>
```
