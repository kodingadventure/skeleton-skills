# Documentation and wrap-up

This page answers one question: which documents outlive a feature, who keeps them current, and what `wrap-up` adds on top.

## Two kinds of documents

Workspace documents (`CONTEXT.md`, `TRACKER.md`, `WHATNEXT.md`, findings, handoffs) are temporary. The workspace folder is git-ignored and you delete it when the feature ships.

Four kinds of documents are permanent. They live in your repository and are committed with the code:

| Document            | What it holds                                                                                       | Updated by                                                                              | When                                         |
| ------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------- |
| Wiki                | Flow pages that cross several modules (business rules, status changes, routes, screens), a feature index, and optionally a page of old behaviour kept on purpose | `update-wiki`                                                                           | After a commit that changes behaviour        |
| Glossary            | Vocabulary only: a term and its meaning. One `GLOSSARY.md` for a small repo, one per code unit in a larger one           | `refine-docs`; a term born in a plan phase is added when that phase is reviewed         | When a new term appears                      |
| Reference docs      | Architecture and patterns: how the code is laid out and why                                         | `refine-docs`                                                                           | When a pattern changes                       |
| ADR                 | One important decision per file: what was decided, the alternatives, and why they lost              | `domain-modeling`, called by `execute-plan`, `review-phase`, `guard-plan`, `refine-docs` or `wrap-up`  | When the code that embodies the decision lands |

The map of where each document lives is the Docs Layout in your repo's `docs/agents/domain.md`. `refine-docs` writes it, and both documentation skills read their paths from it.

## Who reads them

Mostly the agent, and it searches them instead of reading them whole. In one large private project, the wiki and glossaries were searched in about 3 of every 10 sessions, but almost never read in full.

These numbers come from one large private project, about 170 sessions over three weeks, with nothing to compare against. They are observations, not benchmark results.

So documents work as an index. A tidy layout (a doc map, one glossary per module, one wiki page per flow) is what makes a search cheap and its answer easy to trust.

## Why accuracy matters

An agent believes what it reads. That gives three cases:

1. **No document.** The agent reads the code. It is slower, but the result is right.
2. **A wrong document.** The agent is sure of a rule that is false. The plan is built on that rule, the code is written to match the document, and the result is wrong in a tidy way. This is the most expensive case, because it shows up late.
3. **A correct document.** The search lands on the right rule and the right file. The plan is right from the start and there are fewer fix-up rounds.

For people the gain is different:

- An ADR answers "why did we choose this?" months later, without asking anyone.
- A glossary makes the word you type and the word the agent understands mean the same thing.
- A wiki explains how the product behaves without reading code. New team members and testers use it.

## How the documents follow the work

You do not have to remember to write them. Four parts of the workflow do it:

- **ADRs** are written by the phase whose code embodies the decision. A decision tagged `ADR: candidate` in the workspace becomes an ADR when that phase is reviewed.
- **A docs phase** ends a feature plan that changes behaviour. It has one item per installed documentation skill and is reviewed and committed like the code. Reviewing the documentation phase caught 2 real errors before they were committed (numbers: see the note under "Who reads them").
- **`whatnext`** suggests the documentation step once, after the last phase of a plan is committed, or right away after a behaviour-changing commit outside a plan. It stays quiet once the docs have been touched.
- **`wrap-up`** sweeps what is left: ADRs not yet written, findings worth keeping, terms not yet in a glossary.

Details are in the "Keeping the docs current" section of [`skills/workflow/README.md`](../../skills/workflow/README.md).

## What this does not promise

It does not promise documents that are "always in sync". That holds only while the documentation skills are installed and the change goes through a plan. A change made by hand, outside a plan, is not documented until someone runs `update-wiki` or `refine-docs`.

It does not promise token savings from documentation either. Small sessions come from the workspace flow and the phase files: a phase file already carries the rules, the code locations and the tests, so the agent opens few files. Half of the working sessions read 8 files or fewer (numbers: see the note under "Who reads them"). Documentation adds accuracy and tidiness, not speed.

## Why wrap-up matters

The workspace folder is ignored by git and then deleted. Whatever exists only in it is lost.

Here is the pattern. An expensive finding came out of a workspace: the first version of a skill depended on one kind of test, and it failed in projects that do not have that kind of test. The finding sat only in the workspace folder until `wrap-up` moved it into a repo document. Without that step, the next feature would have paid for the same discovery again.

`/wrap-up <slug>` does this, in order:

1. Starts from the updated default branch. If the pull request is still open, it stops and tells you to merge first. In a repo with no remote it says so, skips the pull, and checks locally that your branch is merged.
2. Checks that every work item is `done`, or that you chose to continue anyway.
3. Writes the ADRs still owed, from the decisions tagged `ADR: candidate`.
4. Moves new vocabulary into the glossary and checks that what shipped is documented.
5. Sorts `findings/`: each file is either `repo: <path>` (moved into the repo) or `scope: workspace` (goes away with the folder).
6. Commits the repo side, including a `Workspace root:` or `Plan root:` line a skill left uncommitted, and never anything inside the workspace folder.
7. Writes the final report, when the workspace has a report audience.
8. Moves the workspace to `## Shipped` in `INDEX.md`, with where the knowledge landed, and tells you the exact folder to delete. It does not delete it.

Do not wait for `wrap-up` to write documentation. Workspaces often stay open for weeks while a release is pending, and a wiki written only at the end falls that far behind.

Next: [Model and effort](./model-and-effort.md)
