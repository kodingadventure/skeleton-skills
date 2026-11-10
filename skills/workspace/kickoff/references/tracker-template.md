# <Feature> — Progress Tracker

The single source for progress reports on <feature>. Technical context is in `CONTEXT.md`. Agents add to this file as work happens; a reporting agent turns it into a report (skill `tracker`, or by following `## Report rules` below).

## How this tracker works

- **Baseline: <B>%.** <What the baseline covers, or "Nothing was done before this tracker.">. The remaining <100 − B>% is split across the work items below; each item's weight is its share in percentage points.
- **Progress % = <B> + sum of weights of items with status `done`.** Items `in-progress` count 0 until done, so the number never goes backwards.
- **Status** (`todo` / `in-progress` / `done` / `blocked`) records the work. **The checkbox records reporting**: a row is ticked only after it has appeared in a report the user has actually sent. A work item is ticked only once a sent report has said it is `done`; being mentioned as in progress or next does not count. Agents doing the work never tick boxes; the reporting agent ticks them once the user confirms the report was sent.
- Mark an item `done` only when its work is finished and verified.
- Every action worth reporting goes into the **Action Log** with its date (YYYY-MM-DD), newest at the bottom. **One row per meaningful action** — something built, tested, found, decided or asked; micro-steps merge into one row, and anything nobody outside the session would call an event does not belong here.
- Write every row in plain words the report audience follows: no file names, code symbols or jargon.

## Report rules

- **Audience:** <none, or name, role, how technical>. With `none`, no reports are written: `tracker report` and `tracker sent` decline, and `wrap-up` skips the final report.
- **Language:** <English, or the language the audience reads>, whatever the language of this tracker.
- **Sections, in this order:** What was done · In Progress · Next · Blockers · Open Questions.
- **Style:** short sentences, plain words the audience understands. No file names, paths, code names, symbols, markdown tables or emoji. Bullets are fine.
- **Coverage:** everything unticked; ticked rows only as one-line context.
  - What was done: `done` items, unticked Action Log rows and Decisions.
  - In Progress: `in-progress` items. Next: the next `todo` items in table order.
  - Blockers and Open Questions: unticked rows not yet resolved or answered; say who must act.
  - Report Notes: for every unticked note whose item the report covers, include the note under that item.
- **Header:** the date and the progress %, with the change since the last Report History row.

## Work Items

| Reported? | ID   | Weight | Status | Item   |
| --------- | ---- | ------ | ------ | ------ |
| [ ]       | <ID> | <w>    | todo   | <item> |

Total remaining weight: <100 − B>.

The `Reported?` columns here and in the tables below, and `## Report History`, stay empty when `Audience: none`.

## Decisions

| Reported? | Date | Decision |
| --------- | ---- | -------- |

## Open Questions

Detail of each question (context, options, consequences) lives in its file in `questions/`; the row holds one plain sentence. The `File` column is for agents and never appears in a report.

| Reported? | Date raised | For | Question | Answer | File |
| --------- | ----------- | --- | -------- | ------ | ---- |

## Report Notes

Things a report must say when the related item is reported.

| Reported? | Item | Note |
| --------- | ---- | ---- |

## Blockers

| Reported? | Date | Blocker | Resolved |
| --------- | ---- | ------- | -------- |

## Action Log

| Reported? | Date | Action |
| --------- | ---- | ------ |

## Report History

| Date sent             | Progress % | Notes                      |
| --------------------- | ---------- | -------------------------- |
| (before this tracker) | <B>        | <what the baseline covers> |
