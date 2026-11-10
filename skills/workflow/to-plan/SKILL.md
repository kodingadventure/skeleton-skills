---
name: to-plan
description: Create a phased IMPLEMENTATION_PLAN.md from a spec, issue, or conversation. Each phase contains ordered checklist items with a Weight (drives agent routing) and raw context (mockups, DTO shapes, business rules). Use when the user says "create a plan" or "plan this", or wants to translate a spec/issue into actionable implementation steps. Do not use for executing plans (use execute-plan instead), one-off code generation, or debugging existing implementations.
---

# To Plan

Translate a spec, issue, or conversation into a phased `IMPLEMENTATION_PLAN.md` — a checklist an agent or developer can execute item by item without re-reading the source material.

## Manual Test Checkpoints

Mark one after any phase that produces something a human can actually exercise — an endpoint that's now reachable, a page that now renders, a flow wired end-to-end. Usually just the first
phase where a vertical slice becomes reachable, plus the final phase; not every phase needs one.

At least one checkpoint must exercise the changed behavior **in its enabled state**, end to end — a checkpoint set that only covers the paths where a new feature stays switched off passes trivially on a feature that never works.

A checkpoint that installs, removes or changes settings outside the project names where (scratch folder, project scope) and how to undo it.

```markdown
## Manual Test Checkpoints

1. After Phase 2 (Backend Module) — call the new endpoint directly (curl/Postman): <1-2 concrete scenarios>
2. After Phase 5 (Frontend Feature) — full smoke test of the flow in the browser
```

## Workflow

- [ ] **1. Locate source material** — spec, issue, or conversation
- [ ] **2. Explore the codebase** — collect every target repo, then per repo read its domain doc, gate and failure modes; identify files to touch, classify phases, assign weights
- [ ] **3. Write the plan** — location per the `writing-great-plan` skill's `references/plan-location.md`
- [ ] **4. Read it as the runner** — run the `writing-great-plan` skill's `references/runner-check.md` against the written plan
- [ ] **5. Present and iterate** — show the user, refine, hand off to execute-plan

### 1. Locate the source material

Work from whatever is already in the conversation. If the user passes a path or issue reference, read it:

- **Local markdown**: `.scratch/<feature-slug>/spec.md` or `.scratch/<feature-slug>/issues/<NN>-<slug>.md`
- **GitHub**: `gh issue view <number> --comments`
- **GitLab**: `glab issue view <number> --comments`

If no source is passed, synthesise from the current conversation context. **Capture any mockups, wireframes, DTO shapes, or business rules discussed during the conversation** — these go into the plan as raw context, not as references the executor needs to chase down.

### 2. Explore the codebase

First collect every repo or target the executor will touch, each with its absolute path, including targets outside the current repo. This becomes the plan's `**Repo:**` line (a `## Environment` table only when the plan touches 2+ repos).

Then, for each repo:

- Read `docs/agents/domain.md` and follow its **Consumer Rules**: determine context, read the matching glossary, check ADRs. If that file does not exist, carry on with the root `GLOSSARY.md` and `docs/adr/` where they exist, and suggest once that the user run `/setup-matt-pocock-skills` (from `mattpocock/skills`) to create it; do not stop, and do not create the file yourself.
- Note `docs/agents/verify.md`. When the repo has none, note its verify command: that becomes the `**Verify:**` line.
- Read `docs/agents/failure-modes.md` if it exists and note which entries match each phase; these become that phase's `Prone to:` line. If the file is absent, pass nothing rather than inventing failure modes.

If the source lives in a feature workspace, also read the decisions in its `CONTEXT.md` and the guardrails in its `WHATNEXT.md`. A conflict between those and a repo's `CLAUDE.md` / `AGENTS.md` becomes an Open Question (step 9 of `runner-check.md`).

Then identify the files that will be touched. **Read the actual files** — don't guess their contents.

