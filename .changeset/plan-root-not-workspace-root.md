---
"skeleton-skills": patch
---

`to-plan` and other plan writers: when they ask for the plan root on a repo's first plan outside a workspace, they now refuse the workspace root itself or a folder inside it, and offer a sibling folder (such as `_local/plans/` next to `_local/workspaces/`) so all your local notes stay in one folder. The README explains what each root is for and adds a sentence you can paste to have your agent set the skills up.
