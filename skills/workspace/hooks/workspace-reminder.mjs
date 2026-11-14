#!/usr/bin/env node
// PostToolUse hook (matcher: Bash) for the feature workspace skills.
//
// After a `git commit`, when `.scratch/workspaces/INDEX.md` lists active
// workspaces, it reminds the agent to keep the matching workspace current
// (WHATNEXT.md, TRACKER.md, the INDEX.md row). A session that never opened
// the workspace does not know its conventions; this is the nudge it misses.
// Silent otherwise: no commit, no INDEX.md, no active row, or a commit inside
// the workspace root, in `.scratch`, or in another git repository (for example
// a separate repository for the notes above the workspace root).
//
// Install: copy to .claude/hooks/ and register in .claude/settings.json:
//   "hooks": { "PostToolUse": [{ "matcher": "Bash", "hooks": [{
//     "type": "command",
//     "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/workspace-reminder.mjs\"",
//     "timeout": 10 }] }] }
// A ready-to-copy version of this block is settings-snippet.json next to this file.
// The workspace root is WORKSPACE_ROOT (relative to the project directory)
// when set, else the `Workspace root:` line of the project's CLAUDE.md or
// AGENTS.md (see kickoff/references/workspace-root.md), else .scratch/workspaces.

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
  return ".scratch/workspaces";
}

// The repository a folder belongs to: the nearest ancestor (the folder itself
// included) holding a `.git` entry, a folder or, in a worktree, a file. Null
// when there is none.
export function repoOf(dir) {
  let d = path.resolve(dir);
  for (;;) {
    if (fs.existsSync(path.join(d, ".git"))) return d;
    const parent = path.dirname(d);
    if (parent === d) return null;
    d = parent;
  }
}

// Where the commit runs, and whether the command moved away from startDir.
// Follows the command's `cd <dir>` and `git -C <dir>` targets as paths. With
// afterCommand set, startDir is the shell's directory after the command ran
// (the hook input's `cwd`), so a `cd` target is already reflected in it and
// only the `git -C` targets after the last `cd` still apply.
function resolveCommit(command, startDir, afterCommand) {
  const target = /(?:\bcd\s+|\bgit\s+(?:\S+\s+)*?-C\s+)("[^"]+"|'[^']+'|[^\s;&|]+)/g;
  const start = path.resolve(startDir);
  let dir = start;
  let moved = false;
  for (const m of command.matchAll(target)) {
    if (afterCommand && /^cd\b/.test(m[0])) {
      dir = start;
      moved = false;
      continue;
    }
    dir = path.resolve(dir, m[1].replace(/^["']|["']$/g, ""));
    moved = true;
  }
  return { dir, moved };
}

// The folder a `git commit` command runs in. startDir is the project
// directory, or the hook input's `cwd` when afterCommand is true.
export function commitDir(command, startDir, afterCommand = false) {
  return resolveCommit(command, startDir, afterCommand).dir;
}

// True when the commit runs from a directory inside the workspace root (or
// inside `.scratch`). A folder name that merely appears elsewhere in the
// command does not count. With `cwd` (the shell's directory after the
// command) the shell itself may already sit inside the root.
export function commitsInsideRoot(command, projectDir, root, cwd) {
  const rootAbs = path.resolve(projectDir, root);
  const scratchAbs = path.resolve(projectDir, ".scratch");
  const inside = (dir, base) => {
    const rel = path.relative(base, dir);
    return rel === "" || (!rel.startsWith("..") && !path.isAbsolute(rel));
  };
  const { dir, moved } = resolveCommit(command, cwd ?? projectDir, cwd != null);
  return (moved || cwd != null) && (inside(dir, rootAbs) || inside(dir, scratchAbs));
}

// True when the commit lands in a different git repository than the project's,
// such as a separate repository for the workspace notes.
export function commitsInOtherRepo(command, projectDir, cwd) {
  const dir = commitDir(command, cwd ?? projectDir, cwd != null);
  return repoOf(dir) !== repoOf(projectDir);
}

function main() {
  const input = readStdin();
  const command = input?.tool_input?.command ?? "";
  // `git commit`, `git -C x commit`, `git commit -am` …, not inside .scratch.
  if (!/\bgit\b(\s+-\S+(\s+\S+)?)*\s+commit\b/.test(command)) return;
  const projectDir = process.env.CLAUDE_PROJECT_DIR || input?.cwd || ".";
  const root = workspaceRoot(projectDir);
  const cwd = input?.cwd;
  // A commit inside the workspace root, or in another git repository (such as
  // a separate repository for the notes), is not project work.
  if (commitsInsideRoot(command, projectDir, root, cwd) || commitsInOtherRepo(command, projectDir, cwd)) return;
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
