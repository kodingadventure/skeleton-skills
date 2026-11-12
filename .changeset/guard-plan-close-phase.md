---
"skeleton-skills": patch
---

`guard-plan`: after guarding each phase, it now closes the phase in the feature workspace — the work item's status, the Action Log, `WHATNEXT.md`, the `INDEX.md` row — and writes the ADR for any `ADR: candidate` the phase settled, committed with the phase. Before, these waited until `wrap-up`.
