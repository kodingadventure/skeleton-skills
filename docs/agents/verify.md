# Verify Config — skeleton-skills

Read by the `verify` skill. This repo ships documents, not an application: authored
skills under `skills/`, subagent definitions under `plugins/phase-agents/agents/`, agent docs under
`docs/agents/`, and the plugin manifest. Most diffs here are markdown and gate on
formatting alone.

## Gates

| Touched path                          | Gate                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------ |
| `skills/**`, `plugins/**`             | `npm run format:check`                                                               |
| `package.json`, `plugins/**`          | `npm run check-plugin-version`                                                       |
| `**/*.mjs`                            | `node --check <file>` per changed file                                               |
| `skills/workspace/hooks/**`           | `node --test "skills/workspace/hooks/*.test.mjs"`                                    |
| `**/*.py`                             | `python3 -m py_compile <file>` per changed file                                      |
| `**/.claude-plugin/*.json`            | `node -e "JSON.parse(require('fs').readFileSync('<file>','utf8'))"` per changed file |
| `docs/**`, `.scratch/**`, `README.md` | none — `.prettierignore` excludes them                                               |

`npm run format:check` is `prettier --check skills/ plugins/`. It covers both trees at
once, so run it once per phase rather than per file. Fix with `npm run format`.

## Sequencing

Adding or removing a skill touches three places: the directory, its entry in
`.claude-plugin/marketplace.json`, and its bullet in the group's
`skills/<group>/README.md`. Gate the JSON after editing the manifest — a malformed
manifest makes every skill in the repo uninstallable, and nothing else catches it.

A commit that touches `skills/` or `plugins/` without a new file in `.changeset/` is a failure.

A change to what a skill does, and a new, removed or renamed skill, also touches the user guide: `grep -rn '<skill-name>' docs/guide/` and update every sentence the change makes wrong, in the same commit.

The four `plugins/phase-agents/agents/phase-*.md` bodies are copies of
`skills/workflow/execute-plan/references/executor-rules.md`; edit both.

## Routing

Formatting failures: run `npm run format`. There is no refactor skill in the path —
prettier's output is the fix.

`node --check` and `py_compile` failures: fix inline.

## Runtime policy

**The human runs anything long-lived; the agent does not.** Nothing here is a server,
so in practice the agent may drive every surface below — they are all bounded and exit
on their own.

`writing-great-plan` reads this section and `## Surfaces` to mark each Manual Test
Checkpoint `Runner: guardian` or `Runner: human`, and `guard-plan` runs a `guardian`
checkpoint through a companion sub-agent (ADR 0016 records the marker, ADR 0017 the
agent's permission).

## Surfaces

| Change reaches                    | Surface                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------ |
| A skill's `SKILL.md` frontmatter  | `npx skills add <repo path> --list` from a scratch dir — the listing must show it  |
| `.claude-plugin/marketplace.json` | same listing — every entry must resolve to a directory that exists             |
| A skill's body or references      | manual test in a fixture repo: `docs/agents/manual-test.md`                    |

A skill whose text changed has no automated surface: the gate proves it is formatted,
not that it still works. A phase that rewrites a skill's workflow gets a checkpoint that
runs the manual test in `docs/agents/manual-test.md`, and its `Runner:` marker follows the
runtime policy above.
