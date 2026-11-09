#!/usr/bin/env node
// PostToolUse hook (matcher: Bash) for the feature workspace skills.
//
// After a `git commit`, when `.scratch/plan/INDEX.md` lists active
// workspaces, it reminds the agent to keep the matching workspace current
// (WHATNEXT.md, TRACKER.md, the INDEX.md row). A session that never opened
// the workspace does not know its conventions; this is the nudge it misses.
// Silent otherwise: no commit, no INDEX.md, or no active row.
//
// Install: copy to .claude/hooks/ and register in .claude/settings.json:
//   "hooks": { "PostToolUse": [{ "matcher": "Bash", "hooks": [{
//     "type": "command",
//     "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/workspace-reminder.mjs\"",
//     "timeout": 10 }] }] }
// The workspace root is WORKSPACE_ROOT (relative to the project directory)
// when set, else the `Workspace root:` line of the project's CLAUDE.md or
// AGENTS.md (see kickoff/references/workspace-root.md), else .scratch/plan.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function readStdin() {
  try {
    return JSON.parse(fs.readFileSync(0, "utf8"));
  } catch {
    return null;
  }
}

// Rows of the `## Active` table, as { slug, areas }. Accepts both
// `a | b` and `| a | b |` tables; skips the header and separator rows.
export function activeRows(markdown) {
  const lines = markdown.split("\n");
  const start = lines.findIndex((l) => /^##\s+Active\s*$/.test(l));
  if (start === -1) return [];
  const rows = [];
  for (const line of lines.slice(start + 1)) {
    if (/^##\s/.test(line)) break;
    if (!line.includes("|")) continue;
    const cells = line
      .replace(/^\s*\|/, "")
      .replace(/\|\s*$/, "")
      .split("|")
      .map((c) => c.trim());
    const slug = cells[0];
    if (!slug || /^-+$/.test(slug) || slug === "Slug" || slug.startsWith("<")) continue;
    rows.push({ slug, areas: cells[cells.length - 1] ?? "" });
  }
  return rows;
}

// The path on a `Workspace root: \`<path>\`` line, or null. Backticks
// optional; a trailing slash is dropped.
export function rootFromInstructions(markdown) {
  const m = /^[\s>*-]*Workspace root:\s*`?([^`\s]+)`?/m.exec(markdown);
  return m ? m[1].replace(/\/+$/, "") : null;
}

function workspaceRoot(projectDir) {
  if (process.env.WORKSPACE_ROOT) return process.env.WORKSPACE_ROOT;
  for (const name of ["CLAUDE.md", "AGENTS.md"]) {
    const file = path.join(projectDir, name);
    if (!fs.existsSync(file)) continue;
    const root = rootFromInstructions(fs.readFileSync(file, "utf8"));
    if (root) return root;
  }
  return ".scratch/plan";
}

function main() {
  const input = readStdin();
  const command = input?.tool_input?.command ?? "";
  // `git commit`, `git -C x commit`, `git commit -am` …, not inside .scratch.
  if (!/\bgit\b(\s+-\S+(\s+\S+)?)*\s+commit\b/.test(command)) return;
  const projectDir = process.env.CLAUDE_PROJECT_DIR || input?.cwd || ".";
  const root = workspaceRoot(projectDir);
  // A commit inside the workspace root's own repository is not project work.
  const top = root.split("/")[0];
  if ((/\.scratch\b/.test(command) || command.includes(top)) && /\bcd\b|-C\b/.test(command)) return;
  const indexPath = path.join(projectDir, root, "INDEX.md");
  if (!fs.existsSync(indexPath)) return;

  const rows = activeRows(fs.readFileSync(indexPath, "utf8"));
  if (rows.length === 0) return;

  const list = rows.map((r) => `${r.slug} (areas: ${r.areas})`).join("; ");
  const context =
    `A commit just landed while feature workspaces are active: ${list}. ` +
    `If this commit moved one of them (it touches its areas or finishes a step in its WHATNEXT.md), ` +
    `keep that workspace current before the session ends, per its CONTEXT.md conventions: ` +
    `WHATNEXT.md State now and Next steps, the TRACKER.md item status and one Action Log row, ` +
    `and its ${root}/INDEX.md row — or run \`/tracker <slug> log\`. ` +
    `Skip it if execute-plan or review-phase already did this for the commit, ` +
    `or if the commit is unrelated to every active workspace (unrelated work gets no tracker rows).`;

  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PostToolUse",
        additionalContext: context,
      },
    }),
  );
}

// Compare real paths: Node resolves a symlinked entry script to its target
// for import.meta.url but not for process.argv[1], so a hook installed as a
// symlink would otherwise never run.
function isEntryScript() {
  try {
    return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}

if (isEntryScript()) main();
