---
name: update-wiki
argument-hint: "Optional: a code unit, a flow page, or a commit range (e.g. 'orders', 'checkout', 'HEAD~3..HEAD'). If omitted, asks which commits to document."
description: >
  Updates the repo's wiki from committed changes: flow pages that cross code units, the feature
  index, and a page of deliberately kept wrong behaviour when the repo has one. Reads every path
  from the Wiki table in the Docs Layout of docs/agents/domain.md. Use when the user asks to
  update the wiki or the docs after a change, to document a feature, fix or flow, or when a
  commit that landed changed a business rule, a status transition, a route or a screen.
  Not for architecture docs, glossaries or ADRs (use refine-docs), or for changing code.
---

# Update Wiki

> **Role**: Wiki writer. Brings the wiki in line with a change that is already committed. The
> code is the source of truth: every sentence is checked against the code before it is saved.
> Scope is the files the `### Wiki` table names. Code, tests, glossaries, reference docs and
> ADRs stay as they are; a bug found while reading goes into the final summary.

**This skill hardcodes no paths.** Every path comes from the `### Wiki` table in the repo's
`## Docs Layout` (full spec: the `refine-docs` skill's `references/docs-layout.md`). It is the
only writer of those files; `refine-docs` routes flow content here and never edits them.

## Step 0: Load the layout

Read `docs/agents/domain.md` and find its `## Docs Layout` block.

- **File missing** -> stop before changing anything, with one message: `docs/agents/domain.md`
  is created by the `setup-matt-pocock-skills` skill from `mattpocock/skills`, which is not
  installed or not set up here; see this repo's README for the pinned install command. Do not
  create the file yourself.
- **File present, no `### Wiki` table** -> draft one and show it. Default values: flow pages
  `docs/wiki/*.md`; feature index `docs/wiki/_INDEX.md` -> `## Shipped Features`; `Writer`
  `update-wiki`. Add a `Preserved behaviour` row only when the user asks for one. Write it into
  `## Docs Layout` only after the user agrees, in the format of the `refine-docs` spec. No
  agreement -> stop without writing anything.
- **Table present** -> it is the truth. Write only to the files it names.

Done when the Flow pages and Feature index values are known.

## Step 1: Find the change

- **From a plan item**: the item's `What:` and sub-bullets give the range and the pages; do not ask.
- **Commit range given**: `git log --oneline <range>` and `git diff --stat <range>`.
- **Unit or page given**: `git log --oneline -15 -- <the Where glob of that unit>`, then ask the
  user which commits belong to the change.
- **Nothing given**: show `git log --oneline -10` and ask which commits to document.

Read the diff of every changed file. Skip generated files (`linguist-generated` in
`.gitattributes`, or a "generated" header) and mark documents "no behaviour change". Write each
**behaviour change** in one line: what a user, a caller or another system can now do or sees
differently, and the file that does it.

Done when every changed file is explained by a behaviour change or marked "no behaviour change".

## Step 2: Read the sources, in three layers

1. **Required: the diff and the code.** They are the truth; each sentence is checked against the
   code before it is saved.
2. **Evidence: the tests the repo has.** Read which kinds exist from `docs/agents/verify.md`
   (`## Gates` and `## Surfaces`). End each rule with the test that locks it (test name and file)
   or `(no test)`.
3. **Bonus: user-flow tests.** If `## Surfaces` names a suite that drives a browser or an app,
   it gives the steps from the user's side, and screenshots when the suite produces them.

No `verify.md` -> look for test files next to the changed code and say so in the summary. No
user-flow tests -> write the wiki from layers 1 and 2.

## Step 3: Assign each behaviour change

| The change                                                                                               | Document to edit                                                                                    |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| A rule or status that involves more than one code unit                                                   | every flow page that already covers it: `grep -ln '<route or status>'` in the flow pages folder     |
| A new flow across units that no page covers                                                              | new flow page ([references/flow-page.md](references/flow-page.md)) and one row in the feature index |
| An entry of the preserved-behaviour page was fixed                                                       | delete the entry and every reference to its id, lower the count, set the checked date to today      |
| Wrong behaviour kept on purpose ([references/preserved-behaviour.md](references/preserved-behaviour.md)) | new entry with the next unused id; only when the table has a `Preserved behaviour` row              |

Not written here: a rule or term inside one code unit, an architecture pattern, an operational
document. List them for `/refine-docs <range>`. A decision that is expensive to reverse becomes
an ADR through `refine-docs` or `domain-modeling`.

Done when every behaviour change has a document, or the reason it needs none.

## Step 4: Edit

- Read the whole target document before editing it; its text is the shape and the vocabulary to
  follow.
- Write each rule with its mechanism: which check, where, producing what.
- Set `**Last updated:**` on every flow page you change.
- Write only to files the `### Wiki` table names.

## Step 5: Verify

- Find every code name you wrote (function, type, enum value, test, path) with `grep -rn`.
- Check that every relative link in the changed files points to a file that exists.
- If `verify.md` has a command that runs a single test, run each test you named for a new or
  changed rule. Otherwise say those tests were not run.

## Step 6: Summarise and commit

Report one line each: the files changed; the suggested commit message
(`docs(wiki): <what changed>`); behaviour changes that needed no document, with the reason; items
for `/refine-docs`; code that does not match its tests or its earlier documentation.

Commit under the repo's `CLAUDE.md` / `AGENTS.md`. If they let the agent commit verified changes, commit only the files this run changed, with explicit pathspecs and the suggested message. If they ask for confirmation, ask first. If they are silent or leave commits to the user, print the `git commit` command and stop.

Exception: when this run is a plan item (a phase's `Skill:` line, under `execute-plan`, `guard-plan` or a phase agent), do not commit and do not print a commit command. Hand the changes to the plan runner, which checks and commits the phase as one commit.

The summary and the commit belong to the reply that closes the run only.
