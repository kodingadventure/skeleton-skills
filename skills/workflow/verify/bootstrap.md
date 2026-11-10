# Bootstrap `docs/agents/verify.md`

Reached when [`verify`](SKILL.md) finds no config. Produce one, then continue the run that sent you here.

This is the cold start. Read at most five files and run each candidate command once. Stuck on mechanics unrelated to the change → report `BLOCKED` naming exactly where.

## Find the facts

Read, don't assume. Look for the real command names, not the conventional ones:

- Task runner config — the `scripts` block of `package.json`, `Makefile`,
  `Taskfile.yml`, `justfile`, `Cargo.toml`, then `moon.yml`
- `README.md` / `CONTRIBUTING.md` — the build and run instructions
- CI workflow files — what the project already trusts as a gate
- The directory layout — one stack or several? `<group>/*` directories with
  their own configs mean per-path gates; a single `src/` means one row

Run each candidate gate command once to confirm it exists and passes on a clean tree. A command you wrote from a guess is worse than no row.

## Ask the human one thing

**Runtime policy is a judgement call, not a fact you can read.** Ask whether the agent may start the app itself, or whether the human drives. Their answer
decides how every future run ends. The bounded surfaces — test suites that boot a real server, headless browser runs — are usually granted; long-running
dev servers usually are not.

## Write it

Fill this shape. Drop rows that don't apply — a single-stack project is one gate row and a short surface table, and that is a complete config.

```markdown
# Verify Config — <project>

Read by the `verify` skill. Stacks: <name them>.

## Gates

| Touched path | Gates (in order) |
| ------------ | ---------------- |
| `<glob>`     | `<command>`      |

<Any rule about gate order, e.g. build before lint — linting uncompilable
code reports noise.>

## Sequencing

- <Generator or codegen step> → run **before** <the gate that consumes its
  output>.

## Routing

| Failure                 | Skill or action |
| ----------------------- | --------------- |
| `<linter / error kind>` | `<skill>`       |

<What is _not_ a gate — periodic quality passes, coverage — and what runs
them instead.>

## Runtime policy

<Whether the agent may start the app. State it as what the agent does, not
only what it may not.>

Surfaces the agent may drive itself:

- `<command>` — <what it exercises>

## Surfaces

| Change reaches   | Surface               |
| ---------------- | --------------------- |
| `<path or kind>` | <where to observe it> |
```

## Confirm

Show the human the draft before writing it. They know which commands they actually trust.

No human to ask (you run as a sub-agent)? Do not write `docs/agents/verify.md`. Return the draft in your report with the verdict `BLOCKED — config draft`.
