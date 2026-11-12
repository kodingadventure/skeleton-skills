# `update-wiki` reads the code first and treats tests as evidence

Status: accepted

## Context

`update-wiki` writes the wiki: flow pages across code units, the feature index and, where kept,
a page of behaviour left wrong on purpose. An early version of this skill in the owner's own
project built the wiki from end-to-end tests. It failed in a project without that suite and had
to be rewritten.

## Decision

`update-wiki` reads three layers of source, in this order:

1. **Required: the diff and the code.** They are the truth. Every sentence is checked against the
   code before it is saved.
2. **Evidence: the repo's tests.** Each rule ends with the test that locks it (name and file) or
   `(no test)`.
3. **Bonus: user-flow tests.** A suite that drives a browser or an app adds the steps from the
   user's side, and screenshots when it produces them.

The kinds of test a repo has are read from `docs/agents/verify.md`. The skill names no test
framework or runner.

## Considered options

- Build the wiki from end-to-end tests: rejected. The version that did this failed in a project
  without that suite and had to be written again.

## Consequences

- Do not make `update-wiki` depend on one kind of test, or name a tool in its text.
- A repo without user-flow tests still gets a wiki, written from the code and its other tests.
