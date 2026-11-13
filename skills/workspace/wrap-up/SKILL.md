---
name: wrap-up
description: Run only when the user asks for it by name. Close a finished feature workspace — writes the ADRs still owed, moves durable findings and vocabulary into the repo, sends the final report when the workspace has a report audience, updates the workspace index, and hands the folder to the user to delete.
argument-hint: "<workspace>"
disable-model-invocation: true
---

# Wrap Up

The last stage of a **workspace** (a feature folder set up by `kickoff`, `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root). The folder is deleted after this, so anything still only in it is about to be lost: this skill is the sweep that moves what must survive into the committed repo.

It is a sweep, not the main transfer. Decisions become ADRs as the code that embodies them lands (`execute-plan` Step C / `review-phase`), and a feature plan's docs phase documents shipped behaviour as it ships. What reaches this skill is the remainder.

## Resolving the workspace

The same order in every workspace skill:

1. the slug or path in the argument;
2. the workspace this conversation has already been working in;
3. `INDEX.md` at the workspace root: the only row under `## Active` (no `INDEX.md` → the only `*/WHATNEXT.md` under the root);
4. still more than one → ask, listing the `## Active` rows.

Never pick between two live workspaces. Before writing anything, name the one you resolved in one line: `Workspace: <slug>`.

## Steps

### 1. Start from the updated default branch

The work usually reached the default branch through a pull request, and this skill commits on top of it. Run `git fetch --prune`, then `git branch --show-current`.

- On the default branch → `git pull --ff-only`.
- On the feature branch, and its pull request is merged (`gh pr view --json state`, or the branch is gone from the remote after the prune) → `git switch <default> && git pull --ff-only`, then `git branch -d <feature branch>`.
- On the feature branch, and its pull request is still open → stop: the work has not landed. Tell the user to merge it first, then run this skill again.

Not a git repository → skip this step and say so in the report. The commit in step 6 starts from here: on a new branch when the repo's rules send changes through a pull request, else on the default branch.

Done when: the default branch is checked out and level with its remote, or the user has been told to merge first.

### 2. Check the work is actually finished

Read `CONTEXT.md` (`## Workspace rules`, `## Decisions`, `## Findings`, `## Conventions`), `TRACKER.md` and `WHATNEXT.md`.

**Check the dependency before anything is written.** If `CONTEXT.md` holds an `ADR: candidate` or a coined term to move (steps 3 and 4) and the `domain-modeling` skill is not installed, stop here, before changing anything, with one message: the `domain-modeling` skill is missing, it comes from `mattpocock/skills`, and see this repo's README for the pinned install command. Do not write an ADR or glossary format of your own.

Every work item `done`? If not, list the items that are not and ask the user whether to wrap up anyway — a feature parked indefinitely is a legitimate reason, a feature still in progress is not. Stop until they answer.

Done when: either every item is `done`, or the user has said to continue with the open ones listed.

### 3. Write the ADRs still owed

`grep -n "ADR: candidate" CONTEXT.md`. For each hit: write the ADR with the `domain-modeling` skill (from `mattpocock/skills`), where the repo keeps them, then replace the tag with the ADR id in `CONTEXT.md`.

Each one is a decision whose reasoning now exists nowhere else. Write what was decided, the alternatives that were on the table and why they lost — the workspace's decision entry, its question file and the findings it rests on are the sources; the ADR must stand on its own once they are gone.

A candidate that turns out not to meet `domain-modeling`'s three criteria (hard to reverse · a later reader will ask why · a real trade-off) is retagged `ADR: no` with one line saying where its reasoning lives instead. Do not pad the repo with ADRs for decisions that were never trade-offs.

Done when: no `ADR: candidate` is left in `CONTEXT.md`.

### 4. Move the vocabulary and the behaviour

- **Terms** the workspace coined or sharpened (the ones in `CONTEXT.md` that a new reader of the code would not guess) → the repo's glossary, via `domain-modeling`.
- **What shipped** — a module's rules, a status transition, a route, a screen, a flow → the repo's documentation. A plan's docs phase usually did this already: check it, and write only what is missing, with the documentation skills your agent lists: `update-wiki` for flows across code units and the feature index (when the Docs Layout has a `### Wiki` table), `refine-docs` for reference docs. Neither installed → edit the doc that owns the subject.

Done when: a reader of the repo alone can find what this feature does and what its words mean.

### 5. Triage `findings/` — the step that is easy to skip

Every file in `findings/` is about to be deleted. Each one is exactly one of:

- **Repo knowledge** — a tool, platform, device or environment gotcha that will bite the next feature too (not just this one). Move its content to the repo document that owns that subject, and mark the entry in `CONTEXT.md` `## Findings` as `repo: <path>`. Trim it on the way: the repo wants the rule and the evidence, not the session narrative.
- **Workspace knowledge** — a test result or dead end that only mattered inside this feature. Mark it `scope: workspace`; it goes away with the folder.

Same pass, briefly: `questions/` (an answer that constrains future work is a decision — it belongs in step 3 or 4), and `logs/` (raw logs are workspace-only unless a document cites one).

Done when: every finding carries `repo: <path>` or `scope: workspace`, and every `repo:` one exists at that path.

### 6. Commit the repo side

Verify the repo gates for what you touched (docs-only changes have nothing to gate — say so), then commit under the repo's own rules, with an explicit pathspec.

Never stage or commit anything under the workspace root, and never run git inside it when it has its own repository.

Done when: the ADRs, glossary, docs and moved findings are committed, and the commit hash is in your report.

### 7. Final report

`Audience: none` on `TRACKER.md` `## Report rules` → skip this step: no final report is written, and say so in step 9. Otherwise write it in the language of the `Language:` line.

`/tracker report` → the user sends it → `/tracker sent <date> <N>%`. The progress number should land at 100% once every item is `done` and reported; if it does not, say which item's weight is missing rather than adjusting the arithmetic.

Done when: the final report is sent and ticked, or the user has said they will send it later, or `Audience: none` made the step moot.

### 8. Close the index and hand over the folder

- If the workspace has a `github.md`, offer (do not run) a closing comment on its issue with the `github-send-update` skill, when that skill is installed, and check the issue is closed: `gh issue view <url> --json state`. Report the state; closing the issue is the user's call.
- Move the workspace's row from `## Active` to `## Shipped` in the root `INDEX.md`: the slug, today's date, and **where the knowledge landed** (ADR ids, doc paths, glossary terms). That row outlives the folder and is the only pointer from the feature's name to its reasoning.
- Rewrite `WHATNEXT.md` one last time: state that the wrap-up is done, and that the only step left is the user deleting the folder.
- Tell the user the exact path to delete, and that you are not deleting it. When the root has its own git repository, note that its history keeps these notes recoverable after the folder is gone — committing or tagging there is theirs to do, not yours.

Done when: the index shows the feature shipped, and the user has been told exactly what to delete.

### 9. Report

In the workspace language: the ADRs written, the docs and glossary terms updated, the findings moved (and to where), the commit, the report status (or that no report was due), and the deletion line for the user.
