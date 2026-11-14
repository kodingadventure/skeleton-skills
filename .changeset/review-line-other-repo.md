---
"skeleton-skills": patch
---

`writing-great-plan` (used by `to-plan`): a plan now keeps the `**Review:** guardian` line whenever your agent has the `review-phase` skill, including when the plan's `Repo` is another folder with no `.claude/skills/` of its own, such as a new project or a gitignored one. Before, `to-plan` dropped the line for those plans, so `execute-plan` committed each phase itself instead of handing it to `/review-phase`.
