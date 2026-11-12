---
"skeleton-skills": minor
---

`update-wiki` and `refine-docs`: after a run you start yourself, they now commit their own changes when the repo's rules let the agent commit (only the files they changed), ask first when the rules say so, and otherwise print the commit command. Run from a plan's docs phase, they leave the commit to the plan runner, so a phase stays one reviewed commit.
