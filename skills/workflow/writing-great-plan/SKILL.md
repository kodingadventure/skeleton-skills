---
name: writing-great-plan
description: Formats and writes a plan execute-plan can run — Weight vs Tier, model/thinking-effort recommendations, checkbox atomicity, splitting, and required sections. Use when any plan-producing skill in this repo is ready to write or format its plan. Do not invoke directly to plan a feature from scratch — use to-plan (or another plan-producing skill), which invokes this skill as its final formatting step.
---

# Writing a great plan

A plan is a checklist an agent can execute item by item without re-reading the source spec, issue, or conversation. This is the single source of truth for these rules — every
plan-producing skill in this repo invokes this skill when it's ready to write or format a plan, instead of re-deriving the rules locally.

## When invoked to write a plan

The invoking skill has already done the domain legwork — located the source material, gathered or classified the items, decided phase/session grouping. Apply the rules below to that material:
cut it to what the executor needs (**Economy**), assign Weight/Tier, attach capability recommendations, pick single-file vs multi-file, and format against `references/template.md`. Hand the
finished plan back to the invoker to present. Before handing back, run `references/runner-check.md` — it reads the plan as the runner will and puts the evidence in the plan.

The invoker hands over **more material than belongs in the plan**. It gathered evidence to convince itself a gap is real; that job is done. Transcribing its findings verbatim is the single
biggest source of bloat in plans this repo has produced. Filtering is your job, not the invoker's.

## Economy

Every plan is read cold by a fresh executor, and every line it reads is budget spent before any work happens. Two readers get confused for each other:

- The **reviewer** reads the plan once to approve it, and wants to know _why_.
- The **executor** reads it to act, and needs only _what_ and _where_.

**Write for the executor.** The reviewer is in the session where the plan was authored and already has the invoker's report; the executor is not and never will be.

Economy trims redundancy and evidence — it never trims a fact the executor needs to act correctly. Cutting a load-bearing fact isn't economy, it's a defect that surfaces later as a wrong
decision, a stalled executor, or a re-derivation that lands somewhere different from what was already validated during planning. When a cut is ambiguous, the tie-breaker is Weight — see
"Scale Economy by Weight" below.

### Decisions, not the case for them

A plan records what was decided. It does not re-argue it. Once a phase exists, the executor has no decision to make about whether the work is warranted — that is settled by the plan's
existence. Cut the proof.

```markdown
<!-- Bad: 24 lines proving a doc qualifies as a reference doc. The executor cannot act on any of it. -->

**`docs/forms.md` is missing from that table** but is unambiguously a reference doc:

- 15.6K of pattern documentation (the repo's largest doc outside the architecture files)
- `docs/architecture.md`, section "Forms", explicitly delegates the entire form platform to it: "..."
- Two skills build on it (fictional names): `form-builder`, `form-checker`
  Because the block omits it, the docs audit doesn't know it's a reference doc and would keep re-flagging...

<!-- Good -->

- [ ] **Add `docs/forms.md` to `### Reference docs`** (S)
  - What: Scope `Frontend`. Follow the table's format spec in the `refine-docs` skill's `references/docs-layout.md`. Change nothing else in the block.
  - Files: `docs/agents/domain.md`
  - Skill: `refine-docs`
```

**Keep the rationale only when the executor could contradict it** — a non-obvious ordering constraint, a rejected alternative that looks tempting from inside the file, a trap that a
reasonable agent would walk into. Those earn one line, not a section. "Cheapest fix, so it goes first" is not one of them: phase numbers already carry order.

This bar is for **S/M** items. For **L/XL**, it's lower — see below.

### Scale Economy by Weight

How hard you cut depends on what the checkable unit demands from its executor — the Weight table already says so (`S`/`M`: mechanical/standard, apply literally; `L`/`XL`: reasoning, design
decisions):

- **S/M is mechanical.** The executor applies instructions literally and has no decision to make. Cut all rationale; the item's existence is enough.
- **L/XL requires reasoning.** An executor handed a design decision with no grounding doesn't skip the reasoning — it redoes it, from scratch, without the evidence the planner used to
  reach the answer. It can land somewhere different: "rediscovering" a path that was already tried and rejected during planning, because nothing on the page says it was. Retain the
  load-bearing rationale for these items — the constraint that ruled out the obvious approach, the alternative that was tried and failed, the edge case that shaped the design. Not the
  narrative that led there, just the decision plus the one fact that makes it non-obvious.

**Default when unsure: for L/XL, keep.** The asymmetry runs the other way here than it does for S/M — one extra line costs almost nothing; an executor silently diverging from an
already-validated design costs a re-review at best and a shipped regression at worst.

### Data is not evidence

The line is what the executor _consumes_ vs what merely _justifies_:

- **Data — keep.** A table of 31 verbatim swagger tags, DTO field lists, a state-transition map, a mockup, an exact error string. The executor would have to re-derive these, and might get them wrong.
- **Evidence — cut.** File-size measurements, "this is the largest module", quoted lines proving a claim, counts of nominees that were rejected for reasons already applied.

When cutting a rejected-nominee list, keep the _decision_ only if the executor might otherwise add them back: "Only these three qualify — do not add others." One line, no table of scores.

### Say each fact exactly once

The worst duplication is a `## Context` section that states everything, followed by a `What:` that paraphrases the same thing for the same single item. Ownership rule:

