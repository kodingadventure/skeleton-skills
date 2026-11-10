# Plan templates

Two shapes — pick by plan homogeneity, per `SKILL.md`:

- **Feature-shape** — heterogeneous phases (database → backend → frontend), per-item checkboxes. Used by `to-plan`.
- **Maintenance-shape** — homogeneous, mechanical phases (lint/complexity/fallow fixes), one `[ ] Done` checkbox per phase. Used by the triage skills.

Each shape has a **single-file** and a **multi-file** variant — pick the file variant by the splitting triggers in `SKILL.md` ("Splitting large plans").

These templates show the **maximum** set of sections. Every one of them is subject to `SKILL.md` → **Economy**: drop a section rather than fill it with content the executor can't act on.
An omitted section costs nothing; a padded one costs on every read.

## Contents

- [Feature-shape — single-file](#feature-shape--single-file)
- [Feature-shape — multi-file (split per phase)](#feature-shape--multi-file-split-per-phase)
- [Maintenance-shape — single-file](#maintenance-shape--single-file)
- [Maintenance-shape — multi-file (split per session)](#maintenance-shape--multi-file-split-per-session)
- [Field reference](#field-reference)

---

## Feature-shape — single-file

Use when the plan stays under every splitting trigger.

```markdown
# Implementation Plan: <Feature Name>

**Status:** pending
**Review:** guardian
**Verify:** `<command that proves the work, e.g. npm test>`
**Repo:** `/absolute/path`

<!-- Review: keep only when the repo has review-phase installed.
     Verify: only when the repo has no docs/agents/verify.md; otherwise omit the line.
     Repo: one repo. For 2+ repos replace the line with a `## Environment` table
     (| What | Absolute path |, one row per repo). -->

## Overview

<2–3 sentences: what is being built, which layers are affected, key constraints.>

## Open Questions

<!-- Omit the section when nothing is open. -->

- <Question>? Default: <the assumption the executor uses when this stays unanswered>. Affects: <item title>.

## Phases

### Phase 1: <Name> — Weight: M

- [ ] **<Item title>** (S)
  - What: <Full context inline: DTO shapes, field lists, business rules, mockups. An executor with
    fresh context should be able to copy-paste and go — no back-and-forth. Data, not evidence.>
  - Files: `path/to/file.go`
  - Skill: `<skill>`

- [ ] **<Item title>** (M)
  - [ ] `path/to/file-a.go`
  - [ ] `path/to/file-b.go`
  - What: <Batched item touching both files above in one invocation — see sub-bullet
    convention in `SKILL.md` for how to resume mid-item. Sub-bullets replace the `Files:` line.>
  - Skill: `<skill>`

Suggested commit: feat(phase-01): add <entity> model and migration

---

### Phase 2: <Name> — Weight: L

- [ ] **<Item title>** (L)
  - What: <Business logic details, validation rules, edge cases.>
  - Why: <L/XL only — the constraint that ruled out the obvious approach>
  - Provenance: <command that established the factual claim in What:, or `unverified — check first`>
  - Files: `path/to/form.tsx`

Suggested commit: feat(phase-02): wire <entity> form to the API

---

### Phase 3: <Name> — Weight: L

**Execution unit:** one `<module>` per agent run. Guardian reviews and commits before the next
module starts — never batch modules into one invocation.

**Order:** <list the named units in execution order, e.g. simple → complex>

- [ ] **`<UNIT>` — <item title>** (L)
  - What: <Same instructions apply to every unit; fill in `<UNIT>` at execution time.>
  - Files: `path/to/<unit>/**`

Suggested commit: feat(phase-03): <verb> <unit-placeholder>

## Manual Test Checkpoints

1. After Phase 2 — <surface to drive>: <1–2 concrete scenarios, expected result>

## Notes

<Only what spans two or more phases: cross-cutting constraints, ADR references, traps an executor
would otherwise fall into. Phase-local warnings belong in their phase, not here. In a workspace, point at the workspace's decision instead of copying it.>
```

---

## Feature-shape — multi-file (split per phase)

Use once any splitting trigger fires. Entry point holds no checklist items; each phase file owns its own `Files:`.

### Entry point: `IMPLEMENTATION_PLAN.md`

```markdown
# Implementation Plan: <Feature Name>

**Status:** pending
**Review:** guardian
**Verify:** `<command that proves the work, e.g. npm test>`
**Repo:** `/absolute/path`

<!-- Review: keep only when the repo has review-phase installed.
     Verify: only when the repo has no docs/agents/verify.md; otherwise omit the line.
     Repo: one repo. For 2+ repos replace the line with a `## Environment` table
     (| What | Absolute path |, one row per repo). -->

## Overview

<2–3 sentences: what is being built, which layers are affected, key constraints.>

## Open Questions

<!-- Omit the section when nothing is open. -->

- <Question>? Default: <the assumption the executor uses when this stays unanswered>. Affects: <item title>.

## Phase Index

| #   | Phase             | Weight | Batch | File                                 |
| --- | ----------------- | ------ | ----- | ------------------------------------ |
| 1   | Database & Entity | M      | —     | `phases/phase-01-database-entity.md` |
| 2   | Frontend Feature  | L      | —     | `phases/phase-02-frontend.md`        |

> Open the file for the phase you're executing. Each phase file is self-contained. Start from
> Phase 1 and work forward. Phases sharing a `Batch` letter may run concurrently.

<!-- Drop the Batch column entirely when no batch qualifies — see "Parallel batches" in SKILL.md. -->
<!-- Drop the batch sentence from the callout with it. -->

## Manual Test Checkpoints

1. After Phase 2 — <surface to drive>: <1–2 concrete scenarios, expected result>

## Notes

<Only what spans two or more phases. See single-file variant. In a workspace, point at the workspace's decision instead of copying it.>
```

### Per-phase file: `phases/phase-<NN>-<name>.md`

```markdown
# Phase <N>: <Name>

Weight: <S | M | L | XL>
Depends on: <phases that must complete first, or "nothing">
Prone to: <failure-mode name from the repo's docs/agents/failure-modes.md>, <another> <!-- omit the line if that file doesn't exist -->

## Context

<Omit this section entirely unless two or more items below share these facts — a single-item phase
has none. Shared data only: business rules, DTO shapes, mockups, lookup tables.>

## Checklist

- [ ] **<Item title>** (S)
  - What: <Everything specific to this item. Do not restate Context.>
  - Files: `path/to/file.go`
  - Skill: `<skill>`

- [ ] **<Item title>** (L)
  - What: <as today>
  - Why: <L/XL only — the constraint that ruled out the obvious approach>
  - Provenance: <command that established the factual claim in What:, or `unverified — check first`>
  - Files: `path/to/other-file.go`

Suggested commit: feat(phase-01): add <entity> model and migration
```

---

## Maintenance-shape — single-file

Use for triage/audit plans. One `[ ] Done` checkbox per phase — a phase may
bundle many files behind one skill invocation.

<!-- `Verify` and `Repo` follow the same rules as in the feature-shape header. -->

```markdown
# Implementation Plan: <Description>

**PlanType:** backend-refactor
**Status:** pending
**Review:** guardian
**Verify:** `<command that proves the work>`
**Repo:** `/absolute/path`

## Overview

<1–2 sentences. Total issues, files, phases.>

## Phases

### Phase 1: <Name> · <skill-name> (S)

- [ ] Done
  - [ ] `path/to/file-a.go`
  - [ ] `path/to/file-b.go`

/<skill-name>
path/to/file-a.go (N issues — linter)
path/to/file-b.go (M issues — linter)

Suggested commit: refactor(phase-01): fix <linter> issues in <package>

### Phase 2: <Name> · <other-skill-name> (M)

- [ ] Done

/<other-skill-name>
<app>/src/path/to/file.ts :23 ComponentName 95 lines

Suggested commit: refactor(phase-02): split <ComponentName> below complexity threshold

## Manual Test Checkpoints

None — all changes are internal refactors verified by lint/build.
```

---

## Maintenance-shape — multi-file (split per session)

Use once any splitting trigger fires. Group phases into **sessions of ~5–7 phases** — batching amortizes the context/output overhead of re-deriving patterns each invocation. Sessions replace
per-phase files as the split unit; a session is not a phase.

### Entry point: `IMPLEMENTATION_PLAN.md`

```markdown
# Implementation Plan: <Description>

**PlanType:** backend-refactor
**Status:** pending
**Review:** guardian
**Verify:** `<command that proves the work>`
**Repo:** `/absolute/path`
**Total issues:** <N> · **Phases:** <N> · **Sessions:** <N>

## Overview

<1–2 sentences.>

## Session Index

| Session   | Phases | Weight (dominant) | Batch | File                   |
| --------- | ------ | ----------------- | ----- | ---------------------- |
| Session 1 | 1–5    | S                 | —     | `phases/session-01.md` |
| Session 2 | 6–10   | S                 | —     | `phases/session-02.md` |

> Open the file for the session you're executing. Each session file is self-contained. Start
> from Session 1 and work forward. Sessions sharing a `Batch` letter may run concurrently.

<!-- Batch on the session, never on a phase inside it — the session is the dispatch unit here. -->
<!-- Drop the column and the batch sentence when no batch qualifies. -->
<!-- Per-package refactor sessions are usually disjoint by construction — check before defaulting to —. -->
<!-- See "Parallel batches" in SKILL.md. -->

## Manual Test Checkpoints

None — all changes are internal refactors verified by lint/build.
```

### Per-session file: `phases/session-<NN>.md`

```markdown
# Session <N>: Phases <A>–<B>

<Same phase blocks as the maintenance single-file template above, one per phase in this
session's range — including each phase's `Suggested commit:` line.>
```

---

## Field reference

| Field                     | Applies to                | Description                                                                                                                                                                                                                 |
| ------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Status`                  | header                    | `pending` at authoring time; `execute-plan` sets `in-progress` / `done`; the owner may set `abandoned`.                                                                                                                     |
| `Review`                  | header                    | `guardian` when `review-phase` is installed, else omit.                                                                                                                                                                     |
| `Verify`                  | header                    | Only when the repo has no `docs/agents/verify.md`; the command that proves the work.                                                                                                                                        |
| `Repo`                    | header                    | The single absolute path of the target repo.                                                                                                                                                                                |
| `PlanType`                | header                    | Maintenance plans only (e.g. `backend-refactor`, `fallow`, `docs-fix`, `skill-fix`); no line means a feature plan.                                                                                                          |
| `Environment`             | plan header               | Only for a plan that touches 2+ repos: a table with one absolute path per repo. A plan with one repo uses the `Repo` line instead.                                                                                          |
|                           |                           | Declared per-phase (feature-shape, phases differ in type) or once at the plan header (maintenance-shape, every phase shares one type).                                                                                      |
| `Weight`                  | item / phase              | Bare `(S)`/`(M)`/`(L)`/`(XL)` on the checkable unit. Required, no exceptions.                                                                                                                                               |
| `Depends on`              | phase file                | Phases that must complete first, or `nothing`. Counts shared-file writes, not just logical order — see "Parallel batches" in `SKILL.md`.                                                                                    |
| `Prone to`                | phase file                | One line, phase-level only, next to `Depends on`. Failure-mode name(s) from the repo's `docs/agents/failure-modes.md`; omit if that file doesn't exist. Feature-shape only.                                                 |
| `Execution unit`          | phase file                | Required once a phase's checklist repeats across 5+ named units (modules, files, endpoints), is Weight L/XL, or any unit-checklist item needs a human. Next to `Prone to`. See "Repeating (per-unit) phases" in `SKILL.md`. |
| `Batch`                   | Phase / Session Index     | Letter marking phases an executor may run concurrently. Multi-file plans only; `—` for a phase that runs alone; drop the column when no batch qualifies.                                                                    |
| `Context`                 | phase file                | Facts shared by 2+ items. Omit entirely for single-item phases.                                                                                                                                                             |
| `What`                    | item                      | Item-specific detail inline — DTO shapes, mockups, business rules, no external chasing. Never restates `Context`.                                                                                                           |
| `Why`                     | item                      | L/XL items only — the constraint that ruled out the obvious approach. See "Scale Economy by Weight" in `SKILL.md`. Feature-shape only.                                                                                      |
| `Provenance`              | item                      | Data, not evidence — exempt from the evidence cut. Required only on a codebase claim the executor would otherwise take on faith; never on a decision. See "Data is not evidence" in `SKILL.md`. Feature-shape only.         |
| `Files`                   | item                      | Files to create/modify. Omit for no-file items, or when sub-bullets already name them.                                                                                                                                      |
| `Skill`                   | item                      | Skill to invoke. Omit if no skill covers it.                                                                                                                                                                                |
| `Sub-bullets`             | item                      | Required when an item batches multiple files — see partial-completion convention in `SKILL.md`.                                                                                                                             |
| `Manual Test Checkpoints` | plan-level                | Mandatory section, every plan. Default text when no phase changes observable behavior.                                                                                                                                      |
| `Open Questions`          | plan-level                | Question + `Default:` + `Affects:`; deleted once answered, the answer written into the affected item.                                                                                                                       |
| `Notes`                   | plan-level                | Only what spans 2+ phases. Phase-local traps live in their phase file. In a workspace it points at the workspace's decision.                                                                                                |
| `Suggested commit:`       | phase / commit-checkpoint | Literal, ready-to-use commit message, written at plan-authoring time.                                                                                                                                                       |
