---
name: guard-plan
description: Runs a multi-file IMPLEMENTATION_PLAN.md with the session as guardian — every phase is dispatched to the phase-s/m/l/xl agent matching its Weight, then the guardian re-verifies, fixes, and commits when the run mode allows. Use when the user wants a plan executed by subagents, wants to save tokens on execution, or says "guard"/"supervise" the plan. Do not use for writing plans (to-plan) or for a single inline phase (execute-plan).
---

# Guard Plan

The session is the **guardian**: it never implements a phase. Executors do the work on the model their Weight buys; the guardian spends its (more expensive) tokens only where defects surface — running gates, checking claims, fixing, committing. The saving depends on that split holding: the guardian reads the phase file and the diff, not the codebase.

This skill needs a harness that can start a sub-agent with its own context and send it a follow-up. Without that, run the plan in this session with `execute-plan` under `Review: guardian`, then `review-phase`: the same guard, no dispatch.

## 1. Preflight — once per session

1. Get the plan path from the user, or resolve it per the `writing-great-plan` skill's `references/plan-location.md` → "Which plan runs" (entry point `IMPLEMENTATION_PLAN.md` with a Phase Index; if the `writing-great-plan` skill is not installed, ask the user for the plan path). Read the entry point: Phase Index, Open Questions, Manual Test Checkpoints, Notes. Those four are all the guardian keeps in context.
2. **ADR skill.** When the plan lives in a feature workspace (`CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` two levels above the plan folder), run `grep -c 'ADR: candidate' <workspace>/CONTEXT.md`. A count above 0 needs the `domain-modeling` skill: check your agent lists it. When it does not, stop here, before the baseline and before dispatching anything, and say that `domain-modeling` (from `mattpocock/skills`) is missing — "see this repo's README for the pinned install command". Never defer this check to the phase close: by then a phase is already committed without its ADR.
3. **Executor names.** Ask the harness which agent types it offers (in Claude Code, ask Claude to list the agent types it can dispatch). You need one executor per weight. Use the names exactly as listed:

   - Installed as files in `.claude/agents/`: `phase-s`, `phase-m`, `phase-l`, `phase-xl`.
   - Installed from the `phase-agents` plugin: `phase-agents:phase-s` and so on. A bare `phase-s` is rejected there ("Agent type 'phase-s' not found").

   Record the four names once at preflight and use them verbatim as the dispatch agent type (S → the `-s` name, M → `-m`, L → `-l`, XL → `-xl`). None found: stop and say how to install them (the `phase-agents` plugin, or copy the agent files into `.claude/agents/`); do not substitute a general-purpose agent. If the harness has no sub-agents at all, run the plan in this session with `execute-plan` under `Review: guardian`, then `review-phase`.

   The stop message names both install routes: `claude plugin marketplace add <catalog>` then `claude plugin install phase-agents@skeleton-skills --scope project`; or copy the `phase-*.md` files from the catalog's `plugins/phase-agents/agents/` folder into `.claude/agents/`. For a harness without sub-agents, point to the `execute-plan` route above.

4. **Gates runnable.** Take the gates from `docs/agents/verify.md` for the stacks the plan touches. If the repo has no `verify.md`, take them from the plan header's `Verify:` line. If neither exists, write "no gate" under `## Baseline` and say so in every report; do not stop. A phase that creates `verify.md` moves the gates to that file from the next phase on. Every gate must run to a real verdict. A gate that errors on tooling (missing binary, unreachable dependency, linter built for an older toolchain) is a toolchain defect, not a code defect: fix it now or stop and tell the user what access is missing. When the repo keeps `docs/agents/toolchain.md` (one line per symptom and its fix, for the environments its sessions run in), read it first and add every new fix you find to it.
5. **Baseline.** Run the gates on a clean worktree of `HEAD` (`git worktree add <scratch>/base HEAD`) and record every pre-existing failure in the plan entry point under `## Baseline`. From here on only a failure absent from the baseline counts against a phase.
6. **Run mode.** Ask the user once, then record the answers in the entry point under `## Baseline`:
   - **Commit:** the guardian commits each phase, or it stages the phase, prints the commit command, and stops. When the repo's rules say nothing, the default is to print the command and stop, the same as `execute-plan` and `review-phase`.
   - **Push:** never, and not offered as a choice: the question says the run does not push. Push only when the user asks for it on their own, or when the repo's `CLAUDE.md`/`AGENTS.md` explicitly requires it.
   - **Continue:** go on to the next phase automatically, or stop after each phase.

   The repo's `CLAUDE.md`/`AGENTS.md` rules win over the answer: where they ask for confirmation before a commit or a push, or forbid one, the run mode cannot loosen them.

Done when the ADR-skill check passed (or the plan has no workspace, or no `ADR: candidate`), every gate has produced output on the baseline (or "no gate" is recorded), `## Baseline` lists its failures (or "none"), and the run mode is recorded.

## 2. Phase loop

Take the first phase with unchecked items, or its whole `Batch` group.

**Items that are not the executor's.** An item marked `Runner: guardian` or `Runner: human` never goes into the dispatch prompt. The guardian does the `guardian` items itself after the phase is guarded. For a `human` item, the guardian stops and hands the user its text. A phase whose items are all marked is not dispatched.