| Where               | Owns                                                                                              |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| `## Context`        | Facts **two or more items** in the phase share. Nothing else.                                     |
| `What:`             | Everything specific to that one item.                                                             |
| `## Open Questions` | Only what is unanswered. Once answered, the answer moves into the item and the bullet is deleted. |

**A single-item phase has no `## Context` section** — everything goes in that item's `What:`. This alone cuts most phase files roughly in half.

The same applies across files: a warning belongs to exactly one owner. Phase-local traps live in the phase file; plan-level `Notes` covers only what spans two or more phases. Never both.

### Sections that only re-list

Cut any section whose content is derivable from the checklist:

- **`## Files created/modified in this phase`** — the items' `Files:` lines already say this. Drop it.
- **`## Relevant Files`** — not a section of any plan: the items' `Files:` lines are the list.

### The new fields don't bypass Economy

`Why:`, `Provenance:` and `Prone to:` are subject to every rule above, not an
exception to them:

- **`Why:`** — L/XL items only. This is "Scale Economy by Weight" above, now with a field name;
  don't restate that rule here, point at it.
- **`Provenance:`** — data, not evidence, and therefore exempt from the evidence cut: the executor
  consumes it to decide whether to trust a claim before acting on it. Required only on a claim
  about the codebase the executor would otherwise take on faith — a file's location, what a
  command does, whether something exists. Never on a decision. Not on a claim the item's own text already pins down (a path the item creates, a command it prints): a trivial claim carries no marker.
- **`Prone to:`** — one line per phase, drawn from the repo's `docs/agents/failure-modes.md`. If
  that file is absent, omit the line rather than inventing failure modes.

### Open Questions

A question that is still open when the plan is written goes in `## Open Questions`, one bullet each: the question, `Default:` the assumption the executor uses when it stays unanswered, and `Affects:` the item(s). The executor never waits on it.

- Answered before execution: delete the bullet and write the answer into the item it affects (`What:`), or into `Notes` when it spans phases. The answer lives once, in the item.
- Nothing open: omit the section.
- It holds questions, not decisions. A plan has no `## Decisions` section: a decision that binds one item goes in that item's `What:` (`Why:` for L/XL); one that spans phases goes in `Notes`. In a workspace, `Notes` points at the workspace's decision instead of copying it.

### Self-check before handing back

- [ ] No `## Context` in a single-item phase.
- [ ] No fact stated in both `## Context` and a `What:`.
- [ ] Every retained paragraph is data the executor consumes, a trap it would fall into, or — for L/XL items only — rationale that shaped the design decision.
- [ ] No section re-lists another section's content.
- [ ] Each phase file earns its length: mechanical phases land ~15–30 lines, prose/design phases ~40–70. Well past that, look for re-argued decisions first.
- [ ] **Completeness pass, against the source material, not the draft plan:** re-read the invoker's requirement/decision list one item at a time and confirm each one lands somewhere in the
      plan — a checklist item, a `Files:` entry, or `Notes`. Check the source, not your own draft — you already believe your draft is complete, that's not the failure mode this catches.
      Anything that doesn't land gets a checklist item or an explicit one-line "not in scope" note; it never just disappears.
