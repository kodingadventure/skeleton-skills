---
name: refine-docs
argument-hint: "Optional: a topic, or a commit range (e.g. 'auth', 'HEAD~3..HEAD'). With neither and a clean tree, asks which recent commits to document."
description: >
  Update architecture reference docs, glossaries and ADRs as patterns evolve. Edits the
  repo's reference docs, keeps glossaries vocabulary-only, adds ADRs, and maintains the repo's
  Docs Layout config. Language- and framework-agnostic — reads the repo's layout from
  docs/agents/domain.md. Use when the user asks to update documentation, fix doc gaps, add
  architectural patterns, record design decisions, sync glossary vocabulary, or create ADRs.
  Also use after a commit that changes a pattern, with the commit range as the argument.
  Not for READMEs, tutorials or API reference, read-only audits, or editing generated code files.
---

# Refine Docs Skill

> **Role**: File editor. This skill modifies documentation — it writes, restructures, and creates files.
> Start from a gap list — from the user, from a docs audit you ran, or from an audit skill if the repo has one — then run this skill to fix the gaps.
> No gap list? Take the light path: read the change from, in order, the commit range given (`git log --oneline <range>`, `git diff <range>`); else the uncommitted changes (`git diff HEAD`); else the topic the user named. If none of the three exists, show `git log --oneline -10` and ask which commits belong to the change. Then list the 3-5 gaps you can see, get the user's approval, then run the matching workflow.

Maintain documentation as architecture evolves. Keeps **reference docs** as the source of truth
and **glossaries** (`GLOSSARY.md`) as vocabulary-only layers.

**This skill hardcodes no paths.** Every path comes from the repo's `## Docs Layout` block.
That's what lets it maintain a monorepo's docs and a single-package library's docs with the same
workflows. Never write to a path you remember from another repo.

## Step 0: Load the layout

Read `docs/agents/domain.md` and find its `## Docs Layout` block. Two cases, kept apart:

- **File missing** → stop before changing anything, with one message: `docs/agents/domain.md` is created by the `setup-matt-pocock-skills` skill from `mattpocock/skills`, which is not installed or not set up here; see this repo's README for the pinned install command. Do not create the file yourself.
- **File present, `## Docs Layout` block missing** → infer the layout and offer to write the block (Workflow 0).

The block names this repo's
glossaries, reference docs, topic guides, code units, deep-context tier, ADR location, and
preferred terms. Full spec: `references/docs-layout.md`.

**Route content by doc kind before writing anything.** Reference docs hold architecture
patterns only. If the layout has a **Topic guides** table and a guide owns the subject
(auth, i18n, testing, a tool, a feature walkthrough), edit that guide and cross-link — never
grow the reference doc with a second copy. Operational content (commands, verification steps,
tool config, feature inventories) never belongs in a reference doc, even when no guide exists
yet; propose a new topic guide instead.

If the layout has a **Wiki** table, flow content (what happens across units end to end, status
changes, the user-facing steps of a feature) belongs in the pages it lists, which only the skill
on its `Writer` row edits. Never edit those files: list the flow gaps for the user and name that
skill (`/update-wiki <range>` if installed).

- **Block present** → it's the truth. Write only to files it names.
- **Block absent** (file present) → infer the layout (see `references/docs-layout.md`), and **offer to write the block** (Workflow 0) before doing anything else. An inferred layout re-derived every run is where drift comes from.
- **Table absent** → that concern doesn't exist here. Don't invent it; a repo with no reference docs shouldn't get its first `ARCHITECTURE.md` as a side effect of a vocabulary fix.

## Plan-driven usage (via execute-plan)

When invoked from a plan item, the scope is **pre-defined** by the item's fields:

| Plan item field      | What it means                                                       |
| -------------------- | ------------------------------------------------------------------- |
| `What:`              | The exact edit to make — no exploration needed                      |
| `Files:`             | Which files to edit                                                 |
| `Skill: refine-docs` | Follow the matching workflow below, but only for the specified file |

**Skip** exploration and the full workflow. Just:

