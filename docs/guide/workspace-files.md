# What is in a workspace

This page answers one question: which of the files in a workspace folder do you have to read? Few of them. Most are the agent's working memory.

## The folder

A workspace is one folder under `.scratch/workspaces/` (the default root).

```
.scratch/workspaces/
  INDEX.md                  one row per workspace: active, shipped
  <slug>/
    PRD.md                  the request: written by you, or by kickoff or spin-off
    CONTEXT.md              refined spec and workspace rules
    TRACKER.md              work items, decisions, questions, Action Log
    WHATNEXT.md             what to do next; rewritten, never appended
    plans/NN-<name>/        IMPLEMENTATION_PLAN.md and phases/
    findings/  questions/  handoffs/  reports/  docs/  logs/
```

`logs/` appears only when the work involves manual tests. `guard-plan` writes the prompt and the result of a checkpoint test next to the plan, in `plans/<NN>-<name>/manual-tests/`. If you use `msg`, a `TEAM.md` (names and contacts) sits next to `INDEX.md`, outside any workspace; keep it git-ignored.

## What you read

- **`WHATNEXT.md`.** About 40 lines: where the work stands and what happens next. Open this one first.
- **The `/so-far` recap.** A page that tells you what was done and decided, and what waits on you. It opens in the browser and is saved in the OS temp directory, not in the workspace.
- **Review pages.** When the agent needs a decision from you, it writes a short HTML page to the temp directory and opens it. Read it, pick your options, and send the answer back to the agent.
- **Question files.** Each file in `questions/` is a question for someone outside the session. If it waits on you, it holds the context and the options.
- **Reports.** A draft in `reports/` is a progress report you send to your audience. It exists only when the workspace has one.

## The agent's working memory

You may open these. You do not have to.

- **`CONTEXT.md`.** The full spec, workspace rules, decisions and findings. Every agent reads it first.
- **`TRACKER.md`.** Weights, statuses, the Action Log and report rules.
- **`findings/`.** One discovery per file: a test result, a root cause, a dead end.
- **Plans and phases.** `plans/NN-<name>/IMPLEMENTATION_PLAN.md` and its `phases/` files.
- **`handoffs/`.** A note per paused session, or per thread moved in by `spin-off`; written once and never edited.

## All files at a glance

| File | What it holds | Who reads it | Main writers |
| --- | --- | --- | --- |
| `PRD.md` | The request: the problem, what is known, what is open | You, the agent | You, or `kickoff`, `spin-off` or `github-spin-off` from a conversation |
| `WHATNEXT.md` | State now and the next steps | You, the agent | `kickoff`, `pause-here`, `resume-here`, `discuss`, `spin-off`, `tracker`, `execute-plan`, `guard-plan`, `review-phase`, `wrap-up` |
| `CONTEXT.md` | Refined spec, rules, decisions | The agent | `kickoff`; updated by `discuss`, `pause-here` and others |
| `TRACKER.md` | Work items, Action Log, report rules | The agent | `kickoff`, `tracker`, `pause-here`, `discuss`, `spin-off`, `execute-plan`, `guard-plan`, `review-phase` |
| `plans/` | The plan and its phase files | The agent | `to-plan` |
| `findings/` | Discoveries to keep | The agent | `pause-here`, `spin-off`, `kickoff`, `discuss` |
| `handoffs/` | Session handoffs | The agent | `pause-here`, `spin-off` |
| `questions/` | Questions for others, with options and answers | You, the person who answers | `kickoff`, `pause-here`, `discuss`, `spin-off`, `tracker` (`answer`, `log`), `msg` (when you say it was sent) |
| `reports/` | Progress report drafts | You, then your audience | `tracker report` |
| `docs/` | Input material: mockups, sample data, notes | You, the agent | You; `kickoff` moves loose files in |

## It is temporary

The workspace folder is git-ignored, and you delete it after `wrap-up`. Anything that must outlive it has to be in the repo by then. See [Documentation and wrap-up](./documentation-and-wrap-up.md).

Next: [Documentation and wrap-up](./documentation-and-wrap-up.md)
