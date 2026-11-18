# Manual test of a skill

A skill whose text changed has no automated surface: `npm run format:check` proves it is formatted, not that an agent following it does the right thing. The manual test runs the skill in a throwaway repo, in fresh sessions, and checks what it produced against expectations written before the run. Use it for a plan's manual test checkpoint, a re-test after a skill fix, or a new skill before it ships.

Roles: the **guardian** (the session doing the skill work) writes the scenarios, dispatches one **companion** subagent that runs and checks them, and fixes the skill when a scenario fails. The guardian never runs the test sessions itself; that keeps its context for the fixes.

## Where a test runs

Never in this catalog and never in a real project's own folder. Two targets:

- **Fixture repo** (default): `scripts/manual-test/test-repo.sh init` builds a small shop repo in a `mktemp -d` folder: two modules with `node --test` tests, a glossary, a Docs Layout, a wiki page, `verify.md`, and a `CLAUDE.md` with no commit rule. `install SKILL DIR` copies the skill from this catalog's working tree, so the test runs the branch that is checked out. Every setup goes through a script command; when a scenario needs a setup the script lacks (a commit, a workspace, a `CLAUDE.md` rule), add a command for it. The script's header lists the commands.
- **Clone of a real project**: when the behaviour depends on a real codebase's size or shape. `git clone --no-hardlinks <project> <tmp>`, remove `origin` so nothing can be pushed, then install the skill copy. The original stays untouched.

## Steps

1. **Write the scenarios.** Each one is a setup (script commands), the exact prompt, and expectations as checkboxes the companion can check from files, `git`, or the session's final answer. A prompt for `claude -p` ends with "do not ask; take the defaults for open questions", since nobody can answer. Keep scenarios and logs in the workspace (a plan phase, `logs/`), not in the repo. A re-test after a fix covers the failed scenarios and any other scenario whose skill the fix touched.
   Done when: every expectation names something observable, such as a quoted line or a file, a commit count or a status.
2. **Dispatch the companion.** One Agent call, `model: sonnet`, `effort: medium` (unless the owner sets otherwise), with the scenarios, the script path and the log path. It follows the companion rules below and reports pass or fail per scenario with the evidence quoted.
   Done when: the companion's report is in and its log exists.
3. **Check the report.** Read the log and confirm the quoted lines match what the report says passed. Then confirm `git status --short` in the catalog is unchanged.
4. **Fix and re-run each failure.** Find the cause in the skill's text. The cause is often a rule that lives only in a principles section and not in the step that produces the output. Fix it on the work branch with its own commit and changeset, then send the same companion (`SendMessage`) a re-run of that scenario alone. It appends a `## Re-run <scenario> after fix` section and keeps the first run's record. Re-run only the scenarios the fix touched, once each, one after another. Before a third re-run round, ask the owner: each scenario is a full session on the owner's account (a `guard-plan` scenario starts its executors too), and five rounds of a four-scenario checkpoint once reached the 5-hour usage limit.
   Done when: every scenario passes, or a failure is handed to the owner as a decision (a changed expectation, an accepted failure outside the change, not a skipped one).

## Companion rules

- Run test sessions one at a time, never in parallel: several `guard-plan` sessions at once multiply the usage.
- Run each test session fresh, from inside the test repo: `cd <D> && claude -p --model sonnet --effort medium --permission-mode auto "<prompt>"`. A session reads its skills and agents when it starts, so install first and open a new session after every install.
- Before each run, record the commit count and `git status --short`. After it, check every expectation yourself and quote the exact line, entry or commit you checked.
- On a failed expectation, record what you saw and what was expected, word for word, and go on unless a later step depends on it. Leave the skill alone: fixes are the guardian's.
- Change nothing in the catalog. The only files to write are the log and any script copy in the workspace.
- Write the log as you go: a header line (date · test repo · `catalog: <branch> @ <sha>` as the script prints it), a table `Scenario | Result | Notes`, then `## Findings` for anything odd that broke no expectation.
- At the end, delete the temp folders and report pass or fail per scenario, with the evidence quoted.

## Owner-driven variant

When the owner wants to watch the skill run, they open the test session themselves (`cd <D> && claude`) and type the prompts. The companion runs in a session in this catalog. It prepares each setup, tells the owner what to type, one step per message, and checks the result from files and `git`. It asks the owner to paste only the skill's final answer. After every install, the owner starts a new session or runs `/clear`.

## Gotchas

- `--permission-mode auto`: `acceptEdits` refuses `grep` and `git` in `-p` mode, and most skills under test run both.
- A temp folder is an untrusted workspace: its `permissions.allow` entries and its hooks are ignored (stderr: "workspace has not been trusted"). Grant tools with `--allowedTools`. Test hook behaviour somewhere else.
- A skill that must not write: run it with `--allowedTools` limited to read tools, and compare the commit count and status from before and after.
- To confirm the skill under test loaded, add `--output-format stream-json --verbose`; the `system` init event lists the session's skills.
- `allow-commit` and `silent-commit` cover both commit branches a skill can take under the repo's rules.
- A skill's own final report can claim compliance that its output contradicts (for example "no behaviour in the glossary" above an entry that names a status change). Check the file, not the report.
