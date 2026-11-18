---
"skeleton-skills": patch
---

`guard-plan` now always sends a companion for an agent-run manual test checkpoint, even a one-command one, so every such checkpoint leaves a result file, and reports it with the fixed `🧪 Checkpoint N — agent` line. `execute-plan` hands every manual test checkpoint to you, including those marked `Runner: guardian`, instead of running them itself.
