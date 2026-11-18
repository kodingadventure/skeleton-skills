# Every skill stays visible to the agent

Status: accepted (supersedes ADR 0005)

## Context

ADR 0005 kept the workspace and GitHub skills out of the agent's reach with `disable-model-invocation: true`, so they ran only when the user named them. That flag also removes a skill from the agent's skill list, so the agent reads it as not installed. Other skills route to these by an "installed" condition: `guard-plan` ends a workspace stop with `/resume-here <slug>`, `whatnext` recommends `/wrap-up <slug>`. A manual test (issue #31) showed neither line ever appears, even with the skill installed.

## Decision

Every skill keeps `disable-model-invocation: false`. A skill that should run only when named starts its description with "Run only when the user asks for it by name." and carries no "Use when" triggers: the description, not the flag, keeps it from starting on its own. This covers `discuss`, `msg`, `resume-here`, `so-far`, `tracker`, `wrap-up` and the three GitHub skills. `kickoff`, `pause-here` and `spin-off` still start on their own when the user says so.

## Considered options

- **Keep the flag; split the issue.** Rejected: every "if installed" route to a manual skill stays dead, in `guard-plan`, `whatnext` and any later skill.
- **Keep the flag; detect the skill from its folder in `.claude/skills/`.** Rejected: misses skills installed through a plugin, and every routing skill would need its own file check.

## Consequences

- The agent may now offer a manual skill, or very rarely start it. The GitHub skills still post only after the user approves the draft, and `msg` only drafts; `wrap-up` asks only when a work item is not `done`, so its description opening is what keeps it from closing a workspace unasked.
- A new skill that should run only when named follows `docs/agents/publish-skill.md`: the description opening above, the flag `false`.