- [ ] **For every L/XL item**, the rationale that shaped its design decision survived — not just the conclusion. If you cut it during Economy, that was the wrong call for this tier; put it back.
- [ ] Every factual claim about the codebase carries `Provenance:` or an `unverified` marker.
- [ ] `**Repo:**` names an absolute path (or `## Environment` does, for a plan that touches 2+ repos).
- [ ] Every `## Open Questions` bullet has a `Default:` and an `Affects:`; no `## Decisions` section.
- [ ] The header has no `Source`, `Format`, Weight legend or `## Relevant Files`; `PlanType` appears only in a maintenance plan.
- [ ] Every `## Notes` bullet starts `Applies to: all` or `Applies to: <phases>`.
- [ ] Every item the executor cannot do alone (waits for a person, needs a permission) carries `Runner:`; every phase file carries `Repo:` and uses no placeholder defined only in the entry point.
- [ ] `Status:` is one of the four values; progress text is on a separate `Progress:` line.
- [ ] Ran `references/runner-check.md` and applied what it found.

## Weight vs Tier

Two axes, easy to conflate — keep them separate.

**Weight** (`S`/`M`/`L`/`XL`) sizes a **checkable unit** — an item in a feature-shape plan, a phase in a maintenance-shape plan (a session batches several phases for execution efficiency;
the phase, not the session, is what gets checked off) — by how much work it is and which agent capability it needs. It is the one term for this concept in a plan. "Effort" means the same
thing; don't use it — a plan must not carry both words for one axis.

Some producers also order units by a priority tier; that axis never replaces Weight.

Phases/items must be listed in actual execution-priority order — dependency first, then severity or priority — never left in raw discovery order.

## Capability recommendation

This table is authoritative and is **read by you, not copied into the plan**:

| Weight | Capability needed               | Executor agent |
| ------ | ------------------------------- | -------------- |
| S      | mechanical/repetitive           | `phase-s`      |
| M      | standard/moderate customization | `phase-m`      |
| L      | reasoning, design decisions     | `phase-l`      |
| XL     | cross-cutting, architecture     | `phase-xl`     |

> Which model and effort level each tier runs at is bound in the executor definitions, never in a plan. The plan carries only the letter; the dispatching skill resolves it to the name the harness lists (see its Executor names).

Size each unit by the capability it genuinely needs, not by how important it feels. The letter picks the executor: an over-weighted item burns a reasoning-tier agent on a find-and-replace,
and an under-weighted one hands a design decision to an agent told to apply instructions literally and escalate rather than improvise.

**In the plan**, checkable units carry the bare letter — `(S)`, `(M)`, `(L)`, `(XL)` — and nothing else: the plan carries no legend. The table above is for you; the executor is dispatched by the letter.

## Checkbox atomicity

One checkbox = one atomic invocation. It may span multiple files, as long as they're all dispatched in a single skill call with no pause needed partway through.

**Partial-completion convention**: when a checkbox batches multiple sub-files (a `go vet`
per-package pass, a lint-cleanup pass touching three functions), list those sub-files as visible sub-bullets under the item — not folded into prose:

```markdown
- [ ] **Fix go vet — internal/orders** (S)
  - [ ] `internal/orders/order.model.go`
  - [ ] `internal/orders/order.repository.go`
  - [ ] `internal/orders/order.service.go`
```

If execution stops mid-item (context/token budget), the sub-bullets let it tick off finished sub-files inline and leave the parent unchecked, so a fresh session resumes from exactly what's
left instead of redoing the whole item. `execute-plan` implements the resume side of this protocol — this convention is only the authoring side.

When an item's sub-bullets already name its files, they **are** the `Files:` line — don't write both.

## Repeating (per-unit) phases

Some phases aren't one atomic invocation at all — they're a checklist template meant to run once
per item in a list the plan already knows: "repeat for all 20 modules," "once per migration file,"
"for every endpoint in this group." Distinguish this from **Partial-completion convention** above:
sub-bullets there track a _fixed, small_ set of sub-files inside _one_ invocation; here the unit
count (N) is itself the thing that can grow past what one invocation, one diff, or one guardian
review can safely cover — 20 modules × 4 checklist items is 80 items of work wearing one phase's
clothing.

**Declare the execution grain explicitly** once N exceeds a handful (5+), or the phase is Weight
L/XL, or any unit's own checklist includes a human-in-the-loop step (below) — don't leave "run this
once per X" as the only signal. Checkbox atomicity's default is one checkbox, one invocation; a
repeating phase overrides that default, so the override has to be written down, not implied:

