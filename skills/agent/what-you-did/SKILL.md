---
name: what-you-did
description: Builds an HTML page of recent code changes, grouped by purpose, with before/after diffs and Explain-this prompts. Use when the user asks to see or explain what was just changed in the code, or sends a message starting with `/what-you-did focus`, typed or pasted. Not for judging code quality (use code-review, if installed).
argument-hint: "[commit | A..B | workspace range like 'phase 4' or 'since the last report'] | focus <snapshot> …"
---

# What you did

The user wants to see the code that was just written, the way a reviewer reads a diff, but told as a story. The output is a **change page**: one HTML file in the OS temp directory, opened in the browser, where the changes sit in **groups**, one purpose each, every group showing its **hunks** (one block of changed lines in one file, as in `git diff`) before and after. Each hunk and each group carries an **Explain this** button that copies a prompt; pasted back to your agent, the prompt runs this skill in **focus** mode and produces a **focus page** on that one part, with its own buttons, so the user can dig as deep as they like.

`scripts/wyd.py` does the mechanical work and holds the one hard rule: **the code on a page always comes from git, through the script, never typed by you.** `collect` takes a **snapshot** of the changes (the patch, its hunks, where it came from); `new` validates your grouping against that snapshot and renders the page. `generated.txt` lists the files written by tools (generated API clients, Swagger output, lockfiles); their hunks are folded into one "generated" list on their own, so they never enter a group. A project adds its own generator outputs to `.claude/what-you-did-generated.txt` or `what-you-did-generated.txt` at the repo root (same format; the script reads both), which survive skill updates.