**Repeating phases.** A phase with `Execution unit:` is dispatched once per unchecked unit sub-item, with "only unit X" in the prompt. Guard it, commit it (per the run mode), then repeat until no unit is left.

**Dispatch (Claude Code: the Agent tool).** One agent per phase, with the agent type taken from the four names recorded at preflight (S, M, L, XL by the phase's Weight). Weight is the only interface to the model: do not pass a model override. The prompt carries only:

- the phase file's absolute path and the target repo's absolute path (the phase file's `Repo:` line),
- the gate commands for the paths this phase touches; the executor runs them and pastes their output in its report,
- each plan Note marked `Applies to: all` or whose range includes this phase, pasted verbatim,
- for a batch: which paths the sibling agents own, so each stays inside its own `Files:`,
- known environment facts the executor would otherwise trip on (a dependency that can't be fetched, a gate it must not run),
- each Open Questions bullet whose `Affects:` names this phase, pasted with its `Default:`,
- the report limit: `## Executor report` of 6 lines at most — what landed, Verify, Staged, then one line per plan correction, `Assumed:` or open risk. **Staged:** follows the executor rules in the `execute-plan` skill's `references/executor-rules.md`, as a one-line `git -C <repo> diff --cached --shortstat`.

Batch → dispatch all in one message, in the background; guard each one as it reports. Single phase → dispatch and wait.

**Guard.** Run the `review-phase` rhythm against this phase's diff: re-run the gates yourself, probe the phase's `Prone to:`, check every factual claim in the executor's report against the repo (a claim of "done", "granted", "unchanged", or "not possible" is the one that is wrong). Before calling a phase clean, grep the diff for each concrete thing its items name: field, permission, route, role grant.

Defects:

- A local fix (a path, a missing grant, a stale mock, a lint hit) → fix it inline.
- Missing or wrong item-level work → send the findings back to the same executor (Claude Code: `SendMessage`), then guard again.
- The plan contradicts the code → follow the code; write `> Plan correction — <said> / <true>`.

**Record.** Append `## Review` to the phase file in `review-phase`'s template: gates re-run, defects found and fixed, plan corrections, anything not run and why. Keep it to the verdict, one line per defect, and one line for what was ruled out.

**Close the phase in the workspace.** Do this when the plan lives in a feature workspace (`CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` two levels above the plan folder); else skip it, and the report says `workspace n/a`. The executors never touch the workspace, so this is the guardian's, once per guarded phase. Update it as its `TRACKER.md` `## How this tracker works` says:

- **Status.** The phase's work item (the Phase Index `Tracker` column, else the plan's Notes) → `done` when the phase passed the guard and was the item's last one; else `in-progress`.
- **Action Log.** One new row, today's date, in plain words for the report's audience: what the phase built and what the guard fixed.
- **`WHATNEXT.md`.** Rewrite State now (phase guarded, the commit made or its command printed) and Next steps (the next phase, or the checkpoint that follows).
- **`INDEX.md`.** This workspace's row only: progress and today's date.
- **ADR candidates.** A decision tagged `ADR: candidate` in `CONTEXT.md` whose reasoning this phase's code now embodies becomes an ADR now, written with the `domain-modeling` skill, its tag replaced by the ADR id, and the terms the phase coined added to the glossary.

The ADR and glossary are repo files: they go into this phase's commit. The other workspace files are git-ignored: edit them, never stage them. Done when the item's status, the Action Log row and `WHATNEXT.md` reflect the phase, and `grep -c '^| \[x\]' TRACKER.md` prints the same number as before.

**Commit.** Follow the run mode recorded at preflight. Stage only this phase's paths, its phase file, and the ADR and glossary files the close step wrote (sibling phases in a batch may still be in flight; leave the phase file out when the plan lives in a gitignored folder).

- Run mode "commit": commit with the phase's `Suggested commit:` line. A phase is committed only on a green gate: if a gate could not run, the phase stays staged-but-uncommitted and the loop stops with the reason.
- Run mode "print the command": leave the phase staged, print the commit command with the `Suggested commit:` line, and stop until the user has committed.
- `Suggested commit: none — <reason>`: nothing is staged or committed, but the gates still run to confirm the tree did not change.
- Never push unless the run mode allows it.

The repo's `CLAUDE.md`/`AGENTS.md` commit and push rules win over this step. Where they ask for confirmation before a commit or a push, stage the phase, show the diff summary, and ask before committing or pushing.

**Advance.** Set the entry point's `Status` to one of `pending`, `in-progress`, `done`, `abandoned`; write progress in a separate `Progress:` line. Then follow the run mode's Continue answer: with "automatic", go on to the next phase, unless:

- a Manual Test Checkpoint follows this phase → stop, hand the user the checkpoint text, and wait for their result;
- a blocker or a decision outside the phase's scope → stop and ask;
- the run mode stops after each phase, or the phase was left uncommitted by the commit step.

## 3. Report

Per guarded phase, one line: `✅ Phase N — <what changed> · gates: <commands> green (or "no gate") · defects fixed: <n> · workspace: <ID> → <status> (or "n/a") · <commit sha, or "staged, commit command printed">`. At a stop, add what the user must do next. Paste gate output only when it is red.
