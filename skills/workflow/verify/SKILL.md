---
name: verify
description: Verify a code change — run the project's build/lint/typecheck gates for the paths it touches, then drive the change at its runtime surface, and report a verdict. Reads every project-specific command from docs/agents/verify.md. Use after writing or modifying code, before committing, or when another skill needs a correctness check on what it just produced. Diffs touching only docs or only tests have nothing to gate or drive — report SKIP.
---

# Verify

Two questions, in order: does the change **build**, and does it **work**?

The **gates** answer the first — cheap, mechanical, and the agent's job.
Driving the **surface** answers the second. Answer only the first and you have a change that compiles; you do not yet have one that works.

Everything project-specific — commands, routing, policy — lives in
`docs/agents/verify.md`. This skill holds the flow that reads it.

## 1. Load the config

Read `docs/agents/verify.md`. It carries four things:

- **Gate table** — touched path → the commands that gate it
- **Routing** — which skill fixes which class of failure
- **Sequencing** — what must run before what
- **Runtime policy** — which surfaces the agent may drive itself

In a monorepo where the config is per-package, `<touched-dir>/docs/agents/verify.md`
overrides the root for paths under it.

Config missing → [bootstrap it](bootstrap.md), then continue.

## 2. Establish the diff

**The diff is ground truth.** Any description of it — the user's, a plan's, your own from earlier in the session — is a claim about it. Read both; when
they disagree, that disagreement is a finding.

```bash
git diff HEAD --stat            # uncommitted work
git diff @{u}.. --stat          # committed, upstream set
git diff origin/HEAD... --stat  # committed, no upstream
```

Establish the full range — a branch may be many commits, and `HEAD~1` hides the rest. State the commit count. Output truncating → redirect to a file and
Read it. In a repo with no diff from any of these → say so and stop.

**Completion criterion:** every touched path is named and mapped to a gate row, or explicitly noted as gate-less.

## 3. Skip check

- **Docs, config with no behavioral output, or type-only declarations** →
  `SKIP — no runtime surface: (reason)`. One line. The gates have nothing to prove here.
- **Tests only** → `SKIP`. Tests are the author's evidence; CI runs them.
  Re-running them is a CI rerun wearing a verification hat.
- **Source plus tests** → gate and drive the source; the test files ride along.
  Reading a test to learn what the change should do is fine — it is a spec.
  Then go drive the app.

Anything touching product source has a surface. Find it in step 5.

## 4. Run the gates

Apply the **sequencing** rules first — a generator that feeds another stack runs before that stack's gate, or you gate against stale inputs and pay for
the run twice.

Then map each touched path through the gate table and run the gates its globs hit, **in the order the table lists them**. A diff confined to one stack pays
for one stack's gates.

Gate fails → look the failure up in the **routing** table, invoke the skill it names, then re-run that gate. Green on every gate → step 5. A gate that fails
for reasons the diff didn't cause (toolchain rot, a broken lockfile) → report
`BLOCKED` with the exact command and output; that is not the change's fault.

**Completion criterion:** every gate row the touched paths hit has been run and is green, or a `BLOCKED`/`FAIL` verdict names the one that isn't.

## 5. Drive the surface

The **surface** is where the change meets a user — human or programmatic.
That is where you observe it.

| Change reaches | Surface        | Drive it by                                    |
| -------------- | -------------- | ---------------------------------------------- |
| CLI / TUI      | terminal       | type the command, capture the pane             |
| HTTP handler   | socket         | send the request, capture status + body        |
| GUI / web page | pixels         | drive the browser, screenshot                  |
| Library        | package export | call it through the public entry, not `./src/` |
| Background job | its trigger    | fire the trigger, read the effect              |
| Prompt / agent | the agent      | run it, capture its behavior                   |

**An internal function is not a surface.** Something in the repo calls it, and that caller ends at a row above. Follow it there and drive that.

Take the smallest path that makes the changed code execute. Changed a flag — run with it. Changed error handling — trigger the error. Changed a handler —
hit that route.

**Read your plan back before you run it.** If every step is a gate you already ran, you have planned a rerun, not a verification.

The **runtime policy** in the config decides who drives. Where it grants the agent a bounded surface, drive it yourself. Where it reserves the app for the
human, hand off: name the exact flow, the input, and the observation that would settle it — then let them drive and report back. A handoff is a real
verification; guessing on their behalf is not.

## 6. Verdict

State one: `PASS` · `FAIL` · `SKIP` · `BLOCKED` · `HANDOFF` (driven by the human, awaiting their report).

**The verdict is table stakes; the observations are the signal.** You are the only reviewer who ran the thing. Anything that made you pause, work around, or
go "huh" is information the author does not have. Filter for "would I mention this if they were sitting next to me," not for "is this a bug."

Report the gate results as a list and the surface observation as prose — what you drove, what you saw, what you expected.

## Keeping the config true

Edit `docs/agents/verify.md` when it steered you wrong: a command that failed or turned out stale, a path with no gate row, a surface it doesn't cover. That
is maintenance, and it compounds — the next session reads what you fixed.

Routine confirmations warrant no edit. Leave the wording and arrangement of what is already correct alone.
