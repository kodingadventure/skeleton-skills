# The reader's guide lives in `docs/guide/`, and only that folder becomes the site

Status: accepted

## Context

The repo needs a reading guide for people trying the skills: getting started, which of two similar skills to use, what a workspace holds, model advice, a FAQ. While the repo is private it is read on GitHub; once the repo is public it should become a GitHub Pages site. `docs/` already holds documents written for agents (`docs/agents/`) and the decision records (`docs/adr/`), which are not meant for that audience.

## Decision

The guide is plain Markdown in `docs/guide/`. When the repo goes public, only `docs/guide/` is published to GitHub Pages, through a GitHub Actions workflow. `docs/agents/` and `docs/adr/` stay in the repo and off the site.

## Considered options

- A `guide/` folder at the repo root: rejected. It adds a top-level folder next to `skills/` and `plugins/` for something that is documentation, and splits the docs across two roots.
- Publishing all of `docs/` (GitHub Pages' built-in "/docs" source): rejected. It would put the agent docs and the ADRs on the public site as pages a reader lands on.

## Consequences

- The Pages setup must build from `docs/guide/` alone; the built-in "deploy from a branch, /docs folder" source does not fit and must not be used.
- Pages link to each other with relative links inside `docs/guide/`. A link out to the root `README.md` or another repo file works on GitHub but not on the site; the publish step has to rewrite or replace such links.
