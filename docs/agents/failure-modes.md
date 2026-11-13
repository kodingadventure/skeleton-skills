# Failure modes

Repo-specific catalog `to-plan` reads to fill each phase's `Prone to:` line, and `review-phase`
reads to know what to probe. See `skills/workflow/review-phase/references/failure-modes.md` for
the format this file follows and when to add an entry.

## skill-in-one-place-only

**Shows up as:** a skill installs or lists incorrectly because only some of its required locations
were updated.
**Probe:** confirm the directory, the manifest entry, and the README bullet all exist — a directory
with no manifest entry is uninstallable and nothing else catches it.

## manifest-unparseable

**Shows up as:** every skill in the repo becomes uninstallable because `marketplace.json` is
malformed.
**Probe:** `node -e "JSON.parse(...)"` against the file — the only gate.

## rule-added-enforcement-surface-untouched

**Shows up as:** a rule lands in the prose that states it while the surface that enforces it keeps
the old shape, so verification that only reads the new prose passes.
**Probe:** name the surface the rule governs (a template, a report form, a registration list) and
check the rule reached *it*, not just its description.

## rename-sweep-reads-empty-as-clean

**Shows up as:** a repo-wide rename is declared finished while references remain, because the
sweep's pattern could not match them. A grep for `CONTEXT(-MAP)?\.md` misses prose like "CONTEXT
files", and `git grep -E` with `\b` returns nothing, with no error, on macOS.
**Probe:** search the bare word, case-sensitive, and leave out `\b`. Before trusting an empty
result, confirm the same command finds a term known to be present.

## citation-drifted-in-batch

**Shows up as:** a `file:line` reference written by one phase is confidently wrong by the time
anyone reads it, because a sibling phase in the same batch inserted lines above it.
**Probe:** re-resolve every `file:line` in the diff, or cite files only.

## changeset-missing

**Shows up as:** a change under `skills/` or `plugins/` lands without a changeset, so the next
version PR and `CHANGELOG.md` leave it out.
**Probe:** `git diff --cached --name-only` lists a path under `skills/` or `plugins/` but no new
file in `.changeset/`.

## skill-names-a-skill-it-cannot-assume

**Shows up as:** a skill's rule says "use `<other-skill>` if installed", and the model names that
skill in its answer even when it is not installed (or does not fit), only to say it is missing.
The same happens with `Invoke: none`.
**Probe:** read the rule for a named skill that the rule's own condition can exclude; the
suggestion should come from what is installed, and leave the line out when nothing fits. Test with
the named skill absent, not only present.

## language-rule-covers-one-channel

**Shows up as:** a skill that must answer in the workspace language replies in English, because
the rule is a clause in one step while the repo's "English only" rule is read as covering the
conversation too.
**Probe:** the rule must name every channel (summary, replies, questions including option boxes,
status lines), say what language applies before the workspace file is read, and say that the
repo's English rule is only for what is committed.

## close-step-read-as-reply-format

**Shows up as:** a skill that runs over many replies (a discussion, a resumed workspace) ends
every reply with its continue line, often telling the user to type the slash command of the skill
that is already running. The close step never said which reply it belongs to, so it is read as
the format of every reply.
**Probe:** every close or report step names the one reply it applies to, and says later replies
do not repeat it. A continue line never names the skill that is running in the same conversation;
it names another skill, or the running one only for a new session.

## stop-check-buried-in-a-read-step

**Shows up as:** a skill's "stop before doing anything" check is skipped at run time because it was
appended as one more sentence to a step whose job is reading or locating something; the agent
finishes that step's main job and moves on. The check fires later, if at all, after the work it
should have prevented.
**Probe:** a stop check gets its own numbered step with a command to run and a `Done when` line
that names it; read the step list alone and confirm the check is visible there.

## rule-restated-shorter-elsewhere

**Shows up as:** a skill writes one list or rule twice, in full in a template and shortened in its
`SKILL.md`, or states a rule and then breaks it in its own example. The agent copies the short
version or the example, so the output loses exactly what the full rule named (a plan's docs-phase
review check dropped file paths, UI text and links; a glossary entry got a code pointer because
an example had one).
**Probe:** grep the rule's key terms across the skill and its references. Keep one full copy, have
the other places point to it ("copy word for word"), and check that every example obeys the rule.

## rule-only-in-principles

**Shows up as:** a rule that lives only in a principles or checklist section is ignored by the
step that produces the output, most often when the rule is an abstract word ("no behaviour").
The agent's own report even claims the rule was followed. In one re-test, a glossary entry read
"…which moves it to the refunded status" under a vocabulary-only rule.
**Probe:** the step that writes the output names the rule as a concrete test, with one wrong and
one right example. Re-run the scenario that failed, and check the file, not the skill's report.

## repo-change-with-no-owner

**Shows up as:** a skill writes a repo file as a side effect (a `Workspace root:` line in
`CLAUDE.md`) and calls it "a repo change to commit" or "list it among the files you wrote",
but no step commits it. Every later skill stages only its own paths, so the change stays
uncommitted until the work ships, and `wrap-up` reports it as "left alone".
**Probe:** grep the skill for "repo change" and "list it". Each hit names who commits the
change and when, under the repo's rules, and the last skill of the flow catches a leftover.

## unhandled-state-reported-as-expected

**Shows up as:** a step lists the normal case and one skip case, and its `Done when` names the
normal end state. In a state the step does not cover (a repo with no remote), the agent
reports the normal end state anyway ("level with the remote") and may act on a check that is
trivially true there ("the branch is gone from the remote").
**Probe:** for each git or environment command a step runs, ask what it does with no remote,
no branch, or no network. Each such state gets its own line and its own report wording, and
`Done when` allows for it.
