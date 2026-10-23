<!--
REL-05 submission-post DRAFT, prepared 2026-10-22; source/evidence audit refreshed 2026-10-23. NOT PUBLISHED.
Owner, before publishing (each item is yours; nothing here has been posted or sent):
  1. Video added 2026-10-23: https://www.youtube.com/watch?v=Qlq_kEsDr4g (5:48). Check that the embed shows in DEV's preview.
  2. Confirm your personal eligibility and the deadline (sources conflict: see docs/COMPETITION.md and TASKS REL-04).
  3. Confirm the Prize Categories list against what is actually shown in the post and video.
  4. Fill in the AI-assistance credit with the tools you actually used, and set DEV's ai_disclosure_level in its editor or front matter according to actual authorship. Official dev.to/llms.txt (checked 2026-10-23) distinguishes some_ai from fully_autonomous; merely reviewing an AI-written draft does not make it human-authored. No value has been invented here. Do not publish with this field undisclosed.
  5. Decide whether to keep "My Agent Session" (optional) and "The Lazy Payoff" (optional); remove either if unused.
  6. Release verification is complete for d4b2f76: tests #18 passed all three jobs; a fresh clone and the live Render replay were checked (REL-02, 2026-10-23). Recheck only if the release changes; do not present this dated check as an uptime guarantee or new model-accuracy measurement.
  7. Copy everything below the line into DEV's editor (front matter included), then delete this comment.
Numbers come from evaluation/RESULTS.md (frozen tables and dated historical timings) and PROGRESS.md (including CFG-02 and REL-02). Owner video, selected redacted screenshots, actual credits/disclosure and personal eligibility remain open. The written-rules/API deadline discrepancy remains unresolved in docs/COMPETITION.md; do not infer a resolved deadline or eligibility from the push.
-->
---
title: "Availazy: local AI that turns a week of volunteer chat into an availability sheet you can check"
published: false
tags: devchallenge, hf26challenge, ai, opensource
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

## What I Built

Every week a volunteer coordinator posts the same question in a group chat: *when can you help?* The answers come back as free text. "Tuesday 10–12 works." "Thursday afternoon if my shift gets moved." "Change of plans, Thursday doesn't work anymore." Someone then has to read all of it, remember who changed their mind, and type a sheet by hand.

**Availazy** does the reading and the bookkeeping, and leaves the decisions to the coordinator. You paste a week of dated messages (or a WhatsApp export) and the volunteer list, pick the week, and it:

- suggests availability records, each shown **beside the message it came from** with the quoted words highlighted;
- keeps each person's history day by day, so a later correction or cancellation replaces the earlier answer, and a conditional offer stays conditional until someone settles it;
- lists what it will not guess under **Needs a decision**: "next Tuesday" sent on a Monday, a day outside the week, a name that matches two people;
- exports a **final sheet built only from the records you accepted**. The file is marked *complete* only when three things are true: every non-duplicate message is marked reviewed, no suggestion is still pending, and no blocking issue (an unresolved person, date, time or conflict) is open. Otherwise it says *provisional*, and it still downloads.

It records availability, not shift assignments. The person who gets to be lazier is the coordinator: they check and decide instead of retyping.

## Demo

- **Video (5:48):** the local app reads two invented messages live with Gemma 4, then the hosted replay walks through a fictional week.