As you establish facts about the codebase — a file's location, whether something exists, what a command does — note the command or read that established each one. A claim needs this only when the executor would otherwise act on it without rechecking, not every sentence; carry it into the plan as that item's `Provenance:` field, or the literal marker `unverified — check first` when you couldn't verify it. Most items need no `Provenance:` line: a file the item edits is one the executor opens anyway, and a path the item creates or a command it prints is pinned down by the item's own text. "Read during planning" is not provenance — it names no command and tells the executor nothing; when that is all you could write, omit the line.

Assign each phase a Weight (`S`/`M`/`L`/`XL`). This tells `execute-plan` which agent to dispatch.

Note every question you could not settle from the source or the code, with the assumption you would proceed on if nobody answers. These become the plan's `## Open Questions` (see `writing-great-plan`), each with a `Default:` and the item it `Affects:`.

If a phase's checklist is meant to run once per item in a list rather than once total ("repeat for
all 20 modules," "once per migration file"), note the unit and the count — this is a **repeating
phase**, and `writing-great-plan` needs that count to decide whether it must declare an execution
grain (see its "Repeating (per-unit) phases").

### 3. Write the plan

- **Outside a workspace:** see the `writing-great-plan` skill's `references/plan-location.md`.
- **Inside a workspace** (the source lives in a folder with a `CONTEXT.md` set up by `/kickoff`, `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root):
  - Write to `<workspace>/plans/<NN>-<plan-name>/IMPLEMENTATION_PLAN.md` (`NN` = the next free number).
  - Write in the workspace language from `CONTEXT.md` `## Workspace rules`; code, file names and UI strings stay literal.
  - List the plan under `CONTEXT.md` `## Plans`.
  - Refresh this workspace's row in the root `INDEX.md` (the areas the plan touches, today's date).
  - Give the Phase Index a `Tracker` column naming each phase's work item ID(s) from `TRACKER.md` (an item spread over several phases is listed on each; it becomes `done` after its last one). `execute-plan` and `review-phase` read that column to update `TRACKER.md` and `WHATNEXT.md` after each phase.

Decide the plan's type:

| Condition                                                                        | PlanType         |
| -------------------------------------------------------------------------------- | ---------------- |
| User-facing feature, CRUD, domain capability                                     | `feature`        |
| Cross-cutting: integration tests, lint, dead-code cleanup, skill fix, docs audit | maintenance type |

A `feature` plan has no `PlanType:` line; a maintenance plan carries `PlanType: <type>`.

Invoke `writing-great-plan` to format and write the plan, passing it `PlanType` (maintenance plans only), the phase list with Weight, the `Repo` (and `Verify` when step 2 found no `docs/agents/verify.md`), the per-phase `Prone to:` entries and the Open Questions with their defaults gathered in steps 1–2, and the raw context (mockups, DTO shapes, business rules) gathered above. It picks the **feature-shape** template (single-file or multi-file, per its splitting rule), assigns capability/thinking-effort recommendations, and adds the Manual Test Checkpoints and Suggested commit lines.

**Critical rules when writing items:**

1. **Inline raw context.** Every `What:` field must contain the full information an executor needs. If you discussed a DTO shape with the user, write it out:

   ````markdown
   - What: |
     Create UserPreference entity:
     ```go type UserPreference struct {
       ID        uuid.UUID      `bun:"id,pk,type:uuid"`
       UserID    uuid.UUID      `bun:"user_id,notnull,type:uuid"`
       Key       string         `bun:"key,notnull"`
       Value     json.RawMessage `bun:"value,type:jsonb"`
       CreatedAt time.Time
       UpdatedAt time.Time
       DeletedAt time.Time      `bun:",soft_delete"`
     }
     ```
   ````

   An executor with fresh context should be able to copy-paste and go — no back-and-forth.

