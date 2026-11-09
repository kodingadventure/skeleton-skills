---
name: wrap-up
description: Close a finished feature workspace — writes the ADRs still owed, moves durable findings and vocabulary into the repo, sends the final report, updates the workspace index, and hands the folder to the user to delete.
argument-hint: "<workspace>"
disable-model-invocation: true
---

# Wrap Up

The last stage of a **workspace** (a feature folder set up by `kickoff`, `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root). The folder is deleted after this, so anything still only in it is about to be lost: this skill is the sweep that moves what must survive into the committed repo.

It is a sweep, not the main transfer. Decisions become ADRs as the code that embodies them lands (`execute-plan` Step C / `review-phase`), and shipped behaviour is documented as it ships. What reaches this skill is the remainder.

## Resolving the workspace

The same order in every workspace skill:

1. the slug or path in the argument;
2. the workspace this conversation has already been working in;
3. `INDEX.md` at the workspace root: the only row under `## Active` (no `INDEX.md` → the only `*/WHATNEXT.md` under the root);
4. still more than one → ask, listing the `## Active` rows.

Never pick between two live workspaces. Before writing anything, name the one you resolved in one line: `Workspace: <slug>`.

## Steps

### 1. Check the work is actually finished

Read `CONTEXT.md` (`## Workspace rules`, `## Decisions`, `## Findings`, `## Conventions`), `TRACKER.md` and `WHATNEXT.md`.

Every work item `done`? If not, list the items that are not and ask the user whether to wrap up anyway — a feature parked indefinitely is a legitimate reason, a feature still in progress is not. Stop until they answer.

Done when: either every item is `done`, or the user has said to continue with the open ones listed.

### 2. Write the ADRs still owed

`grep -n "ADR: candidate" CONTEXT.md`. For each hit: write the ADR with the `domain-modeling` skill, where the repo keeps them, then replace the tag with the ADR id in `CONTEXT.md`.

Each one is a decision whose reasoning now exists nowhere else. Write what was decided, the alternatives that were on the table and why they lost — the workspace's decision entry, its question file and the findings it rests on are the sources; the ADR must stand on its own once they are gone.

A candidate that turns out not to meet `domain-modeling`'s three criteria (hard to reverse · a later reader will ask why · a real trade-off) is retagged `ADR: no` with one line saying where its reasoning lives instead. Do not pad the repo with ADRs for decisions that were never trade-offs.

Done when: no `ADR: candidate` is left in `CONTEXT.md`.

### 3. Move the vocabulary and the behaviour

- **Terms** the workspace coined or sharpened (the ones in `CONTEXT.md` that a new reader of the code would not guess) → the repo's glossary, via `domain-modeling`.
- **What shipped** — a module's rules, a status transition, a route, a screen, a flow → the repo's documentation, via the repo's own docs skill (`update-wiki` where it is installed; else the doc that owns the subject). Skip what is already documented; a feature documented as it shipped needs only a check.

Done when: a reader of the repo alone can find what this feature does and what its words mean.

### 4. Triage `findings/` — the step that is easy to skip

Every file in `findings/` is about to be deleted. Each one is exactly one of:

- **Repo knowledge** — a tool, platform, device or environment gotcha that will bite the next feature too (not just this one). Move its content to the repo document that owns that subject, and mark the entry in `CONTEXT.md` `## Findings` as `repo: <path>`. Trim it on the way: the repo wants the rule and the evidence, not the session narrative.
- **Workspace knowledge** — a test result or dead end that only mattered inside this feature. Mark it `scope: workspace`; it goes away with the folder.

Same pass, briefly: `questions/` (an answer that constrains future work is a decision — it belongs in step 2 or 3), and `logs/` (raw logs are workspace-only unless a document cites one).

Done when: every finding carries `repo: <path>` or `scope: workspace`, and every `repo:` one exists at that path.

### 5. Commit the repo side

Verify the repo gates for what you touched (docs-only changes have nothing to gate — say so), then commit under the repo's own rules, with an explicit pathspec.

Never stage or commit anything under the workspace root, and never run git inside it when it has its own repository.

Done when: the ADRs, glossary, docs and moved findings are committed, and the commit hash is in your report.

### 6. Final report

`/tracker report` → the user sends it → `/tracker sent <date> <N>%`. The progress number should land at 100% once every item is `done` and reported; if it does not, say which item's weight is missing rather than adjusting the arithmetic.

Done when: the final report is sent and ticked, or the user has said they will send it later.

### 7. Close the index and hand over the folder

- Move the workspace's row from `## Active` to `## Shipped` in the root `INDEX.md`: the slug, today's date, and **where the knowledge landed** (ADR ids, doc paths, glossary terms). That row outlives the folder and is the only pointer from the feature's name to its reasoning.
- Rewrite `WHATNEXT.md` one last time: state that the wrap-up is done, and that the only step left is the user deleting the folder.
- Tell the user the exact path to delete, and that you are not deleting it. When the root has its own git repository, note that its history keeps these notes recoverable after the folder is gone — committing or tagging there is theirs to do, not yours.

Done when: the index shows the feature shipped, and the user has been told exactly what to delete.

### 8. Report

In the workspace language: the ADRs written, the docs and glossary terms updated, the findings moved (and to where), the commit, the report status, and the deletion line for the user.
