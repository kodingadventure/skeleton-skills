# Decision Tree — What Next

Generic routing for any repo. Skills marked _(if installed)_ come from outside this repo; when one is missing, fall back to the nearest installed skill or describe the step in plain words. Commands such as "the project's test command" are found in the project's own config (see SKILL.md Step 0.4), never assumed.

## Contents

- [After Discovery / Design](#after-discovery--design)
- [After Specification](#after-specification)
- [After Planning](#after-planning)
- [Workspace sessions](#workspace-sessions)
- [During Implementation](#during-implementation)
- [After Quality / Fixes](#after-quality--fixes)
- [After Commit](#after-commit)
- [When Stuck](#when-stuck)

## After Discovery / Design

| Completed                        | Next → Skill                                                                                                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /grilling session                | Hand the thread to a workspace → `/spin-off <slug> <topic>` (workspace skills installed), or write a spec → `/to-spec` _(if installed)_, or plan → `/to-plan` |
| /prototype answered the question | Hand the thread to a workspace → `/spin-off <slug> <topic>` (workspace skills installed), or write a spec → `/to-spec` _(if installed)_, or plan → `/to-plan` |

## After Specification

| Completed                                                                                                                                          | Next → Skill                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| PRD discussed in a `.scratch/workspaces/<slug>/` workspace without `CONTEXT.md`, or still under `## Seeded` in `INDEX.md` (a seed from `spin-off`) | Set up the workspace → `/kickoff <slug>`                                           |
| Spec written                                                                                                                                       | Plan directly → `/to-plan`, or break into tickets → `/to-tickets` _(if installed)_ |
| Issues created                                                                                                                                     | Plan first issue → `/to-plan <path>`                                               |

## After Planning

| Completed                                      | Next → Skill                                          |
| ---------------------------------------------- | ----------------------------------------------------- |
| Plan created                                   | Execute inline → `/execute-plan`                      |
| Plan created, many phases or a guardian wanted | Execute by subagents under a guardian → `/guard-plan` |
| Phase staged under a `Review: guardian` plan   | Check it before commit → `/review-phase`              |

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

## During Implementation

| Completed                                    | Next → Skill                                                                             |
| -------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Code written for a plan item                 | Tick the item, run the next one → `/execute-plan`                                        |
| Code written, no plan                        | Verify → `/verify`                                                                       |
| New behaviour with no test beside it         | Write the test first or now → `/tdd` _(if installed)_, otherwise add it directly         |
| Verify passed                                | Commit under the repo's own rules; read the change back → `/what-you-did`                |
| Verify failed                                | Fix the reported gate; a cause that is not obvious → `/diagnosing-bugs` _(if installed)_ |
| Unsure the design holds before building more | Throwaway experiment → `/prototype` _(if installed)_                                     |
| A choice needs the user's eyes               | Show it on a page → `/review-page`                                                       |

## After Quality / Fixes

| Completed                    | Next → Skill                                                  |
| ---------------------------- | ------------------------------------------------------------- |
| Tests pass                   | Commit under the repo's own rules (see below)                 |
| Bug diagnosed and fixed      | Add a regression test, then commit under the repo's own rules |
| Lint or type errors fixed    | Re-verify → `/verify`                                         |
| Code review feedback applied | Re-verify → `/verify`                                         |
| Branch ready for review      | Review the changes → `/code-review` _(if installed)_          |

## After Commit

Commit under the repo's own commit rules (`CONTRIBUTING.md`, `CLAUDE.md` / `AGENTS.md`, recent `git log` style). The optional `caveman-commit` skill from `JuliusBrussee/caveman` can draft the message if installed.

| Completed                          | Next → Skill                                                          |
| ---------------------------------- | --------------------------------------------------------------------- |
| Plan phase committed, items remain | Next phase → `/execute-plan` (or `/guard-plan` for a multi-file plan) |
| Plan finished                      | Read the whole change back → `/what-you-did`                          |
| Workspace work item finished       | Update the tracker and handoff → `/pause-here`                        |
| Feature committed, no plan left    | Start the next thing → `/whatnext` again, or `/to-plan` for a new one |
| Quick fix committed                | (done)                                                                |

## When Stuck

| Situation                      | Next → Skill                                                                   |
| ------------------------------ | ------------------------------------------------------------------------------ |
| Complex failure                | `/diagnosing-bugs` _(if installed)_                                            |
| Not sure what the user wants   | `/grilling` _(if installed)_                                                   |
| Architecture feels wrong       | `/codebase-design` _(if installed)_, otherwise `/review-page` with the options |
| Session too long               | In a workspace → `/pause-here`; otherwise summarise state in chat              |
| Docs out of sync with the code | `/refine-docs`                                                                 |