The page reads like the `review-page` skill's pages: same look, the user's language, plain sentences. Its Mermaid rules (the `review-page` skill's Mermaid rules; `new` checks them itself when that skill is not installed) hold here too. Write raw `<br/>` in a diagram label: the script escapes it.

## Mode

- The argument, or a pasted message, starts with `focus` / `/what-you-did focus` (an Explain-this prompt): go to **Focus** below. A pasted prompt is a request for a focus page, not for an answer in chat.
- Anything else, or nothing: the steps below.

## Steps

### 1. Source and workspace

Pick the changes, in this order:

1. **An argument**: a commit (that commit alone) or a range `A..B` goes to `collect` as it is. "Since X" is `X..HEAD`; "the last 3 commits" is `HEAD~3..HEAD`.
2. **No argument**: `collect` takes every uncommitted change (staged, unstaged and untracked, each labelled on the page), or the last commit when nothing is uncommitted.

Then decide whether the changes belong to a **workspace** (a feature folder under `.scratch/workspaces/<slug>/` unless the `Workspace root:` line in `CLAUDE.md` or `AGENTS.md` names another root, listed in `INDEX.md` at that root; no such line and no `INDEX.md` means no workspace, so continue to step 2): the argument names it or uses its words, the conversation is already working in it, or the changed paths fall under the Areas of exactly one Active row of `INDEX.md`. Never pick between two workspaces: with two candidates, go without one and say so. Name the one you use in one line: `Workspace: <slug>`.

A workspace phrase in the argument becomes a git range: "phase 4" or "plan 01", "since the last report", "since checkpoint 3". Find its dates and commits in the workspace's tracker (Action Log, Report History), `WHATNEXT.md` and the plan's phase files, then confirm with `git log --format='%h %ad %s' --date=short` over that window. Say the resolved range in chat in one line. A range that also holds another workspace's commits keeps them: their hunks become an outside-plan group naming that workspace.

_Done when_ you hold one source (a range, or the uncommitted work) and know whether a workspace applies.

### 2. Collect and read

Needs Python 3 (standard library only) and git; if `python3` is missing, use `python` or `py`. `<skill-dir>` below is the folder holding this `SKILL.md`.

```bash
python3 <skill-dir>/scripts/wyd.py collect [REVS] --slug <short-topic>
```

`collect` handles three git situations with one clear sentence instead of a raw git error: outside a git repository it stops with "not a git repository: this skill reads changes through git"; in a repository with no commits it compares against the empty tree, so new files still show; with a single commit and no changes it shows that commit against the empty tree. When `collect` refuses, tell the user its sentence in plain words and what to do next (run it inside a repository, make a first change, or name a commit); do not fall back to reading files by hand.

It prints the snapshot directory, each commit of the range with its full message, and one index line per hunk (`h7  path:line  +6 -1  [label, status by 2a8f11619]  first changed line`). `by` names the commits that wrote the hunk: blame places each added line; removed lines cannot be blamed, so a hunk with removals also names every commit of the range that changed the file.

**What** a hunk does comes from the code alone: read every hunk you will group in the snapshot's `changes.patch`, and the surrounding code wherever a hunk alone does not say what it does.

**Why** comes from a **claim**: a commit message, a plan item, or something said in this conversation. A claim is written by someone who may have been wrong, hurried, or describing an earlier version, so check each one against the code before it becomes a purpose: does the code do what the claim says, no more and no less? Read the message of the commits the index names for that hunk, never a neighbouring commit's. A commit message covers its whole commit, so one that also speaks of other groups is fine; the part about this group must hold. A plan item can drift the same way: the plan asked for X, the code does Y.

The page tags each purpose with its source:

- `conversation`, `plan`, `commit`: the purpose rests on that claim, and the claim holds against the code;
- `inferred`: no claim holds; you read the purpose off the code. The page marks these yellow, so the user knows which purposes to doubt.

When a claim fails, the group's purpose comes from the code (`inferred`) or from another claim that holds, and the group carries a `mismatch`: the claim in a few words, then what the code does instead. The page shows it in a yellow box. The script quotes each group's commit messages as git holds them, so the user can weigh them too; it refuses `commit` as the source of a group with a `mismatch`, or of hunks no commit wrote (uncommitted work).

In a workspace, also read its `CONTEXT.md` (language, vocabulary, decisions, findings) and the plan phase files the range covers: their checklist items, their verification steps, and the manual test docs they point to.

_Done when_ you can say, for every hunk outside the generated list, what it does (from the code) and why, every claim you used was checked against the code, and every claim that failed is written down as a mismatch.

### 3. Group

Write the grouping as a JSON file in the scratchpad or temp directory:

```json
{
  "title": "Export orders as CSV",
  "lead": "One or two sentences: what this work changed, for whom.",
  "workspace": "order-export",
  "groups": [
    {
      "title": "Export button on the orders list",
      "kind": "change",
      "source": "plan",
      "plan_item": "Orders list: export to CSV",
      "purpose": "Why this group exists, in one or two sentences (HTML allowed).",
      "mismatch": "Only when a claim failed: 'The commit message says X; the code does Y.'",
      "links": [{ "text": "Decision: export only the filtered rows", "href": "file:///abs/path/CONTEXT.md" }],
      "diagram": "flowchart TD\n  A[Orders list] --> B[Export button]",
      "notes": "Optional HTML: details the reader needs before the code.",
      "how_to_see": "Sign in as an admin, open Orders, filter by status, tap Export: the CSV holds only the filtered rows.",
      "hunks": ["h7", "h8", "h12:1-29"],
      "excerpts": [{ "file": "src/orders/OrdersPage.tsx", "rev": "HEAD", "start": 10, "end": 24, "caption": "Unchanged caller, for context" }]
    }
  ],
  "no_code": ["A plan item of this stretch of work that no hunk carries out"]
}
```

- **One purpose per group**, ordered as the story reads best: the main change first, then what it needed. Every hunk outside the generated list sits in exactly one group. `h12:30-37` puts only those lines of a hunk in a group (new-file numbering, old for a deleted file): split one big hunk, such as a whole new file, across groups this way. A group needs at least one hunk or excerpt.
- **Excerpts** show unchanged code from `rev` (a commit, or `worktree` for the file on disk) when a group needs context, such as the caller of a changed function.
- **Words**: the page's language is the one the repo states (a workspace's language rules win), and when it states none, the language the user writes in during the conversation. Write purposes and titles in plain sentences, as step 3 of the review-page skill asks: name things the way the user does, and keep IDs, decision numbers and phase codes in the files. Paths belong in the code headers, which the script writes.
- **Diagram** a group when its point is a flow, a before/after, or who calls whom.
- **More than 7 change groups**: the page renders as an overview with the code folded; prefer merging small groups first.

In a workspace, add:

