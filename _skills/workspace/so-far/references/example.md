# Example recap

The content of a recap for `/so-far <slug> yesterday`, in a workspace whose language is English. Shown for its shape, density and plain wording; the content belongs to one project. The real output is the recap page built from [`template.html`](../template.html): the timeline below becomes day rows of stage chips, each stage becomes a card, each decision ends in a provenance badge.

---

Workspace: repo-foundation

## Yesterday, in short

```
Morning        Midday                     Afternoon
Foundation  →  Spec split by topic    →   Flow catalog    →   [next] Spec review
(done)         (done)                     (done)              ← you are here
```

**1. Repo foundation (morning).** You approved the ten starting decisions at once. Result: a README and a roadmap, old documents that contradicted the current spec archived, unused skills removed.

**2. Spec split by topic (around 10:00).** The long spec was split into one file per topic, with a glossary and a quick-search table. Two of your suggestions were accepted: collect test material while drawing mockups, and let the agent commit on its own.

**3. Flow catalog (midday to afternoon).** Step-by-step flows for customers, staff and the app admin. This is where most questions came up:

- **Customers:** you reviewed the first two flows on the summary page. Decided: the order form goes file by file, binding becomes a per-item option, and the WhatsApp number field is removed.
- **Staff:** you asked for recommendations to save time and accepted all of them.
- **App admin:** you accepted all recommendations **without reading them**. The per-role reading check was **skipped**; you chose to check the flows when the mockups are drawn.

That last part is probably where you lost the thread: two batches of decisions went in unread.

## Why the spec review comes next

1. The current spec version has never been reviewed; the last review covered the version before it.
2. The staff and admin screens have no mockups yet and will be drawn straight from this spec.
3. Yesterday's decisions are queued, not yet in the spec. The review weighs them together, so you decide in one sitting.

## What comes next

1. Agent: reviews the whole spec and the flows, and writes the report. You don't need to read it.
2. **You:** decide in rounds of at most seven items, each with a recommendation, on a short page with diagrams. The riskiest items are marked.
3. Agent: applies your decisions as the next spec version.

## Open to you now (optional)

- The admin decisions you approved unread are due to be shown again at mockup time. Want to see them earlier, in the review rounds?
- Still waiting on you, not blocking: how binding is priced.

Continue: `/resume-here repo-foundation`, or `/discuss repo-foundation <topic>`.
