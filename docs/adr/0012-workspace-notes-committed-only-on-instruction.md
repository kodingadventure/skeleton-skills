# Workspace skills commit the notes repository only when the repo's instructions say so

Status: accepted

## Context

The workspace root is git-ignored by the main repo (see 0004). Users may give the folder that holds it its own git repository to keep a history of their notes. The workspace skills used to say they never run git there, so a user who wanted their notes committed had to override the skill text with a local instruction, and every skill run left the notes uncommitted.

## Decision

By default the skills still run no git in the notes repository. When the repo's instructions (`CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`) say to commit the workspace notes, a skill that writes notes (`kickoff`, `discuss`, `pause-here`, `spin-off`, `wrap-up`) commits in that repository only the files its run wrote, with explicit paths, and names the commit in its report. The rule is one sentence, pasted word for word into the step that writes notes in each skill and into the `CONTEXT.md` template. They never stage anything under the workspace root from the main repo.

## Considered options

- **Commit whenever the root has its own repository.** Rejected: it changes behaviour silently for users who keep that history by hand.
- **`kickoff` asks once and writes the rule into a committed instructions file.** Rejected: that file is shared, so one person's choice would bind the whole team.

## Consequences

- The guide's FAQ ("Is the workspace folder committed?") carries a rule users can copy; keep it in step with the skill sentence.
- The optional commit reminder hook stays silent for commits in another git repository, so these notes commits do not trigger it.
- Skills that write notes without carrying the sentence (`tracker`, `resume-here`, `execute-plan`, `review-phase`, `guard-plan`) follow the repo's instructions directly; a skill that adds a "run no git" line must use this sentence instead.
