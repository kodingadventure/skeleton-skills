---
name: whatnext
description: "Analyzes conversation context and project artifacts (feature workspaces, specs, issues, plans, git status, the project's own test and lint commands) to recommend the single next development step and skill to invoke. Maps completed work to a generic pipeline: discovery → specification → planning → implementation → quality → commit. Use when the developer asks 'what next?', after a phase completes, when unsure which skill to invoke, or in a fresh session with no prior conversation. Do not use for one-off code generation questions that are not part of a feature workflow."
argument-hint: "What was just completed?"
---

# What Next

Suggests the single next development step and skill to invoke by analyzing conversation context or scanning project artifacts. Works in any repo: it assumes no stack, directory layout, or task runner.

## Safety

- Everything this skill runs is read-only: `git status`, `git log --oneline -5`, and listing or reading files. Safe to run unattended.
- A project check command (test, lint, build) is run only when the project's own config names it, and only when a recommendation depends on its result. Never run a command that deploys, migrates, publishes, or writes outside the working tree.
- Never invent a path or a command. If the project does not name one, say so and ask, rather than guessing a conventional name.

## Anti-patterns

- **Never** output more than one next step — pick the highest-priority action and stop.
- **Do not** suggest documentation or cleanup steps when uncommitted changes or a failing check still exist.
- **Never** recommend maintenance tasks (lint triage, refactors) when an incomplete feature is actively in progress — finish the feature first.
- **Avoid** assuming a feature is done just because one check passes — confirm against the plan, spec, or ticket that started it.

## How it works

### Step 0: Cold start — no conversation context

If this is a fresh session with no prior conversation, scan project artifacts for clues:

1. **Workspaces first** — read `.scratch/workspaces/INDEX.md` when it exists (feature workspaces set up by `/kickoff`; another root when the repo's `CLAUDE.md` / `AGENTS.md` names one with a `Workspace root:` line): every workspace with its status, progress, `Updated:` date and who is being waited on, in one read. One `## Active` row → open that workspace's `WHATNEXT.md`, whose `## Next steps` item 1 is the next step, and recommend `/resume-here <slug>`. Several `## Active` rows → recommend the most recently updated one and name the others in one line, instead of reading every `WHATNEXT.md`. A workspace whose work items are all `done` → recommend `/wrap-up <slug>`. A row under `## Seeded` (a folder `spin-off` seeded, not kicked off yet) → recommend `/kickoff <slug>`, or `/discuss <slug>` first when its `PRD.md` still needs shaping. No `INDEX.md` → fall back to `.scratch/workspaces/*/WHATNEXT.md`. This outranks every scan below.

2. **Scan `.scratch/` and the plan root** for active features:
   - Specs (`.scratch/*/spec.md`) — features planned but not started
   - Issues (`.scratch/*/issues/*.md`) — tickets waiting for implementation
   - Implementation plans — `<plan root>/*/IMPLEMENTATION_PLAN.md` (the repo's `Plan root:` line, `.plans/` by default; also the folder of a legacy `Plan output` key), `.scratch/*/IMPLEMENTATION_PLAN.md` and `.scratch/workspaces/*/plans/*/IMPLEMENTATION_PLAN.md` — plans whose `**Status:**` is `pending` or `in-progress`, or that still have unchecked `[ ]` items → resume with `/execute-plan`. Skip `done` and `abandoned`.

3. **Check git for dirty state:**
   - Uncommitted changes → suggest verifying them (`/verify`), then committing under the repo's own commit rules, or continuing what is in progress
   - Recent commits (`git log --oneline -5`) — understand the active branch context

4. **Check project health with the project's own commands** — find them, never assume them. Read, in this order, whichever exist: the `scripts` block of `package.json`, `Makefile`, `justfile`, `Taskfile.yml`, `moon.yml`, `Cargo.toml`, `pyproject.toml`, then `README.md` / `CONTRIBUTING.md` and CI workflow files (the `verify` skill's `bootstrap.md` lists the same sources). Then:
   - A test, lint, or build command exists and the working tree has changes → run it once. Failing → recommend `/diagnosing-bugs` (if installed) or fix it directly; passing → carry on to the next check.
   - Source files changed but no test file changed alongside them → recommend writing the missing tests (`/tdd` if installed).
   - No such command can be found → say so in the rationale, and recommend `/verify`, which bootstraps a config for the repo.

5. **No artifacts at all?** → the repo may be fresh or the work may live in the user's head:
   - Nothing under `.scratch/`, no plans, a clean tree → ask what to build, and recommend `/grilling` (if installed) to shape the idea, or `/to-plan "<what to build>"` when the request is already clear.

### Step 1: Scan conversation context (if available)

If the conversation has prior messages, scan for indicators of the completed phase:

- Files created or modified (source, tests, docs)
- Commands run (the project's build, test, or lint commands)
- Artifacts generated (specs, plans, migration files, review pages)
- Explicit user statements ("I finished the billing module", "tests pass")

### Step 2: Match against the decision tree

See `references/decision-tree.md` for the full lookup table.

If the decision tree has no clear match (unusual phase, edge case, or a newly added skill), the
authoritative list of skills is **the installed skills themselves** — their descriptions are
already loaded in your context, and `.claude/skills/` is the registry on disk. Match the current
state against those descriptions. Never treat any prose doc as the skill catalogue: a
hand-written list drifts, and it drifts worst for exactly the case that sent you here — a skill
too new to be in it.

Skills from outside this repo (from `mattpocock/skills`: the grilling, spec, ticket, tdd, diagnosing, code-review and prototype family) are recommended only when they are installed. Not installed → pick the nearest installed skill, or describe the step in plain words with no `Invoke` skill.

### Step 3: Output next action + rationale + skill invocation

## Output format

```
→ Next step: [action]
→ Why: [rationale based on what was just completed]
→ Invoke: /<skill-name> [args]
```

## Examples

```
→ Next step: Resume the checkout-redesign workspace
→ Why: INDEX.md lists it as the only Active workspace; item 1 of its WHATNEXT.md is wiring the payment form
→ Invoke: /resume-here checkout-redesign
```

```
→ Next step: Verify the uncommitted changes, then commit them
→ Why: 6 files changed under src/, and package.json defines a `test` script that has not been run yet
→ Invoke: /verify
```

```
→ Next step: Debug the failing checkout test
→ Why: `npm test` fails on "applies discount code" with a timeout on the confirm step
→ Invoke: /diagnosing-bugs checkout test "applies discount code" times out on the confirm step
```
