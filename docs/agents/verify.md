# Verify Config — skeleton-skills

Read by the `verify` skill. This repo ships documents, not an application: authored
skills under `skills/`, subagent definitions under `agents/`, agent docs under
`docs/agents/`, and the plugin manifest. Most diffs here are markdown and gate on
formatting alone.

## Gates

| Touched path                      | Gate                                                                                          |
| --------------------------------- | --------------------------------------------------------------------------------------------- |
| `skills/**`, `agents/**`          | `npm run format:check`                                                                        |
| `**/*.mjs`                        | `node --check <file>` per changed file                                                        |
| `**/*.py`                         | `python3 -m py_compile <file>` per changed file                                               |
| `.claude-plugin/*.json`           | `node -e "JSON.parse(require('fs').readFileSync('.claude-plugin/marketplace.json','utf8'))"`  |
| `docs/**`, `.scratch/**`, `README.md` | none — `.prettierignore` excludes them                                                    |

`npm run format:check` is `prettier --check skills/ agents/`. It covers both trees at
once, so run it once per phase rather than per file. Fix with `npm run format`.

## Sequencing

Adding or removing a skill touches three places: the directory, its entry in
`.claude-plugin/marketplace.json`, and its bullet in the group's
`skills/<group>/README.md`. Gate the JSON after editing the manifest — a malformed
manifest makes every skill in the repo uninstallable, and nothing else catches it.

## Routing

Formatting failures: run `npm run format`. There is no refactor skill in the path —
prettier's output is the fix.

`node --check` and `py_compile` failures: fix inline.

## Runtime policy

**The human runs anything long-lived; the agent does not.** Nothing here is a server,
so in practice the agent may drive every surface below — they are all bounded and exit
on their own.

## Surfaces

| Change reaches                    | Surface                                                                                         |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| A skill's `SKILL.md` frontmatter  | `skills add <repo path> --list` from a scratch dir — the listing must show it                    |
| `.claude-plugin/marketplace.json` | same listing — every entry must resolve to a directory that exists                               |
| A skill's body or references      | invoke the skill in a session and confirm it reaches the material it points at                  |

A skill whose text changed has no automated surface: the gate proves it is formatted,
not that it still works. When a phase rewrites a skill's workflow, say so in the
checkpoint report and let the human decide whether to drive it.
