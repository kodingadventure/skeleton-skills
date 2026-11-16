# skeleton-skills

## 0.4.0

### Minor Changes

- [#25](https://github.com/kodingadventure/skeleton-skills/pull/25) [`52a2589`](https://github.com/kodingadventure/skeleton-skills/commit/52a25898dd127420243f8b534b089987701bcc58) Thanks [@budiadiono](https://github.com/budiadiono)! - `to-plan`, `writing-great-plan` and `whatnext`: plans written outside a workspace now default to `.scratch/plans/`, next to the default workspace root `.scratch/workspaces/`, instead of `.plans/`. All your local notes now sit under `.scratch/` by default. When your workspace root is a `workspaces/` folder somewhere else (such as `_local/workspaces/`), the plan root offered is its sibling (`_local/plans/`). A repo that already has a `Plan root:` line keeps it.

### Patch Changes

- [#25](https://github.com/kodingadventure/skeleton-skills/pull/25) [`bbd431b`](https://github.com/kodingadventure/skeleton-skills/commit/bbd431b7d5a4251c9e41d74f57f2e14f6aa1bc45) Thanks [@budiadiono](https://github.com/budiadiono)! - `to-plan` and other plan writers: when they ask for the plan root on a repo's first plan outside a workspace, they now refuse the workspace root itself or a folder inside it, and offer a sibling folder (such as `_local/plans/` next to `_local/workspaces/`) so all your local notes stay in one folder. The README explains what each root is for and adds a sentence you can paste to have your agent set the skills up.

## 0.3.0

### Minor Changes

- [#8](https://github.com/kodingadventure/skeleton-skills/pull/8) [`67fdba3`](https://github.com/kodingadventure/skeleton-skills/commit/67fdba39350b78f2de4ef6ea2a077efcd13af74d) Thanks [@budiadiono](https://github.com/budiadiono)! - `update-wiki` and `refine-docs`: after a run you start yourself, they now commit their own changes when the repo's rules let the agent commit (only the files they changed), ask first when the rules say so, and otherwise print the commit command. Run from a plan's docs phase, they leave the commit to the plan runner, so a phase stays one reviewed commit.

- [#8](https://github.com/kodingadventure/skeleton-skills/pull/8) [`7344edc`](https://github.com/kodingadventure/skeleton-skills/commit/7344edc9c2d09840abcf9f68c3f4cb457ad8a2af) Thanks [@budiadiono](https://github.com/budiadiono)! - `writing-great-plan`: a feature plan that changes behaviour now ends with a docs phase, reviewed and committed like the code. It holds one item per installed documentation skill (`update-wiki` for the wiki, `refine-docs` for glossaries and reference docs); a repo without a wiki gets one only when there is something to write. Missing tests become their own phase before it. A doc sentence that one code phase makes wrong is fixed in that phase.

- [#8](https://github.com/kodingadventure/skeleton-skills/pull/8) [`7cd8b90`](https://github.com/kodingadventure/skeleton-skills/commit/7cd8b904f90267072418c8776840ae8950d9b740) Thanks [@budiadiono](https://github.com/budiadiono)! - `to-plan`: while exploring, it now finds the doc pages the plan will touch, so a feature plan that changes behaviour ends with a docs phase naming those pages, and a doc sentence one phase makes wrong is fixed in that phase.

- [#17](https://github.com/kodingadventure/skeleton-skills/pull/17) [`6cc1153`](https://github.com/kodingadventure/skeleton-skills/commit/6cc11531038ab112d4608b844b7b38e2e0c1b95d) Thanks [@budiadiono](https://github.com/budiadiono)! - Workspace skills (`kickoff`, `discuss`, `pause-here`, `spin-off`, `wrap-up`): when your workspace root sits in its own git repository and your repo's instructions (`CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`) say to commit the workspace notes, they now commit the files they wrote in that repository and name the commit in their report. Without such an instruction nothing changes. The guide's FAQ shows a rule you can copy.

- [#11](https://github.com/kodingadventure/skeleton-skills/pull/11) [`d4b369b`](https://github.com/kodingadventure/skeleton-skills/commit/d4b369b68fe2a5a2c958b7c4c5794c13140568c4) Thanks [@budiadiono](https://github.com/budiadiono)! - `wrap-up`: a new first step switches to the default branch and pulls the merged work before anything is written, and stops when the pull request is still open. `pause-here`: when a finished workspace's work is still in an open pull request, the next steps are now merge, then switch to the default branch and pull, then `/wrap-up`.

### Patch Changes

- [#6](https://github.com/kodingadventure/skeleton-skills/pull/6) [`71d47c9`](https://github.com/kodingadventure/skeleton-skills/commit/71d47c9bd9f7f5f4eb828473988a99e4077e148c) Thanks [@budiadiono](https://github.com/budiadiono)! - `discuss`: the close now comes once, in the reply that records what the discussion settled (or when you say you are stopping). It offers the next topic directly (not when you are stopping), and names `/discuss <slug> <topic>` only as the way to pick it up in a new session.

  `so-far`, `kickoff`, `pause-here`, `spin-off`: the continue line appears once, in the skill's closing reply, and is not repeated on later replies. `whatnext`: in a conversation that already resumed or is discussing a workspace, it names that workspace's next step and never suggests the skill already running for it (`/resume-here` after a resume, `/discuss` inside a discussion).

- [#8](https://github.com/kodingadventure/skeleton-skills/pull/8) [`b8c58f4`](https://github.com/kodingadventure/skeleton-skills/commit/b8c58f4de3996932a00924d2849e8c05dd5b95ad) Thanks [@budiadiono](https://github.com/budiadiono)! - `execute-plan`: the completion report's `Docs:` line names the plan's docs phase and the documentation skills it ran, instead of always `refine-docs`. `wrap-up`: the behaviour step checks what the plan's docs phase already documented, and writes the rest with the installed documentation skills (`update-wiki`, `refine-docs`).

- [#10](https://github.com/kodingadventure/skeleton-skills/pull/10) [`9dd965d`](https://github.com/kodingadventure/skeleton-skills/commit/9dd965d7ab0a09d81b15247e69f251a93441e7c9) Thanks [@budiadiono](https://github.com/budiadiono)! - `refine-docs`: the steps that write a glossary entry now run a short test that strikes any clause about a status change, a rule or a side effect, so an entry no longer says what the term causes, only what it is.

- [#10](https://github.com/kodingadventure/skeleton-skills/pull/10) [`eea6ecd`](https://github.com/kodingadventure/skeleton-skills/commit/eea6ecde50ad6f7df5d2150e3b3c5e7ea7f26096) Thanks [@budiadiono](https://github.com/budiadiono)! - `refine-docs`: glossary entries now hold the term's definition only, with no behaviour and no code paths, and link out only to doc pages. Its own examples no longer put a code pointer or a rule in a glossary entry.

- [#8](https://github.com/kodingadventure/skeleton-skills/pull/8) [`5b4426a`](https://github.com/kodingadventure/skeleton-skills/commit/5b4426a82d09c08b9cb9cf08a92a0b4e40caa150) Thanks [@budiadiono](https://github.com/budiadiono)! - `guard-plan`: the check for the `domain-modeling` skill is now its own preflight step, so a plan whose workspace holds an `ADR: candidate` stops before the first phase runs instead of after it is committed. `guard-plan`, `execute-plan` and `review-phase`: the "reported rows unchanged" check now counts the tracker's table rows (`grep -c '^| \[x\]' TRACKER.md`); the old pattern always counted 0.

- [#8](https://github.com/kodingadventure/skeleton-skills/pull/8) [`c6fdf3e`](https://github.com/kodingadventure/skeleton-skills/commit/c6fdf3e75471bf0dc9eed6b4f48393b311ebd901) Thanks [@budiadiono](https://github.com/budiadiono)! - `guard-plan`: after guarding each phase, it now closes the phase in the feature workspace — the work item's status, the Action Log, `WHATNEXT.md`, the `INDEX.md` row — and writes the ADR for any `ADR: candidate` the phase settled, committed with the phase. Before, these waited until `wrap-up`.

- [#10](https://github.com/kodingadventure/skeleton-skills/pull/10) [`f0a5606`](https://github.com/kodingadventure/skeleton-skills/commit/f0a5606732c7be7bc9cc96ef91b6f31ea49cddfc) Thanks [@budiadiono](https://github.com/budiadiono)! - `writing-great-plan`: the docs phase's review check is now written once, in the plan template, and copied into the plan word for word, so a plan no longer drops file paths, UI text or links from the claims it checks against the code.

- [#17](https://github.com/kodingadventure/skeleton-skills/pull/17) [`5e48038`](https://github.com/kodingadventure/skeleton-skills/commit/5e48038e7db3bd0d7968e89dbe60508ea4eb4fe1) Thanks [@budiadiono](https://github.com/budiadiono)! - Workspace commit reminder hook: it now stays silent for a commit in another git repository, such as a separate repository that holds your workspace notes above the workspace root, including a commit run from a shell already inside that folder. Commits in your project's own repository still get the reminder.

- [#16](https://github.com/kodingadventure/skeleton-skills/pull/16) [`64d03a0`](https://github.com/kodingadventure/skeleton-skills/commit/64d03a010a2f0940fd9c4d024a1e5513c720350f) Thanks [@budiadiono](https://github.com/budiadiono)! - `writing-great-plan` (used by `to-plan`): a plan now keeps the `**Review:** guardian` line whenever your agent has the `review-phase` skill, including when the plan's `Repo` is another folder with no `.claude/skills/` of its own, such as a new project or a gitignored one. Before, `to-plan` dropped the line for those plans, so `execute-plan` committed each phase itself instead of handing it to `/review-phase`.

- [#15](https://github.com/kodingadventure/skeleton-skills/pull/15) [`8120831`](https://github.com/kodingadventure/skeleton-skills/commit/8120831ee844468c74e0503f6c7f7c55e1e6b00d) Thanks [@budiadiono](https://github.com/budiadiono)! - `kickoff`, `spin-off` and `writing-great-plan`: the `Workspace root:` or `Plan root:` line they write to `CLAUDE.md` / `AGENTS.md` is now committed right away when your repo's rules let the agent commit (otherwise they print the command), instead of being left uncommitted for the rest of the work. When the file already had other uncommitted changes, they leave the commit to you and say so.

- [#17](https://github.com/kodingadventure/skeleton-skills/pull/17) [`d06cb2d`](https://github.com/kodingadventure/skeleton-skills/commit/d06cb2d010bf2200b443f4a0ff217b3e3f8d4c09) Thanks [@budiadiono](https://github.com/budiadiono)! - `kickoff`: when the workspace root has its own git repository, the notes-commit rule is now copied into the new workspace's `CONTEXT.md` word for word, in English, instead of being rewritten to match the repo's own rule (which could drop the "only when the repo's instructions say so" condition). `discuss`: its closing reply now names the notes commit, or says the notes were not committed.

- [#15](https://github.com/kodingadventure/skeleton-skills/pull/15) [`3e9b16a`](https://github.com/kodingadventure/skeleton-skills/commit/3e9b16aea3e6048d0e4b1fe56b589a3d1433c391) Thanks [@budiadiono](https://github.com/budiadiono)! - `wrap-up`: in a repo with no remote it now says "no remote; nothing to pull" instead of claiming the branch is level with a remote, and checks locally that a feature branch is merged before switching away from it. It also commits a `Workspace root:` or `Plan root:` line a skill left uncommitted, when that line is the file's only change. `pause-here`: suggests a pull request and a pull only when the repo has a remote.

## 0.2.0

### Minor Changes

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`cf95c2d`](https://github.com/kodingadventure/skeleton-skills/commit/cf95c2de4f7e77753475a9af086243b0799a50dd) Thanks [@budiadiono](https://github.com/budiadiono)! - `refine-docs`: the Docs Layout gains an optional Wiki section (flow pages, feature index, preserved behaviour) and a `Required` column in the deep-context tier. `refine-docs` routes flow content to the wiki without writing it, and takes a commit range (`HEAD~3..HEAD`); with a clean tree and no argument it asks which recent commits to document.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`85604c2`](https://github.com/kodingadventure/skeleton-skills/commit/85604c2fe849ee623b00ee36e56aec389478c23e) Thanks [@budiadiono](https://github.com/budiadiono)! - New skill `update-wiki` (workflow group, optional): writes the wiki from committed changes — flow pages across code units, the feature index and, if the repo keeps one, a page of behaviour kept wrong on purpose. Reads every path from the Docs Layout's Wiki section; install it with `refine-docs`.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`e7d0f52`](https://github.com/kodingadventure/skeleton-skills/commit/e7d0f52d59fd38249cb4da15261d33e0e4cdce5e) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: after a commit that changed behaviour, it now suggests updating the docs — once for a plan's whole commit range after its last phase, or right away for a commit outside a plan — with `update-wiki` if installed, else `refine-docs`. It also flags code units the Docs Layout says must each have a glossary but don't.

### Patch Changes

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`3f4170d`](https://github.com/kodingadventure/skeleton-skills/commit/3f4170d0657817509ff7569d7cec65c6b1fe1d83) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: for committed code with no test, it now suggests adding tests for that code instead of a test-first skill, and never names a skill that is not installed. `resume-here` and `discuss`: every message, question included, is in the workspace language, even in a repo whose committed files are English-only.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`b8785d3`](https://github.com/kodingadventure/skeleton-skills/commit/b8785d3e7e0390c482ad92ee1ad7f017b118e0d5) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: when no installed skill fits, the answer now leaves out the `Invoke` line entirely instead of writing `Invoke: none`.

- [#3](https://github.com/kodingadventure/skeleton-skills/pull/3) [`229e330`](https://github.com/kodingadventure/skeleton-skills/commit/229e3303f197e184faa0639ba2eaa2bbe60255ec) Thanks [@budiadiono](https://github.com/budiadiono)! - `whatnext`: when a commit changed behaviour without a test beside it, it now asks for the missing tests before suggesting the docs update, and keeps asking for them even after a later commit documented the change.

## 0.1.1

### Patch Changes

- [`236e4e7`](https://github.com/kodingadventure/skeleton-skills/commit/236e4e7b2099508cbc23047239811e78691e064e) Thanks [@budiadiono](https://github.com/budiadiono)! - `review-page`: the page template is reformatted; pages look and behave the same.
