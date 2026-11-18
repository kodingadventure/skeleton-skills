import test, { before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { activeRows, rootFromInstructions, commitsInsideRoot, commitsInOtherRepo, repoOf } from "./workspace-reminder.mjs";

test("activeRows reads the Active table, with and without outer pipes", () => {
  const md = [
    "# Workspaces",
    "## Active",
    "| Slug | Goal | Areas |",
    "| ---- | ---- | ----- |",
    "| alpha | a goal | src/a |",
    "beta | b goal | src/b",
    "| <slug> | placeholder | x |",
    "## Shipped",
    "| gamma | 2026-01-01 | src/g |",
  ].join("\n");
  assert.deepEqual(activeRows(md), [
    { slug: "alpha", areas: "src/a" },
    { slug: "beta", areas: "src/b" },
  ]);
});

test("activeRows returns [] without an Active section", () => {
  assert.deepEqual(activeRows("# nothing\n## Shipped\n| a | b |"), []);
});

test("rootFromInstructions reads the Workspace root line", () => {
  assert.equal(rootFromInstructions("Workspace root: `docs/workspaces/`"), "docs/workspaces");
  assert.equal(rootFromInstructions("- Workspace root: notes/ws"), "notes/ws");
  assert.equal(rootFromInstructions("no such line"), null);
});

test("a plain commit is not inside the root even when the folder name appears in the command", () => {
  const cmd = 'cd backend && git commit -m "update docs"';
  assert.equal(commitsInsideRoot(cmd, "/proj", "docs/workspaces"), false);
});

test("cd or -C into the root is inside", () => {
  assert.equal(commitsInsideRoot("cd docs/workspaces && git commit -m x", "/proj", "docs/workspaces"), true);
  assert.equal(commitsInsideRoot("git -C docs/workspaces/foo commit -m x", "/proj", "docs/workspaces"), true);
  assert.equal(commitsInsideRoot("cd .scratch/workspaces && git commit -m x", "/proj", "docs/workspaces"), true);
});

test("a command without cd or -C is never inside", () => {
  assert.equal(commitsInsideRoot('git commit -m "docs/workspaces"', "/proj", "docs/workspaces"), false);
});

// Fixture: a project repo with a separate notes repo inside it, a sibling repo,
// a worktree-style `.git` file, and a folder with no repo.
let t;
let proj;
before(() => {
  t = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "wr-")));
  proj = path.join(t, "proj");
  for (const d of ["proj/.git", "proj/_local/.git", "proj/_local/workspaces/x", "proj/src", "proj/docs/workspaces", "other/.git", "wt", "nogit"]) {
    fs.mkdirSync(path.join(t, d), { recursive: true });
  }
  fs.writeFileSync(path.join(t, "wt/.git"), "gitdir: x\n");
});
after(() => fs.rmSync(t, { recursive: true, force: true }));

const ROOT = "_local/workspaces";
const silent = (command, cwd, root = ROOT) => commitsInsideRoot(command, proj, root, cwd) || commitsInOtherRepo(command, proj, cwd);

test("git -C into the notes repo is a commit in another repository", () => {
  assert.equal(silent("git -C _local commit -m x", proj), true);
  assert.equal(commitsInOtherRepo("git -C _local commit -m x", proj, proj), true);
});

test("cd into the notes repo is silent; cwd is the shell directory after the command", () => {
  assert.equal(silent("cd _local && git commit -m x", path.join(proj, "_local")), true);
});

test("git -C into a workspace inside the notes repo is silent", () => {
  assert.equal(silent("git -C _local/workspaces/x commit -m x", proj), true);
});

test("a bare commit from a shell already inside the notes repo is silent", () => {
  assert.equal(silent("git commit -m x", path.join(proj, "_local")), true);
});

test("a commit in the project's own repository is not silent", () => {
  assert.equal(silent("git commit -m x", proj), false);
  assert.equal(silent("git commit -m x", path.join(proj, "src")), false);
});

test("git -C into a sibling repository is silent", () => {
  assert.equal(silent("git -C ../other commit -m x", proj), true);
});

test("a root without its own repository stays silent through the old path check", () => {
  assert.equal(silent("git -C docs/workspaces commit -m x", proj, "docs/workspaces"), true);
  assert.equal(commitsInOtherRepo("git -C docs/workspaces commit -m x", proj, proj), false);
});

test("repoOf finds the nearest .git entry, folder or file", (t2) => {
  assert.equal(repoOf(path.join(t, "wt")), path.join(t, "wt"));
  assert.equal(repoOf(path.join(proj, "src")), proj);
  assert.equal(repoOf(path.join(proj, "_local/workspaces/x")), path.join(proj, "_local"));
  if (repoOf(path.join(t, "nogit")) !== null) {
    t2.skip("a .git entry exists above the temp directory");
    return;
  }
  assert.equal(repoOf(path.join(t, "nogit")), null);
});

test("a project without a repository: a plain commit is not silent", () => {
  const nogit = path.join(t, "nogit");
  assert.equal(commitsInOtherRepo("git commit -m x", nogit, nogit), false);
  assert.equal(commitsInsideRoot("git commit -m x", nogit, ROOT, nogit), false);
});
