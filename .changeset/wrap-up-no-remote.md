---
"skeleton-skills": patch
---

`wrap-up`: in a repo with no remote it now says "no remote; nothing to pull" instead of claiming the branch is level with a remote, and checks locally that a feature branch is merged before switching away from it. It also commits a `Workspace root:` or `Plan root:` line a skill left uncommitted, when that line is the file's only change. `pause-here`: suggests a pull request and a pull only when the repo has a remote.
