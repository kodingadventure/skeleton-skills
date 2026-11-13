#!/usr/bin/env node
// Links this catalog's own skills and agents into the repo's .claude/ folder, so
// a Claude Code session opened in this repo loads the versions being edited here.
// Runs on `npm install` (the `prepare` script); re-run with `npm run link-skills`
// after adding, removing or renaming a skill.
//
// The links stay inside this repo on purpose: a link in ~/.claude/skills would
// make the work-in-progress version active in every project, over the released
// version those projects installed. .claude/skills/ and .claude/agents/ are
// git-ignored and must never be committed (docs/adr/0001).

import { existsSync, lstatSync, mkdirSync, readdirSync, readlinkSync, rmSync, symlinkSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const skillsDir = join(repo, ".claude", "skills");
const agentsDir = join(repo, ".claude", "agents");

function link(target, path) {
  const rel = relative(dirname(path), target);
  if (existsSync(path) || isLink(path)) {
    if (isLink(path) && readlinkSync(path) === rel) return false;
    rmSync(path, { recursive: true, force: true });
  }
  symlinkSync(rel, path);
  return true;
}

function isLink(path) {
  try {
    return lstatSync(path).isSymbolicLink();
  } catch {
    return false;
  }
}

mkdirSync(skillsDir, { recursive: true });
mkdirSync(agentsDir, { recursive: true });

const wanted = new Map();
for (const group of readdirSync(join(repo, "skills"), { withFileTypes: true })) {
  if (!group.isDirectory()) continue;
  for (const skill of readdirSync(join(repo, "skills", group.name), { withFileTypes: true })) {
    const dir = join(repo, "skills", group.name, skill.name);
    if (skill.isDirectory() && existsSync(join(dir, "SKILL.md"))) wanted.set(skill.name, dir);
  }
}
// Maintainer-only skill, present only where the private _local/ repo is checked out.
const backflow = join(repo, "_local", "backflow");
if (existsSync(join(backflow, "SKILL.md"))) wanted.set("backflow", backflow);

let changed = 0;
for (const [name, dir] of wanted) if (link(dir, join(skillsDir, name))) changed++;

// Drop links to skills that no longer exist; leave anything that is not a link alone.
for (const name of readdirSync(skillsDir)) {
  const path = join(skillsDir, name);
  if (!wanted.has(name) && isLink(path)) {
    rmSync(path);
    changed++;
  }
}

const agentSrc = join(repo, "plugins", "phase-agents", "agents");
for (const file of readdirSync(agentSrc)) {
  if (file.endsWith(".md") && link(join(agentSrc, file), join(agentsDir, file))) changed++;
}

console.log(`link-skills: ${wanted.size} skills linked into .claude/skills (${changed} changed)`);

// Reminder only: no network, nothing installed. The suite is installed on request
// by `npm run install-suite`, never from `prepare`.
if (!existsSync(join(skillsDir, "domain-modeling"))) {
  console.log("link-skills: run npm run install-suite to install the mattpocock/skills suite (see CONTRIBUTING.md)");
}
