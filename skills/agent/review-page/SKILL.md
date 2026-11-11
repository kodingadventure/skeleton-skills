---
name: review-page
description: Writes a short, diagram-led HTML page to the temp directory and opens it for the user to review or decide on. Use when there are two or more decisions, or one that needs a diagram or background, including a decision round handed over by another skill, or when a message starts with `/review-page explain` (pasted from a page's Explain button). Ask a short question directly in the conversation (or with your agent's question tool). Not for documents written for agents.
---

# Review page

Use a review page when there are two or more decisions, or one that needs a diagram or background. Ask a short question directly in the conversation (or with your agent's question tool).

The user reads plain sentences and diagrams. IDs, codes, file paths, and dense tables are for agents. A **review page** is the human version of material the agent already holds: one self-contained HTML file per **round**, written in the repo's language, opened in the user's browser, readable in a few minutes, and answered by pasting one block of text. The page lives in the OS temp directory, so nothing lands in the repo; the decisions it collects are recorded in the repo's own documents.

Two kinds share every rule below:

- **Decision page**: up to 7 items, each with options, the **recommended option** preselected in a green frame, and an **answer box** at the end.
- **Read-through page**: something already written (flows, a plan) retold in plain words. Open questions sit inline as yellow-flagged notes or diagram nodes; options and the answer box appear only when the page also asks for decisions.

Users tend to accept recommendations as given. Every recommendation must hold up unread, and the **risk flag** (yellow) is where you invite scrutiny.

`scripts/page.py` in this skill's directory does the mechanical work: `new` builds the page, `check` turns the rules below into errors and warnings, `decide` records answers, `refresh` moves an older page onto the current template. `<skill-dir>` below is the folder holding this `SKILL.md`. A round runs like this:

Needs Python 3 (standard library only) and git; if `python3` is missing, use `python` or `py`.

```bash
python3 <skill-dir>/scripts/page.py new decisions-round-2 --lang id --title "Keputusan Putaran 2" --main <draft>/main.html
# prints /tmp/review-page/decisions-round-2-20261028-1034.html (the OS temp directory)
python3 <skill-dir>/scripts/page.py check /tmp/review-page/decisions-round-2-20261028-1034.html
open /tmp/review-page/decisions-round-2-20261028-1034.html
# after the user answers:
python3 <skill-dir>/scripts/page.py decide /tmp/review-page/decisions-round-2-20261028-1034.html item-1=B item-2=A
```

## Steps

1. **Gather.** From the source material, write down each item the user must see: the problem in one or two sentences, the facts it rests on, your recommendation with its reason, each alternative with its cost, and what goes wrong if the recommendation is wrong. When a caller hands over findings that already carry options and a recommendation, start from those and check each against its source; when an option fails to hold up unread, sharpen it (a safeguard, a warning) and say on the page what you added. An item with nothing to choose (a note, a cleanup) goes in the noted list, one line each, not in a decision. _Done when_ every item has a recommendation you would defend without the user's review.

2. **Flag and cut.** Flag yellow only the two or three items where a wrong recommendation would cost the most (user-visible, data, money, or legal consequences, or a guess about the user's business); when every item is yellow, none stands out. One page holds at most 7 decisions. Keep the ones that block the next piece of work, list the rest as one-line bullets under "next round", and give them their own page after this round is answered. _Done when_ the page has 7 decisions or fewer and few enough flags that each one stands out.

3. **Say it plainly.** Replace every ID, code, file path, section number, document name, and internal label with the everyday name of the thing, and keep every term the user already uses (a developer says commit, branch, deploy): a paraphrase of a known word reads as something new. A requirement becomes what it makes the app do, a role becomes the name the user calls it. Define each term where it first appears; the lead carries only the terms the whole page relies on. Say what numbered things are and why the count starts where it does ("Work is split into numbered phases. Phases 1 to 3 are done, so the comparison starts at 5."). _Done when_ a reader who never saw the source can follow each sentence.

4. **Draw.** Give an item a Mermaid diagram when the point is a flow, a before/after, a structure, or who does what. Diagrams scale down to the column width, so a wide one becomes unreadable: grow every diagram **downward**.
   - Use `flowchart TD`. A left-to-right chain is fine up to 4 short nodes.
   - Let no node branch out to more than 3 others, and use at most one subgraph per diagram.
   - Keep label lines under 25 characters and break them with `&lt;br/&gt;`, written escaped like that: a raw `<br/>` inside `<pre class="mermaid">` is swallowed by the browser before Mermaid sees it. Quote speech inside a label with single quotes: a double quote ends the label.
   - Start every label with plain words, and number steps as `Step 1` or `1:`. Mermaid draws other Markdown (a list, a heading, a quote, a backtick) as "Unsupported markdown" instead of the text, and `page.py check` rejects it.
   - Colour a risky or open node with `classDef q` (yellow) and a new or chosen node with `classDef n` (green), as in the template.
   - Show a before/after as two diagrams inside `<div class="pair">`, which stacks on a phone.

5. **Build.** Write the page's `<main>…</main>` block to a draft file in the temp directory, starting from the `<main>` block of [`template.html`](template.html) and keeping its `[[key]]` markers as they are, then run `page.py new <topic> --lang <code> --title "<page name>" --main <draft>`. `<topic>` is a short slug, and `<code>` the page's language: the one the repo states, and when it states none, the language the user writes in during the conversation. `strings/` holds `en` and `id`; add another by copying `strings/en.json` and translating it. A language with no file in `strings/` falls back to `en` with one warning line, so the page's fixed text is English until you add the file. The script wraps the draft in the template's styling and scripts, fills every `[[key]]` with the fixed string in that language, and prints the page's path. The draft holds:
   - **Header**: a back link when this page continues another, the title, a lead saying what the page is, why now, and how many items, on a later round the **recap** (what earlier rounds decided, one line each, so nothing below repeats a settled item), the reading guide paragraph as the template has it, and the item list linking to each section, with the yellow chip on flagged ones.
   - **One section per item**: numbered heading, problem, diagram, details, options with the recommended one first, and a risk box under flagged items saying why it is risky and what to check. Give each `.opts` a short `data-name` for the answer box and its own radio `name`.
   - **Noted** for items with nothing to choose, **next round** when something is deferred, then the **answer box**, whose `data-title` becomes the first line of the answer.

   Copy a section block for each further item. The template's HTML comments are instructions: leave them out of the draft, together with every block the page does not use. Make every cross-reference a link: an in-page anchor for a section, the bare file name for another review page (they share one directory). The script marks every item with options with a question mark until it is answered. It also adds, under every decision, an **Another answer** option with a text field and a **comment box**, and puts a **notes box** in the answer box; all of them reach the copied answer. It also gives every section an **Explain** button (see [Explain](#explain)). Never write any of these into the draft yourself.

6. **Check and open.** Run `page.py check <file>`, fix every ERROR, and run it again until no ERROR remains; fix a WARN unless you can say why it does not apply. Open the page for the user (`open <path>` on macOS, `xdg-open <path>` on Linux, `start <path>` on Windows). If the open command fails or there is no desktop session, do not retry it and never say the page is "opened": give the file path, say the file must be copied to the user's own machine, or serve it with `python3 -m http.server --directory <folder>` when a port can be opened. In chat, give the absolute path and one sentence on what to decide and how to answer; the page carries the content. Write the path wherever the work tracks its state, so a later session can find the page while it still exists. No such place: give the path in the conversation, and ask once where the user wants decisions recorded. _Done when_ the check prints `ok` or only warnings you can justify, and the page is open or its path and way to reach it are given.

7. **Record the answer.** When the user answers, write the decisions into their source of truth first. No such place: give the path in the conversation, and ask once where the user wants decisions recorded. Then turn the page into a **record** of what was decided, so nothing on it asks for an answer that was already given:
   - An answer of "agree to all" (the page writes it when nothing was changed) picks every recommended option. Read every comment and the notes in the answer first: a question gets its answer in chat (and a next-round decision when it reopens the item), and a comment that changes the item is recorded with it. A comment never counts as a choice; the letter or the user's own answer does.
   - Run `page.py decide <file> <radio-name>=<letter> …` for every answered decision, or `<radio-name>=other:<the user's own answer>` for an answer outside the options (the page shows that text in the locked option). The page's script then locks the chosen option, fades the others while keeping the recommendation tag visible on one the user passed over, greys the item's risk box, drops its yellow chips, and swaps its question mark for a check, in the heading and the item list. It then folds the item to its heading and a one-line summary of the answer, so the open items keep the reader's focus; a click on the heading or a link to the item opens it again. Once every decision is answered, it hides the answer box and the reading guide.
   - Add the **decided banner** from the template's comment at the top of the header: the date, then each item's outcome, naming every answer that differs from the recommendation.
   - An answered page never takes a new question: a page that mixes settled and open items leaves the reader unsure what still needs an answer. When an answer opens one (a counter-proposal, a "who presses this button?", a comment that contradicts the letter chosen), it goes on the **next round's page**: build it with steps 1-6, open it with the recap, and put only the open questions below. Record the item it came from with `page.py decide <file> <its radio-name>=follow-up`: it counts as settled on this page, folds, and points to the next round through the decided banner's link, which `check` requires. The user answers the new page through its own answer box; never ask them to reply in chat instead.
   - Rewrite the lead so it reads as a record (what was decided, not what to decide), and link the next round's page from the banner once it exists, and link back from it.

   Run `page.py check` again and open the same file. _Done when_ the decisions are recorded at their source, every answered decision carries `data-chosen`, and the check passes. The temp directory may have been cleared by then; with the page gone, the recorded decisions suffice.

## Explain

The **Explain** button on a section copies a prompt for the reader to paste into the conversation when something on the page is unclear:

```
/review-page explain <page path>
Page: <page title>
Item: <the section's heading>
About: <one option's name>     (only when the reader picked one)
Question: <the reader's question, or the default one>
```

The first line is only a marker; if your agent has no slash commands, treat it as a request for this skill. It asks for an explanation, not a decision: nothing in it counts as an answer. The reader is mid-choice on the page, so leave the page file untouched: a reload would reset the choices they have not copied yet.

1. **Find the item.** Read the section at the page path, then the source material behind it. When the page is gone, work from the Item and About lines and the source material.
2. **Answer in chat.** Answer the question first, in a few plain sentences under the rules of step 3. When About names an option, say what choosing it changes compared with the recommendation.
3. **A recommendation that no longer holds.** When explaining shows the recommendation is wrong, say so in chat: which option you now recommend and why. The reader changes the choice on the page, and the decision still comes through the answer box.

_Done when_ the question is answered in chat and the page file is unchanged.

## Safety

- `page.py new` writes one new file under `<tmpdir>/review-page/`; `decide` and `refresh` rewrite only the page file you name, and `check` only reads. None of them touches the repo or the network.
- Point `decide` and `refresh` only at review pages: they rewrite the file in place.
- The opened page loads Mermaid from jsDelivr and fonts from Google Fonts, and runs only the template's own script. Put nothing secret on a page: it sits unencrypted in the temp directory.