```markdown
- **Execution unit:** one `<module>` per agent run. Guardian reviews and commits before the next
  module starts — never batch modules into one invocation.
  - [ ] `orders`
  - [ ] `invoices`
  - [ ] `shipments`
```

Place it right after the phase header, next to `Prone to:`. List the units as checkbox sub-bullets of the `Execution unit:` item, one per unit, not as a prose or `Order:` list: the dispatcher sends the executor once per unchecked unit and ticks the unit when it lands.

**A human-in-the-loop step inside the unit forces this regardless of N.** If any item in the
repeating checklist needs a person — manual device testing, a click in an external dashboard, an
approval a script can't give — the execution grain is already one-unit-per-pause; state that
explicitly rather than relying on the reader to notice it from the item text.

**Flag size variance too**, when the N units aren't roughly equal (a module with 1 endpoint vs. one
with 21): name the largest few and note that they may need splitting further, item-by-item, rather
than assuming every repetition costs what the phase's stated Weight suggests.

This also feeds **Splitting large plans** below: count a repeating phase's items as `(items per
unit) × N`, not as written on the page, when checking it against that section's thresholds.

## Splitting large plans

A plan that's too long wastes tokens on a fresh executor reading phases it won't touch. Split when any of these hold:

| Trigger         | Threshold                                                                 |
| --------------- | ------------------------------------------------------------------------- |
| Checklist items | > 30                                                                      |
| Phases          | > 3                                                                       |
| Files touched   | > 20                                                                      |
| File length     | ~200 lines — independent trigger, applies even if every other row is fine |

The file-length ceiling is independent of the others: heavy inline context (mockups, DTO shapes, per-directory issue lists) can push a plan past a comfortable read length while every
item/phase/file-count heuristic still says "single file is fine." Split anyway.

Apply **Economy** before you measure against these triggers, not after. A plan that splits only because it re-argues its own decisions should have been cut, not split — splitting bloat just
spreads it across more files.

The split **unit** depends on plan shape:

- **Feature-shape** (heterogeneous phases, e.g. `to-plan`) → split **per phase**:
  `phase-01-<name>.md`, `phase-02-<name>.md`, ...
- **Maintenance-shape** (homogeneous, mechanical phases, e.g. a lint-cleanup plan) → split
  **per session**: `session-01.md`, `session-02.md`, ... — each session is the same ~5–7-phase batch the plan shape already groups for execution efficiency.

Either way, the split files go in a `phases/` folder next to the entry point, and a lightweight index/entry-point file lists every phase/session and its file pointer — see `references/template.md` for the exact shape.

## Parallel batches

Multi-file plans mark phases that an executor with sub-agent capability may run concurrently. Compute this at authoring time — you hold every phase at once, so it costs nothing here; an
executor would have to re-derive it from a cold start on every checkpoint.

**`Depends on:` must count shared-file writes, not just logical order.** Two phases that write the same file are dependent even when neither needs the other's result. This is the single trap:
in a 10-phase docs plan, seven phases declared `Depends on: nothing` while four of them wrote `docs/GLOSSARY.md` — a naive fan-out on that field would have clobbered it.

**Detect this mechanically, don't eyeball it while writing each phase.** Once every phase's `Files:` (or sub-bullet) list is drafted, build one flat list of every file across every phase and
sort it — any file appearing under 2+ phases is shared, full stop, regardless of whether the phases look independent. Do this as one discrete pass over the finished draft, not from memory
while authoring phase N — a fresh reviewer of the plan cannot verify a shared write that was only ever held in the authoring agent's head.

Mark a `Batch` letter in the Phase Index only when **all** hold:

- Two or more phases, none depending on another.
- Their `Files:` sets are disjoint — no shared file, including registries, indexes, and barrel files.

Weight does not gate a batch, and mixed letters are fine: `execute-plan` routes each phase to a model by its own letter, so an all-`S` batch is the cheap case rather than the wasteful one.
Keep sizing each phase honestly — the letter is what picks the agent downstream.

**Split the shared-file write out when it's the only blocker.** A phase shaped "create `<module>/docs/GLOSSARY.md` + register it in the shared index" collides with every sibling phase on the
index alone. Move the registrations into one follow-up phase — the creates then batch cleanly:

```markdown
| 8 | visit glossary | docs | L | A | `phases/phase-08-visit-glossary.md` |
| 9 | encounter glossary | docs | L | A | `phases/phase-09-encounter-glossary.md` |
| 10 | prescription glossary | docs | L | A | `phases/phase-10-prescription-glossary.md` |
| 11 | Register glossaries | docs | S | — | `phases/phase-11-register-glossaries.md` |
```

Leave the column `—` when a phase runs alone. If no batch qualifies, drop the column entirely rather than filling it with dashes. `execute-plan` reads the marker and owns dispatch — never
encode agent counts, spawn instructions, or a sequential fallback in the plan.

## Manual Test Checkpoints

Every plan carries a **Manual Test Checkpoints** section, including maintenance and audit plans.
Automated verify (build/typecheck/lint) confirms the code compiles, not that the behavior is correct — this section is where a human-observable checkpoint gets flagged so `execute-plan` can
surface it.

`execute-plan` surfaces each checkpoint to the user right after the phase commits, and owns a defined protocol for handling whatever feedback comes back (see its "Handling manual-test
feedback on a completed phase" section). A plan-producing skill's only job is to identify and list the checkpoints — never encode the recovery flow in the plan itself.

Name the phase, the surface, and the expected result — not the reasoning for why a checkpoint exists there. Never omit the section silently; when no phase changes observable behavior, write
it explicitly:

```markdown
## Manual Test Checkpoints

