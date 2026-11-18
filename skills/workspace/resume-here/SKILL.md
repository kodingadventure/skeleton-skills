---
name: resume-here
description: Run only when the user asks for it by name. Resume work on a workspace in a fresh session — reads WHATNEXT.md, CONTEXT.md and the linked handoff, reconciles drift with the repo, briefs the user, then starts the first next step.
argument-hint: "<workspace> [what to do today, if different]"
disable-model-invocation: false
---

# Resume Here

Pick up a **workspace** (a feature folder set up by `kickoff`, `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root) where `pause-here` left it.

## Language

Every message to the user is in the workspace language from `CONTEXT.md` `## Workspace rules`: the brief, each question (through a question tool too), each progress line. Before `CONTEXT.md` is read, use the language of the user's message. A repo rule that code, docs or commits be in English covers what gets committed, not the conversation.

## Steps

### 1. Locate

The same order as every workspace skill: the slug or path in the argument; else `INDEX.md` at the workspace root — the only row under `## Active` (no `INDEX.md` → the only `*/WHATNEXT.md` under the root); else ask, listing the `## Active` rows (slug, goal, progress, `Updated:`, who is being waited on) for the user to pick from. A fresh session has no conversation to fall back on: never pick between two live workspaces.

Done when: one workspace is chosen and named in one line (`Workspace: <slug>`).

### 2. Read, in order

1. `WHATNEXT.md` — the whole file.
2. `CONTEXT.md` — the whole file. `## Workspace rules` sets the language (see [Language](#language)).
3. The handoff named under "How to resume", if any.

Open anything else (`TRACKER.md`, a finding, a plan phase) only when a next step needs its detail.

Done when: you can state the first next step, who acts on it, and every guardrail.

### 3. Check for drift

Compare `## State now` with the repo, read-only: `git branch --show-current`, `git log --oneline <recorded commit>..HEAD`, `git status --short`. Not a git repository → skip this and say "not a git repo" in the brief. Note each mismatch: a different branch, commits made since, uncommitted files that appeared or vanished.

Drift means work happened after `WHATNEXT.md` was written. Map each new commit (and each plan checkbox ticked since) to the next steps: done, partly done, or unrelated. Anything you cannot place is a question for the user, not a guess.

Done when: every line of `## State now` is confirmed, or every drift item is mapped or listed as a question.

### 4. Brief the user

Short:

- where the work stands (3–5 bullets);
- drift, if any, with your mapping, as a question;
- who and what is still awaited;
- the next step you are about to take.

### 5. Start

**Drift first.** Once the user confirms the mapping, bring the workspace up to date with the `pause-here` skill's steps from "Reconcile what happened" to "Rewrite `WHATNEXT.md`" (if the `pause-here` skill is not installed, update `WHATNEXT.md` State now and Next steps, and the `INDEX.md` row), then re-read the new next step 1.

Take next step 1 (or what the argument asks for instead), under the repo's own rules and the guardrails. A step that belongs to the user — a manual test, a decision, a message to someone — becomes guidance: tell them exactly what to do and what to report back.

From here on, the workspace's conventions in `CONTEXT.md` apply: settled decisions go into `CONTEXT.md` (with their `ADR:` tag) and `TRACKER.md`, each finished next step updates `WHATNEXT.md` and this workspace's row in the root `INDEX.md` — by rewriting `State now` and `Next steps`, never by patching around them: a finished step is deleted (not struck through, not kept as "done" or numbered 0), and a half-done step keeps only what remains (the full rules are in the `pause-here` skill's "Rewrite `WHATNEXT.md`" step) — and `/pause-here` closes the session when those files are behind (new findings, open questions, a half-done step, a handoff to write). If every finished step already updated them as it went, the session can end without it: the next `/resume-here` reads the same files.

Two neighbours of this skill: the user who wants to think a topic through rather than work on it → `/discuss <slug> <topic>`; every work item `done` → `/wrap-up <slug>`.
