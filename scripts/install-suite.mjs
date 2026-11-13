#!/usr/bin/env node
// Installs the mattpocock/skills suite into this repo's .claude/skills/ for a
// maintainer. The pinned ref lives in one place only: the `npx skills add
// 'mattpocock/skills#<ref>' ...` line in a code block of README.md. This script
// reads that line and runs it with `-a claude-code -y` from the repo root.
//
// Run it once after `npm install`, and again when the pinned ref in README.md
// changes. It is not part of `prepare` on purpose: `npm install` also runs in CI,
// and contributors should not download third-party code without asking.
//
// The installed skills and skills-lock.json are git-ignored and must never be
// committed (docs/adr/0001).

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const readme = join(repo, "README.md");

function fail(message) {
  console.error(`install-suite: ${message}`);
  process.exit(1);
}

// Splits a shell-like line into words, honouring single and double quotes.
function words(line) {
  const out = [];
  const pattern = /'([^']*)'|"([^"]*)"|(\S+)/g;
  let match;
  while ((match = pattern.exec(line)) !== null) out.push(match[1] ?? match[2] ?? match[3]);
  return out;
}

const lines = readFileSync(readme, "utf8").split("\n");
let command = null;
for (let i = 0; i < lines.length && command === null; i++) {
  if (!/^npx skills add\s+'mattpocock\/skills#/.test(lines[i])) continue;
  let joined = lines[i];
  // Follow trailing backslashes onto the next line.
  while (joined.endsWith("\\") && i + 1 < lines.length) joined = joined.slice(0, -1) + " " + lines[++i];
  command = joined;
}
if (command === null) {
  fail("no line starting with `npx skills add 'mattpocock/skills#` found in README.md");
}

// Drop `npx skills` and any -a/-y the line carries, then add ours once.
const args = [];
const parts = words(command).slice(2);
for (let i = 0; i < parts.length; i++) {
  if (parts[i] === "-a") i++;
  else if (parts[i] !== "-y") args.push(parts[i]);
}
args.push("-a", "claude-code", "-y");

console.log(`install-suite: npx skills ${args.join(" ")}`);
const result = spawnSync("npx", ["skills", ...args], { cwd: repo, stdio: "inherit" });
if (result.error) fail(result.error.message);
process.exit(result.status ?? 1);
