# Agent

Helpers for how the agent talks to you and learns from the work. They stand alone and need no workspace.

- **[review-page](./review-page/SKILL.md)** — Writes a short, diagram-led HTML page and opens it so you can read or decide there, with an Explain button on each item. Use it when there are two or more decisions, or one that needs a diagram; the agent may open one on its own for that.
- **[what-you-did](./what-you-did/SKILL.md)** — Builds a page of the recent code changes grouped by purpose, with before/after diffs and Explain prompts. Use it when you want to see or understand what was just changed.
- **[skill-from-context](./skill-from-context/SKILL.md)** — Captures a repeatable pattern from the conversation into a new or refined skill. Use it when the agent offers after seeing the same solution twice, or when you ask. Needs `writing-for-agents` from [`mattpocock/skills`](https://github.com/mattpocock/skills) and stops with a message if it is missing.

The pages are generated with Python 3 scripts in the skill folders and are written to the temp directory.