1. Read the layout block (Step 0) — you still need its rules, even when the paths are given
2. Read the target file(s) listed in `Files:`
3. Make the specific edit described in `What:`
4. Read neighboring sections for consistency (don't create orphans)
5. Update cross-links if the edit introduces a new section anchor

The verify step and the commit are the plan runner's (`execute-plan`, `guard-plan`): run no checks and do not commit or print a commit command.

## Doc structure

Read from the layout block, not from memory. The general shape it describes:

```
<reference docs>     # Source of truth: architecture patterns, diagrams, flows, examples
<topic guides>       # Optional: single-subject docs (auth, i18n, testing, tools) owning their topic
<wiki>               # Optional: cross-unit flow pages + feature index, edited only by the Wiki table's Writer
<glossaries>         # Vocabulary ONLY + links out to doc pages (reference docs, topic guides, wiki)
<deep-context tier>  # Optional: per-unit business vocab + file map
<ADR location>       # One file per hard-to-reverse decision
```

A single-context repo collapses this to a root `GLOSSARY.md` + `docs/adr/`, with no reference
docs at all. That's the Matt Pocock default and a perfectly valid target — most workflows below
then reduce to glossary and ADR upkeep.

## Workflows

### Workflow 0: Write or refresh the Docs Layout block

Run when `docs/agents/domain.md` exists but has no `## Docs Layout` block, or when a docs audit reported
layout drift (a block path that doesn't exist on disk).

1. **Explore** — infer glossaries, reference docs, code units, and ADR location per `references/docs-layout.md`
2. **Show the user the draft block** and let them correct it — you're inferring intent from file layout, and a wrong glob silently misdirects every future audit
3. **Write** it into `docs/agents/domain.md` using the template in `references/docs-layout.md`
4. **Emit only tables the repo actually has** — an empty Reference docs table invites inventing files

Never put this config in a `GLOSSARY.md`: glossaries are vocabulary only. And never edit
`setup-matt-pocock-skills` or `domain-modeling` (both from `mattpocock/skills`) to accommodate the block — it's additive, they ignore it.

### Workflow 1: Add new architectural pattern

1. **Identify scope** — which Code units row or reference-doc scope does this belong to?
   First check the layout's Topic guides table: if a guide owns the subject, this is
   Workflow 1 against that guide, not the reference doc.
2. **Update the reference doc** for that scope, with examples
3. **Extract vocabulary** — pull 1–2 key terms from the new pattern
4. **Update the glossary** named by that scope
   - Add the term, terse, one line, saying what it **is**: never what it causes or what rule governs it (see "Glossary entry test" below)
   - Add a link out to the reference doc section; no doc page to link to → no link
   - A unit-specific business term goes in the deep-context glossary **only if that unit already has one** — don't create one to hold a single term
5. **Verify links** — no circular refs; all links resolve to real sections

### Workflow 2: Refactor a reference doc section

1. **Identify what's moving**
2. **Create/extend the destination** with problem statement, detailed patterns, examples, and links
3. **Update the parent** — keep the high-level summary, replace detail with a link
4. **Glossary** — no change needed if the vocabulary didn't shift
5. **Remove redundant content** from the old location
6. **Verify all internal links** point to the new locations

### Workflow 3: Update a glossary after reference-doc changes

**Golden rule**: glossaries are vocabulary + links ONLY. Never copy detailed explanations or flows.

1. **Read** the updated reference doc(s)
2. **Identify new terms** — extract 3–5 key concepts
3. **Update the glossary** the layout names for that scope:
   ```
   **NewTerm** = terse one-line definition
   ```
   Run the "Glossary entry test" below on every entry you write.
4. **Add a section reference** out to the reference doc
5. **Check for removed terms** — drop vocabulary for deprecated patterns
6. **Never copy**: diagrams, code samples, data flows, prose explanations

### Glossary entry test

Before saving a glossary entry, strike every clause that says what happens because of the term: a status it moves something to, a rule it enforces, when it is rejected or allowed, a side effect. Those belong in a reference doc or the wiki, and they are the part that goes stale. Strike any code path too. What is left is the entry.

- Wrong: `**Cancellation** — a customer's request to stop an order, which moves it to cancelled`
- Right: `**Cancellation** — a customer's request to stop an order`

### Workflow 4: Document a design decision (ADR)

1. **Check the ADR bar first** — the `domain-modeling` skill sets it (if it is not installed, stop with the same missing-skill message as Step 0, naming `domain-modeling`, and write no ADR of your own): hard to reverse, surprising without context, and the result of a real trade-off. If any of the three is missing, skip the ADR.
2. **Create the file** at the layout's ADR **Location**, using the next sequence number
3. **Use the layout's ADR Format** — if it names one (e.g. the `domain-modeling` skill's `ADR-FORMAT.md`), that file wins over any shape below. Otherwise:

   ```
   # ADR NNNN: Decision Title

   Date: YYYY-MM-DD
   Status: Accepted | Proposed | Superseded

   ## Context
   Why this decision was needed. What problem were we solving?

   ## Decision
   What we decided and why. Which alternatives were considered?

   ## Consequences
   Positive and negative outcomes.

   ## Related
   Links to reference docs, glossaries, or other ADRs.
   ```

4. **Link it** from the relevant reference doc: `See [ADR NNNN](...) for reasoning.`

### Workflow 5: Audit & validate

Read-only auditing is out of scope here. After editing, re-check the original gap list (or re-run the docs audit) to confirm the gaps are closed.

## Commit

After a manual run, commit under the repo's `CLAUDE.md` / `AGENTS.md`. If they let the agent commit verified changes, commit only the files this run changed, with explicit pathspecs and the message `docs(<scope>): <what changed>`. If they ask for confirmation, ask first. If they are silent or leave commits to the user, print the `git commit` command and stop. A run from a plan item does not commit (see Plan-driven usage). The summary and the commit belong to the reply that closes the run only.

## Key principles

**Reference docs = source of truth for architecture**

- Architecture patterns, diagrams, flows, and data models live there
- When in doubt between reference doc and glossary, add detail to the reference doc
- But a subject owned by a topic guide goes in the guide — a reference doc that accretes
  tool how-tos, command lists, and feature inventories stops being an architecture doc

**Topic guides = single-subject ownership**

- One guide owns one subject end-to-end; the reference doc links to it
- New operational/how-to content with no owning guide → new topic guide, registered in the
  layout's Topic guides table (Workflow 0 keeps that table current)

**Wiki = owned by its Writer**

- Flow pages and the feature index are edited only by the skill on the Wiki table's `Writer` row
- This skill lists flow gaps and hands them over; it never writes those files

**Glossary = vocabulary indexing layer**

- Just the terms agents read to understand the domain language
- Terse definitions, 1–2 lines per term
- Always link out for detail; no code samples, diagrams, or flows
- No behaviour and no code paths: what a term does goes in a reference doc or the wiki, and a file path goes stale. With no doc page to link to, the entry is the definition alone
- Exception: sections the layout marks as owned by another skill

**Deep-context tier = business vocab, not stack vocab**

- Only for units the layout's threshold actually catches (see `references/feature-context-template.md`)
- Never copy one unit's deep-context glossary to bootstrap another — it's specific business vocab, not a template
- Must be registered in its scope glossary's Context Map table, or it's undiscoverable

**DRY docs**

- Don't repeat a pattern across reference docs; cross-reference instead
- One data flow per file, linked from others

**The layout block is the contract**

- Skill logic stays generic; repo specifics live in `docs/agents/domain.md`
- Found something the block doesn't describe? Fix the block (Workflow 0) — don't hardcode it here

## Examples

Paths below are from an invented repo's block — illustrative only.

### Example 1: Add a new pattern (rate-limiting middleware)

1. **Reference doc** (`docs/ARCHITECTURE.md`) → add to "Key Patterns":

   ```
   ### Rate Limiting Middleware

   Middleware that tracks and limits request rates per API key. Configured via the service's settings module.
   ```

2. **Glossary** (`GLOSSARY.md`) → add the term:

   ```
   **Rate Limiting Middleware** = tracks and limits request rates per key
   ```

3. Root glossary already defines `Middleware` generically → no change

### Example 2: Refactor code generation

Change how client code generation works:

1. **Reference doc** → update the "Code Generation Pipeline" section with the new diagram + steps
2. **Glossary** → term unchanged (`**Code Generation** = API spec → typed client`)

No glossary change needed, because the vocabulary didn't shift. Only edit a glossary when the
_language_ changes, not when the mechanism does.

### Example 3: Single-context repo, no reference docs

A single-package library whose block lists a root `GLOSSARY.md` and `docs/adr/`, no reference docs:

1. New pattern → **no reference doc exists to update**. Don't create one as a side effect
2. Add the term to `GLOSSARY.md`: its definition only, with no code path and no behaviour (run the "Glossary entry test")
3. If the pattern clears the ADR bar → write `docs/adr/0004-....md`
4. If reference docs would genuinely help, propose that to the user as its own decision

## Checklist

### Full session (manual invocation)

- [ ] Read the `## Docs Layout` block (or inferred it and offered Workflow 0)
- [ ] Identified the scope the change belongs to
- [ ] Updated the reference doc(s) the layout names for that scope
- [ ] Extracted vocabulary and updated the matching glossary if concepts changed
- [ ] Verified no code, code paths, behaviour, flows or diagrams leaked into a glossary
- [ ] Left other-skill-owned glossary sections untouched
- [ ] Left the Wiki table's files untouched; listed flow gaps for its Writer
- [ ] Added/updated cross-links
- [ ] Created an ADR only if it clears the three-part bar
- [ ] Ran a link audit (all refs resolve)
- [ ] Checked cross-glossary consistency
- [ ] Committed under the repo's rules, or printed the commit command

### Plan-driven (via execute-plan)

- [ ] Read the layout block
- [ ] Read target file(s) listed in `Files:`
- [ ] Made the specific edit from `What:`
- [ ] Checked neighboring sections for orphaned references
- [ ] Updated cross-links if a section anchor was added or renamed

## Related Skills

- **domain-modeling** — Owns glossary and ADR _content_ conventions; this skill maintains the doc _structure_ around them
