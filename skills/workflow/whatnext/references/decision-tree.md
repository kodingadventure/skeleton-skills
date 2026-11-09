# Decision Tree — What Next

## Contents

- [After Discovery / Design](#after-discovery--design)
- [After Specification](#after-specification)
- [After Planning](#after-planning)
- [Workspace sessions](#workspace-sessions)
- [During Implementation (backend)](#during-implementation-backend)
- [During Implementation (frontend)](#during-implementation-frontend)
- [During Implementation (E2E)](#during-implementation-e2e)
- [After Quality / Fixes](#after-quality--fixes)
- [After Commit](#after-commit)
- [After Documentation](#after-documentation)
- [When Stuck](#when-stuck)

## After Discovery / Design

| Completed                        | Next → Skill                                                                                                                                                        |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /grill-with-docs session         | Hand the thread to a workspace → `/spin-off <slug> <topic>` (workspace skills installed), or write a spec → `/to-spec` (if installed)                               |
| /prototype answered the question | Hand the thread to a workspace → `/spin-off <slug> <topic>` (workspace skills installed), or write a spec → `/to-spec` (if installed), or skip to plan → `/to-plan` |

## After Specification

| Completed                                                                                                                                    | Next → Skill                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| PRD discussed in a `.scratch/workspaces/<slug>/` workspace without `CONTEXT.md`, or still under `## Seeded` in `INDEX.md` (a seed from `spin-off`) | Set up the workspace → `/kickoff <slug>`                                         |
| Spec written                                                                                                                                 | Plan directly → `/to-plan`, or break into tickets → `/to-tickets` (if installed) |
| Spec/request is one feature to build end to end (backend + frontend + tests + docs)                                                          | Orchestrate → `/orchestrate-feature` (if installed)                              |
| Issues created                                                                                                                               | Plan first issue → `/to-plan <path>`                                             |

## After Planning

| Completed    | Next → Skill              |
| ------------ | ------------------------- |
| Plan created | Execute → `/execute-plan` |

## Workspace sessions

Feature workspaces (`.scratch/workspaces/<slug>/`, set up by `/kickoff`) — only when the workspace skills are installed.

| Situation                                                                     | Next → Skill                                                                          |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| User stops mid-task in a workspace                                            | Save state → `/pause-here`                                                            |
| `WHATNEXT.md` is behind the repo (work done without the workspace)            | Sync → `/pause-here <what was done>`                                                  |
| Fresh session, a `WHATNEXT.md` exists                                         | Resume → `/resume-here <slug>`                                                        |
| User wants to think a workspace topic through, not work on it                 | Discuss → `/discuss <slug> <topic>`                                                   |
| A thread in this session (often outside any workspace) deserves its own focus | Hand it to a workspace → `/spin-off <slug> <topic>` or `/spin-off new <slug> <topic>` |
| Every work item `done`                                                        | Close the workspace → `/wrap-up <slug>`                                               |
| Work moved, or a stakeholder answered                                         | Update the tracker → `/tracker log` or `/tracker answer "<answer>"`                   |
| Report due                                                                    | Draft → `/tracker report`; once sent → `/tracker sent <date> <N>%`                    |

## During Implementation (backend)

| Completed                     | Next → Skill                                      |
| ----------------------------- | ------------------------------------------------- |
| Entity + DTO + migration done | Build repository → `/api-module-repository`       |
| Repository done               | Build service → `/api-module-service`             |
| Service done                  | Build handlers → `/api-module-handler`            |
| Handlers done                 | Wire module → `/api-module-wire`                  |
| Module wired                  | Verify → `/verify`                                |
| Verify failed (lint)          | `/lint-dispatch`                                  |
| Verify passed                 | Write integration tests → `/api-integration-test` |

**After backend integration tests are committed, run the full-stack gate before recommending wiki:**

1. Check `apps/<app>/src/features/` for a matching frontend feature directory.
2. If **missing** → recommend frontend CRUD pages first: `/ts-react-crud-feature`
3. If frontend exists, check `apps/<app>/e2e/` for a matching `.spec.ts`.
4. If **missing** → recommend E2E tests: `/ts-e2e-test`
5. Only after frontend pages **and** E2E tests exist → recommend `/update-wiki`

## During Implementation (frontend)

| Completed           | Next → Skill                                         |
| ------------------- | ---------------------------------------------------- |
| Swagger regenerated | Build CRUD pages → `/ts-react-crud-feature`          |
| CRUD pages done     | Write tests → `/ts-gen-test`                         |
| Custom page done    | Write tests → `/ts-gen-test`                         |
| Component done      | Write tests → `/ts-gen-test`                         |
| Tests pass          | Type-check → `moon run <app>:typecheck` or `/verify` |

## During Implementation (E2E)

| Completed           | Next → Skill                                         |
| ------------------- | ---------------------------------------------------- |
| Feature UI complete | Write E2E spec → `/ts-e2e-test`                      |
| E2E tests fail      | Debug → `/diagnosing-bugs` or fix selectors manually |
| E2E tests pass      | Commit → `/caveman-commit`                           |

## After Quality / Fixes

| Completed                    | Next → Skill                                         |
| ---------------------------- | ---------------------------------------------------- |
| Integration tests pass       | Commit → `/caveman-commit`                           |
| Unit tests pass              | Commit → `/caveman-commit`                           |
| Bug diagnosed and fixed      | Add regression test, then commit → `/caveman-commit` |
| Backend lint fixed           | Re-verify → `/verify`                                |
| Frontend fallow fixed        | Type-check → `moon run <app>:typecheck`              |
| Code review feedback applied | Re-verify → `/verify`                                |
| Translations synced          | No next step needed                                  |

## After Commit

Before recommending `/update-wiki`, always run the **full-stack completeness check**:

1. Does `apps/<app>/src/features/<module>/` exist? If **no** → `/ts-react-crud-feature` first.
2. Does `apps/<app>/e2e/<module>/` (or equivalent spec) exist? If **no** → `/ts-e2e-test` first.
3. Only when both exist → `/update-wiki`

| Completed                                    | Next → Skill                                |
| -------------------------------------------- | ------------------------------------------- |
| Feature committed, frontend + E2E both exist | Document → `/update-wiki`                   |
| Feature committed, frontend missing          | Build CRUD pages → `/ts-react-crud-feature` |
| Feature committed, E2E missing               | Write E2E spec → `/ts-e2e-test`             |
| Quick fix committed                          | (done)                                      |

## After Documentation

| Completed            | Next → Skill                                             |
| -------------------- | -------------------------------------------------------- |
| Wiki page written    | Code health → `/lint-dispatch` if needed                 |
| Full feature shipped | Start next feature, or run `/handoff` if session is long |

## When Stuck

| Situation                | Next → Skill                     |
| ------------------------ | -------------------------------- |
| Complex failure          | `/diagnosing-bugs`               |
| Architecture feels wrong | `/improve-codebase-architecture` |
| Session too long         | `/handoff`                       |
| Docs out of sync         | `/audit-docs` → `/refine-docs`   |
