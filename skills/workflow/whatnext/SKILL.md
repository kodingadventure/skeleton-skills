---
name: whatnext
description: "Analyzes conversation context and project artifacts (feature workspaces, specs, issues, plans, git status, the project's own test and lint commands) to recommend the single next development step and skill to invoke. Maps completed work to a generic pipeline: discovery → specification → planning → implementation → quality → commit. Use when the developer asks 'what next?', after a phase completes, when unsure which skill to invoke, or in a fresh session with no prior conversation. Do not use for one-off code generation questions that are not part of a feature workflow."
argument-hint: "What was just completed?"
---

# What Next

Suggests the single next development step and skill to invoke by analyzing conversation context or scanning project artifacts. Works in any repo: it assumes no stack, directory layout, or task runner.

Every `Invoke` line names a skill your agent lists; otherwise there is no `Invoke` line at all, and the step is written in plain words. Never name a skill that is not installed, not even to say it is missing: the step reads as if a tool were expected.

## Safety

- Read-only except the project's own check command: `git status`, `git log -5 --name-only --format='%h %s'`, and listing or reading files (including `docs/agents/domain.md`) are safe to run unattended.
- Step 4 only reads the list of project commands; it does not run them. A dirty working tree → recommend `/verify`. If a command must still be run: only `test`, `lint`, `typecheck` or `build`, one run with no watch mode, with a timeout, and name the command before running it. Never run a command that deploys, migrates, publishes, or writes outside the working tree.
- Never invent a path or a command. If the project does not name one, say so and ask, rather than guessing a conventional name.

## Anti-patterns

