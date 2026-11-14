# Workspace

Feature workspaces: one git-ignored folder per feature or task, from a hand-written PRD to a shipped feature whose knowledge has moved into the repo. The nine skills reference each other — install them together.

- **[kickoff](./kickoff/SKILL.md)** — Turns a PRD discussion into a workspace: `CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`, the folder layout and the `INDEX.md` row, in the PRD's language.
- **[tracker](./tracker/SKILL.md)** — `log` a session, record a stakeholder's `answer`, and — when the workspace has a report audience — draft a progress `report` and mark it `sent`.
- **[pause-here](./pause-here/SKILL.md)** — Closes a session (or syncs a stale `WHATNEXT.md`): tracker logged, findings and questions written, `WHATNEXT.md` rewritten, a handoff when needed. The model may invoke it on its own.
- **[resume-here](./resume-here/SKILL.md)** — Opens a session: reads `WHATNEXT.md`, `CONTEXT.md` and the handoff, reconciles drift with git, then takes next step 1.
- **[discuss](./discuss/SKILL.md)** — Talks a topic through without starting work; loads only what the topic touches and records whatever gets settled.
- **[so-far](./so-far/SKILL.md)** — Recaps a workspace for a user who lost the thread: stages of work, decisions with how each was made (reviewed, unread, skipped), why the next step is next. Read-only.
- **[spin-off](./spin-off/SKILL.md)** — Hands one thread of the current session to a workspace (a brief + a next step), or seeds a new one (`PRD.md` + brief + minimal `CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`) that `kickoff` completes. The model may invoke it on its own; the user still confirms the slice and the destination.
- **[wrap-up](./wrap-up/SKILL.md)** — Closes a finished workspace: ADRs still owed, findings triaged into the repo, final report, `INDEX.md` row to `## Shipped`; the user deletes the folder.
- **[msg](./msg/SKILL.md)** — Drafts a chat message to a teammate from a question file or workspace file, in the tone recorded in `.scratch/TEAM.md`.

## The flow

```
0. User writes PRD.md             .scratch/workspaces/<slug>/PRD.md (+ input files)
1. Discuss the PRD                free, or /grilling (mattpocock/skills)
2. /kickoff <slug>                CONTEXT.md, TRACKER.md, WHATNEXT.md, layout, INDEX.md row
3. /to-plan                       plans/01-<name>/IMPLEMENTATION_PLAN.md (+ phases/)
4. /execute-plan                  phase by phase; after each: tracker status, Action Log, WHATNEXT.md,
   │                              and the ADR of any decision the phase's code just settled
   ├─ stakeholder answers         /tracker answer "<answer>"
   └─ report due (optional)       /tracker report → user sends → /tracker sent <date> <N>%
 * Think, don't work yet          /discuss <slug> <topic>
 * Lost the thread                /so-far <slug> [period]
 * A thread from another session  /spin-off <slug> | new <slug>
5. Stop for today                 /pause-here <slug>
6. Next session                   /resume-here <slug>  → back to 4
7. Feature done                   /wrap-up <slug>  → final report; the user deletes the folder
```

## Layout

```
.scratch/workspaces/
  INDEX.md                  # one row per workspace (English): active, seeded, shipped
  <slug>/
    PRD.md                  # written by the user
    CONTEXT.md              # refined spec + workspace rules (language, layout, conventions)
    TRACKER.md              # work items, weights, decisions, questions, Action Log, report rules
    WHATNEXT.md             # what to do next; rewritten, never appended (~40 lines)
    plans/NN-<name>/        # IMPLEMENTATION_PLAN.md + phases/
    findings/  questions/  handoffs/  reports/  docs/  logs/ (optional)
```

