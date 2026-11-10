---
name: refine-docs
description: >
  WRITE mode — update architecture and context documentation as patterns evolve. Edits the
  repo's reference docs, keeps glossaries vocabulary-only, adds ADRs, and maintains the repo's
  Docs Layout config. Language- and framework-agnostic — reads the repo's layout from
  docs/agents/domain.md. Use when the user asks to update documentation, fix doc gaps, add
  architectural patterns, record design decisions, sync glossary vocabulary, or create ADRs
  after a gap list exists. Do not use for read-only audits or editing generated code files.
---

# Refine Docs Skill

> **Role**: File editor. This skill modifies documentation — it writes, restructures, and creates files.
> Start from a gap list — from the user, from a review, or from a docs-audit skill if the repo has one — then run this skill to fix the gaps.

Maintain documentation as architecture evolves. Keeps **reference docs** as the source of truth
and **glossaries** (`GLOSSARY.md`) as vocabulary-only layers.

**This skill hardcodes no paths.** Every path comes from the repo's `## Docs Layout` block.
That's what lets it maintain a Go monorepo's docs and a Rust workspace's docs with the same
workflows. Never write to a path you remember from another repo.

## Step 0: Load the layout

Read `docs/agents/domain.md` and find its `## Docs Layout` block — it names this repo's
glossaries, reference docs, topic guides, code units, deep-context tier, ADR location, and
preferred terms. Full spec: `references/docs-layout.md`.

**Route content by doc kind before writing anything.** Reference docs hold architecture
patterns only. If the layout has a **Topic guides** table and a guide owns the subject
(auth, i18n, testing, a tool, a feature walkthrough), edit that guide and cross-link — never
grow the reference doc with a second copy. Operational content (commands, verification steps,
tool config, feature inventories) never belongs in a reference doc, even when no guide exists
yet; propose a new topic guide instead.

- **Block present** → it's the truth. Write only to files it names.
- **Block absent** → infer the layout (see `references/docs-layout.md`), and **offer to write the block** (Workflow 0) before doing anything else. An inferred layout re-derived every run is where drift comes from.
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

The verify step is handled by `execute-plan` — no need to run checks yourself.

## Doc structure

Read from the layout block, not from memory. The general shape it describes:

```
<reference docs>     # Source of truth: architecture patterns, diagrams, flows, examples
<topic guides>       # Optional: single-subject docs (auth, i18n, testing, tools) owning their topic
<glossaries>         # Vocabulary ONLY + links out to reference docs / topic guides
<deep-context tier>  # Optional: per-unit business vocab + file map
<ADR location>       # One file per hard-to-reverse decision
```

A single-context repo collapses this to a root `GLOSSARY.md` + `docs/adr/`, with no reference
docs at all. That's the Matt Pocock default and a perfectly valid target — most workflows below
then reduce to glossary and ADR upkeep.

## Workflows

### Workflow 0: Write or refresh the Docs Layout block

Run when `docs/agents/domain.md` has no `## Docs Layout` block, or when a docs audit reported
layout drift (a block path that doesn't exist on disk).

1. **Explore** — infer glossaries, reference docs, code units, and ADR location per `references/docs-layout.md`
2. **Show the user the draft block** and let them correct it — you're inferring intent from file layout, and a wrong glob silently misdirects every future audit
3. **Write** it into `docs/agents/domain.md` using the template in `references/docs-layout.md`
4. **Emit only tables the repo actually has** — an empty Reference docs table invites inventing files

Never put this config in a `GLOSSARY.md`: glossaries are vocabulary only. And never edit
`setup-matt-pocock-skills` or `domain-modeling` to accommodate the block — it's additive, they ignore it.

### Workflow 1: Add new architectural pattern

1. **Identify scope** — which Code units row or reference-doc scope does this belong to?
   First check the layout's Topic guides table: if a guide owns the subject, this is
   Workflow 1 against that guide, not the reference doc.
2. **Update the reference doc** for that scope, with examples
3. **Extract vocabulary** — pull 1–2 key terms from the new pattern
4. **Update the glossary** named by that scope
   - Add the term, terse, one line
   - Add a link out to the reference doc section
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
4. **Add a section reference** out to the reference doc
5. **Check for removed terms** — drop vocabulary for deprecated patterns
6. **Never copy**: diagrams, code samples, data flows, prose explanations

### Workflow 4: Document a design decision (ADR)

1. **Check the ADR bar first** — `domain-modeling` sets it: hard to reverse, surprising without context, and the result of a real trade-off. If any of the three is missing, skip the ADR.
2. **Create the file** at the layout's ADR **Location**, using the next sequence number
3. **Use the layout's ADR Format** — if it names one (e.g. `domain-modeling/ADR-FORMAT.md`), that file wins over any shape below. Otherwise:

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

Read-only auditing is out of scope here. After editing, re-check the original gap list (or re-run the repo's docs audit, if any) to confirm the gaps are closed.

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

**Glossary = vocabulary indexing layer**

- Just the terms agents read to understand the domain language
- Terse definitions, 1–2 lines per term
- Always link out for detail; no code samples, diagrams, or flows
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

Paths below are from one repo's block — illustrative only.

### Example 1: Add a new backend pattern (rate-limiting middleware)

1. **Reference doc** (`docs/ARCHITECTURE-BACKEND.md`) → add to "Key Patterns":

   ```
   ### Rate Limiting Middleware

   Middleware that tracks and limits request rates per API key. Configured via `internal/config/`.
   ```

2. **Backend glossary** (`docs/GLOSSARY.md`) → add the term:

   ```
   **Rate Limiting Middleware** = tracks and limits request rates per key
   ```

3. Root glossary already defines `Middleware` generically → no change

### Example 2: Refactor code generation

Change how RTK code generation works:

1. **Reference doc** → update the "Code Generation Pipeline" section with the new diagram + steps
2. **Glossary** → term unchanged (`**Code Generation** = Swagger tags → DTOs → RTK hooks; never edit generated files`)

No glossary change needed, because the vocabulary didn't shift. Only edit a glossary when the
_language_ changes, not when the mechanism does.

### Example 3: Single-context repo, no reference docs

A Rust workspace whose block lists a root `GLOSSARY.md` and `docs/adr/`, no reference docs:

1. New pattern → **no reference doc exists to update**. Don't create one as a side effect
2. Add the term to `GLOSSARY.md` with a pointer to the code that implements it
3. If the pattern clears the ADR bar → write `docs/adr/0004-....md`
4. If reference docs would genuinely help, propose that to the user as its own decision

## Checklist

### Full session (manual invocation)

- [ ] Read the `## Docs Layout` block (or inferred it and offered Workflow 0)
- [ ] Identified the scope the change belongs to
- [ ] Updated the reference doc(s) the layout names for that scope
- [ ] Extracted vocabulary and updated the matching glossary if concepts changed
- [ ] Verified no code/flows/diagrams leaked into a glossary
- [ ] Left other-skill-owned glossary sections untouched
- [ ] Added/updated cross-links
- [ ] Created an ADR only if it clears the three-part bar
- [ ] Ran a link audit (all refs resolve)
- [ ] Checked cross-glossary consistency

### Plan-driven (via execute-plan)

- [ ] Read the layout block
- [ ] Read target file(s) listed in `Files:`
- [ ] Made the specific edit from `What:`
- [ ] Checked neighboring sections for orphaned references
- [ ] Updated cross-links if a section anchor was added or renamed

## Related Skills

- **domain-modeling** — Owns glossary and ADR _content_ conventions; this skill maintains the doc _structure_ around them
