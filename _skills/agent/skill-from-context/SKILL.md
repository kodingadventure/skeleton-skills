---
name: skill-from-context
description: >
  Captures a repeatable pattern from this conversation into a new or refined skill. Use when the user asks to capture a pattern as a skill, when the agent
  has produced a structurally similar solution 2+ times, or when a gap surfaces in an existing skill. Do not use for one-off work that won't repeat, or to
  draft a skill from an idea with no concrete example — write that directly
  with `writing-for-agents` instead.
---

# Skill From Context

Turn a pattern from this conversation into a skill — new or refined.

Everything about **how** to write a skill well — description wording, structure, pruning, leading words — belongs to `writing-for-agents`, with the
skill-only mechanics (frontmatter, invocation choice, router skills) disclosed to its `SKILL-MECHANICS.md`. Read both before writing or editing any `SKILL.md`. This file covers only what's specific to extracting a pattern out of a conversation.

## 1. Confirm the pattern is real

Find at least 2 concrete instances in this conversation — code, edits, workflow steps, or decisions the agent repeated or would repeat — and be able
to say what's invariant (always true) versus variable (changes per use).

- Clear on both → go to step 2.
- Not clear — fuzzy scope, only one instance, or you can't tell what should
  generalize — **stop**. Ask the user directly what should generalize, or offer to run `grilling` to work it out with them.

## 2. Generate or refine

Search existing skills for name/description overlap first.

- No existing skill covers this pattern → **generate**: scaffold a new skill
  file at wherever this project keeps its skills (e.g. `.claude/skills/<kebab-name>/SKILL.md`
  for Claude Code — check the project's convention, or ask if unclear), built from the conversation examples generalized into invariant structure plus
  parameterized variables. Append `<!-- DRAFT: review before first use -->`.
- An existing skill is close but has a gap (missing trigger, missing step,
  wrong abstraction, missing anti-pattern) → **refine**: edit that skill in place to close the gap.
- Overlap already covers the pattern fully, or it's ambiguous which mode
  applies → ask the user.

## 3. Validate and present

Re-check the new or edited skill against `writing-for-agents` — description triggers, information hierarchy, pruning, failure modes — and fix anything
that falls short. Then show the user: name + description (or the diff, for a refine), the source examples it generalizes from, and the invariant/variable
split. For a new skill, confirm the draft marker is still in place.

Get explicit approval before treating the skill as done — never remove the draft marker, or call a refine final, without it.
