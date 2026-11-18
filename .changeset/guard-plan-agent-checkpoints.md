---
"skeleton-skills": minor
---

`guard-plan`: a manual test checkpoint marked `Runner: guardian` is now run by a companion sub-agent without stopping the run, re-run after each fix, and listed in the report with its result file so you can spot-check it. When the agent cannot drive a scenario, that scenario is handed to you like any manual test. The guardian may adjust how a scenario is run to match the code, never what it expects.
