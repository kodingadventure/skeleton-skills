---
name: guard-plan
description: Runs a multi-file IMPLEMENTATION_PLAN.md with the session as guardian — every phase is dispatched to the phase-s/m/l/xl agent matching its Weight, then the guardian re-verifies, fixes, and commits when the repo's commit rules allow. Use when the user wants a plan executed by subagents, wants to save tokens on execution, or says "guard"/"supervise" the plan. Do not use for writing plans (to-plan) or for a single inline phase (execute-plan).
---

# Guard Plan

The session is the **guardian**: it never implements a phase. Executors do the work on the model their Weight buys; the guardian spends its (more expensive) tokens only where defects surface — running gates, checking claims, fixing, committing. The saving depends on that split holding: the guardian reads the phase file and the diff, not the codebase.

This skill needs a harness that can start a sub-agent with its own context and send it a follow-up. Without that, run the plan in this session with `execute-plan` under `Review: guardian`, then `review-phase`: the same guard, no dispatch.

## 1. Preflight — once per session

1. Get the plan path from the user, or resolve it per the `writing-great-plan` skill's `references/plan-location.md` → "Which plan runs" (entry point `IMPLEMENTATION_PLAN.md` with a Phase Index; if the `writing-great-plan` skill is not installed, ask the user for the plan path). Read the entry point: Phase Index, Open Questions, Manual Test Checkpoints, Notes, and `## Baseline` (for a `Waiting:` line). Those five are all the guardian keeps in context.
2. **Pending checkpoint.** Run `grep -n '^Waiting:' <entry point>`. Take the path of the result file from the line.
   - No line: go on.
   - A line and its result file exists: finish the preflight, then process the result ("Process the result" in section 3) before the next phase, without asking. Processing it earlier would delete the line the Baseline step reads.
   - A line but no result file: say that the test for checkpoint N has not been run, print the guide-session command again (`references/manual-test-handoff.md` → The command), and stop.
   - Several `Waiting:` lines: handle each as above, in checkpoint number order. Process every one whose result file exists; for each one without a result file, print the guide-session command again for that checkpoint only, and stop after the others are processed.
3. **ADR skill.** When the plan lives in a feature workspace (`CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` two levels above the plan folder), run `grep -c 'ADR: candidate' <workspace>/CONTEXT.md`. A count above 0 needs the `domain-modeling` skill: check your agent lists it. When it does not, stop here, before the baseline and before dispatching anything, and say that `domain-modeling` (from `mattpocock/skills`) is missing — "see this repo's README for the pinned install command". Never defer this check to the phase close: by then a phase is already committed without its ADR.
4. **Executor names.** Ask the harness which agent types it offers (in Claude Code, ask Claude to list the agent types it can dispatch). You need one executor per weight. Use the names exactly as listed:

   - Installed as files in `.claude/agents/`: `phase-s`, `phase-m`, `phase-l`, `phase-xl`.
   - Installed from the `phase-agents` plugin: `phase-agents:phase-s` and so on. A bare `phase-s` is rejected there ("Agent type 'phase-s' not found").

   Record the four names once at preflight and use them verbatim as the dispatch agent type (S → the `-s` name, M → `-m`, L → `-l`, XL → `-xl`). None found: stop and say how to install them (the `phase-agents` plugin, or copy the agent files into `.claude/agents/`); do not substitute a general-purpose agent. If the harness has no sub-agents at all, run the plan in this session with `execute-plan` under `Review: guardian`, then `review-phase`.

   The stop message names both install routes: `claude plugin marketplace add <catalog>` then `claude plugin install phase-agents@skeleton-skills --scope project`; or copy the `phase-*.md` files from the catalog's `plugins/phase-agents/agents/` folder into `.claude/agents/`. For a harness without sub-agents, point to the `execute-plan` route above.

