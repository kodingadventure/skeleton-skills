---
name: whatnext
description: "Analyzes conversation context and project artifacts (specs, plans, git status, missing tests, undocumented features) to recommend the single next development step and skill to invoke. Maps completed work to Developer Workflow phases: discovery → specification → planning → implementation → quality → commit → docs. Use when the developer asks 'what next?', after a phase completes, when unsure which skill to invoke, or in a fresh session with no prior conversation. Do not use for one-off code generation questions that are not part of a feature workflow."
argument-hint: "What was just completed?"
---

# What Next

Suggests the single next development step and skill to invoke by analyzing conversation context or scanning project artifacts.

## Safety

- `node scripts/init-project.mjs` — renames packages, writes `.env` files, and configures DB credentials. **Never run this on an already-initialised project** — it overwrites `.env` files and renames package identifiers. Only recommend it when both `.env` files are confirmed absent.
- `moon run api:lint` and `yarn fallow health --format json --top 5` — read-only analysis commands. Safe to run unattended.
- `git log --oneline -5` — read-only. Safe to run unattended.

## Anti-patterns

- **Do not** recommend `/update-wiki` until both a matching frontend feature directory and an E2E spec exist for the module — check first, then recommend.
- **Never** output more than one next step — pick the highest-priority action and stop.
- **Do not** suggest wiki or documentation steps when uncommitted changes or a failing verify still exist.
- **Never** recommend maintenance tasks (lint triage, fallow) when an incomplete feature is actively in progress — finish the feature first.
- **Avoid** assuming the full-stack is complete just because backend tests pass — always run the full-stack completeness check (see decision tree).

## How it works

### Step 0: Cold start — no conversation context

If this is a fresh session with no prior conversation, scan project artifacts for clues:

1. **Workspaces first** — read `.scratch/plan/INDEX.md` when it exists (feature workspaces set up by `/kickoff`; another root when the repo's `CLAUDE.md` / `AGENTS.md` names one): every workspace with its status, progress, `Updated:` date and who is being waited on, in one read. One `## Active` row → open that workspace's `WHATNEXT.md`, whose `## Next steps` item 1 is the next step, and recommend `/resume-here <slug>`. Several `## Active` rows → recommend the most recently updated one and name the others in one line, instead of reading every `WHATNEXT.md`. A workspace whose work items are all `done` → recommend `/wrap-up <slug>`. A row under `## Seeded` (a folder `spin-off` seeded, not kicked off yet) → recommend `/kickoff <slug>`, or `/discuss <slug>` first when its `PRD.md` still needs shaping. No `INDEX.md` → fall back to `.scratch/plan/*/WHATNEXT.md`. This outranks every scan below.

2. **Scan `.scratch/` and the plan root** for active features:
   - Specs (`.scratch/*/spec.md`) — features planned but not started
   - Issues (`.scratch/*/issues/*.md`) — tickets waiting for implementation
   - Implementation plans — `<plan root>/*/IMPLEMENTATION_PLAN.md` (the repo's `Plan root:` line, `.plans/` by default; also the folder of a legacy `Plan output` key), `.scratch/*/IMPLEMENTATION_PLAN.md` and `.scratch/plan/*/plans/*/IMPLEMENTATION_PLAN.md` — plans whose `**Status:**` is `pending` or `in-progress`, or that still have unchecked `[ ]` items → resume with `/execute-plan`. Skip `done` and `abandoned`.

3. **Check git for dirty state:**
   - Uncommitted changes → suggest commit or continue what's in progress
   - Recent commits (`git log --oneline -5`) — understand the active branch context

4. **Check for missing tests:**
   - Backend modules without matching `apps/api/tests/*_test.go` files → suggest `/api-integration-test`
   - Frontend features under `apps/*/src/features/` with no co-located `*.test.tsx`/`*.test.ts` files → suggest `/ts-gen-test`
   - Features without `apps/<app>/e2e/*.spec.ts` → suggest `/ts-e2e-test`

5. **Check for unshipped features (have code but no wiki doc):**
   - Only flag this if frontend AND E2E also exist — backend modules alone are not "shippable" for wiki purposes

6. **Check lint health:**
   - Run `moon run api:lint` for existing issues → suggest `/lint-dispatch`

7. **No artifacts at all?** → the project may be fresh:
   - Check if `apps/api/.env` and `apps/<app>/.env` exist. If **missing** → the project has not been bootstrapped yet. Recommend running `node scripts/init-project.mjs` first (sets up DB credentials, renames packages, generates `.env` files). Do not recommend `/init-product` until this step is done.
   - If `.env` files exist but `docs/PRODUCT.md` does not exist, or it contains only placeholder content (e.g., `[Actor 1]` or `_Fill this section...`) → project is bootstrapped but not documented. Recommend `/init-product`.
   - If `docs/PRODUCT.md` exists with real content (no placeholders) but no features started → recommend `/to-plan "what should I build?"` to start from a blank slate.

### Step 1: Scan conversation context (if available)

If the conversation has prior messages, scan for indicators of completed phase:

- Files created/modified (backend Go modules, frontend components, tests, docs)
- Commands run (`moon run api:build`, `moon run <app>:test`, etc.)
- Artifacts generated (specs, plans, migration files, wiki pages)
- Explicit user statements ("I finished the billing module", "tests pass")

### Step 2: Match against the decision tree

See `references/decision-tree.md` for the full lookup table.

If the decision tree has no clear match (unusual phase, edge case, or a newly added skill), the
authoritative list of skills is **the installed skills themselves** — their descriptions are
already loaded in your context, and `.claude/skills/` is the registry on disk. Match the current
state against those descriptions. Never treat any prose doc as the skill catalogue: a
hand-written list drifts, and it drifts worst for exactly the case that sent you here — a skill
too new to be in it.

For how skills _compose_ — phase pipeline, cross-skill gates, common recipes — see
`docs/DEVELOPER_WORKFLOW.md`. That's sequencing knowledge no single skill description carries.

Key rule that is often missed: **after backend integration tests are committed, always run the full-stack gate**:

1. Does `apps/<app>/src/features/<module>/` exist? If no → `/ts-react-crud-feature`
2. Does `apps/<app>/e2e/<module>/` exist? If no → `/ts-e2e-test`
3. Only when both exist → `/update-wiki`

### Step 3: Output next action + rationale + skill invocation

## Output format

```
→ Next step: [action]
→ Why: [rationale based on what was just completed]
→ Invoke: /<skill-name> [args]
```

## Examples

```
→ Next step: Write integration tests for the billing module
→ Why: The billing Go module compiled and lint passed
→ Invoke: /api-integration-test billing
```

```
→ Next step: Build CRUD frontend pages for the billing module
→ Why: Integration tests are committed but apps/<app>/src/features/billing/ does not exist yet
→ Invoke: /ts-react-crud-feature billing
```

```
→ Next step: Debug the failing E2E test
→ Why: The subscription creation spec fails with a timeout on step 3
→ Invoke: /diagnosing-bugs E2E subscription creation times out on confirm step
```
