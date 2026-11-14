#!/usr/bin/env bash
# Throwaway fixture repo for manual skill tests. Method: docs/agents/manual-test.md.
# Skills are copied from this catalog's working tree, so a test runs the checked-out branch.
# Usage: test-repo.sh <command> [args]
#   init                    create the fixture in a new mktemp dir, print its path
#   install SKILL DIR       copy skills/<group>/SKILL from the catalog into DIR/.claude/skills/
#   uninstall SKILL DIR     remove DIR/.claude/skills/SKILL
#   install-agents DIR      copy plugins/phase-agents/agents/phase-*.md into DIR/.claude/agents/
#   install-suite DIR [SKILL]  copy a suite skill (default domain-modeling) from the catalog's .claude/skills/
#   allow-commit DIR        CLAUDE.md: "the agent may commit after the gates pass" (committed)
#   silent-commit DIR       CLAUDE.md: no commit rule (committed)
#   drop-wiki DIR           remove the "### Wiki" table and docs/wiki/ (committed)
#   behaviour-commit DIR    commit a cross-unit rule (refund) with its test and no docs
#   workspace DIR           write .scratch/workspaces/demo/ (CONTEXT, TRACKER, WHATNEXT, a two-phase plan) and its INDEX.md
#   prd DIR                 write .scratch/workspaces/double-pay/PRD.md, a short PRD for /kickoff
#   root-line DIR [other]   append the "Workspace root" line to CLAUDE.md, uncommitted; with "other", also an unrelated rule line
#   finish-workspace DIR    needs workspace: mark the demo tracker and plan done, WHATNEXT step 1 = /wrap-up demo, commit the W1 code
#   feature-branch DIR NAME [merged]  branch NAME off main with one commit and stay on it; with "merged", merge it into main (--no-ff) first
#   notes-repo DIR [rule]   needs workspace or prd: git init DIR/.scratch and commit its notes; with "rule", write the notes-commit rule to DIR/CLAUDE.local.md (kept out of git via .git/info/exclude)
#   status DIR              show log, status, installed skills and agents
# Add a command here for each new setup a scenario needs, rather than editing a fixture by hand.
set -euo pipefail

CATALOG="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cmd="${1:-}"

need_dir() { [[ -n "${1:-}" && -d "$1/.git" ]] || { echo "error: not a test repo: ${1:-<missing>}" >&2; exit 1; }; }
need_clean() { [[ -z "$(git -C "$1" status --porcelain)" ]] || { echo "error: tree not clean in $1:" >&2; git -C "$1" status --short >&2; exit 1; }; }
commit() { git -C "$1" add -A && git -C "$1" -c user.name="Test User" -c user.email="test@example.invalid" commit -q -m "$2"; }
check_branch() { # the log header records this line
  echo "catalog: $(git -C "$CATALOG" branch --show-current) @ $(git -C "$CATALOG" rev-parse --short HEAD)" >&2
}
sedi() { if sed --version >/dev/null 2>&1; then sed -i "$@"; else sed -i '' "$@"; fi; }

