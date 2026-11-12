---
name: so-far
description: Run only when the user asks for it by name. Recaps a workspace for the user — what was done and decided, where they approved unread or skipped a review, why the next step is next, and what it needs from them. Read-only. Use when the user lost the thread of a workspace ("what did we do yesterday?", "kemarin kita ngapain?").
argument-hint: "<workspace> [period, e.g. yesterday, this week]"
disable-model-invocation: true
---

# So Far

Catch the user up on a **workspace** (a feature folder set up by `kickoff`, `.scratch/workspaces/<slug>/` unless the repo's `CLAUDE.md` / `AGENTS.md` names another root) after they lost the thread: away for a while, or decisions moving faster than they could follow. The output is a **recap page** (HTML, opened in the browser): how the work arrived where it is, told so the user takes back control of the next step. `resume-here` briefs the agent's next move; this skill briefs the person.

`scripts/recap.py` in this skill's directory does the mechanical work: `new` wraps a drafted `<main>` in the page's styling and fixed strings, `check` turns the wording and layout rules below into errors and warnings. If `python3` is not on the PATH, use `python` or `py` instead. A run ends like this:

```bash
python3 <skill-dir>/scripts/recap.py new repo-foundation --lang id --main <draft>/main.html
# prints /tmp/so-far/repo-foundation-20261028-1034.html (the OS temp directory)
python3 <skill-dir>/scripts/recap.py check /tmp/so-far/repo-foundation-20261028-1034.html
open /tmp/so-far/repo-foundation-20261028-1034.html
```

Section names below are English. A workspace written in another language carries them translated (`## Decisions` → `## Keputusan`, `Action Log` → `Log Tindakan`): match by meaning.

## Resolving the workspace

The same order in every workspace skill:

1. the slug or path in the argument;
2. the workspace this conversation has already been working in;
3. `INDEX.md` at the workspace root: the only row under `## Active` (no `INDEX.md` → the only `*/WHATNEXT.md` under the root);
4. still more than one → ask, listing the `## Active` rows.

Never pick between two live workspaces. Name the one you resolved in one line: `Workspace: <slug>`.

## Steps

### 1. Load

1. `CONTEXT.md` and `WHATNEXT.md`, whole. `## Workspace rules` sets the language.
2. Fix the **window** as two absolute dates, start and end, from today's date:
   - a period in the argument → its dates ("kemarin" / "yesterday" → yesterday to yesterday; "minggu ini" / "this week" → this Monday to today);
   - no period → the whole workspace: the earliest date in the tracker's Action Log to today.
3. The history inside the window:
   - the tracker's Action Log rows dated in the window (`TRACKER.md`);
   - the repo's commits, with times, run from the repo root with the window's dates (here, a one-day window; not a git repository → skip the commits and say so on the page):

     ```bash
     git log --reverse --since="2026-10-27 00:00" --until="2026-10-27 23:59" \
       --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M'
     ```

     Keep the commits that touch this workspace's areas (the Areas column of its `INDEX.md` row, or the paths its plan names). Leave the workspace's own repository alone, as every workspace skill does.
4. The plan phase that next step 1 names (`plans/*/phases/`, or the plan's Phase Index): its Context section holds the reasons that step comes next. Also the repo's roadmap or status file, when `CONTEXT.md` or the repo's `README.md` names one.

Open a finding, question or handoff only when a decision in the window points to it.

Done when: you hold the window's dates, its Action Log rows and commits, and the reasons for next step 1 in the plan's own words.

### 2. Reconstruct

Group the window into **stages**: runs of work toward one result (a phase, a review round, a checkpoint), in time order. Commit times show where one stage ends and the next begins.

For each stage, its result and every decision made in it. A decision is in the window when its entry, or the opening line of the decisions section, carries a date in the window; with no period, every decision is.

Give each decision its **provenance**, read from the user's words recorded in its entry:

- **reviewed**: the entry says the user read the material and chose ("after reviewing", "saat meninjau");
- **unread**: the entry says the user approved without reading it ("without reviewing", "tanpa meninjaunya");
- **skipped**: a checkpoint or review the plan scheduled, waived by the user;
- **on recommendation**: the user accepted the agent's proposal and the entry says nothing about reading it ("agree to all", "setuju semua");
- **not recorded**: the entry carries no words from the user.

Unread and skipped are where control slipped, and the likeliest reason the user feels lost: the recap names them plainly.

Then check for **drift**: commits after the last commit `WHATNEXT.md` records are work it does not know about. Add them to their stage and mention the drift in step 3.

Done when: every Action Log row and kept commit sits in a stage, and every decision in the window has its provenance.

### 3. Tell it

Present the recap as a **recap page** opened in the browser, not as chat text: a long recap in the terminal is hard to scan.

The page holds, in the workspace language and in this order:

1. **Timeline**: the stages as day rows at the top, oldest first, marking where the user is now and the next step. At most seven rows: in a long window the older days shrink to one line each. A stage holding an unread or skipped decision carries a red dot. Progress figure, when the tracker records one; never invent one.
2. **What happened**: one card per stage, two to four bullets with its result and decisions, each decision ending in its provenance badge. Before the cards, one callout listing every unread and skipped decision again, or one line saying there were none. Drift goes in a yellow callout inside the stage that holds it. A long window: the older stages collapse, the latest day gets the detail.
3. **Why the next step**: two or three numbered reasons, from the plan's Context and the state the stages left.
4. **What comes next**: the next steps from `WHATNEXT.md` in order, each opening with who acts; the user's own steps are framed.
5. **Open to you now**: what is waiting on the user, and any unread or skipped decision they could revisit at the next step. Acting on it is optional: the plan stands otherwise.

Write plain sentences. Name each decision, flow or document by what it is: "you accepted the admin flow proposals without reading them", not "decision 15" or "PT3–PT9". IDs and codes (decision numbers, requirement IDs, question numbers, phase codes like F4) stay in the files. Give a path only where the user would open the file, inside `<code>`. The content reads like [`references/example.md`](references/example.md).

Build the page:

1. **Draft.** Write the page's `<main>…</main>` block to a draft file in the OS temp directory, starting from the `<main>` block of [`template.html`](template.html) and keeping its `[[key]]` markers as they are. The template's HTML comments are instructions: leave them out of the draft, together with every block the recap does not use (the progress bar, a quiet day, the drift callout). Copy a day row, stage chip or stage card for each further one; each chip links its card by id.
2. **Build.** Run `recap.py new <slug> --lang <code> --main <draft>`, where `<code>` is the workspace language: `strings/` holds `en` and `id`; add another by copying `strings/en.json` and translating it. The script fills every `[[key]]` (section titles, badges, chip labels, the slug in the continue commands) and prints the page's path.
3. **Check.** Run `recap.py check <file>`, fix every ERROR in that file, and run it again until no ERROR remains; fix a WARN unless you can say why it does not apply. Then check by hand what the script cannot see: every unread and skipped decision from step 2 is named with its provenance; every reason in "Why the next step" traces to the plan or `WHATNEXT.md`; the timeline shows every stage.
4. **Open.** Open the page (`open <path>` on macOS, `xdg-open <path>` on Linux, `start <path>` on Windows). Reply in chat with only: `Workspace: <slug>`, the state in one or two sentences, the absolute page path, and the close line from "Boundaries and close" below. Do not repeat the recap in chat.

Done when: the check prints `ok` or only warnings you can justify, the page is open, and the user can say what happened, why the next step is next and what it asks of them, from the page alone, without opening another file.

### 4. Boundaries and close

Read-only toward the repo and the workspace: no workspace file writes, no commits. The only files written are the draft and the page in the OS temp directory: `recap.py new` writes one new file under `<tmpdir>/so-far/`, `check` only reads, and neither touches the network. The opened page loads fonts from Google Fonts and runs only the template's own script; it sits unencrypted in the temp directory, so put nothing secret on it. A user who decides something in reply has started a discussion: record it as the `discuss` skill's "Record before the end" step says.

Close with the line to continue: `/resume-here <slug>` to start the next step, or `/discuss <slug> <topic>` to talk one through first. This line belongs to the reply that opens the page; later replies in this conversation do not repeat it.
