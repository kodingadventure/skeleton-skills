---
"skeleton-skills": patch
---

`guard-plan`: the check for the `domain-modeling` skill is now its own preflight step, so a plan whose workspace holds an `ADR: candidate` stops before the first phase runs instead of after it is committed. `guard-plan`, `execute-plan` and `review-phase`: the "reported rows unchanged" check now counts the tracker's table rows (`grep -c '^| \[x\]' TRACKER.md`); the old pattern always counted 0.