install_skill() {
  local skill="$1" dir="$2" src=""
  check_branch
  for d in "$CATALOG"/skills/*/"$skill"; do
    [[ -f "$d/SKILL.md" ]] && src="$d"
  done
  [[ -n "$src" ]] || { echo "error: no skill $skill in catalog" >&2; exit 1; }
  mkdir -p "$dir/.claude/skills"
  rm -rf "$dir/.claude/skills/$skill"
  cp -R "$src" "$dir/.claude/skills/$skill"
  echo "installed $skill"
}

claude_md() { # $1 = dir, $2 = "allow" | "silent"
  {
    printf '# Shop\n\nA tiny shop: orders and payments. Tests: `npm test`.\n'
    if [[ "$2" == "allow" ]]; then
      printf '\n## Commits\n\nThe agent may commit after the gates pass. Use conventional commit messages.\n'
    fi
  } > "$1/CLAUDE.md"
}

case "$cmd" in
init)
  check_branch
  dir="$(mktemp -d)/shop"
  mkdir -p "$dir"/{docs/agents,docs/wiki,src/orders,src/payments}
  cd "$dir"
  git init -q -b main
  printf '.claude/\n.scratch/\nnode_modules/\n' > .gitignore
  cat > package.json <<'EOF'
{
  "name": "shop",
  "private": true,
  "type": "module",
  "scripts": { "test": "node --test" }
}
EOF
  claude_md "$dir" silent
  cat > GLOSSARY.md <<'EOF'
# Glossary

- **Order** — a customer's request to buy, with an amount and a status.
- **Payment** — money received against one order.
EOF
  cat > docs/agents/domain.md <<'EOF'
# Domain

## Docs Layout

> Read by `refine-docs`, `update-wiki`, `to-plan` and any docs audit. Format spec: the
> `refine-docs` skill's `references/docs-layout.md`.

**Layout:** single-context

### Glossaries

| Scope | File          |
| ----- | ------------- |
| Root  | `GLOSSARY.md` |

### Wiki

| Key           | Value                                         |
| ------------- | --------------------------------------------- |
| Flow pages    | `docs/wiki/*.md`                              |
| Feature index | `docs/wiki/_INDEX.md` → `## Shipped Features` |
| Writer        | `update-wiki`                                 |

### Code units

| Unit   | Where    | Registry      | Documented in | Vocab in      |
| ------ | -------- | ------------- | ------------- | ------------- |
| Module | `src/*/` | `GLOSSARY.md` | `GLOSSARY.md` | `GLOSSARY.md` |
EOF
  cat > docs/agents/verify.md <<'EOF'
# Verify Config — shop

## Gates

| Touched path | Gate       |
| ------------ | ---------- |
| `src/**`     | `node --test` |

## Surfaces

None. No suite drives a browser or an app.
EOF
  cat > src/orders/orders.js <<'EOF'
export function createOrder(id, amount) {
  return { id, amount, status: "pending" };
}

export function orderStatus(order) {
  return order.status;
}

export function markPaid(order) {
  if (order.status !== "pending") throw new Error(`cannot pay a ${order.status} order`);
  order.status = "paid";
}
EOF
  cat > src/orders/orders.test.js <<'EOF'
import { test } from "node:test";
import assert from "node:assert/strict";
import { createOrder, orderStatus } from "./orders.js";

test("a new order is pending", () => {
  assert.equal(orderStatus(createOrder("o1", 100)), "pending");
});
EOF
  cat > src/payments/payments.js <<'EOF'
import { markPaid } from "../orders/orders.js";

export function pay(order, amount) {
  if (amount < order.amount) return { ok: false, reason: "insufficient" };
  markPaid(order);
  return { ok: true };
}
EOF
  cat > src/payments/payments.test.js <<'EOF'
import { test } from "node:test";
import assert from "node:assert/strict";
import { createOrder } from "../orders/orders.js";
import { pay } from "./payments.js";

test("rejects a payment below the order amount", () => {
  assert.deepEqual(pay(createOrder("o1", 100), 50), { ok: false, reason: "insufficient" });
});

test("a successful payment marks the order paid", () => {
  const order = createOrder("o2", 100);
  pay(order, 100);
  assert.equal(order.status, "paid");
});
EOF
  cat > docs/wiki/order-payment.md <<'EOF'
# Order payment

**Last updated:** 2026-11-12

Paying an order, across `src/orders/` and `src/payments/`.

## Flow

1. `pay(order, amount)` rejects an amount below the order amount.
2. Otherwise it calls `markPaid`, and the order goes `pending` → `paid`.

## Business Rules

- A payment below the order amount is rejected. `rejects a payment below the order amount` (`src/payments/payments.test.js`)
- A successful payment marks the order paid. `a successful payment marks the order paid` (`src/payments/payments.test.js`)
- Only a pending order can be paid. (no test)
EOF
  cat > docs/wiki/_INDEX.md <<'EOF'
# Wiki

## Shipped Features

| Feature | Page | Units |
| ------- | ---- | ----- |
| Order payment | [order-payment.md](order-payment.md) | `src/orders/`, `src/payments/` |
EOF
  node --test >/dev/null 2>&1 || { echo "error: test suite fails in $dir" >&2; exit 1; }
  commit "$dir" "feat: orders and payments"
  echo "$dir"
  ;;
install)
  need_dir "${3:-}"; install_skill "${2:?skill name}" "$3"
  ;;
uninstall)
  need_dir "${3:-}"; rm -rf "$3/.claude/skills/${2:?skill name}" && echo "removed ${2}"
  ;;
install-agents)
  need_dir "${2:-}"; check_branch
  mkdir -p "$2/.claude/agents"
  cp "$CATALOG"/plugins/phase-agents/agents/phase-*.md "$2/.claude/agents/"
  ls "$2/.claude/agents"
  ;;
install-suite)
  need_dir "${2:-}"
  suite="${3:-domain-modeling}"; src="$CATALOG/.claude/skills/$suite"
  [[ -f "$src/SKILL.md" ]] || { echo "error: no $suite at $src (run npm run install-suite in the catalog)" >&2; exit 1; }
  mkdir -p "$2/.claude/skills"; rm -rf "$2/.claude/skills/$suite"
  cp -RL "$src" "$2/.claude/skills/$suite" && echo "installed $suite"
  ;;
allow-commit)
  need_dir "${2:-}"; need_clean "$2"
  claude_md "$2" allow; commit "$2" "docs: let the agent commit after the gates pass"
  git -C "$2" log --oneline -1
  ;;
silent-commit)
  need_dir "${2:-}"; need_clean "$2"
  claude_md "$2" silent; commit "$2" "docs: no commit rule"
  git -C "$2" log --oneline -1
  ;;
drop-wiki)
  need_dir "${2:-}"; need_clean "$2"
  python3 - "$2/docs/agents/domain.md" <<'EOF'
import re, sys
p = sys.argv[1]; s = open(p).read()
n = re.sub(r"### Wiki\n.*?(?=### )", "", s, flags=re.S)
assert n != s, "no ### Wiki table found"
open(p, "w").write(n)
EOF
  rm -rf "$2/docs/wiki"
  commit "$2" "docs: drop the wiki"
  git -C "$2" log --oneline -1
  ;;
behaviour-commit)
  need_dir "${2:-}"; need_clean "$2"
  cat >> "$2/src/orders/orders.js" <<'EOF'

export function markRefunded(order) {
  if (order.status !== "paid") throw new Error(`cannot refund a ${order.status} order`);
  order.status = "refunded";
}
EOF
  cat >> "$2/src/payments/payments.js" <<'EOF'

export function refund(order) {
  markRefunded(order);
  return { ok: true };
}
EOF
  sedi 's/^import { markPaid } from/import { markPaid, markRefunded } from/' "$2/src/payments/payments.js"
  sedi 's/^import { pay } from/import { pay, refund } from/' "$2/src/payments/payments.test.js"
  cat >> "$2/src/payments/payments.test.js" <<'EOF'

test("a refund marks a paid order refunded", () => {
  const order = createOrder("o3", 100);
  pay(order, 100);
  refund(order);
  assert.equal(order.status, "refunded");
});
EOF
  (cd "$2" && node --test >/dev/null 2>&1) || { echo "error: test suite fails" >&2; exit 1; }
  commit "$2" "feat(payments): refund a paid order"
  git -C "$2" log --oneline -1
  ;;
workspace)
  need_dir "${2:-}"; need_clean "$2"
  w="$2/.scratch/workspaces/demo"
  p="$w/plans/01-double-pay"
  mkdir -p "$p/phases"
  cat > "$2/.scratch/workspaces/INDEX.md" <<'EOF'
# Workspaces

## Active

| Slug | Goal | Status | Progress | Updated | Waiting on | Areas |
| ---- | ---- | ------ | -------- | ------- | ---------- | ----- |
| demo | Paying an order twice is refused | active | 0% | 2026-11-13 | — | orders, payments |
EOF
  cat > "$w/CONTEXT.md" <<'EOF'
# Double payment — Context

## Goal

Paying an order that is not pending is refused with a reason instead of throwing.

## Keputusan

1. `pay` on an order that is not pending returns `{ ok: false, reason: "not-pending" }` and does not throw. ADR: candidate
2. The wiki page for order payment is updated when the rule ships. ADR: no
EOF
  cat > "$w/TRACKER.md" <<'EOF'
# Double payment — Tracker

## How this tracker works

- Progress % = 0 + the weights of `done` items. Status: `todo` / `in-progress` / `done` / `blocked`.
- Every meaningful action goes to the Action Log with its date, one row, in plain words.

## Work Items

| Reported? | ID | Weight | Status | Item |
| --------- | -- | ------ | ------ | ---- |
| [ ] | W1 | 70 | todo | Paying an order that is not pending is refused with a reason |
| [ ] | W2 | 30 | todo | The order payment wiki page says so |

## Action Log

| Date | Action |
| ---- | ------ |
| 2026-11-13 | Workspace created. |
EOF
  cat > "$w/WHATNEXT.md" <<'EOF'
# Double payment — What next

## State now

The plan is written. Nothing is built.

## Next steps

1. Run the plan: `plans/01-double-pay/IMPLEMENTATION_PLAN.md`.
EOF
  cat > "$p/IMPLEMENTATION_PLAN.md" <<EOF
# Implementation Plan: Refuse a second payment

**Status:** pending
**Repo:** \`$2\`

## Overview

\`pay\` refuses an order that is not pending, with a reason. Phase 2 documents it.

## Phase Index

| #   | Phase              | Weight | File                                   |
| --- | ------------------ | ------ | -------------------------------------- |
| 1   | Refuse a second payment | M | \`phases/phase-01-refuse-second-payment.md\` |
| 2   | Documentation      | M      | \`phases/phase-02-documentation.md\`     |

> Open the file for the phase you're executing. Each phase file is self-contained. Start from
> Phase 1 and work forward.

## Manual Test Checkpoints

1. After Phase 2 — \`docs/wiki/order-payment.md\` lists the new rule.

## Notes

- Applies to: all — Work item for phase 1 is W1, for phase 2 is W2 (TRACKER.md).
EOF
  cat > "$p/phases/phase-01-refuse-second-payment.md" <<EOF
# Phase 1: Refuse a second payment

Weight: M
Depends on: nothing
Repo: \`$2\`

## Checklist

- [ ] **Refuse paying an order that is not pending** (M)
  - What: In \`pay\`, when the order status is not \`pending\`, return \`{ ok: false, reason: "not-pending" }\` before calling \`markPaid\`; do not throw. Add a test \`paying a paid order is refused\` in \`src/payments/payments.test.js\`. Realises decision 1.
  - Files: \`src/payments/payments.js\`, \`src/payments/payments.test.js\`

Suggested commit: feat(payments): refuse paying an order that is not pending
EOF
  cat > "$p/phases/phase-02-documentation.md" <<EOF
# Phase 2: Documentation

Weight: M
Depends on: Phase 1
Repo: \`$2\`

## Context

Write only what the code holds after phase 1. Never name the plan, the workspace or its folders.
Range: the commit of phase 1.
Review check: every claim in the changed docs matches the code: file paths, identifiers, test names.

## Checklist

- [ ] **Document the refused second payment in the wiki** (M)
  - [ ] \`docs/wiki/order-payment.md\` — Flow and Business Rules: a payment on an order that is not pending is refused with reason \`not-pending\` (locked by \`paying a paid order is refused\`)
  - [ ] \`docs/wiki/_INDEX.md\` — keep the row for order payment
  - Provenance: \`grep -n 'pending' docs/wiki/*.md\`
  - Skill: \`update-wiki\`

Suggested commit: docs(wiki): document the refused second payment
EOF
  git -C "$2" status --short
  echo "workspace written under $w (git-ignored); tree stays clean"
  ;;
prd)
  need_dir "${2:-}"
  mkdir -p "$2/.scratch/workspaces/double-pay"
  cat > "$2/.scratch/workspaces/double-pay/PRD.md" <<'EOF'
# Refuse a second payment

## Problem

Paying an order that is already paid throws an error (`cannot pay a paid order`). The caller gets an exception instead of an answer.

## What I want

`pay` on an order that is not pending returns `{ ok: false, reason: "not-pending" }` and does not throw.

## Known

- `markPaid` in `src/orders/orders.js` throws for an order that is not pending.
- The wiki page for order payment lists the rules.

## Open

- Should `markPaid` keep throwing when it is called directly? I think yes.

## Out of scope

Refunds.
EOF
  echo "PRD written under $2/.scratch/workspaces/double-pay/ (git-ignored); tree stays clean"
  ;;
root-line)
  need_dir "${2:-}"
  printf '\nWorkspace root: `.scratch/workspaces/`\n' >> "$2/CLAUDE.md"
  if [[ "${3:-}" == "other" ]]; then
    printf '\nRun npm test before every push.\n' >> "$2/CLAUDE.md"
  fi
  git -C "$2" status --short
  ;;
finish-workspace)
  need_dir "${2:-}"; need_clean "$2"
  w="$2/.scratch/workspaces/demo"
  [[ -f "$w/CONTEXT.md" ]] || { echo "error: no demo workspace in $2 (run workspace first)" >&2; exit 1; }
  cat > "$w/TRACKER.md" <<'EOF'
# Double payment — Tracker

## Report rules

- **Audience:** none
- **Language:** English

## Work Items

| Reported? | ID | Weight | Status | Item |
| --------- | -- | ------ | ------ | ---- |
| [ ] | W1 | 70 | done | Paying an order that is not pending is refused with a reason |
| [ ] | W2 | 30 | done | The order payment wiki page says so |

## Action Log

| Date | Action |
| ---- | ------ |
| 2026-11-13 | Workspace created. |
EOF
  sedi 's/^\*\*Status:\*\* .*/**Status:** done/' "$w/plans/01-double-pay/IMPLEMENTATION_PLAN.md"
  cat > "$w/WHATNEXT.md" <<'EOF'
# Double payment — What next

## State now

The plan is done. Both work items are done.

## Next steps

1. Wrap up the workspace: `/wrap-up demo`.
EOF
  cat > "$2/src/payments/payments.js" <<'EOF'
import { markPaid } from "../orders/orders.js";

export function pay(order, amount) {
  if (order.status !== "pending") return { ok: false, reason: "not-pending" };
  if (amount < order.amount) return { ok: false, reason: "insufficient" };
  markPaid(order);
  return { ok: true };
}
EOF
  cat >> "$2/src/payments/payments.test.js" <<'EOF'

test("paying a paid order is refused", () => {
  const order = createOrder("o4", 100);
  pay(order, 100);
  assert.deepEqual(pay(order, 100), { ok: false, reason: "not-pending" });
});
EOF
  (cd "$2" && node --test >/dev/null 2>&1) || { echo "error: test suite fails" >&2; exit 1; }
  commit "$2" "feat(payments): refuse paying an order that is not pending"
  git -C "$2" log --oneline -1
  git -C "$2" status --short
  echo "demo workspace finished; tree clean"
  ;;
feature-branch)
  need_dir "${2:-}"; need_clean "$2"
  name="${3:?branch name}"
  git -C "$2" checkout -q main
  git -C "$2" checkout -q -b "$name"
  printf '\nNote: payments are refused for non-pending orders.\n' >> "$2/docs/wiki/order-payment.md"
  commit "$2" "docs(wiki): add a note on $name"
  if [[ "${4:-}" == "merged" ]]; then
    git -C "$2" checkout -q main
    git -C "$2" -c user.name="Test User" -c user.email="test@example.invalid" merge -q --no-ff -m "Merge $name" "$name"
    git -C "$2" checkout -q "$name"
  fi
  git -C "$2" branch --show-current
  git -C "$2" log --oneline --graph --all
  ;;
