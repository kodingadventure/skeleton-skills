# Deep-Context Glossary Template

Use when a **code unit** — whatever the `## Docs Layout` block calls them: backend module,
frontend feature, crate, package, service — is complex enough to need its own `docs/GLOSSARY.md`:
business vocabulary plus a file-responsibility map for that one unit.

This is the layout's **Deep-context tier**. If the block has no such table, this repo doesn't use
the tier — don't introduce it here. Read the block for the real threshold, location pattern, and
registration table; the values below are only the common defaults.

## When to create one

Any of:

- The unit's folder has 15+ files
- Non-trivial state/status logic (multi-step completion, status computed from child state)
- Multiple sub-concepts under one unit (several sub-folders, each with their own files)
- A bug report references business terms that don't map obviously to file names by grepping

Skip it for simple CRUD/master-data units — the scope glossary + reference docs already cover those.

## Template

```markdown
# Context: <Unit Name> Domain Vocabulary

<One sentence: what business capability this unit covers.>

## Business Glossary

**<Term>** = <one-line definition — business meaning, not code meaning>
**<Term>** = <one-line definition>

## File Map

| File     | Responsibility           |
| -------- | ------------------------ |
| `<file>` | <what it owns, one line> |
| `<file>` | <what it owns, one line> |

## Related Documentation

- [GLOSSARY.md](<relative path to the scope glossary>) — scope-level tech-stack vocabulary
```

## Rules

Same golden rule as every other glossary:

- Terse — 1–2 lines per term/file. No code samples, no diagrams, no prose explanations.
- **Business meaning, not code meaning.** If a term's definition just restates the type signature, it doesn't belong.
- **The File Map covers every file** in the folder (or every file in the complex sub-area), one line each. This is the part that lets an agent jump straight to the 2–3 relevant files instead of reading all 28.
- **Register it** in the scope glossary's Context Map table — the layout's `Registered in` value names which one. An orphaned deep-context glossary with nothing pointing at it is dead weight.
- Fix the relative depth of the link out — it varies with how deep the unit sits.

## Not a template to copy

This tier is **specific business vocab for one unit**. Unlike scope glossaries, which can be
copied between sibling apps and customized, a unit's deep-context glossary must never be copied
to bootstrap another unit's. Write each one from that unit's own code.
