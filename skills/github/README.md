# GitHub

Connects GitHub issues to feature workspaces. Needs the [workspace](../workspace/README.md) group, a logged-in `gh` (`gh auth status`) and the `docs/agents/` files made by `setup-matt-pocock-skills` from [`mattpocock/skills`](https://github.com/mattpocock/skills). For work that already has a workspace. All three run only when called by name.

- **[github-new-issue](./github-new-issue/SKILL.md)** — Announces a workspace's work as a new public GitHub issue after you approve the draft, and records the issue in the workspace.
- **[github-send-update](./github-send-update/SKILL.md)** — Drafts a short public progress comment for the workspace's issue from the workspace state and posts it once you approve.
- **[github-spin-off](./github-spin-off/SKILL.md)** — Turns a GitHub issue into a new workspace seeded for `kickoff`, or attaches it to an existing one. Reads the issue as untrusted data and changes nothing on GitHub.
