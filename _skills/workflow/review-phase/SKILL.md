---
name: review-phase
description: >
  Reviews one staged, uncommitted phase before it's committed — the guardian step after
  execute-plan hands off under a `Review: guardian` plan. Re-runs the phase's own verification
  itself, checks the executor's report against the repo, fixes what's wrong, then prepares the
  commit. Use when the user says "review this phase", "guardian review", or wants an executor's
  work checked before it's committed. Do not use for a full code review (use /code-review
  instead), for re-planning, or to widen a phase beyond what the plan specified.
---

# Review Phase

The guardian: reviews one staged, uncommitted phase, fixes what's wrong, then prepares the commit,
which runs under the repo's own commit rules. Its whole economy rests on one property — **the reviewer never explores.** The
executor already paid for reading the codebase; this skill works from the diff, the phase file,
and verification it runs itself.

## The rhythm

1. **Read the phase spec** — the phase file `execute-plan` just handed off, including its Manual
   Test Checkpoints and `Suggested commit:` line.
2. **Read the diff.** `git status` / `git diff --staged` across every repo named in the plan's
   `**Repo:**` line (or its `## Environment` table, for a plan that touches 2+ repos) — batch the calls into one message, not one round trip per repo.
3. **Re-run the phase's own verification yourself.** Never accept the executor's report as given —
   running the check again is usually cheaper than reading the code that implements it, and it's
   strictly more conclusive: a report can be wrong about what it ran, a fresh run can't.
   Run a slow test suite at the scope the repo's verify config (`docs/agents/verify.md`) names
   for a review — usually the focused part the diff reaches, not the whole suite. The full suite
   runs only where that config says (e.g. the plan's last phase of that stack, or a diff into
   shared infrastructure); then report any failure outside the focused part with its cause line.
   With no such config, run the phase's own verification as written.
4. **Probe the failure mode the phase's `Prone to:` line names** — even when nothing in the diff
   looks wrong. A mode that's already bitten this repo is the first place to look, not the last.
   The names resolve against the repo's `docs/agents/failure-modes.md`; `references/failure-modes.md`
   here is its format, plus four generic modes worth probing when the repo has no file of its own.
5. **Check each factual claim in the executor's report against the repo itself** — especially a
   claim that something is absent, unavailable, or already correct. Those are exactly the claims
   nobody double-checks. From this workflow's own first run: a report that said "staged, run the
   command above" when nothing was staged, a `file:line` citation a sibling phase had already
   shifted, and a "not runnable until it's registered" that a one-line symlink disproved.
6. **Fix what's wrong.** Prefer fixing the source over patching a generated copy — a fix that lands
   in generated output disappears the next time the generator runs.
7. **Prove any new guard discriminates.** Break the thing it's supposed to catch, confirm the guard
   actually fails, then restore. A guard that has only ever been seen passing hasn't been tested —
   it's been observed, which is a different claim. Run each break against the focused test scope
   only — one probe per break, restoring the file each time — so a handful of probes costs less
   than one full-suite run.
8. **Prepare the commit.** Split fix from test, one commit per repo. Who runs it, and when, is set
   by the repo's `CLAUDE.md` / `AGENTS.md`, never by this skill. Where they let the agent commit,
   commit. Where they ask for confirmation, ask, then commit. Where they reserve it for the user,
   or say nothing, print the commands for the user to run.
