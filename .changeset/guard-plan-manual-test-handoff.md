---
"skeleton-skills": minor
---

`guard-plan`: at a manual test you run yourself, the guardian now writes a prompt for a separate guide session and prints one command to open it, with a suggested model and effort. The guide session walks you through the test step by step and records the result next to the plan. The guardian suggests whether to wait or stop; if it stops, `/guard-plan` in a new session reads the result and continues, without re-running the baseline when nothing was committed in between.
