# The `## Docs Layout` Contract

`audit-docs` and `refine-docs` hold no paths of their own. Everything repo-specific —
where code lives, which file documents it, which glossary holds its vocabulary — comes from a
`## Docs Layout` block in `docs/agents/domain.md`.

That indirection is the whole portability story. The same two skills run against a Go+React
monorepo, a Rust workspace, or a single-package Python library; only the block changes.

## Why `docs/agents/domain.md` and not `GLOSSARY.md`

`GLOSSARY.md` is a glossary and nothing else — `domain-modeling` states it must be "totally
devoid of implementation details." Path globs and doc-tier thresholds are exactly that.
`docs/agents/domain.md` is the per-repo agent config file that `setup-matt-pocock-skills`
already writes and that other skills already read. The layout block belongs there.

Do not move this config into any `GLOSSARY.md`, and do not edit `setup-matt-pocock-skills` or
`domain-modeling` to accommodate it. The block is additive: those skills ignore it, these two read it.

## Reading the block

1. Read `docs/agents/domain.md`. If it has a `## Docs Layout` block, that is the truth — use it and do not second-guess it against the filesystem.
2. No block? **Infer** the layout by exploring (see below), state the inference you made, and work from it.
3. A table that's absent means that concern doesn't exist here — skip the matching step silently rather than reporting the whole repo as a gap.

Verify paths from the block resolve before reporting against them. A path in the block that
doesn't exist on disk is itself a finding — the block has drifted from the repo.

## Inferring a layout (no block yet)

Follow the Matt Pocock defaults, which most repos satisfy already:

| Signal                       | Inference                                                       |
| ---------------------------- | ---------------------------------------------------------------- |
| `GLOSSARY.md` at root        | Single-context. That's the only glossary.                        |
| `GLOSSARY-MAP.md` at root    | Multi-context. It points at one `GLOSSARY.md` per context — those are the glossaries. |
| `docs/adr/`                  | ADR location. Also check `<context>/docs/adr/` for scoped decisions. |
| `ARCHITECTURE*.md` in `docs/` | Reference docs.                                                 |
| No `ARCHITECTURE*.md` at all | This repo keeps no reference docs. Audit glossary + ADR coverage only; do not invent an ARCHITECTURE file. |
| Package/module dirs with their own manifest (`go.mod`, `Cargo.toml`, `package.json`, `pyproject.toml`) or a workspace glob | Candidate code units. |

A single-context repo with a root `GLOSSARY.md`, `docs/adr/`, and no reference docs is a
perfectly valid input. It just means most audit steps report "not applicable."

After inferring, offer to persist the block — an inferred layout re-derived every run is
where drift comes from.

## Writing the block

Emit only the tables the repo actually has. Every path relative to the repo root.

````markdown
## Docs Layout

> Read by `audit-docs` and `refine-docs`. Those skills carry no hardcoded paths — this
> block is the only place this repo's layout lives. Drop a table and the matching audit
> step is skipped. Format spec: `.claude/skills/refine-docs/references/docs-layout.md`.

**Layout:** single-context | multi-context

### Glossaries

| Scope | File |
| ----- | ---- |
| Root  | `GLOSSARY.md` |

### Reference docs

| Scope | File |
| ----- | ---- |
| Root  | `docs/ARCHITECTURE.md` |

### Topic guides

| Subject | Guide |
| ------- | ----- |
| Auth flows | `docs/AUTHENTICATION.md` |

### Code units

| Unit | Where | Registry | Documented in | Vocab in |
| ---- | ----- | -------- | ------------- | -------- |
| Crate | `crates/*/` | `docs/ARCHITECTURE.md` → `### Crates` | `docs/ARCHITECTURE.md` | `GLOSSARY.md` |

### Deep-context tier

| Key | Value |
| --- | ----- |
| Nominate if | 15+ files |
| Flag only if | AND non-trivial state/status logic, or multiple sub-concepts |
| Never flag | scaffold-shaped CRUD / master-data / lookup units, whatever their file count |

| Unit | Glossary path | Registered in |
| ---- | ------------- | ------------- |
| Crate | `crates/<unit>/docs/GLOSSARY.md` | `GLOSSARY.md` → `## Crate Context Map` |

### ADRs

| Key | Value |
| --- | ----- |
| Location | `docs/adr/NNNN-title.md` |
| Format | `.claude/skills/domain-modeling/ADR-FORMAT.md` |

### Preferred terms

| Use | Not | Scope |
| --- | --- | ----- |
| `Handler` | endpoint, route | `docs/ARCHITECTURE-BACKEND.md` |

### Plan runner

| Key | Value |
| --- | ----- |
| Plan writer | `writing-great-plan` |
| Executor | `execute-plan` |
| Plan output | `.scratch/triage/docs-audit-<timestamp>/IMPLEMENTATION_PLAN.md` |
````

## Table semantics

**Glossaries** — every `GLOSSARY.md` the skills may edit. Each one holds vocabulary only, with
no exceptions.

**Reference docs** — where architecture patterns, diagrams, and flows live. Absent means the
repo keeps none; audit glossaries and ADRs only.

**Topic guides** — single-subject docs, each owning its topic end-to-end (auth, i18n, testing,
a tool, a feature walkthrough). This table is the content router: a subject listed here is
documented in its guide, never duplicated into a reference doc. `refine-docs` extends the
owning guide and cross-links; `audit-docs` treats guide-covered subjects as documented. Absent
table means the repo folds everything into its reference docs — then don't invent guides.

**Code units** — the generic abstraction that replaces per-language hardcoding. A unit is any
independently-documented chunk of code: a Go module, a React feature, a Rust crate, a Python
package, a service. `Where` is a glob. `Documented in` and `Vocab in` must each name a file
from the tables above.

`Registry` and `Documented in` do different jobs, and conflating them is what makes an audit
scream. A **registry** is a table that must enumerate every unit — a missing row is a real,
cheap gap. **Documented in** teaches patterns by worked example, so only a unit that *deviates*
from the pattern belongs there. Without this split, an audit reports every conventional unit as
undocumented and demands prose that would duplicate the pattern N times. Set `Registry` to `—`
when a unit type has none; then only deviation and vocabulary are checked.

**Deep-context tier** — omit entirely if the repo doesn't use a per-unit glossary tier. Keep the
qualitative gate mandatory: where a scaffold generates one-file-per-operation, file count
measures scaffold output, not complexity, and a raw threshold flags every average-sized unit.

Give the tier **one row per Unit name** from the Code units table, spelling out that unit type's
own glossary path and registration table. A single `<unit>/docs/GLOSSARY.md` placeholder shared
across unit types is not enough: an agent resolving it will quietly write a backend module's
glossary into the frontend tree and register it in the frontend's map, because that's where the
only existing Context Map lives. The wrong file gets created, and the next audit sees a file and
reports no gap.

**Preferred terms** — drives the consistency check. `Scope` is required: a term policy names a
layer, and outside that layer the same word is often correct (`endpoint` is wrong for a Go
handler but is RTK Query's own API). Absent table means no terminology policy; skip the check.

**Plan runner** — `Plan writer` is the skill that owns plan format (Weight, atomicity,
template); `audit-docs` hands it the grouping instead of re-deriving those rules. `Executor`
runs the finished plan. Absent means neither is installed: report findings and offer direct
edits, or fall back to a plain checklist.