- **Plan items as groups**: each `change` group carries the `plan_item` it carries out, in the plan's words. Small fixes the plan items needed (an import, a test fixture, a lint fix) go in one `supporting` group. A change no plan item asks for goes in an `outside-plan` group, which the page flags yellow: name what it does plainly, as a fact, without blame.
- **`no_code`**: the plan items of this stretch of work that no hunk carries out.
- **`links`**: the workspace decisions and findings each group carries out, named in words, linked with an absolute `file://` path.
- **`how_to_see`**: for each group that changes what a screen or the API does, the screen to open, what to do, and what should appear, from the phase's verification and manual test docs. Groups that only reshape code leave it out.

_Done when_ the JSON holds every hunk, each group's purpose has its true source, and each failed claim sits in its group's `mismatch`.

### 4. Build and open

```bash
python3 <skill-dir>/scripts/wyd.py new <snapshot> --groups <file.json> --lang <en|id>
```

Open the printed page (`open <path>` on macOS, `xdg-open <path>` on Linux, `start <path>` on Windows). If the open command fails or there is no desktop session, do not retry it and never say the page is "opened": give the file path, say the file must be copied to the user's own machine, or serve it with `python3 -m http.server --directory <folder>` when a port can be opened.

`new` refuses with ERROR lines and writes nothing until the grouping is valid; fix every ERROR. Fix each WARN unless you can say why it does not apply. `strings/` holds `en` and `id`; add a language by copying `strings/en.json` and translating it. A language with no file there falls back to `en` with one warning line.

In chat: the workspace line when one applies, the resolved source in one line, the absolute page path, and one sentence on how to use the page: read by group, **Explain this** copies a prompt to paste back, **Copy path** gives `path:line` for VS Code's Ctrl+P. The page carries the content; leave it out of chat.

_Done when_ `new` printed a path with no ERROR and the page is open, or its path and way to reach it are given.

## Focus

A pasted Explain-this prompt looks like this. The first line is only a marker; if your agent has no slash commands, treat it as a request for this skill.

```
/what-you-did focus <snapshot dir>
Source: commits <A..B> | uncommitted changes on <sha>
Workspace: <slug>            (only when the page had one)
Page: <title of the page it came from>
Part: <group title>          (group buttons only)
Hunks: h7,h12:30-37
Where: <path:line; …>
Question: <the user's question, or the default one>
```

1. **Find the code.** Read the snapshot's `source.json` and `hunks.json`. When the snapshot is gone (the temp directory was cleared): for commits, run `collect A..B` again, which numbers the hunks the same way, and check each `Where` path against the new index; for uncommitted changes, find the code at `Where` in the working tree or in the commits since that sha, and tell the user on the page that the original snapshot is gone and which code you used instead. With a `Workspace:` line, load that workspace's `CONTEXT.md` as in step 2.
2. **Dig.** Answer the question first, then whatever the part needs to make sense: what the code does now and did before, who calls it and what it calls (search for callers and show them as excerpts), which decision or finding it carries out, and what would break without it. Every statement about the code rests on code you read. Check each claim behind the part as in step 2: the focus page is where a wrong commit message or a drifted plan item matters most, so a failed claim gets its `mismatch` here too.
3. **Build the focus page** with the same `new` command and JSON, plus `"focus": { "part": "<the part>", "question": "<the question>" }` and `"back": "<file name of the page it came from>"` (pages share one directory). Its groups are the facets of the answer (the answer itself, before and after, callers, why), each showing the hunks or excerpts it rests on; a hunk may appear in several facets here, and nothing has to cover every hunk. Its Explain-this buttons keep working, so the user can go deeper.
4. **A problem found**: when digging shows the code contradicts a workspace decision, or holds a bug, say so on the page in a yellow note, and in chat offer to record it as a finding in the workspace, following its `CONTEXT.md` conventions. Write the finding only when the user says yes.

Reply as in step 4.

## Safety

Read-only toward the repo and the workspace: no commits, no edits, no workspace writes except a finding the user approved. `collect` writes one snapshot directory and `new` one page, both under `<tmpdir>/what-you-did/`; neither touches the network. The opened page loads Mermaid from jsDelivr and fonts from Google Fonts, and runs only the template's own script. Code from the repo sits unencrypted on the page in the temp directory: when a hunk holds a secret (a key, a password, a token in a config file), list it under `"omitted": [{ "hunk": "h4", "reason": "holds an API key" }]` instead of in a group: the page names the file and the reason, never the code.