2. **Include mockups.** If the user showed wireframes during discussion, describe them in detail or embed them as ASCII/markdown references:

   ````markdown
   - What: |
     Create the settings page with these tabs (from mockup):

     ```markdown
     ┌────────────────────────────────┐
     │ Settings --------------------- │
     │ ┌───────┬──────┬─────────────┐ │
     │ │Profile│Theme │Notifications│ │
     │ ├───────┴──────┴─────────────┤ │
     │ │ [form fields............ ] │ │
     │ └────────────────────────────┘ │
     └────────────────────────────────┘
     ```
   ````

3. **Business rules & edge cases.** If the user specified business rules (e.g., "no double-booking"), include them in the relevant item's `What:` (single-item) or in `## Notes` (spans 2+ phases) — the same two landing spots `writing-great-plan`'s completeness check verifies against. Never a separate reference file: nothing outside a checklist item, `Files:` entry, or `Notes` is checked for completeness, so it can silently drop out of the plan.

See the **Rules** section below for the hard requirements (Weight, Manual Test
Checkpoints, sub-bullets, Suggested commit) — apply them while writing each item, not just as a final checklist.

### 4. Read it as the runner

Run the `writing-great-plan` skill's `references/runner-check.md` against the written plan, fix what it finds, and tell the user in one line what changed (or "nothing to change"): one sentence, not a list; the details are in the plan.

### 5. Present the plan to the user

Show the plan and ask:

- Does the phase order feel right?
- Are the weights right? (Helps dispatch the right agent.)
- Any missing mockups or business rules?
- Are the Manual Test Checkpoints in the right places?
- Open Questions: ask them in one batch. Each answer removes its bullet and is written into the affected item (`What:`), or `Notes` when it spans phases; a question the user leaves open keeps its `Default:`.

Iterate until approved. Do **not** start implementation — that is `execute-plan`'s job.

---

## Rules

- **Order phases by dependency.**
- **Every phase declares Weight.** Every item declares Weight (`S`/`M`/`L`/`XL`, no exceptions — default `M` if unsure). Weight alone drives capability/agent routing (`phase-s/m/l/xl` per `writing-great-plan`'s Capability recommendation table) — there is no separate `Agent:` field.
- **Inline raw context.** An executor with fresh context and no spec must understand every item from the plan alone — no back-and-forth.
- **Mark Manual Test Checkpoints** for any phase with human-observable behavior; never omit the section — write `None — ...` when it doesn't apply, except a plan that adds a feature: that always needs at least one checkpoint exercising it in its enabled state, end to end.
- **Batch items get sub-bullets** for their bundled files (`writing-great-plan`'s partial-completion convention) so a stopped run can resume mid-item.
- **Every phase gets a `Suggested commit:` line** at authoring time (`writing-great-plan`'s convention; `none — <reason>` when the phase changes no repo file) — `execute-plan` surfaces it as the starting point for the commit message (to the optional `caveman-commit` skill from `JuliusBrussee/caveman` if installed; otherwise the commit follows the repo's own rules) instead of generating one from scratch.
- **Do NOT write verify steps as checklist items.** The executing skill runs the gates after each phase (the `verify` skill when installed).
- **Every factual claim about the codebase carries `Provenance:` or the literal marker `unverified — check first`.** Required only when the executor would act on the claim without rechecking — a file's location, whether something exists, what a command does — not every sentence, and never `Provenance: read during planning` (omit the line instead). File paths must be real; explore the codebase first, read actual files, don't guess.
- **A phase that repeats its checklist across a list of units (modules, files, endpoints) declares its execution grain.** Don't leave "run once per X" as the only signal once the list is more than a handful of items — see `writing-great-plan`'s "Repeating (per-unit) phases".
- **Skill names must match exactly** the names your agent lists.
- **Read the plan as its runner** before presenting it: run the `writing-great-plan` skill's `references/runner-check.md`, fix what it finds, and tell the user in one sentence what changed.
- **No implementation.** This skill only creates the plan.
