---
name: discuss
description: Open a discussion about a feature workspace's topic — loads CONTEXT.md, WHATNEXT.md and only the files the topic touches, then talks it through and records whatever gets settled. No code changes, no commits.
argument-hint: "<workspace> [topic]"
disable-model-invocation: true
---

# Discuss

Talk about a **workspace** (a feature folder set up by `kickoff`, or seeded by `spin-off` and not kicked off yet; `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root) without starting work on it. `resume-here` takes the next step; this skill thinks about it instead, and makes sure nothing the discussion settles is lost.

## Resolving the workspace

The same order in every workspace skill:

1. the slug or path in the argument;
2. the workspace this conversation has already been working in;
3. `INDEX.md` at the workspace root: the only row under `## Active` (no `INDEX.md` → the only `*/WHATNEXT.md` under the root);
4. still more than one → ask, listing the `## Active` rows.

Never pick between two live workspaces. Before writing anything, name the one you resolved in one line: `Workspace: <slug>`.

## Steps

### 1. Load, narrowly

1. `CONTEXT.md` — the whole file. `## Workspace rules` sets the language for the discussion.
2. `WHATNEXT.md` — the whole file, so the discussion knows where the work stands.
3. **Only what the topic touches.** Grep the topic's words across `## Decisions` and `## Findings` in `CONTEXT.md`, `findings/`, `questions/` and the plans' Phase Index, and open the few files that hit. A plan phase, `TRACKER.md` or a handoff is opened only when the topic is about that phase, the progress numbers, or an interrupted session.

Do not load the workspace wholesale: `TRACKER.md` and the plans are the big files, and a discussion rarely needs them.

No topic in the argument → say what is live (the open questions, the `ADR: candidate` decisions, next step 1, who is being waited on) and ask what to discuss.

Done when: you can state what the workspace already settled about this topic, and what it left open.

### 2. Discuss

In the workspace language. Lead with what the existing decisions and findings already fix, then the part that is genuinely open — a question that is already answered in `CONTEXT.md` gets the answer, not a fresh debate.

- Contradiction between what the user says now and a settled decision or finding → surface it immediately, naming the decision ("decision 9 says the row is deleted on logout; you are describing it staying").
- The topic is a term or a model boundary → bring in the `domain-modeling` skill (from `mattpocock/skills`), if installed.
- The user wants their own thinking stress-tested → `grilling` (if installed).
- The question is empirical and cheap to answer from the repo → read the code and answer it, rather than speculating.

### 3. Record before the end

A discussion that changes nothing on disk is how decisions get lost. Before your closing message, write down whatever the discussion produced, in the workspace's own language and format:

- **Settled something** → a `## Decisions` entry in `CONTEXT.md`, carrying its `ADR:` tag (see `## Conventions` there), plus a Decision row and an Action Log row in `TRACKER.md`, unticked.
- **A question for someone outside the session** → its file in `questions/`, its `TRACKER.md` row and its `CONTEXT.md` index line (format: the files already in `questions/`, else `.claude/skills/kickoff/references/question-template.md`). `/msg <file>` drafts the message.
- **A discovery a later agent must not re-learn** → `findings/YYYY-MM-DD-<topic>.md`, with its one-line entry and `scope:` tag in `CONTEXT.md` `## Findings`.
- **Changed what comes next** → rewrite the affected part of `WHATNEXT.md` (Next steps, Waiting on) and refresh the workspace's `INDEX.md` row.
- **Settled nothing** → say so, and write nothing.

Tick no checkbox: only `/tracker sent` does that. A seeded workspace is recorded in like any other: its `TBD (kickoff)` fields and placeholder work item stay for `kickoff` to replace.

Done when: every outcome of the discussion is in exactly one file, or you have said there was none.

### 4. Boundaries

- No code changes, no staging, no commits. A discussion that turns into work ends here: say so, and hand over to `/to-plan` (new scope), `/resume-here` (the existing next step) or `/execute-plan`.
- Never run git inside the workspace root when it has its own repository.
- Secrets (keys, tokens, passwords, personal data) stay out of every file; refer to where they are kept.

### 5. Close

In the workspace language: what the discussion settled, what it left open, what you wrote where, and the one line to continue with (`/resume-here <slug>` to start working, or `/discuss <slug> <next topic>`).
