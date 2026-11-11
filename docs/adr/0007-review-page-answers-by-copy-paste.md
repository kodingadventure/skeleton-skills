# `review-page` answers come back by copy and paste

Status: accepted

## Context

`review-page` shows a page for the user to decide on. The user's answers must get back to the agent. A path without copy and paste was considered, as other review tools do it with a local server or a feedback channel.

## Decision

Answers come back by copy and paste: the page builds the answer text and the user pastes it into the conversation. There is no server and no other return path. The Explain button on each item works the same way: it copies a prompt about the item or one option, the agent answers in the conversation only, and the page is not changed, so an option the user has not copied yet is never lost on reload. Choices are not saved in the browser, and the prompt preview is hidden.

## Considered options

- An answer server or a feedback endpoint that the page posts to: rejected. It adds a process to run and secure, and it moves control from the user to a background channel.
- Saving choices in browser storage: rejected. State then lives in two places and can disagree with the conversation.
- The agent rewriting the page to answer an Explain request: rejected. It discards unsent choices.

## Consequences

- Do not add a server, a listener or a write-back path to `review-page`, and do not make Explain edit the page.
- A richer return path, if ever wanted, is a separate tool's job and needs a new ADR.
