---
name: execute-plan
description: >
  Runs IMPLEMENTATION_PLAN.md by executing unchecked items one at a time.
  Use when the user says "execute the plan" or "work through the plan".
  Stages and hands off for review, or commits, per the plan's `Review:` line and the repo's rules,
  and offers to continue after each item.
  Do not use for creating plans (use to-plan instead), one-shot implementation
  without a plan, or non-implementation tasks.
---

# Execute Plan

Work through `IMPLEMENTATION_PLAN.md` one checklist item at a time. Each checkpoint is staged and handed off for review, or committed, per the plan's `Review:` line and the repo's own rules. Offer to continue — never auto-proceed.

## Before starting

### 1. Get the plan

Use the path the user gives. Without one, resolve it per the `writing-great-plan` skill's `references/plan-location.md` → "Which plan runs" (if that skill is not installed, ask for the path): exactly one open plan → use it and name it in one line; several → ask which; none → ask for the path.

### 2. Find first unchecked item

- **Multi-file plan** (the entry point holds a Phase Index and no checkboxes): read the Phase Index, then open the first file under `phases/` that still has a `- [ ]`, in index order. Grepping the entry point for a checkbox finds none and would report "all checked" on a plan that has not started.
- **Single-file plan:**

  ```bash
  grep -n "- \[ \]" IMPLEMENTATION_PLAN.md | head -1
  ```

  Read the plan from that line forward — don't re-read completed phases.

Every box checked: report done and stop.

Before the first item, read the plan's `## Overview`, `## Open Questions` and `## Notes` once. An Open Questions bullet applies as written: use its `Default:`. A question the plan does not list that blocks an item: take the safest reading, keep going, and say so in the report as `Assumed: <what>`.

**Resuming a paused item:** if the first unchecked line has a `> Paused — N/M sub-files done` marker, read the sub-bullets to see which are done and resume from the first unticked one.

---

## Execution loop

For each unchecked item:

### Step A — Read

Before writing any code, read every file listed under the item's `Files:` and `Skill:` fields. Don't re-read what's already in context.

