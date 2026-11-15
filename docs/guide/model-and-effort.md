# Model and effort

This page answers one question: which model and effort level should you pick for each kind of session.

It names model tiers only (Haiku, Sonnet, Opus, Fable), not version numbers, so it does not go stale when versions change.

## What is already automatic

Two things need no choice from you:

- **Phase executors.** `guard-plan` (and `execute-plan`, when it dispatches a batch of phases) picks the agent from the phase's Weight. Each agent carries its own model and effort in its frontmatter. (With the plugin install they are named `phase-agents:phase-s` and so on.)

  | Weight | Meant for                        | Agent      | Model  | Effort |
  | ------ | -------------------------------- | ---------- | ------ | ------ |
  | S      | mechanical, repetitive work      | `phase-s`  | Haiku  | low    |
  | M      | standard work                    | `phase-m`  | Sonnet | medium |
  | L      | reasoning, design decisions      | `phase-l`  | Sonnet | high   |
  | XL     | cross-cutting, architecture      | `phase-xl` | Opus   | high   |

  A plan never names a model. It only carries a Weight per phase.

- **`msg`.** It sets `model: haiku` in its own frontmatter, because drafting a short chat message is light work.

Only Claude Code honours these settings. Every other skill uses the model and effort of your session. Change them with `/model` and `/effort`.

## In guard-plan, you choose the guardian

In a `guard-plan` run, the model of your session is the model of the **guardian**: the one that re-checks each phase, fixes what is wrong and commits. The phase work itself is already set by Weight (see the table above). So the choice you make for `guard-plan` is about the guardian, not the executors.

## A starting point

This is a starting point from what each skill does. It has not been measured.

Fable is another option for the Opus rows if your subscription includes it.

| Kind of session        | Skills                                                                                              | Suggested                     |
| ---------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------- |
| Weighing and designing | `to-plan`, `kickoff`, `discuss` for big decisions, `review-phase`, `code-review`, `diagnosing-bugs` (both from `mattpocock/skills`) | Opus, high effort             |
| Guarding a plan        | the `guard-plan` session                                                                            | Opus, high effort             |
| Running and upkeep     | `execute-plan` inline, `refine-docs`, `update-wiki`, `wrap-up`, `what-you-did`                      | Sonnet or Opus, medium effort |
| Notes and resuming     | `pause-here`, `resume-here`, `so-far`, `tracker`, `whatnext`                                        | Sonnet, medium effort         |
| Light                  | `msg`                                                                                               | nothing to set                |

The idea behind the rows: decisions and reviews are where a weak answer costs the most, so they get the strongest model. Recording and resuming only move known facts around, so a lighter model is enough.

## Tell me what you ran

When you report a problem, say which model and effort the session used. That is how this table gets corrected from real use instead of guesses.

Next: [FAQ](./faq.md)
