---
"skeleton-skills": minor
---

`refine-docs`: the Docs Layout gains an optional Wiki section (flow pages, feature index, preserved behaviour) and a `Required` column in the deep-context tier. `refine-docs` routes flow content to the wiki without writing it, and takes a commit range (`HEAD~3..HEAD`); with a clean tree and no argument it asks which recent commits to document.