- **Never** output more than one next step — pick the highest-priority action and stop.
- **Do not** suggest documentation or cleanup steps when uncommitted changes or a failing check still exist.
- **Never** recommend maintenance tasks (lint triage, refactors) when an incomplete feature is actively in progress — finish the feature first.
- **Do** suggest the docs update once the work is committed and clean, under the rules in [Documentation after a behaviour-changing commit](#documentation-after-a-behaviour-changing-commit).
- **Avoid** assuming a feature is done just because one check passes — confirm against the plan, spec, or ticket that started it.

## Documentation after a behaviour-changing commit

- **Behaviour-changing** — the commit touches files other than docs, tests, or lock/format files. When `docs/agents/domain.md` has a Code units table, only files inside its `Where` globs count.
- **Already documented** — that commit or a later one touched a Wiki-table page, a glossary, or a reference doc from the Docs Layout: no suggestion.
- **Tests first** — when the commit's source changes have no test beside them (see Step 0, item 4), the missing tests come first and the docs suggestion waits until they are committed: the wiki cites the test that locks each rule.
- **When** — while a plan has phases left, the next phase wins. After the plan's last phase is committed, suggest once for the plan's whole commit range. A behaviour-changing commit outside a plan gets the suggestion right away. Never with uncommitted changes or a failing check.
- **Which skill** — `/update-wiki <range>` when installed (or an installed documentation skill whose description mentions commits that change rules, statuses, routes or screens); else `/refine-docs <range>` when installed and `docs/agents/domain.md` exists; else the step in plain words with no `Invoke` line.
- **Glossaries** — see Step 0, item 5; only `Required: every unit` rows count.

## How it works

### Step 0: Cold start — no conversation context

If this is a fresh session with no prior conversation, scan project artifacts for clues:

1. **Workspaces first** — read `.scratch/workspaces/INDEX.md` when it exists (feature workspaces set up by `/kickoff`; another root when the repo's `CLAUDE.md` / `AGENTS.md` names one with a `Workspace root:` line): every workspace with its status, progress, `Updated:` date and who is being waited on, in one read. One `## Active` row → open that workspace's `WHATNEXT.md`, whose `## Next steps` item 1 is the next step, and recommend `/resume-here <slug>`. Several `## Active` rows → recommend the most recently updated one and name the others in one line, instead of reading every `WHATNEXT.md`. A workspace whose work items are all `done` → recommend `/wrap-up <slug>`. No `INDEX.md` → fall back to `.scratch/workspaces/*/WHATNEXT.md`. This outranks every scan below.

2. **Scan `.scratch/` and the plan root** for active features:
   - Specs (`.scratch/*/spec.md`) — features planned but not started
   - Issues (`.scratch/*/issues/*.md`) — tickets waiting for implementation. If `docs/agents/issue-tracker.md` exists, read the tracker location from it instead of assuming `.scratch/`.
   - Implementation plans — `<plan root>/*/IMPLEMENTATION_PLAN.md` (the repo's `Plan root:` line, `.scratch/plans/` by default; also the folder of a legacy `Plan output` key), `.scratch/*/IMPLEMENTATION_PLAN.md` and `.scratch/workspaces/*/plans/*/IMPLEMENTATION_PLAN.md` — plans whose `**Status:**` is `pending` or `in-progress`, or that still have unchecked `[ ]` items → resume with `/execute-plan`. Skip `done` and `abandoned`.

3. **Check git for dirty state** (not a git repo → skip this step and say so in the rationale):
   - Uncommitted changes → suggest verifying them (`/verify`), then committing under the repo's own commit rules, or continuing what is in progress
   - Recent commits (`git log -5 --name-only --format='%h %s'`) — understand the active branch context, and read the files the last commit touched. A behaviour-changing commit not yet documented, with no open plan that holds it → suggest the docs update (see [Documentation after a behaviour-changing commit](#documentation-after-a-behaviour-changing-commit)).
   - Clean tree, but commits ahead of the base branch → recommend a review (`/code-review` if installed) or "open a PR"

4. **Check project health with the project's own commands** — find them, never assume them. Read, in this order, whichever exist: the `scripts` block of `package.json`, `Makefile`, `justfile`, `Taskfile.yml`, `moon.yml`, `Cargo.toml`, `pyproject.toml`, then `README.md` / `CONTRIBUTING.md` and CI workflow files (the `verify` skill's `bootstrap.md` lists the same sources). Then:
   - A test, lint, or build command exists and the working tree has changes → recommend `/verify`, which runs the gates. Do not run the command yourself unless the Safety rules above allow it; if you do and it fails → recommend `/diagnosing-bugs` (if installed) or fix it directly; if it passes, carry on to the next check.
   - Source files changed — in the working tree, or in a behaviour-changing commit among the recent ones — and no test file changed alongside them or in a later commit → recommend writing tests for the code that already exists, in plain words, with an `Invoke` line only when an installed skill's description covers adding tests to existing code. A test-first skill (red-green-refactor) does not fit: the code is already written. This holds even when a later commit documented the change, and it outranks the docs suggestion (Step 3) and glossaries (Step 5).
   - No such command can be found → say so in the rationale, and recommend `/verify`, which bootstraps a config for the repo.

5. **Required glossaries** — when `docs/agents/domain.md` has a Deep-context tier row with `Required: every unit`, check each folder matching that unit's `Where` glob for a file at its `Glossary path`; a missing one → suggest the installed documentation skill that covers glossaries (`/refine-docs <unit>`). Rows marked `by threshold`, or tiers without a `Required` column, are skipped.

   Steps 3 (documentation suggestion) and 5 yield to an active workspace, an open plan, a dirty tree, a failing check and missing tests (Step 4).

6. **No artifacts at all?** → the repo may be fresh or the work may live in the user's head:
   - Nothing under `.scratch/`, no plans, a clean tree → ask what to build, and recommend `/grilling` (if installed) to shape the idea, or `/to-plan "<what to build>"` when the request is already clear.

### Step 1: Scan conversation context (if available)

If the conversation has prior messages, scan for indicators of the completed phase:

- Files created or modified (source, tests, docs)
- Commands run (the project's build, test, or lint commands)
- Artifacts generated (specs, plans, migration files, review pages)
- Explicit user statements ("I finished the billing module", "tests pass")

A workspace this conversation already resumed (`/resume-here <slug>` ran here) or is discussing (`/discuss <slug>`): the next step is item 1 of its `WHATNEXT.md` `## Next steps`. Never recommend the skill the conversation is already running for that workspace (`/resume-here <slug>` after a resume, `/discuss <slug>` inside that discussion): its instructions are already loaded, and re-running it only re-reads the same files. When item 1 names another installed skill, that skill is the `Invoke` line. Otherwise, after a resume leave the `Invoke` line out; inside a discussion, `/resume-here <slug>` is the `Invoke` line, since starting the work is another skill.

### Step 2: Match against the decision tree

See `references/decision-tree.md` for the full lookup table.

If the decision tree has no clear match (unusual phase, edge case, or a newly added skill), the
authoritative list of skills is **the skills your agent has loaded** — their descriptions are
already loaded in your context. Match the current
state against those descriptions. Never treat any prose doc as the skill catalogue: a
hand-written list drifts, and it drifts worst for exactly the case that sent you here — a skill
too new to be in it.

Skills from outside this repo (from `mattpocock/skills`: the grilling, to-spec, to-tickets, tdd, diagnosing, code-review and prototype family) are recommended only when they are installed. Not installed → pick the nearest installed skill, or describe the step in plain words with no `Invoke` skill. A test-first skill fits only behaviour that is not written yet.

### Step 3: Output next action + rationale + skill invocation

## Output format

```
→ Next step: [action]
→ Why: [rationale based on what was just completed]
→ Invoke: <skill-name> [args]
```

Write `/name` when your agent uses slash commands. No fitting skill is loaded → leave the `Invoke` line out entirely: the answer has two lines, `Next step` and `Why`. Never write `Invoke: none`, `Invoke: —` or an `Invoke` line that names no skill; if the reader needs to know why no skill fits, say it in `Why`.

## Examples

```
→ Next step: Write down what the checkout page should do before coding it
→ Why: The conversation settled the design but no spec or plan exists, and no spec or planning skill is loaded
```

```
→ Next step: Write tests for refund() in src/payments/refund.js — a paid order becomes refunded, any other status throws — then commit them
→ Why: The last commit changed refund.js with no test beside it, and no installed skill adds tests to existing code; the docs update waits until the tests are committed
```

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
→ Next step: Update the wiki for the checkout plan's commits
→ Why: The plan's last phase is committed; its 4 commits changed order status rules under src/orders/ and src/payments/, and no commit since touched docs/wiki/
→ Invoke: /update-wiki a1b2c3d..HEAD
```

```
→ Next step: Debug the failing checkout test
→ Why: `npm test` fails on "applies discount code" with a timeout on the confirm step
→ Invoke: /diagnosing-bugs checkout test "applies discount code" times out on the confirm step
```