notes-repo)
  need_dir "${2:-}"
  [[ -d "$2/.scratch" ]] || { echo "error: no .scratch/ in $2 — run workspace or prd first" >&2; exit 1; }
  git -C "$2/.scratch" init -q -b main
  commit "$2/.scratch" "docs: notes"
  if [[ "${3:-}" == "rule" ]]; then
    cat > "$2/CLAUDE.local.md" <<'EOF'
## Workspace notes

`.scratch/` is its own git repository. After you create or change files under `.scratch/workspaces/`, commit them there: `git -C .scratch add <explicit paths>`, then `git -C .scratch commit -m "docs: <summary>"`. Never stage `.scratch/` from the main repo, and leave out changes you did not make.
EOF
    grep -qxF 'CLAUDE.local.md' "$2/.git/info/exclude" || echo 'CLAUDE.local.md' >> "$2/.git/info/exclude"
    rule=yes
  else
    rule=no
  fi
  echo "notes repo: $2/.scratch (rule: $rule)"
  ;;
status)
  need_dir "${2:-}"
  git -C "$2" log --oneline; echo "--- status"; git -C "$2" status --short
  echo "--- skills"; ls "$2/.claude/skills" 2>/dev/null || true
  echo "--- agents"; ls "$2/.claude/agents" 2>/dev/null || true
  if [[ -d "$2/.scratch/.git" ]]; then echo "--- notes repo"; git -C "$2/.scratch" log --oneline | wc -l; fi
  ;;
*)
  sed -n '2,22p' "$0"; exit 1
  ;;
esac