The root is `.scratch/workspaces/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another. It must be git-ignored by the main repo; giving `.scratch/` its own git repository keeps a history of the notes after a workspace is deleted (the skills never run git inside it).

The user picks the root once, on the repo's first workspace, and `spin-off` or `kickoff` writes it as a `Workspace root:` line in `CLAUDE.md` / `AGENTS.md`, which every skill and the commit reminder hook read: `kickoff/references/workspace-root.md`.

## Principles

- **Self-describing.** A workspace's rules live in its own files (`CONTEXT.md` `## Workspace rules`, `TRACKER.md` `## How this tracker works` / `## Report rules`). A plain prompt — "read `CONTEXT.md`, continue with `WHATNEXT.md`" — works without any skill, and where a file and a skill differ, the file wins.
- **Languages.** The workspace language is the language of the PRD's prose; progress reports are written in the language `kickoff` asked for (the `Language:` line of `TRACKER.md`), and `INDEX.md` is always English; code, commits and committed docs follow the repo's rules.
- **Status records work, the checkbox records reporting.** Only `/tracker sent` ticks a row; a work item is ticked once a sent report called it `done`.
- **Knowledge moves into the repo as it is learned.** Decisions carry an `ADR:` tag when written (`candidate` / `no`); the phase whose code embodies a candidate writes its ADR (`execute-plan` Step C, or `review-phase` / `guard-plan` under guardian), and a feature plan's docs phase documents what shipped. `wrap-up` only sweeps the remainder and triages `findings/` (`repo: <path>` or `scope: workspace`). Never cite a workspace by its folder name from the repo — it will be deleted.
- **Ask, don't guess, which workspace.** Every skill resolves the workspace the same way (argument → this conversation's workspace → the only `## Active` row of `INDEX.md` → ask) and names it (`Workspace: <slug>`) before writing. `spin-off` never falls back: the destination is always the user's choice.

## Progress reports are optional

`kickoff` asks whether anyone receives progress reports on the work. The default is `Audience: none`: the tracker is then only the work log, `tracker report` and `tracker sent` decline, and `wrap-up` skips the final report. Answer with an audience and a language and the report skills switch on.

## Optional hook: reminder after a commit

`hooks/workspace-reminder.mjs` is a `PostToolUse` hook (matcher `Bash`). After a `git commit`, when the workspace root's `INDEX.md` has rows under `## Active`, it tells the agent which workspaces are live and asks it to update the one the commit moved (`WHATNEXT.md`, `TRACKER.md`, the `INDEX.md` row) — the nudge a session that never opened the workspace would otherwise miss. Silent in every other case, including a commit in another git repository, such as a separate repository for your notes. Claude Code only, and safe to skip. Copy it to `.claude/hooks/` and register it in `.claude/settings.json` with the block in `hooks/settings-snippet.json`. It is not installed by `skills add`.

## Companion changes in other groups

These workflow skills are workspace-aware and do nothing different when no workspace is involved:

- `to-plan` writes a workspace's plans to `plans/NN-<name>/`, in the workspace language, with a `Tracker` column in the Phase Index.
- `execute-plan` (Step C, step 2) and `review-phase` (step 10) update the tracker, `WHATNEXT.md`, the `INDEX.md` row and owed ADRs after each phase; their reports carry a `**Workspace:**` line.
- `writing-great-plan` puts split phase files in `phases/`.
- `whatnext` reads `INDEX.md` first and routes to `/resume-here`, `/kickoff`, `/discuss` or `/wrap-up`.

They also rely on skills from [`mattpocock/skills`](https://github.com/mattpocock/skills): `domain-modeling` (required by `wrap-up` for ADRs and the glossary, and by `execute-plan` and `review-phase` when an ADR is due; each stops with a clear message when it is missing), `grilling` (recommended, used by `discuss` if installed) and `setup-matt-pocock-skills` (creates `docs/agents/`). The full table and the pinned install command are in the [root README](../../README.md).

## Notes

- Three skills may start on their own: `kickoff`, `pause-here` and `spin-off`. The rest run only when called by name.
- `msg` sets `model: haiku` in its frontmatter; only Claude Code honours it.