5. **Gates runnable.** Take the gates from `docs/agents/verify.md` for the stacks the plan touches. If the repo has no `verify.md`, take them from the plan header's `Verify:` line. If neither exists, write "no gate" under `## Baseline` and say so in every report; do not stop. A phase that creates `verify.md` moves the gates to that file from the next phase on. Every gate must run to a real verdict. A gate that errors on tooling (missing binary, unreachable dependency, linter built for an older toolchain) is a toolchain defect, not a code defect: fix it now or stop and tell the user what access is missing. When the repo keeps `docs/agents/toolchain.md` (one line per symptom and its fix, for the environments its sessions run in), read it first and add every new fix you find to it.
6. **Baseline.** Run the gates on a clean worktree of `HEAD` (`git worktree add <scratch>/base HEAD`) and record every pre-existing failure in the plan entry point under `## Baseline`. From here on only a failure absent from the baseline counts against a phase. When a `Waiting:` line exists and `git rev-parse HEAD` equals the SHA on that line exactly, keep the recorded `## Baseline` and skip the gate run in the worktree; when HEAD differs, run the baseline as usual. The ADR-skill check, the executor names and the commit mode are always re-derived.
7. **Commit mode.** Ask nothing: derive it from the repo's rules, once per session (never reuse an earlier note). Run `grep -inE 'commit|push' CLAUDE.md CLAUDE.local.md AGENTS.md` in the target repo (skip files that do not exist), map the hits to one mode, announce it in one line, and record `Commit mode: <commit | confirm | print> — <the rule line quoted, or "no commit rule">` in the entry point under `## Baseline`.
   - **`commit`:** no commit rule, or a rule that lets the agent commit. The guardian commits each phase with its `Suggested commit:` line, then goes on.
   - **`confirm`:** a rule that asks for confirmation before a commit, **or a rule that is ambiguous**. The guardian shows the diff summary (`git diff --cached --stat`), asks, commits when approved, then goes on. Ambiguous rules fall here: "Commit only when the user asks", "Don't commit without review", "Be careful with git operations". Reading a prohibition as permission would commit in a repo that forbids it; the other mistake only costs one question per phase.
   - **`print`:** a rule that forbids the agent to commit. The guardian leaves the phase staged, prints the commit command and waits. When the user says to go on, check `git diff --cached --quiet` (exit 0) and that `git log -1 --format=%s` holds that phase's commit; go on only then, else say what is missing.
   - **Push:** never, and not offered as a choice. Push only when the user asks for it on their own, or when the repo's rules explicitly require it.

Done when the pending-checkpoint check ended in one of its three states (no line; a line with its result file, queued for processing; a line without it, stopped), the ADR-skill check passed (or the plan has no workspace, or no `ADR: candidate`), every gate has produced output on the baseline (or "no gate" is recorded), `## Baseline` lists its failures (or "none"), and the commit mode is recorded.

## 2. Phase loop

Take the first phase with unchecked items, or its whole `Batch` group.

**Items that are not the executor's.** An item marked `Runner: guardian` or `Runner: human` never goes into the dispatch prompt. The guardian does the `guardian` items itself after the phase is guarded. For a `human` item, the guardian stops and hands the user its text. A phase whose items are all marked is not dispatched.

**Repeating phases.** A phase with `Execution unit:` is dispatched once per unchecked unit sub-item, with "only unit X" in the prompt. Guard it, commit it (per the commit mode), then repeat until no unit is left.

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

**Commit.** Follow the commit mode recorded at preflight. Stage only this phase's paths, its phase file, and the ADR and glossary files the close step wrote (sibling phases in a batch may still be in flight; leave the phase file out when the plan lives in a gitignored folder).

- Commit mode `commit`: commit with the phase's `Suggested commit:` line.
- Commit mode `confirm`: show `git diff --cached --stat`, ask, and commit with the `Suggested commit:` line only when the user approves.
- Commit mode `print`: leave the phase staged, print the commit command with the `Suggested commit:` line, and stop until the user has committed (see Advance).
- A phase is committed only on a green gate: if a gate could not run, the phase stays staged-but-uncommitted and the loop stops with the reason.
- `Suggested commit: none — <reason>`: nothing is staged or committed, but the gates still run to confirm the tree did not change.
- Never push, unless the user asks for it or the repo's rules require it.

**Advance.** Set the entry point's `Status` to one of `pending`, `in-progress`, `done`, `abandoned`; write progress in a separate `Progress:` line. Then go on to the next phase, unless:

- a Manual Test Checkpoint follows this phase → run it (see "3. Manual test checkpoints");
- a blocker or a decision outside the phase's scope → stop and ask;
- commit mode `print`: the phase waits for the user's commit (see Commit); or the commit step left the phase uncommitted (a gate could not run, or the user declined under `confirm`).

## 3. Manual test checkpoints

A checkpoint marked `Runner: guardian` is run by a companion sub-agent (see "Agent checkpoint" below). A checkpoint marked `Runner: human`, or with no `Runner:`, goes to a guide session:

1. Prepare the files as `references/checkpoint-files.md` says.
2. Write the handoff prompt as `references/manual-test-handoff.md` says.
3. Write the `Waiting:` line under `## Baseline`.
4. Print the one-line command, then suggest wait or stop with one sentence of reason, and let the user choose.
5. Wait: when the user says "done", process the result. Stop: in a workspace, rewrite `WHATNEXT.md` (State now: waiting for checkpoint N; Next steps 1: run the guide session with that command, then `/guard-plan` in a new session), report as section 4 says (ending with the line for a new session), and end.
6. **Process the result.** Read the result file. If the user only pasted a summary in chat and no result file exists, write the result file from that summary first, so the file stays the single source. The guide writes the file as it goes, so a file can exist before the test ends: when a scenario of the checkpoint has no row, the test is unfinished. Name the scenarios still missing, print the command again, and wait or stop as in step 5; process nothing.
   - All `pass`: delete the `Waiting:` line, add the checkpoint's `🧪` line to the report in exactly the format section 4 gives, and go on.
   - Any `fail`: triage and patch the plan as the `execute-plan` skill's "Handling manual-test feedback" says (a regression reopens the item; a coverage gap becomes a new item `Found-in: manual test`), fix it through the usual defect flow in section 2, then write a new handoff for the failed scenarios and any other scenario the fix touched, to be recorded as a `## Re-run … after fix` section in the same result file, and go on from step 3.
   - Any `not run`: ask the user to run it again, or to accept it with its reason.

