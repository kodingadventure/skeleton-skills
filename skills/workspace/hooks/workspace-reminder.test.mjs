import test from "node:test";
import assert from "node:assert/strict";
import { activeRows, rootFromInstructions, commitsInsideRoot } from "./workspace-reminder.mjs";

test("activeRows reads the Active table, with and without outer pipes", () => {
  const md = [
    "# Workspaces",
    "## Active",
    "| Slug | Goal | Areas |",
    "| ---- | ---- | ----- |",
    "| alpha | a goal | src/a |",
    "beta | b goal | src/b",
    "| <slug> | placeholder | x |",
    "## Seeded",
    "| gamma | g | src/g |",
  ].join("\n");
  assert.deepEqual(activeRows(md), [
    { slug: "alpha", areas: "src/a" },
    { slug: "beta", areas: "src/b" },
  ]);
});

test("activeRows returns [] without an Active section", () => {
  assert.deepEqual(activeRows("# nothing\n## Seeded\n| a | b |"), []);
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
