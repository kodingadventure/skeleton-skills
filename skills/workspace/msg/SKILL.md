---
name: msg
description: Run only when the user asks for it by name. Draft a chat message (Discord, Slack, …) to a teammate about workspace work — ask a question file, give a short update, or follow up — in the recipient's language and tone from TEAM.md. Also marks a message as sent when the user says "sent" or "udah dikirim".
argument-hint: "[<who>] <question file | workspace file | topic> | sent"
disable-model-invocation: true
model: haiku
---

# Msg

Drafts one chat message the user copies into the team chat (Discord, Slack, …; the person's Channel in TEAM.md). The user sends it; this skill never sends anything.

## Inputs

- **TEAM.md**: `TEAM.md` in the folder that holds the workspace root's `INDEX.md`. Keep it git-ignored; it holds names and contacts. Missing → create it with the first person you are asked to write to. One `## <Name>` section per person with fields such as Role, Language, Tone, Technical detail, Channel, Example messages. Fields the entry has win over the defaults below.
- **Source**: a path (usually `.scratch/workspaces/<slug>/questions/<file>.md`; also WHATNEXT, TRACKER, a finding) or a free-text topic.
- **Who**: optional. When omitted, take it from the source's `For:` line. Neither given → ask.

## Steps

1. Read the person's section in TEAM.md. Not there → ask the user for role, language, tone, then add a section in the same shape before drafting.
2. Read the source. For a question file, use `## Question`, `## Context`, `## Options` (with the recommendation), any partial `## Answer`, and `## Consequences` → Follow-up. Read files it points to only if the message needs a fact from them.
3. Pick the kind:
   - **ask**: the question is open and has no `Asked:` line.
   - **follow-up**: it has an `Asked:` line — remind briefly, mention when it was asked, restate only what is still unanswered.
   - **update**: the source is progress, not a question. A question file whose follow-up says to tell the person something first → combine update + ask in one message.
4. Write the message:
   - In the person's **Language**, in their **Tone**. If TEAM.md has example messages, imitate their greeting, length and phrasing.
   - Only the context this person needs to answer. For non-technical people: no file paths, work-item IDs (L5, Q1), library internals or jargon — say the impact (blocked, cost, date). Technical teammates may get paths and details.
   - Questions numbered, each answerable on its own. With options, list them short and say which one the user recommends and why.
   - Give the time reason when there is one (a deadline, an expiring trial, what is blocked).
   - Chat-friendly: short paragraphs, plain lists, no tables or headings, under the channel's message limit (Discord: 2000 characters; aim for well under).
   - Never invent facts, dates or commitments not in the sources.
5. Show the message in one fenced code block, then one line: who it is for, the kind, and the source. Stop and wait — the user may ask for edits.

## `sent`

When the user says the message was sent (`/msg sent`, "sent", "udah dikirim"): if the source was a question file, add or update the line under `Raised:` as `Asked: YYYY-MM-DD via <channel>` (append `, follow-up YYYY-MM-DD` for later follow-ups). Nothing else changes — the answer is recorded later with `/tracker answer`.