**Several human checkpoints at once.** When more than one `Runner: human` checkpoint falls due after the same phase (a fallback from an agent checkpoint counts), prepare all of them before asking anything: one prompt file and one `Waiting:` line per checkpoint (steps 1-3). Then print every guide-session command at once, in checkpoint number order, one line per checkpoint, with one wait-or-stop suggestion for all of them. On wait, process each complete result file in checkpoint number order (step 6); a checkpoint whose result file is incomplete keeps waiting (step 6).

### Agent checkpoint

A `Runner: guardian` checkpoint does not stop the run: no `Waiting:` line, no guide-session command.

1. Prepare the result file as `references/checkpoint-files.md` says.
2. Start the companion as `references/agent-checkpoint.md` says (model, effort and brief) and wait for its report. Never drive a scenario yourself, even one that is a single command: without the companion's result file the checkpoint has no evidence, and its rows are what the report and the re-test rely on.
3. Read the result file, not the report, and match every row with the report. A row that differs, or a scenario with no row, is unfinished: send the companion a follow-up (Claude Code: `SendMessage`) to finish it.
4. Process the rows:
   - All `pass`: add the checkpoint's `🧪` line to the report, in exactly the format section 4 gives, and go on to the next phase, without stopping and without a `Waiting:` line.
   - Any `fail`: triage, patch the plan and fix as the `fail` bullet of "Process the result" says. Then re-test through the same companion, not through steps 3-5: send it the failed scenarios and any other scenario the fix touched, and it records a `## Re-run … after fix` section in the same result file. Process that section the same way.
   - Any `not run` because the companion could not drive the scenario: hand that scenario, and only that one, to the user as a human checkpoint (steps 1-5 above). Put the companion's "could not drive" text from the result file under `## What the agent already tried` in the prompt (`references/manual-test-handoff.md`). The guide session appends its rows to the same result file as a `## Re-run <scenario> by a person` section and keeps the companion's rows; process that section, not the companion's `not run` row. The marker moves from `guardian` to `human` only this way, never back: the user chooses to look at a scenario, the guardian does not.

**Changing a scenario.** This holds for both runners. The guardian may change _how_ a scenario is run so that it matches the code: a route name, a flag, a setup step. Note it as `> Plan correction — <said> / <true>` under the checkpoint in the entry point. The guardian may not weaken or delete a scenario, or change what it expects so that it matches what the code does. A test run by an agent proves only what the scenario says, and a loosened scenario deletes the only evidence.

- Wrong: the expected result "the command exits 1 with `not-pending`" becomes "the command exits 0", because the code exits 0.
- Right: the route `/orders/:id/pay` becomes `/orders/:id/payment`, because the phase named it that way; noted as a `> Plan correction`.

When a change to what a scenario expects looks needed, it is a decision outside the phase: stop and ask the user.

## 4. Report

Per guarded phase, one line: `✅ Phase N — <what changed> · gates: <commands> green (or "no gate") · defects fixed: <n> · workspace: <ID> → <status> (or "n/a") · <commit sha, or "staged, commit command printed">`. At a stop, add what the user must do next; at a checkpoint, that is the one-line guide-session command, one per checkpoint due. In a workspace (the close step ran, so the line is not "workspace n/a"), end every report that ends the session (a stop, or the final report of the plan) with next step 1 of `WHATNEXT.md` and the skill it names when it names one, then one line for a new session, chosen from your skill list: `/resume-here <slug>` when `resume-here` is in it, else "read `<workspace>/CONTEXT.md`, then continue with `<workspace>/WHATNEXT.md`". Write exactly one of the two. The close step already recorded every phase, so the session can end here. Paste gate output only when it is red.

Per checkpoint, one line in one format, for agent and human checkpoints alike: `🧪 Checkpoint N — <agent | human | agent → human> · <n> pass, <n> fail, <n> not run · result <path>`. `agent → human` marks a checkpoint that fell back to a person; count it from the person's re-run rows, not from the companion's `not run` row. The guardian writes the line after the result file is processed. The final report of the plan lists every checkpoint with its line, so the user can spot-check it; never add results across checkpoints in a sentence ("two of three passed").
