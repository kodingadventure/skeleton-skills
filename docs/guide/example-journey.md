# An example journey

This page answers one question: what does one small feature look like from the first PRD until the work is closed? The last step, `wrap-up`, moves what is worth keeping into the repo and closes the workspace. The snippets come from one real run on a small shop repo with two modules, orders and payments. Parts are cut with `…`. Workspace files sit in the default root, `.scratch/workspaces/`.

## The request

The PRD is `.scratch/workspaces/double-pay/PRD.md`. It is short and has one open question.

```markdown
# Refuse a second payment

## Problem

Paying an order that is already paid throws an error (`cannot pay a paid order`). The caller gets an exception instead of an answer.
…
## Open

- Should `markPaid` keep throwing when it is called directly? I think yes.
```

## 1. kickoff

You type `/kickoff double-pay`. It writes `CONTEXT.md`, `TRACKER.md` and `WHATNEXT.md` next to the PRD, lays out the empty folders, and adds a row to `.scratch/workspaces/INDEX.md`. Once you confirm it, the open question becomes a decision: `markPaid` keeps throwing. From `WHATNEXT.md`:

```markdown
## Next steps

1. The agent writes the first plan into `plans/01-refuse-second-payment/` with `to-plan` (the work items are in `TRACKER.md`).
…
## Guardrails

- Do not change `markPaid` behaviour (it keeps throwing); only `pay` returns `{ ok: false, reason: "not-pending" }`.
```

## 2. to-plan

You type `/to-plan for the double-pay workspace`. The plan has three phases: failing tests, the fix, and the wiki. (This repo already had a wiki and a Docs Layout; see [Documentation and wrap-up](./documentation-and-wrap-up.md).) Its phase headings:

```markdown
### Phase 1: Failing tests — Weight: S (Tracker: W1, W3)
…
### Phase 2: Refuse in `pay` — Weight: S (Tracker: W2)
…
### Phase 3: Documentation — Weight: M
```

## 3. execute-plan

You type `/execute-plan`. Phase 1 adds three payment tests and one test that `markPaid` still throws. The plan says `Review: guardian`, so `/execute-plan` stopped after staging the phase and you ran `/review-phase`, which checked it before anything was committed. The three new tests are red on purpose:

```
ok 2 - markPaid still throws for a non-pending order
…
not ok 5 - refuses to pay an order that is not pending
not ok 6 - a refused payment leaves the order unchanged
not ok 7 - checks status before amount
```

`git log --oneline` has no new line yet. Red tests would fail the gate, so phase 1 waits and is committed together with phase 2.

## 4. pause-here and resume-here

You type `/pause-here double-pay`. It rewrites `WHATNEXT.md` and writes a handoff for the staged work. From `WHATNEXT.md`:

```markdown
- Progress: 30% (`TRACKER.md`). W1, W3 done (Phase 1 reviewed). Next: W2.
…
1. Execute Phase 2 (`pay` checks status first), review it, then commit Phases 1 and 2 together with `feat(payments): refuse paying an order that is not pending`.
2. Phase 3 (wiki).
```

In a new session you type `/resume-here double-pay`. It takes the first next step. Phase by phase, you run `/execute-plan`, it stages the work and stops, you run `/review-phase`, and then `/execute-plan` again, until the plan is done. These are the first line of its closing summary and the new `git log --oneline` lines:

```
All three phases of the double-pay plan are done and committed. Paying an order that isn't pending now returns `{ ok: false, reason: "not-pending" }` instead of throwing.
…
c062948 docs(wiki): document refusal of a second payment
45cb116 feat(payments): refuse paying an order that is not pending
```

## 5. The documents

Phase 3 updated the wiki page `docs/wiki/order-payment.md`. The old rule "(no test)" was replaced by one that names its test:

```diff
-- Only a pending order can be paid. (no test)
+- Only a pending order can be paid; paying any other order returns `{ ok: false, reason: "not-pending" }` and does not throw. `refuses to pay an order that is not pending` (`src/payments/payments.test.js`)
```

## 6. wrap-up

You type `/wrap-up double-pay`. It adds one line to `GLOSSARY.md`. No ADR is needed, because the decisions were marked `ADR: no`.

```diff
+- **Refusal** — the result `{ ok: false, reason }` that a payment returns when it is declined by a rule (for example `not-pending`), as opposed to throwing an error.
```

It moves the INDEX row from Active to Shipped. It does not delete the workspace folder; it tells you to do that:

```
Wrap-up is done. The only step left is yours: delete `.scratch/workspaces/double-pay/`. I haven't deleted it.
…
| double-pay | 2026-11-13 | docs/wiki/order-payment.md (refusal rule + tests); GLOSSARY.md term "Refusal"; no ADRs (decisions tagged ADR: no) |
…
3369862 docs(glossary): add refusal
```

Next: [Skills that look alike](./skills-that-look-alike.md)
