---
name: tracker
description: Keep a workspace's TRACKER.md current and turn it into progress reports — log a session, record a stakeholder's answer, draft a report (always English), mark a report as sent.
argument-hint: '<workspace> log | answer "<answer>" | report | sent <YYYY-MM-DD> <N>%'
disable-model-invocation: true
---

# Tracker

Works on the `TRACKER.md` of a **workspace** (a feature folder set up by `kickoff`, `.scratch/plan/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root).

## Before any command

1. **Locate the workspace** — the same order in every workspace skill:
   1. the slug or path in the argument (in any position);
   2. the workspace this conversation has already been working in;
   3. `INDEX.md` at the workspace root: the only row under `## Active` (no `INDEX.md` → the only `*/TRACKER.md` under the root);
   4. still more than one → ask, listing the `## Active` rows.

   Never pick between two live workspaces. Name the one you resolved in one line before writing anything: `Workspace: <slug>`.

2. **Read** `CONTEXT.md` `## Workspace rules` (the languages) and the whole `TRACKER.md`. Its `## How this tracker works` and `## Report rules` sections bind every command below; where they differ from this skill, the tracker wins.
3. **Today's date** is the date for every new row.

**The tick rule:** only `sent` ticks checkboxes. Every other command adds and edits rows unticked, and leaves weights, the baseline and Report History alone. A **work item's** tick means a sent report said it is `done`; an item a report only mentioned as in progress or next stays unticked, so its completion is still reported later.

Write rows in the tracker's own language (the workspace language unless `CONTEXT.md` lists the tracker as an exception), in plain words the report audience follows.

## `log` — record what happened in this session

From this conversation (and `git log` for commits made in it):

- One Action Log row per meaningful action: something built, tested, found, decided or asked. Merge micro-steps into one row.
- Move the status of every work item whose work moved. `done` only when finished and verified.
- New decisions, blockers and report notes as new rows; fill the Answer / Resolved column of existing rows that were settled.
- A new open question gets its file in `questions/`, its row (one plain sentence, `File` column) and its `CONTEXT.md` index line, per `.claude/skills/kickoff/references/question-template.md`.
- When a decision or question was settled, update the question's file and `CONTEXT.md` `## Decisions` / `## Open questions` too. Every decision entry carries its `ADR:` tag (the criteria are in `CONTEXT.md` `### Conventions`): `candidate` when it is hard to reverse, will make a later reader ask why, and was a real trade-off; else `no`.
- **Always refresh `WHATNEXT.md` `## State now`** — progress, branch, last commit, uncommitted files — even when this session finished none of the next steps. Those three lines are what goes stale in a session that worked outside the workspace, and they are cheap to rewrite. Update Next steps too whenever this session moved them: a finished step leaves, a partly done one keeps only what remains, and work this session created that the next session must act on becomes a step of its own, naming who acts — that is the whole point of logging from a session that was working elsewhere.
- **New work this session surfaced**, in this order: it is really part of an existing work item → no new row, just its status and a report note; else a new work item row, `todo`, with its weight **carved out of items that are not yet `done`** so the weights still total `100 − baseline`; never take weight from a `done` item, which would lower a percentage already reported. Nothing left to carve from → weight 0, and say in your reply that the arithmetic needs the user's call.
- **Work unrelated to this feature gets no rows here.** The tracker feeds a report to the audience in `## Report rules`; a bug fix in another area would put something in that report they never asked about. Refresh `## State now` and stop there.

Done when: every action, status change and settled question in this session has its row, and nothing is ticked.

## `answer "<text>"` — record a stakeholder's answer

- Fill the Answer column of the matching open question (quote the gist).
- In its file under `questions/`: `Status: answered`, the `Answered:` line, `## Answer` and `## Consequences`. A question with no file yet gets one now.
- If it settles something: a Decision row, plus the same change in `CONTEXT.md` (`## Decisions`, with its `ADR:` tag; the question leaves `## Open questions`).
- When the answer changes what comes next, update `WHATNEXT.md` (Next steps, Waiting on).
- Unblock the related work items and blockers (status, Resolved column).
- One Action Log row.

Ambiguous match → show the candidate questions and ask.

Done when: the question's row and file, its decision, the items it unblocks, `WHATNEXT.md` and the log all reflect the answer.

## `report` — draft a progress report

- **Progress % = baseline + the sum of weights of `done` items.** State the number and the change since the last Report History row.
- Follow `## Report rules` exactly: audience, sections, style, coverage, report notes. For an open question, read its file in `questions/` and give the audience what they need to answer it (the options, in plain words). Write in **English** whatever the tracker's language; translate, never transliterate.
- Save the draft to `reports/progress-report-<today>.md` (add `-2`, `-3` when the file exists), marked as a draft not yet sent.
- Show the draft in the conversation and wait. Tick nothing.

Done when: every unticked row the rules require is covered, and the draft is saved and shown.

## `sent <YYYY-MM-DD> <N>%` — mark a report as sent

The report is the latest draft in `reports/` unless the user names another.

- Tick every row that report covered: Decisions, Report Notes, Open Questions, Blockers, Action Log, and the work items it reported as `done`. A work item that appeared only under In Progress or Next stays unticked.
- Add a Report History row: the sent date, the percentage, a one-line summary.
- Leave rows the report did not cover unticked.
- Mark the draft file as sent (its header line).

Done when: every covered row is ticked, every ticked work item has status `done`, the history row exists, and uncovered rows are untouched.

## Finish

When the progress %, a status, who is being waited on or the areas touched changed, refresh this workspace's row in the root `INDEX.md` — that row is how other sessions find this work. Leave every other row alone.

Reply in the workspace language with what changed (rows added, statuses moved, rows ticked) and the current progress %.
