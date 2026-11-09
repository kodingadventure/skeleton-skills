# <Feature> — Agent Context

**Start here.** The refined spec and shared memory for every agent working on <feature>. It supersedes `PRD.md` where they differ (`PRD.md` is the user's original request, kept for reference). Progress and reporting: `TRACKER.md`. The next step: `WHATNEXT.md`.

## Workspace rules

### Language

- **Workspace language: <language>.** Talk with the user in it, and write every document in this folder in it (this file, `TRACKER.md`, `WHATNEXT.md`, plans, findings, questions, handoffs).
- **Exceptions:** <none, or "file or section: language">
- **Progress reports** (`reports/`): English, always.
- **Code, commits and files committed to the repo:** follow the repo's own rules (`CLAUDE.md` / `AGENTS.md`).
- Keep literal in every language: file names, code, status tokens, UI strings.

### Layout

Everything about this <feature> stays in `<workspace path>/` (git-ignored). The folder is deleted when the work ships. `INDEX.md` at the root above lists every workspace; this one has a row there while it is live.

<When the root has its own git repository: it is separate from the main repo — never stage anything under it from the main repo, and never run git inside it unless the user asks.>

- `PRD.md` — the original request.
- `CONTEXT.md` — this file.
- `TRACKER.md` — progress and report rules.
- `WHATNEXT.md` — what to do next; rewritten, never appended.
- `plans/NN-<name>/IMPLEMENTATION_PLAN.md` (+ `phases/phase-NN-<name>.md`) — one folder per plan, numbered in order.
- `findings/YYYY-MM-DD-<topic>.md` — one discovery per file: a test result, a root cause, a gotcha. Listed in `## Findings` below.
- `questions/YYYY-MM-DD-<topic>.md` — one question per file, for someone outside the session to answer: context, options, answer, consequences. Open ones are listed in `## Open questions` below; each has a row in `TRACKER.md`.
- `handoffs/YYYY-MM-DD-<topic>.md` — session handoffs; written once, never edited.
- `reports/progress-report-YYYY-MM-DD.md` — progress report drafts.
- `docs/` — input material: mockups, sample data, earlier notes.
- `logs/` (optional) — raw logs and notes from manual tests.

### Conventions

- When a discussion settles something, update `## Decisions` here and the question's file, **and** log it in `TRACKER.md` (see its rules).
- **Every decision carries an `ADR:` tag**, set when the decision is written and the reasoning is still fresh: `candidate` when all three hold — hard to reverse · a later reader will ask why · the result of a real trade-off — else `no`. It is a note to the agent that closes the phase, not a promise to the user.
- **An `ADR: candidate` becomes an ADR when the code that embodies it lands**, not when this folder is deleted: the phase that ships it writes the ADR (`execute-plan` Step C, or `review-phase` under guardian) and replaces the tag with the ADR id. Terms this work coins go into the repo's glossary in the same pass.
- **Nothing in this folder is visible to other work.** A decision, term or gotcha another feature would need is shared only once it is in the repo; cite it by ADR id or doc path, never by this folder's name. The repo's own `CONTEXT.md` is a different document with different rules (a glossary); this file is a spec and shared memory.
- **Keep `WHATNEXT.md` current.** When a session finishes one of its next steps (a plan phase, a test, an answer received), update its State now and Next steps before the session ends: done steps leave, a partly done step keeps only what remains. Keep this workspace's row in the root `INDEX.md` in step with it.
- Before the folder is deleted, `/wrap-up` sweeps what is left into the committed codebase: <how this repo records decisions and docs, e.g. ADRs, module docs>. It triages `findings/` too, so each entry in `## Findings` carries `repo: <path>` (its content now lives there) or `scope: workspace` (it dies with the folder).
- <project-specific rules>

## Summary

<What the feature does, for whom, and why. The refined version of the PRD.>

## Decisions

1. <decision> — <why> · `ADR: no | candidate | <id>`

## Open questions

- <who>: <one line> — `questions/<file>.md`

## Findings

- <YYYY-MM-DD> <one line> — `findings/<file>.md` · `scope: workspace | repo: <path>`

## Plans

- `plans/01-<name>/` — <one line: scope, status>
