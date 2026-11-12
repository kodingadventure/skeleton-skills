# The wiki layer is three parts with one writer

Status: accepted

## Context

The catalog maintains architecture docs, ADRs and glossaries, but has no place for what the
system does end to end across code units, and it never suggests updating the docs after a commit.

## Decision

The wiki layer has three parts:

1. `refine-docs` only extends the doc map with a `### Wiki` table and respects it. It does not
   write wiki pages.
2. `update-wiki` is the only writer of wiki pages. It is optional and carries no
   project-specific paths.
3. `whatnext` suggests `update-wiki` when installed, `refine-docs` when not, and a step in plain
   words when neither can be used.

Anyone using the wiki needs `docs/agents/domain.md` from `mattpocock/skills`.

## Considered options

- `refine-docs` writes the wiki pages itself: rejected. One skill writing architecture,
  glossaries and cross-unit flows becomes too broad, and small projects pay for it.
- Copy a project's own `update-wiki` as it is: rejected. Its paths and layout are specific to
  one project.

## Consequences

- Do not let `refine-docs` or any other skill edit files listed in the `### Wiki` table.
- A repo without that table has no wiki and must not get one silently.
- Changing who owns the wiki pages needs a new ADR.

Related: ADR 0009, `skills/workflow/refine-docs/references/docs-layout.md`.