**Item markers** (the plan's standard form):

- `Runner: human` — stop and wait for the user's answer; do not do the item.
- `Runner: guardian` — in a single session, do it yourself after the phase.
- `Execution unit:` with one sub-checkbox per unit — run one unit per round, tick its sub-checkbox, and checkpoint after each unit.
- `Suggested commit: none — <reason>` — nothing is staged or committed, but the gates still run.

Skip Steps A and B when you're dispatching a marked batch — each agent reads and implements its own phase. Go to Parallel batches, then resume at Step C.

### Step B — Implement

Execute the item. Read `docs/agents/domain.md` (if present) to determine which context you're working in, and use it for context and glossary only; it does not name gates. If the file does not exist, carry on with the root `GLOSSARY.md` and `docs/adr/` where they exist, and suggest once that the user run `/setup-matt-pocock-skills` (from `mattpocock/skills`) to create it; do not stop, and do not create the file yourself.

**The gates.** One source, in this order: the `verify` skill when it is installed; otherwise the gates in `docs/agents/verify.md`; otherwise the plan header's `Verify:` line; with none of these, report `no gate`. Every later "the gates" or "verify" in this skill means this order.

**Slow test suites run at the scope the verify config names.** When that config defines a focused run (e.g. an `## Integration test scope` section in `docs/agents/verify.md`), run only the focused part the phase reaches while building and at its checkpoint — even when the phase file asks for the whole suite — and leave the full suite to the point that config names (usually the plan's last phase of that stack, or a diff into shared infrastructure). Report the focused command and its output as the phase's verification; a full suite you didn't run is `not run` plus that reason. With no such config, run the suite the phase file names.

If verify fails: attempt to fix (import paths, missing interfaces, type mismatches). If not obvious after two attempts, invoke `/diagnosing-bugs` if installed. If diagnosing-bugs cannot resolve (or is not installed), invoke `/handoff` (from `mattpocock/skills`, if installed) or stop and report the failure to the user.

**Report verification honestly.** A verification is reported only two ways: the command's actual output, pasted, or the literal words `not run` plus the reason it wasn't. "All green" or "PASS" with nothing pasted under it is not a report — it's a claim, and an unfalsifiable one. A check whose result decides something (ship this, mark this phase done, trust this number) is re-run through a tool whose output is not summarized by a shell wrapper before it's reported — a wrapper that prints only "5/5 passed" hides the one line that would show it was wrong.

**The plan is a hypothesis, not a spec.** When the code contradicts what the plan says, follow the code — it's the ground truth — and record the correction in the plan file as `> Plan correction — <what the plan said> / <what is true>`. Don't silently comply with a plan that's now wrong, and don't stop to ask when the contradiction is unambiguous; escalate only when it's genuinely unclear which side is right.

**Never hand the user an unreviewable command.** Don't print a command whose effect the user can't read before running it — no `git update-index --cacheinfo`, no hardcoded blob SHAs, nothing that stages content the diff doesn't show. A commit split that needs intermediate file states is built from explicit edits (write the file, stage, repeat), never from index plumbing the user would have to trust blind.

### Step C — Wrap up

Do these in order. The plan file is edited **before** anything is staged — a phase whose code is committed but whose boxes are still empty has to be repaired by a second commit.

**Guardian handoff:** if the plan's header carries the `**Review:** guardian` line, steps 3-5 below are replaced by "Guardian handoff mode" at the end of this section. Without that header, follow steps 1-5 as written — today's behavior is unchanged.

1. **Tick the boxes and set `Status`** — `- [x]` on what landed, `Status: in-progress` (any unchecked) or `done` (all checked). Tick only what you can see in the diff, not what you remember writing: run `git diff --stat HEAD` (add `--staged` if already staged) and confirm
   - every file under the item's `Files:` appears in the diff — one that doesn't is the finding;
   - everything the item names concretely — a field, a method, a constraint, a validation — exists in the hunks;
   - every plan-level `Note` naming this phase. Those rules are split across phases on purpose ("Applies to Phase 1 (field) and Phase 3 (enforcement)"), which is exactly how one half ships alone. Grep the diff for it; don't recall it.

   Anything missing: do it now, or leave that box unchecked with `> Incomplete — <what's missing>` above it. Never tick past a gap — a `[x]` is a claim every later phase and session trusts without rechecking. This is a conformance check, not a code review: does the described change exist, not is it well written.

   For a **batched** phase the agents already ticked their own files. Don't re-read the phase files to redo it — take items-left-unchecked from the batch report, and run the `Note` sweep yourself, since the agents never saw the plan-level notes.

2. **Update the workspace** — when the plan lives in a feature workspace (its folder is `plans/NN-<name>/`, with `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` two levels up, set up by the `kickoff` skill; else skip, and the report's **Workspace:** line reads `n/a`). The step lives here and not only in the plan's Notes because a phase file is self-contained: the agent running one phase never reads the Notes.

   If an ADR is due (below) and the `domain-modeling` skill is not installed, stop before changing anything: say that `domain-modeling` (from `mattpocock/skills`) is missing, and "see this repo's README for the pinned install command". Do not write an ADR format yourself.

   Update the workspace as its `TRACKER.md` `## How this tracker works` says, plus `WHATNEXT.md` and the workspace's `INDEX.md` row (this workspace's row only; leave every other row alone). Where `CONTEXT.md` `## Workspace rules` (the tracker's language) differs, it wins. What this skill adds:
   - **Status.** This phase's work item is in the Phase Index `Tracker` column (else the plan's Notes). Set it `done` when this phase was the item's last one and is verified, else `in-progress`. Under `Review: guardian` the executor stops at `in-progress`: `/review-phase` sets `done` once the phase passes review.
   - **Action Log.** One row, today's date, plain words for the report's audience: what this phase built, plus "waiting for review" under guardian.
   - **`WHATNEXT.md`.** Rewrite State now (last commit, what is staged) and Next steps: the finished step leaves, a partly done one keeps only what remains, and under guardian the next step is the review of this phase.
   - **ADR candidates.** A decision tagged `ADR: candidate` in `CONTEXT.md` (`grep -n "ADR: candidate" CONTEXT.md`) whose reasoning this phase's code now embodies becomes an ADR now, written with the `domain-modeling` skill, with its tag replaced by the ADR id and the terms the phase coined added to the glossary; the ADR is a repo file, so stage it with the phase. Under `Review: guardian` leave this to `/review-phase`, along with the `done` status.
   - Apart from the ADR, these files are git-ignored: edit them, never stage them.

   Done when: the work item's status, one new Action Log row and `WHATNEXT.md` all reflect this phase, and `grep -c '^\[x\]' TRACKER.md` prints the same number as before you edited it.

3. If the phase has a `Suggested commit:` line that is not `none`: **stage the plan file together with the code** (a plan inside a git-ignored workspace is edited, not staged), then commit using the phase's `Suggested commit:` line if present — via the optional `/caveman-commit` skill (from `JuliusBrussee/caveman`) when installed, otherwise per the repo's own commit rules.
4. **Commit under the repo's own rules.** Who runs a commit, and when, is set by the repo's `CLAUDE.md` / `AGENTS.md`, never by this skill. Where they let the agent commit, commit. Where they ask for confirmation, ask, then commit. Where they reserve it for the user, or say nothing, print the `git commit -m "..."` as a fenced one-liner for the user to run, and stop there. `Suggested commit:` in a phase file is the _message text_, not advance permission — the plan pre-approves the wording, never the act.
5. **Always stop and confirm.** Never auto-proceed.
   - **Recompute `Next` from disk, not memory.** Before reporting what's next, re-read the plan's Phase Index from disk right now — don't rely on what this session remembers ticking or dispatching. A phase another agent, an earlier checkpoint, or a parallel batch already finished (or one still open that this session assumed was done) only shows up reliably in the file on disk.
   - **Check whether fresh session is a live option — don't skip this check, but don't dangle it as a choice unless it's real.** Read the next unchecked item's `Files:`/`Skill:` fields and diff them against what's already in context this session. Fresh is only worth raising when at least one holds: the next item starts a **new phase**, its file list **doesn't overlap** what's already in context, or it carries a **`Batch`** letter with sub-agents available (see Parallel batches). If none of those hold — same phase, same files, no batch — staying is the only sensible move; don't present fresh as an alternative.
   - **Report using the matching template below.** Use the **full form** (with `Recommendation:` and the stay-or-fresh question) only when fresh is a live option per the check above. Otherwise use the **compact form** — no `Recommendation` line, just a plain "Continue?".
   - If the user says continue, loop back to Step A. If fresh session, stop and tell the user the plan path to hand to the new session.

**Guardian handoff mode** (plan header carries the `**Review:** guardian` line) — replaces steps 3-5 above (step 2, the workspace, still runs):

1. Stage the code and the plan file together (skip the separate commit step). With `Suggested commit: none — …` nothing is staged.
2. Write a short phase report into the plan file itself, under its own `## Executor report` heading — not the chat, and not the `## Review` heading the reviewer owns — the reviewer reads it from there via `/review-phase`. Keep it to 6 lines at most: what landed (one line), **Verify:**, **Staged:**, then one line per plan correction, `Assumed:` and open risk. No file list (the diff has it), no restating the items. On the **Staged:** line, paste the one-line output of `git diff --cached --shortstat` run just now (e.g. `4 files changed, 120 insertions(+), 3 deletions(-)`): the claim that the code is staged travels with the evidence that it actually is, same contract as the Verify line. Not the `git status` block: it grows one line per file and lists files left unstaged on purpose. Keep it separate from **Verify:** — that one stays the gate output for the paths this phase touched (`docs/agents/verify.md`). Two claims, two labels; a report that shows staging where the gate belongs has quietly dropped the gate.
3. Stop. Do **not** print a `git commit` command — the commit comes after the review, under the repo's own commit rules (see `/review-phase`).
4. Report `Next: awaiting /review-phase` in place of naming the next phase.

If `review-phase` is not available in this session, say so and follow its steps yourself: re-run the gates, check the diff against the items, then commit per the repo's rules.

Without the `Review: guardian` header, none of this applies — steps 1-5 above are the whole of Step C.

---

## Parallel batches

A multi-file plan's Phase Index may carry a `Batch` column. Phases sharing a letter were verified at authoring time to have no dependency and disjoint file writes.

**No sub-agent capability? Ignore the column** and run the phases in order — the plan is correct sequentially either way. Never batch phases the index didn't mark: `Depends on: nothing` alone
is not permission, because file-write conflicts don't show up in that field.

With sub-agents, when the next unchecked phase carries a batch letter:

1. Dispatch **one agent per phase**, concurrently, routing each by its own Weight letter to the executor of that weight (names below). The agent definitions carry the model and effort for the tier — don't override the model per invocation. Weight already encodes the capability the phase needs; that is
   what the letter is for. Mixed letters in one batch are normal: route per phase, not per batch. Never split one phase across agents.

   **Executor names.** Ask the harness which agent types it offers (in Claude Code, ask Claude to
   list the agent types it can dispatch). You need one executor per weight. Use the names exactly
   as listed:

   - Installed as files in `.claude/agents/`: `phase-s`, `phase-m`, `phase-l`, `phase-xl`.
   - Installed from the `phase-agents` plugin: `phase-agents:phase-s` and so on. A bare `phase-s`
     is rejected there ("Agent type 'phase-s' not found").

   Record the four names once at preflight and use them verbatim as the dispatch agent type
   (S → the `-s` name, M → `-m`, L → `-l`, XL → `-xl`). None found: stop and say how to install
   them (the `phase-agents` plugin, or copy the agent files into `.claude/agents/`); do not
   substitute a general-purpose agent. If the harness has no sub-agents at all, run the plan in
   this session with `execute-plan` under `Review: guardian`, then `review-phase`.

   Without sub-agents, ignore the `Batch` column (above) and run each phase in this session under this skill's `references/executor-rules.md`.

2. **Hand each agent its phase file path and nothing else.** Phase files are self-contained by design, and the agent definitions (the same text as `references/executor-rules.md`) already forbid opening sibling phase files, the plan's entry
   point, committing, or starting a second phase — a 10-phase plan must cost each agent one phase file, not ten. When you run a phase in this session instead, follow `references/executor-rules.md` yourself. If a plan-level `Note`
   applies to a phase, paste that line into its prompt rather than pointing at the file it lives in.
3. **The batch is one checkpoint.** Wait for all agents, then run the gates once over the combined diff (a slow suite at the focused scope of the combined diff, per the verify config). Never let batch agents run a database-backed suite at the same time if the verify config says runs share one test database — have them stop at build/lint and run the tests once here.
4. Report it as a single Step C. `Next:` names the batch, not one phase; commit with the batch's `Suggested commit:` lines — one commit per phase, unless the user wants them squashed. Under `Review: guardian`, stop after staging instead: each phase's commit follows its review.
5. If an agent fails, report which phases landed and which didn't. Fix or re-dispatch only the failed phase — never re-run the whole batch over work that already landed.

Routing by Weight is where the token saving actually lives: an `S` phase on a cheap model costs a fraction of the same edit made inline, and its file reads never enter your context. Heavy
phases are the opposite trade — an `L` agent re-reads its files at full price, buying flat parent context and wall-clock rather than cheaper tokens. Take the batch the plan marks either way;
don't go hunting for extra ones.

**Weight sizes the phase, never the session.** Dispatching an `S` phase to a cheap agent is the intended saving; dropping the _session_ to a cheap model because the next phase is `S` is not the
same trade. The session doesn't only implement — it owns Step C, the plan file, the stop-and-confirm, and the commit boundary, and that bookkeeping is the same difficulty whatever the phase's
letter. An unbatched `S` phase has no cheap lane by design: run it here at full strength, or hand the whole plan to a fresh cheap session and accept that the bookkeeping degrades with it.

---

## Report Template

Every agent, regardless of model, reports checkpoints and completion in this exact shape — so output is consistent across sessions. Fill the placeholders; drop a line only if it's genuinely not applicable (e.g. no commit yet).

### Checkpoint report (after Step C, mid-plan)

**Full form — use only when fresh is a live option (new phase, file lists diverge, or a batch is available):**

```
✅ **Phase <N> done** — <one-line summary of what changed, plain language, no jargon>

**Verify:** `<command run>`
<pasted output — or the literal "not run" plus the reason>

**Commit:**
`git commit -m "<type>(phase-<NN>): <subject>"`
<one of: "— staged, run the command above" | "— already committed" | "— nothing to commit (docs/tests only)">

**Workspace:** <`TRACKER.md` <ID> → <status> + Action Log row, `WHATNEXT.md` rewritten | n/a — plan not in a workspace>

**Next:** Phase <N+1> (<phase name>, <weight>) — touches `<key files/dirs>`
<or, for a marked batch: "**Next:** Batch <letter> — Phases <N+1>, <N+2>, <N+3> (<names>) in parallel">

**Recommendation:** <fresh session | stay | batch> — <one-clause reason tied to file overlap>

**Plan:** `<path/to/IMPLEMENTATION_PLAN.md>`

Continue here, or start fresh for <whatever Next: names>?
```

**Compact form — use when staying is the only sensible move (same phase, same files, no batch). No `Recommendation` line, no fresh mention:**

```
✅ **Phase <N> done** — <one-line summary of what changed, plain language, no jargon>

**Verify:** `<command run>` → <pasted output, or "not run" plus the reason>

**Commit:** `git commit -m "<type>(phase-<NN>): <subject>"` <staged | already committed | nothing to commit>

**Workspace:** <`TRACKER.md` <ID> → <status> + Action Log row, `WHATNEXT.md` rewritten | n/a>

**Next:** <next phase name, weight> — touches `<key files/dirs>`

Continue?
```

Rules:

- Bold the phase-done line with a ✅ so it's scannable in a long transcript.
- The commit line is always a fenced one-liner — never prose describing the command.
- **Next** always names the _phase_ (or batch), not just the next checkbox item — the user thinks in phases.
- **Recommendation**, when present, is one clause, not a paragraph — see Step C for how to compute it. Omit the field entirely in the compact form rather than filling it with "stay" — a field that's never in question isn't worth a line.
- **Workspace** names what step 2 actually changed, read back from the files — a template field left at its placeholder means the step was skipped.
- **Verify** is the command and its output, or `not run` plus the reason — never a bare PASS. Same contract as Step B; a checkpoint is where an unrun check gets reported as green.
- **Under `Review: guardian`** (see Step C): drop the **Commit** line entirely and report `**Handoff:** staged, awaiting /review-phase`, with **Next:** reading `awaiting /review-phase`. The executor prints no commit command in that mode — the commit follows the review.
- The closing question always mirrors what **Next:** just named — never hardcode "Phase N+1" literally, since **Next** may be a batch or a differently-numbered phase.

### Completion report (all items checked, see Completion section)

```
✅ **Plan complete** — <plan name/path>, all <N> phases done

**Verify:** `<command run>`
<pasted output — or the literal "not run" plus the reason>

**Docs:** <"refine-docs run" | "N/A — no doc phase">

**Suggested commit / PR:** <commit message, or "skip — maintenance plan">
```

Drop the PR line for maintenance plans per the Completion section rule.

---

## Partial completion (batched items)

If the item bundles multiple sub-files and you must stop before finishing all of them:

1. Tick off completed sub-bullets, leave parent unchecked.
2. Add above the parent: `> Paused — N/M sub-files done, resuming from <next file>`
3. Stop — don't commit or offer continuation.

---

## Handling manual-test feedback

When the user reports behaviour that doesn't match expectations on a completed (`[x]`) phase:

1. **Locate via git** — find the phase's commit by its `Suggested commit:` text, or by `git log -- <a file from its Files:>`, then `git show <hash> -- <file>`
2. **Classify** — regression (item does wrong thing) vs scope gap (plan missed a case)
3. **Patch the plan** — regression: uncheck item, add `> Reopened — manual test: expected <X>, got <Y>`, fix, re-check. Scope gap: add new item tagged `Found-in: manual test`.
4. **Re-verify** — run the gates that apply to the phase's touched context
5. **Commit** — `fix(phase-NN): <description>`

---

## Completion

When all items are checked:

1. Update `Status` to `done`
2. Run a final verify — the gates for whichever stacks the diff touched, with each slow suite at full scope once, unless a reviewer already ran it full after the last phase
3. If docs were a phase, confirm `refine-docs` was run
4. For a plan with no `PlanType:` line (a feature plan): suggest commit and PR. For a plan with a maintenance `PlanType:`: skip commit/PR suggestions
5. Report using the Completion report template above
