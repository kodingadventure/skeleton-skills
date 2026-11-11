# Failure modes

Repo-specific catalog `to-plan` reads to fill each phase's `Prone to:` line, and `review-phase`
reads to know what to probe. See `skills/workflow/review-phase/references/failure-modes.md` for
the format this file follows and when to add an entry.

## skill-in-one-place-only

**Shows up as:** a skill installs or lists incorrectly because only some of its required locations
were updated.
**Probe:** confirm the directory, the manifest entry, and the README bullet all exist — a directory
with no manifest entry is uninstallable and nothing else catches it.

## manifest-unparseable

**Shows up as:** every skill in the repo becomes uninstallable because `marketplace.json` is
malformed.
**Probe:** `node -e "JSON.parse(...)"` against the file — the only gate.

## rule-added-enforcement-surface-untouched

**Shows up as:** a rule lands in the prose that states it while the surface that enforces it keeps
the old shape, so verification that only reads the new prose passes.
**Probe:** name the surface the rule governs (a template, a report form, a registration list) and
check the rule reached *it*, not just its description.

## rename-sweep-reads-empty-as-clean

**Shows up as:** a repo-wide rename is declared finished while references remain, because the
sweep's pattern could not match them. A grep for `CONTEXT(-MAP)?\.md` misses prose like "CONTEXT
files", and `git grep -E` with `\b` returns nothing, with no error, on macOS.
**Probe:** search the bare word, case-sensitive, and leave out `\b`. Before trusting an empty
result, confirm the same command finds a term known to be present.

## citation-drifted-in-batch

**Shows up as:** a `file:line` reference written by one phase is confidently wrong by the time
anyone reads it, because a sibling phase in the same batch inserted lines above it.
**Probe:** re-resolve every `file:line` in the diff, or cite files only.

## changeset-missing

**Shows up as:** a change under `skills/` or `plugins/` lands without a changeset, so the next
version PR and `CHANGELOG.md` leave it out.
**Probe:** `git diff --cached --name-only` lists a path under `skills/` or `plugins/` but no new
file in `.changeset/`.
