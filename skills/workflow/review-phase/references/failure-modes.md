# Failure modes reference

The format a consuming repo's own `docs/agents/failure-modes.md` follows. `to-plan` reads that
file to fill each phase's `Prone to:` line; `review-phase` step 4 reads it to know what to probe on
a phase it's reviewing. If the file doesn't exist in a repo, both skills skip it — this file is
what to create, not something either skill requires.

## Format

One entry per failure mode:

```markdown
## <short-name>

**Shows up as:** <how you'd notice it without knowing to look — the symptom>
**Probe:** <the concrete check that surfaces it — a command, a diff pattern, a question to ask the code>
```

`<short-name>` is what a phase's `Prone to:` line cites, e.g. `Prone to: generated-file-also-hand-edited`.

## Growth

This file is per-repo and grows by accident, not by design. Add an entry when a defect actually
gets through review — never speculatively. A mode nobody has hit yet is a guess, and a guess in a
probe list spends the reviewer's budget on nothing.

## Starter set

Four modes recur across enough codebases to seed a new repo's file with. Each is stated
generically — replace or extend with what this specific repo actually produces.

## generated-file-also-hand-edited

**Shows up as:** a regenerate step (codegen, a swagger/schema build, a scaffolding script) silently
reverts a manual fix, because the fix landed in the generated file instead of its source.
**Probe:** re-run the generator on the touched file and diff the result against what's staged — a
manual edit that survives is safe; one that doesn't was never in the source.

## green-gates-not-a-working-app

**Shows up as:** lint/typecheck/build all pass, but the feature does nothing when exercised — the
gates check that the code compiles, not that it runs.
**Probe:** exercise the feature in its enabled state, end to end, not just its off-path.

## write-before-validate

**Shows up as:** a script or migration writes output before checking its preconditions, so a bad
input leaves a half-written file or table instead of failing clean.
**Probe:** run it once against a deliberately invalid input and inspect what got written before the
failure.

## fresh-scaffold-is-not-an-aged-consumer

**Shows up as:** a fix verified against a just-scaffolded project works, then breaks on a real
project that has since diverged (extra deps, custom config, prior migrations).
**Probe:** re-run the same check against an existing, non-trivial consumer repo, not only the
disposable scaffold used to develop the fix.
