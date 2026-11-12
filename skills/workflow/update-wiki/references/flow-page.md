# Wiki flow page

One page per flow that passes through more than one code unit. A unit's glossary answers "what
does this unit do"; a flow page answers "what happens from start to end, which status changes
into which, and which unit changes it". Readers: a developer fixing a bug in the middle of the
flow, and the writer of the user manual.

Existing pages in the flow pages folder are the examples; follow their wording. Sections in this
fixed order, 80-160 lines in total:

```markdown
# <Flow name>

> <One sentence: what a user can do through this flow.>

**Status:** Shipped
**Last updated:** <YYYY-MM-DD>

---

## Overview

<2-4 sentences from the user's side. Name every code unit involved, each linked to its document
or glossary from the Docs Layout.>

## Actors

| Actor | What they can do in this flow |
| ----- | ----------------------------- |

## Status Flow

| From | Action (who, route or trigger) | To  | Side effects |
| ---- | ------------------------------ | --- | ------------ |

<One row per status change of the main entity. Side effects = notifications, status of other
entities that change with it, e-mails. Only changes that exist in the code.>

## User Flows

<3-6 subsections, one per main path of a user. Numbered steps; screen and button names exactly
as in the app. When a user-flow test proves the path, put its id in the heading.>

## Interface Reference

| Interface | Name | Access | Description |
| --------- | ---- | ------ | ----------- |

<The routes, commands or events this flow uses, with who may call them. Only those this flow
uses.>

## Business Rules

<Rules that involve more than one unit or more than one entity, at most 25. One bullet per rule,
with its mechanism, ending with the test that locks it or "(no test)". Rules of a single unit
stay in that unit's glossary.>

## Preserved behaviour

<Only the ids that touch this flow, each linked to the preserved-behaviour page; their content
is not repeated. Delete this section when the repo has no such page.>

## Out of Scope

<What this flow does not do although readers often expect it. Only what the code proves.
"None." is allowed.>

## Test Coverage

| Layer | File | What it locks |
| ----- | ---- | ------------- |

<One row per test layer listed in `docs/agents/verify.md`, per unit involved.>
```

## Register the page in the feature index

Every new page gets one row in the feature index (the file and heading named by the Wiki table):

```markdown
| Feature | Description | Shipped |
| ------- | ----------- | ------- |
```

Shipped = the date the change was released, or the commit date when that is not known yet.

When the index file does not exist yet, create it in this shape: a title, one paragraph saying
the pages are updated with `update-wiki`, a `## Reference pages` table (`| Page | Description |`)
for the preserved-behaviour page when the repo keeps one, and the `## Shipped Features` table
above.