{% embed https://www.youtube.com/watch?v=Qlq_kEsDr4g %}

- **Try it in your browser:** <https://availability-ledger-replay.onrender.com/app>. This is a fixed-data **replay**: a fictional pantry's week (50 messages, 18 volunteers) with Gemma's answers saved in advance, so it runs on free hosting without a model. Review decisions, history, the chart and both exports work; pasting your own messages is switched off. The free instance sleeps when idle, so the first visit can take about a minute; [Render describes this as an approximate wake time](https://render.com/docs/free), not a maximum.
- **Read your own messages:** follow the [README's local setup](https://github.com/bipul724/availability-ledger#readme). Live Gemma inference happens only in the local app.

## Code

{% github bipul724/availability-ledger %}

The core uses Python's standard library and plain HTML/CSS/JS, under an MIT licence. Opt-in tracing has one separate optional dependency, `sentry-sdk`; the app works without it. A guide with diagrams is at <https://availability-ledger-replay.onrender.com/docs>.

## How I Built It

The design rule is a strict split: **the model proposes, code decides, a person accepts.**

1. **Gemma 4 E2B proposes phrases and hints.** Running in Ollama on the laptop ([`gemma4:e2b-it-qat`, Apache 2.0](https://ollama.com/library/gemma4:e2b-it-qat)), the model fills a JSON schema per message: who, copied day/time/condition words, a verbatim quote, a proposed status and a replacement hint. Code computes the dates, time ranges, history and counts. A historical 20 October observation on an 8 GB Apple M2 took 131 s end to end for a fictional 50-message week with Gemma + rules. Ollama reported about 1.59 GB allocated to the loaded model, not total system memory use. These are dated observations, not a controlled benchmark or a promise of typical speed ([provenance](https://github.com/bipul724/availability-ledger/blob/main/evaluation/RESULTS.md#speed-and-memory-measured-with-the-claude-desktop-app-and-a-browser-open)).
2. **Python decides.** Ordinary code turns "next Tuesday" and "after 3" into dates and times using the message's own timestamp, checks that the quoted words really appear in the message, cross-checks the model against a rule-based reader, keeps the per-day history and does every count. Ambiguities are flagged, never guessed.
3. **You decide.** Accept, edit or reject each suggestion; marking a message reviewed is a separate, explicit step. Only accepted records reach the final sheet.

Three readers are available: *Rules only* (no model), *Model only*, and *Model + rules*, the default.

**Infrastructure I actually used:**

- **Render** hosts the fictional replay. The server runs in a demo mode that refuses any message, roster or week it did not serve, and it never calls a model.
- **GitHub Actions** runs on pushes and pull requests to `main`: 116 unit tests (8 tracing tests skip without the optional SDK), a SHA-256 check that the frozen evaluation results are untouched, and a re-score of all three test sets from saved model outputs. [tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754) passed all three jobs for release `d4b2f76` on 23 October IST. A clean public clone also passed unit/integrity checks; the hosted replay passed a bounded review/export check with nine served UI files matching that release.
- **Sentry Agent Tracing** is opt-in and off by default. When enabled, two allowlists in my adapter restrict outgoing spans to structural metadata such as timings, token counts, model and stage names, excluding message text, names, quotes, prompts and replies; offline tests check planted fake content is absent. The traces were useful: four calls in one run reached the Python client's 300-second deadline while waiting for Ollama, and a later 49-call run took 1.42 minutes with no errors. That does not establish why the earlier calls timed out. One caveat: received traces displayed location (geo) attributes, which my code does not send. After a settings change, four visible geo values on the inspected chat span and its parent appeared filtered. Their origin and a complete audit of everything Sentry receives remain unverified ([dated evidence and limits](https://github.com/bipul724/availability-ledger/blob/main/docs/SENTRY_HANDOFF.md)).

## Why Does Open Innovation Matter?

Group-chat availability is personal: names, schedules, family plans, health. An open-weight model that runs on the coordinator's own laptop means those messages are read right there. The local core needs no account, model API key, per-message bill or cloud database; once Ollama and the model are installed, it can run offline. Optional tracing sends structural metadata externally only when enabled. Open code makes the processing inspectable. The model proposes phrases that can still be wrong; plain Python checks and reconciles them, and a person makes the review decisions.

## How well does it work?

All evaluation messages are fictional. The assistant authored sets A and B, their references and the rules baseline, so they share authorship. An isolated ChatGPT session wrote set C, and I rewrote five of its messages; its manifest was frozen before implementing agents saw it. No independent person reviewed the references. The retained first-scored tables remain unchanged, and later changes made after seeing held-out errors are labelled post-hoc.

**Set C** (24 fictional messages, unseen at its first scoring on 21 October 2026, with that first score frozen):

| Reader | Units right | Silent errors | Missed cancellations | Provisional-ledger slot agreement |
|---|---|---|---|---|
| Rules only | 15/20 | 5 | 4/8 | 0.433 |
| Gemma 4 E2B only | 17/20 | 2 | 4/8 | 0.403 |
| Gemma 4 E2B + rules | 17/20 | 2 | 2/8 | **0.527** |

These metrics score resolved suggestions with **all claims pending and no human review**. The ledger columns concern the provisional ledger, not the accepted-only CSV after a coordinator's decisions. A unit is one person/day statement in a message; slot agreement compares the resulting availability intervals. The units were mostly right, but the ledger was not: two corrections had the right times without replacing earlier answers.

I then used AI coding assistance to fix the causes (explicit dates, replacement cue words, firm follow-ups, an initial-plus-surname match, more negation forms) with new invented regression messages. Re-scored from the same saved outputs, Gemma + rules reaches 1.0 set C slot agreement, but that number is **post-hoc**: the fixes came after seeing C's errors and are not independent evidence. Earlier set B (20 messages) had Gemma + rules at 30/35 units, 3 silent errors and 0.776 provisional-ledger slot agreement as first scored. [The evaluation record](https://github.com/bipul724/availability-ledger/blob/main/evaluation/RESULTS.md) preserves provenance and metric scopes.

Separately, a manual two-message local check on 23 October verified Ana/Ben's source quotes, names, dates and times, acceptance, and provisional-to-complete CSV status after explicit message review. Both populated cells changed from `needs_review` to `confirmed`. That is a small workflow check, not full-week model-accuracy evidence.

## The Lazy Payoff

I have not measured anyone's time, so I will not claim minutes saved. What I can show is the workflow: check each suggestion beside its source, accept/edit/reject it, inspect revision history, and work through flagged decisions in one list. It aims to replace retyping with review; whether that saves a coordinator time is unmeasured. A protocol for a real timing study is in the repo, but no real-coordinator study has been run.

## Known limitations

- Fictional data only, no real users, and the fixtures and references share an author.
- Times are read as written; the timezone field is stored but nothing is converted.
- Up to 20 volunteers; one person, one browser tab; no saved sessions.
- The rules reader misses some phrasings. In a final check, Rules only read "Saturday 9–12 if it isn't raining" as *unavailable* instead of conditional, which is exactly why every suggestion sits beside its message.
- Safari, Firefox and screen readers have not been tested.

## Prize Categories

<!-- Owner: keep only categories whose use is shown in this post and the video. -->

- **Best Use of Gemma**: Gemma 4 E2B is the reader in the local app and produced the replay's saved answers.
- **Best Use of Render**: hosts the interactive fictional replay.
- **Best Use of GitHub Copilot** (GitHub Actions route): tests, protected-evidence check and cache-only re-scoring on pushes and pull requests to `main`.
- **Best Use of Sentry Agent Tracing**: opt-in traces that carry no message content from my code; the timeout finding above came from them.

## My Agent Session

<!-- Optional. Remove this section unless you save and embed or link a session. -->

---

*AI assistance: <!-- Owner: name the AI tools you used, e.g. "This project was built with AI coding assistants (…), with every change reviewed and tested by me." -->*
