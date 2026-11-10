---
name: guard-plan
description: Runs a multi-file IMPLEMENTATION_PLAN.md with the session as guardian — every phase is dispatched to the phase-s/m/l/xl agent matching its Weight, then the guardian re-verifies, fixes, commits, and pushes before moving on. Use when the user wants a plan executed by subagents, wants to save tokens on execution, or says "guard"/"supervise" the plan. Do not use for writing plans (to-plan) or for a single inline phase (execute-plan).
---

# Guard Plan

The session is the **guardian**: it never implements a phase. Executors do the work on the model their Weight buys; the guardian spends its (more expensive) tokens only where defects surface — running gates, checking claims, fixing, committing. The saving depends on that split holding: the guardian reads the phase file and the diff, not the codebase.

## 1. Preflight — once per session

1. Get the plan path from the user, or resolve it per `.claude/skills/writing-great-plan/references/plan-location.md` → "Which plan runs" (entry point `IMPLEMENTATION_PLAN.md` with a Phase Index). Read the entry point: Phase Index, Open Questions, Manual Test Checkpoints, Notes. Those four are all the guardian keeps in context.
2. **Executors exist.** The `phase-s`, `phase-m`, `phase-l` and `phase-xl` agents must be available: in `.claude/agents/`, or from the `phase-agents` plugin (`phase-agents@skeleton-skills`, which ships them from this catalog's root `agents/` folder and names them `phase-agents:phase-s` and so on). The `skills` CLI does not install agents; when one is missing, stop and tell the user rather than dispatching a general-purpose agent in its place.
3. **Gates runnable.** Every gate in `docs/agents/verify.md` for the stacks the plan touches must run to a real verdict. A gate that errors on tooling (missing binary, unreachable dependency, linter built for an older toolchain) is a toolchain defect, not a code defect: fix it now or stop and tell the user what access is missing. When the repo keeps `docs/agents/toolchain.md` (one line per symptom and its fix, for the environments its sessions run in), read it first and add every new fix you find to it.
4. **Baseline.** Run the gates on a clean worktree of `HEAD` (`git worktree add <scratch>/base HEAD`) and record every pre-existing failure in the plan entry point under `## Baseline`. From here on only a failure absent from the baseline counts against a phase.

Done when every gate has produced output on the baseline and `## Baseline` lists its failures (or "none").

## 2. Phase loop

Take the first phase with unchecked items, or its whole `Batch` group.

**Dispatch.** One agent per phase, `subagent_type` = `phase-<weight letter>` (S→`phase-s`, M→`phase-m`, L→`phase-l`, XL→`phase-xl`). A phase file with a `Model:` line (e.g. `Model: opus`) overrides the agent's model: pass it as the dispatch `model`. Reserve it for phases whose defects would pass the gates silently (schema transforms, data migrations). The prompt carries only:

- the phase file's absolute path,
- each plan-level Note that names this phase or its phase range, pasted verbatim,
- for a batch: which paths the sibling agents own, so each stays inside its own `Files:`,
- known environment facts the executor would otherwise trip on (a dependency that can't be fetched, a gate it must not run),
- each Open Questions bullet whose `Affects:` names this phase, pasted with its `Default:`,
- the report limit: `## Executor report` of 6 lines at most — what landed, Verify, Staged, then one line per plan correction, `Assumed:` or open risk. **Staged:** is the one-line `git -C <repo> diff --cached --shortstat` output, overriding the agent file's raw `git status --porcelain` block.

Batch → dispatch all in one message, in the background; guard each one as it reports. Single phase → dispatch and wait.

**Guard.** Run the `review-phase` rhythm against this phase's diff: re-run the gates yourself, probe the phase's `Prone to:`, check every factual claim in the executor's report against the repo (a claim of "done", "granted", "unchanged", or "not possible" is the one that is wrong). Before calling a phase clean, grep the diff for each concrete thing its items name: field, permission, route, role grant.

Defects:

- A local fix (a path, a missing grant, a stale mock, a lint hit) → fix it inline.
- Missing or wrong item-level work → send the findings back to the same executor (`SendMessage`), then guard again.
- The plan contradicts the code → follow the code; write `> Plan correction — <said> / <true>`.

**Record.** Append `## Review` to the phase file in `review-phase`'s template: gates re-run, defects found and fixed, plan corrections, anything not run and why. Keep it to the verdict, one line per defect, and one line for what was ruled out.

**Commit.** Stage this phase's paths plus its phase file only (sibling phases in a batch may still be in flight; leave the phase file out when the plan lives in a gitignored folder), commit with the phase's `Suggested commit:` line, push. A phase is committed only on a green gate: if a gate could not run, the phase stays staged-but-uncommitted and the loop stops with the reason.

The repo's `CLAUDE.md` commit and push rules win over this step. Where it asks for confirmation before a commit or a push, stage the phase, show the diff summary, and ask before committing or pushing.

**Advance.** Set the entry point's `Status`. Continue to the next phase automatically, unless:

- a Manual Test Checkpoint follows this phase → stop, hand the user the checkpoint text, and wait for their result;
- a blocker or a decision outside the phase's scope → stop and ask;
- the user asked to confirm after each phase.

## 3. Report

Per committed phase, one line: `✅ Phase N — <what changed> · gates: <commands> green · defects fixed: <n> · <commit sha>`. At a stop, add what the user must do next. Paste gate output only when it is red.
