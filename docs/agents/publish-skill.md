# Publishing a new skill

How to add a brand-new skill to this catalog (`npx skills add kodingadventure/skeleton-skills`).

## Where it goes

Skills live under `skills/<group>/<skill-name>/SKILL.md`. There are four groups, each mapped 1:1 to a plugin block in `.claude-plugin/marketplace.json`:

| Folder       | Plugin name | Domain                                                               |
| ------------ | ----------- | -------------------------------------------------------------------- |
| `workspace/` | `workspace` | Feature workspace family (discuss, kickoff, pause and resume, wrap-up) |
| `workflow/`  | `workflow`  | Planning and execution: plans, guardian review, verify               |
| `agent/`     | `agent`     | Helpers for agent behaviour: review pages, skill capture, explainers |
| `github/`    | `github`    | GitHub issues connected to feature workspaces                        |

Fit a new skill into the closest group by subject matter. If none fits, add a new folder under `skills/` and a new plugin block to the manifest, and flag the new group name to the user. Do not force an unrelated skill into a group to avoid this.

The Matt Pocock suite (`mattpocock/skills`) is a dependency, not part of this catalog: never copy it here or list it in the manifest. The README names it and its pinned install command.

A skill adapted from someone else's work keeps their credit: ship their license file in the skill directory and name the source in the group README bullet.

## Register in the manifest

Every skill needs an entry in `.claude-plugin/marketplace.json`, in its group's plugin `skills` array, as `"./skills/<group>/<skill-name>"`, alphabetical within the array. A skill folder that is not listed will never be installable: the folder alone is not enough. Parse the JSON after editing; a malformed manifest makes every skill uninstallable.

One file serves two installers. The `skills` CLI reads the group blocks and flattens them into sibling folders; Claude Code reads the same blocks as plugins (the entry-level `skills` field is a known plugin field), so no `plugin.json` is needed for them. The `phase-agents` entry is separate on purpose: the CLI never installs agents, and a CLI user who already has the skills needs only the agents, so its source is `./plugins/phase-agents` (with its own `.claude-plugin/plugin.json`, including `author`, to pass `claude plugin validate`). Putting the agents in a group plugin would duplicate skills.

## Add the README bullet

Every group has `skills/<group>/README.md`: add one bullet for the new skill (name, one sentence of what it does, when to use it). Update the per-group count in the root `README.md` structure table.

## Choose who can invoke it

`disable-model-invocation: true` removes a skill from the model's skill list, though the user can still type it. The model then reads the skill as not installed, so another skill's "recommend `/x` if installed" never fires. Choose by how the skill is reached:

- **Manual** (`disable-model-invocation: true`): the skill writes or sends something and should only run when named, such as `tracker`, `wrap-up` or the GitHub skills. Start the description with "Run only when the user asks for it by name."
- **Model-invocable, starts on its own**: only `kickoff`, `pause-here` and `spin-off`. They fit a moment the user would not think to name: closing a session, splitting a topic out, turning a discussion into a workspace. Put the "Use when" triggers in the description and any write behind a user confirmation in the steps.
- **Model-invocable, reached by other skills or a fixed threshold**: `writing-great-plan`, `verify`, `review-phase`, `review-page`, `skill-from-context`. A skill that others route to by an "installed" condition stays visible to the model.
- **Model-invocable, picked on a matching request**: `to-plan`, `execute-plan`, `guard-plan`, `whatnext`, `refine-docs`, `what-you-did`. The user asks for the job ("create a plan") rather than naming the skill; the description's "Use when" triggers carry the routing.

Test routing with real sessions rather than by reading the skill: `claude -p` in a disposable clone, one prompt per fork from a session that has not yet run the skill, several samples. Test what the skill does with the manual test in `docs/agents/manual-test.md`.

## Add a changeset

Run `npx changeset`, pick `minor` for a new skill, and write one line for the user: the skill name and what it does. Commit the file in `.changeset/` with the skill. Do not edit the version by hand.

## Before opening a change

- `npm run format:check` (covers `skills/` and `plugins/`; group READMEs are included, the root `README.md` and `docs/` are not).
- A `description` is YAML: a colon followed by a space inside an unquoted value makes the skill disappear from the install list. Use a quoted string or a `>` block.
- Run `npx skills add <this repo> --list` from a scratch folder, never from a real project, and confirm the new skill is listed.
- `npm run link-skills`, so sessions in this repo load the new skill.
- Hook tests: `node --test "skills/workspace/hooks/*.test.mjs"` (a folder argument fails on Node 24).
- Further gates and sequencing: `docs/agents/verify.md`. Known failure modes: `docs/agents/failure-modes.md`.
