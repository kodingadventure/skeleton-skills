# Read the plan as the runner

Run this after the plan is written and before it is shown to the user. A plan is read twice: by the person who approves it, and by whatever runs it (`execute-plan`, or `guard-plan` dispatching executors). The second reading is the one that fails, and a self-review asked "did I cover the runner?" is answered "yes" from memory. So each step below is a **command to run or evidence to paste into the plan**, never a question to answer.

Run the steps in order. Fix the plan as you go.

1. **Commit and push rules of every target repo.** Run `grep -inE 'commit|push' <repo>/CLAUDE.md <repo>/AGENTS.md` once per target repo. Summarize the result in a `## Notes` bullet starting `Applies to: all`. When the repo says nothing, write what the runner will do: `guard-plan` asks for its Run mode, and `execute-plan` prints the commit command instead of committing. Never leave the plan silent on pushing.
2. **Runner and gate from phase 1.** Check `test -f <repo>/docs/agents/verify.md` for every target repo. When a repo has none, the plan carries a `Verify:` line, or states "no gate until phase N creates it" so the runner knows what the baseline is before then.
3. **Items that need a person or a permission.** An item that waits for an answer (a review page), installs a tool, needs a login, or needs a click in a dashboard cannot go to an executor agent. Mark it `Runner: guardian` (the guardian does it after the phase) or `Runner: human` (the run stops and waits). Unmarked items default to the executor.
4. **Repeating phases.** A phase whose checklist runs once per unit gets `Execution unit:` plus one checkbox sub-item per unit. The executor is dispatched once per unchecked unit.
5. **Things that go stale.** In the plan text, replace: a date in a file name the phase creates with the literal `YYYY-MM-DD` (the day the phase runs); a commit SHA with the command that produces it; a `file:line` with a symbol name or section title.
6. **CLI flags.** For every command-line flag in the plan, run `<cli> --help` (or the subcommand's help) and compare. A flag you cannot check gets the marker `unverified — check first`.
7. **Side effects of manual checkpoints.** Anything a checkpoint installs, removes, or reconfigures outside the project (a plugin, a global setting, a login) names where it happens (a scratch folder, a project scope) and how to undo it.
8. **Folders the plan writes.** Run `git check-ignore -v <path>` for each new folder. When it is not ignored, say so in the plan. When a formatter or linter ignore list scans it, add the exclusion as an item.
9. **Plans from a feature workspace.** Read the decisions in `CONTEXT.md` and the guardrails in `WHATNEXT.md`, and compare them with the target repo's `CLAUDE.md` or `AGENTS.md`. A conflict becomes an Open Question whose `Default:` follows this order of authority: the user's latest instruction, the repo's rules, the workspace's decisions, then the skill's defaults.
10. **Standalone phase files.** Each phase file has a `Repo:` line and absolute paths, and uses no placeholder that is defined only in the entry point. The executor is told not to open the entry point.

When done, report one line to the user: what this check changed in the plan (or "nothing to change"). One sentence, not a list: the evidence is already in the plan.

For an L or XL plan, a fresh-eyes subagent may repeat the check on the finished plan when the harness has subagents. It is optional.

## Growth

Add a step only when the user's review of a finished plan finds a kind of problem no step above would have caught. A step nobody has needed is a guess, and every step costs a command on every plan.