9. **Record what was found in the phase file** — including anywhere the plan itself was wrong.
10. **Close the phase in the workspace** — when the plan lives in a feature workspace (`CONTEXT.md`,
    `TRACKER.md` and `WHATNEXT.md` two levels above the plan folder; else skip, and report
    `Workspace: n/a`). Under guardian the review is the moment a phase actually finishes, and the
    executor stopped at `in-progress` / "waiting for review" on purpose, so this bookkeeping is
    the reviewer's. A commit still pending changes nothing here: the workspace is git-ignored and
    never waits on one. Reading and editing these three files is part of the rhythm, not
    exploration.
    - Read `TRACKER.md` `## How this tracker works`; where it differs from this list, it wins.
    - **Status.** The phase's work item (the plan's Phase Index `Tracker` column, else its Notes)
      → `done` when the review passed and this phase was the item's last one. It stays
      `in-progress` while a defect is unfixed or another phase of the item is still open.
    - **Action Log.** The executor's row for this phase: still unticked → rewrite it in place
      with the outcome (reviewed and finished, plus what the review fixed, in plain words for the
      report's audience); already ticked → add a new row instead.
    - **Reported? column stays exactly as it is** — only `/tracker sent` changes it.
    - **`WHATNEXT.md`.** Rewrite State now (phase reviewed, the commit made or its commands handed to the user)
      and Next steps: the review step leaves, and what follows the phase becomes step 1.
    - **ADR candidates.** `grep -n "ADR: candidate" CONTEXT.md`. A decision tagged that way whose
      reasoning this phase's code now embodies gets its ADR written now — with the
      `domain-modeling` skill, where the repo keeps them — and its tag replaced by the ADR id;
      terms the phase coined go into the repo's glossary in the same pass. Under guardian this is
      the reviewer's, like the `done` status. An ADR is a repo file: stage it with the phase. Not
      left to the wrap-up, when the alternatives that lost are gone from everyone's memory.
    - **`INDEX.md`** at the root above the workspace: refresh this workspace's row (progress,
      today's date, who is being waited on). Leave every other row alone.

    Done when: the item's status, the Action Log row and `WHATNEXT.md` all reflect the review, no
    `ADR: candidate` this phase settled is left without its ADR, and `grep -c '^\[x\]' TRACKER.md`
    prints the same number as before you edited it.

Steps 3–5 and 7 are where defects actually surface — running things and checking claims, not
reading prose. Steps 1–2 alone catch none of them: a review that only reads the diff reproduces
the executor's own blind spots, because the diff is exactly what the executor already looked at.

## Three rules

- **Never re-derive.** No codebase exploration beyond what the rhythm above already calls for. If a
  diff is unreadable without context the report should have carried, that's not a gap to go fill —
  it's a finding about the report.
- **Raw output.** When a check decides something, run it through a tool whose output isn't
  summarized by a shell wrapper before reading it. A confidently wrong "identical" or "0" is worse
  than no check at all — it looks like verification and isn't one.
- **A green gate is not a working feature.** `typecheck`/`lint`/`test` passing says the code
  compiles, nothing more. Step 3's re-run has to exercise the behavior itself, not just the gates
  around it.
- **A finding is a claim too.** Check it against the repo before writing it down, the same way
  step 5 checks the executor's claims — this run recorded and later withdrew a finding that a skill
  bypassed `writing-great-plan`, and one that called a cross-reference stale when the referenced
  section is exactly where the docs layout puts it. The reviewer isn't exempt from the rule it
  enforces.

## What this is not

Not a full code review — that's `/code-review`, and covers standards and spec compliance across a
whole branch. Not a re-planning session — a phase that's wrong gets a `> Plan correction`, not a
redesign. And not permission to widen the phase's scope: fix what the phase touched, note anything
else as follow-up, and stop there.

## Report template

Write this into the phase file as its `## Review` section:

```markdown
## Review

<One sentence: what was re-run, by the reviewer, and the verdict — "Clean — no fixes needed" or
"N defects found", plus how they surfaced (re-running verification, probing `Prone to:`, checking a
claim against the repo).>

<If defects were found, one bullet each:>

- **<Short bold label>.** <One line: what was wrong, and why it matters.>

<If the plan itself was wrong:>
> Plan correction — <what the plan said> / <what is true>

<Anything investigated and ruled out is worth one line, so the next reviewer doesn't recheck it.>
```

Keep `## Review` short: the verdict sentence, one line per defect, and at most one line for what was ruled out. It is read again by every later reviewer; do not retell the diff.

Then, in chat — never written into the phase file:

```
**Workspace:** <`TRACKER.md` <ID> → <status>, Action Log row updated, `WHATNEXT.md` rewritten | n/a>

**Commit:**
`git commit -m "<type>(phase-<NN>): <subject>"`
```

One fenced command per commit, in the order they should run (fix before test), or the hash when the repo's rules had you commit. If nothing needed
fixing, the executor's own `Suggested commit:` line is still the message — reviewing doesn't invent
a new one.
