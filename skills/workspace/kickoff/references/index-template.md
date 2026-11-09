# Workspaces

One row per workspace under this root. Detail never lives here — it lives in the workspace. This file exists so that any skill or session can find the live work, and the workspaces, in one short read.

`kickoff` adds the row (moving it from `## Seeded` when `spin-off` seeded the folder), `pause-here`, `tracker`, `execute-plan` and `review-phase` keep it current, `wrap-up` moves it to `## Shipped`. Status: `active` · `paused` · `blocked`.

Rows are written in **English**, whatever language a workspace itself uses: this file is read across workspaces.

## Active

| Slug   | Goal                    | Status | Progress | Updated      | Waiting on                   | Areas                                          |
| ------ | ----------------------- | ------ | -------- | ------------ | ---------------------------- | ---------------------------------------------- |
| <slug> | <one line, plain words> | active | <N>%     | <YYYY-MM-DD> | <who owes what, or "nobody"> | <the modules, apps or paths this work touches> |

The **Areas** column is the collision warning: two active rows naming the same area means two sessions are editing the same code.

## Seeded

| Slug   | Goal                    | Seeded       | Areas                                           |
| ------ | ----------------------- | ------------ | ----------------------------------------------- |
| <slug> | <one line, plain words> | <YYYY-MM-DD> | <the modules, apps or paths the thread touches> |

A seeded folder holds a `PRD.md`, an origin brief and minimal `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` written by `spin-off` (fields owed by the user say `TBD (kickoff)`): its next step is `/discuss <slug>` to shape the PRD, then `/kickoff <slug>`. It is not a live workspace until then.

## Shipped

| Slug   | Shipped      | Knowledge landed in                                                                              |
| ------ | ------------ | ------------------------------------------------------------------------------------------------ |
| <slug> | <YYYY-MM-DD> | <the repo files that now carry what this workspace learned: ADR ids, wiki pages, glossary terms> |

A shipped row stays after the folder is deleted: it is the only pointer left from a feature's name to where its reasoning ended up.
