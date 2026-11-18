# Workspaces

One row per workspace under this root. Detail never lives here — it lives in the workspace. This file exists so that any skill or session can find the live work, and the workspaces, in one short read.

`kickoff` adds the row, `pause-here`, `tracker`, `execute-plan` and `review-phase` keep it current, `wrap-up` moves it to `## Shipped`. Status: `active` · `paused` · `blocked`.

Rows are written in **English**, whatever language a workspace itself uses: this file is read across workspaces.

## Active

| Slug   | Goal                    | Status | Progress | Updated      | Waiting on                   | Areas                                          |
| ------ | ----------------------- | ------ | -------- | ------------ | ---------------------------- | ---------------------------------------------- |
| <slug> | <one line, plain words> | active | <N>%     | <YYYY-MM-DD> | <who owes what, or "nobody"> | <the modules, apps or paths this work touches> |

The **Areas** column is the collision warning: two active rows naming the same area means two sessions are editing the same code.

## Shipped

| Slug   | Shipped      | Knowledge landed in                                                                              |
| ------ | ------------ | ------------------------------------------------------------------------------------------------ |
| <slug> | <YYYY-MM-DD> | <the repo files that now carry what this workspace learned: ADR ids, wiki pages, glossary terms> |

A shipped row stays after the folder is deleted: it is the only pointer left from a feature's name to where its reasoning ended up.