None — all changes are internal refactors verified by lint/build.
```

## Suggested commit

Every phase/commit-checkpoint carries a `Suggested commit:` line, written when the plan is authored — not left for `execute-plan` to invent later from a cold start. The plan-writer holds
spec/conversation context a fresh executor won't; write the literal, ready-to-use message (type, scope/phase-tag, description):

```markdown
Suggested commit: refactor(phase-02): extract validation helpers in internal/orders
```

`execute-plan` surfaces this line as the starting point for the commit message (the optional `caveman-commit` skill from `JuliusBrussee/caveman`, or the repo's own commit rules) instead of generating a message from nothing.

A phase that changes nothing in the repo (it only writes notes elsewhere, or only runs checks) writes `Suggested commit: none — <reason>`. Nothing is staged or committed for it, but the phase's gates still run. Never invent a commit message for such a phase, and never omit the line.

## Standard fields

These are fixed forms; do not invent variants.

- **`Runner:`** — an optional item field, `Runner: guardian` or `Runner: human`. No line means the executor does it. An item with the field is not dispatched to an executor agent: the guardian does it after the phase, or the run stops and waits for the person. Use it for work an agent cannot finish alone — a page that waits for an answer, installing a tool, a login, a click in a dashboard.
- **`Applies to:`** — every `## Notes` bullet starts with `Applies to: all` or `Applies to: <phase or range>`. The dispatcher attaches the bullets that apply to the phase it sends out, so a bullet without it may never reach the executor.
- **`Repo:`** — every phase file carries a `Repo: <absolute path>` line (from the plan's `**Repo:**` line or its `## Environment` table). Phase files use absolute paths, or placeholders defined in the file itself, never ones defined only in the entry point: the executor does not open the entry point.
- **`Execution unit:`** — for a repeating phase, one checkbox sub-bullet per unit (see "Repeating (per-unit) phases").
- **`Status:`** — exactly one of `pending`, `in-progress`, `done`, `abandoned`. Progress text goes on a separate `Progress:` line, because skills select the plan to run by reading `Status:`.

## Where the plan goes

Where a plan is written, and how a skill picks which plan to run, is set in `references/plan-location.md`.

## Template

Canonical templates — feature-shape and maintenance-shape, each with single-file and multi-file variants — live in `references/template.md`. Every plan-producing skill uses that
file instead of maintaining a local copy; keep only what's genuinely specific to a producer (linter bucket tables, JSON schemas, pattern-prediction rules) in that producer's own skill.

Every template header carries `**Review:** guardian`: `execute-plan` stops after staging each phase and `/review-phase` reviews it and prepares the commit. Keep the line when the
repo has `review-phase` installed; delete it when the user wants `execute-plan` to commit each phase itself, or when `review-phase` is not installed, since nothing would pick up
the staged phase.

The header is four lines: `Status`, `Review`, `Verify`, `Repo`, plus an optional `Progress` line. `Verify` appears only when the repo has no `docs/agents/verify.md`; `PlanType` only on a maintenance plan.
