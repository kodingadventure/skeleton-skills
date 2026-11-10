---
name: skill-from-context
description: >
  Captures a repeatable pattern from this conversation into a new or refined skill; requires the `writing-for-agents` skill (from `mattpocock/skills`).
  Use when the user asks to capture a pattern as a skill, or after the user agrees to your offer when you see the same solution twice or a gap in an
  existing skill. Do not use for one-off work that won't repeat, or to
  draft a skill from an idea with no concrete example — write that directly
  with `writing-for-agents` instead.
---

# Skill From Context

Turn a pattern from this conversation into a skill — new or refined.

If you notice a pattern yourself (the same solution twice, or a gap in an existing skill), do not start this skill: say once that the pattern appeared twice and ask whether the user wants it captured. Start only after the user agrees.

If the `writing-for-agents` skill is not installed, stop and tell the user to install it from `mattpocock/skills` (see this repo's README for the pinned command); do not write a skill without it.

Everything about **how** to write a skill well — description wording, structure, pruning, leading words — belongs to `writing-for-agents` (from `mattpocock/skills`; required for this skill), with the
skill-only mechanics (frontmatter, invocation choice, router skills) disclosed to its `SKILL-MECHANICS.md`. The frontmatter that file discusses follows the agent in use. Read both before writing or editing any `SKILL.md`. This file covers only what's specific to extracting a pattern out of a conversation.

## 1. Confirm the pattern is real

Find at least 2 concrete instances in this conversation — code, edits, workflow steps, or decisions the agent repeated or would repeat — and be able
to say what's invariant (always true) versus variable (changes per use).

- Clear on both → go to step 2.
- Not clear — fuzzy scope, only one instance, or you can't tell what should
  generalize — **stop**. Ask the user directly what should generalize, or offer to run `grilling` (if installed) to work it out with them.

## 2. Generate or refine

Search existing skills for name/description overlap first, in three places: the project's skills folder, the user's install folder, and the skills in this session's list.

- No existing skill covers this pattern → **generate**: scaffold a new skill
  file at wherever your agent loads project skills from (Claude Code: `.claude/skills/<kebab-name>/SKILL.md`
  — check the project's convention, or ask if unclear), built from the conversation examples generalized into invariant structure plus
  parameterized variables. Append `<!-- DRAFT: review before first use -->`.
- An existing skill is close but has a gap (missing trigger, missing step,
  wrong abstraction, missing anti-pattern) → **refine**: edit that skill in place to close the gap. If the skill was installed from a package (it is listed in `skills-lock.json` or sits in a plugin folder), do not edit it in place: an update overwrites the edit. Offer a local copy under a new name, or a proposal to its source.
- Overlap already covers the pattern fully, or it's ambiguous which mode
  applies → ask the user.

## 3. Validate and present

Re-check the new or edited skill against `writing-for-agents` — description triggers, information hierarchy, pruning, failure modes — and fix anything
that falls short. Then show the user: name + description (or the diff, for a refine), the source examples it generalizes from, and the invariant/variable
split. For a new skill, confirm the draft marker is still in place.

Get explicit approval before treating the skill as done — never remove the draft marker, or call a refine final, without it.
