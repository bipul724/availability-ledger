<!--
REL-05 submission-post DRAFT, prepared 2026-10-22 from the repository and checks run that day. NOT PUBLISHED.
Owner, before publishing (each item is yours; nothing here has been posted or sent):
  1. Replace [VIDEO LINK — not recorded yet] with the real video URL, or delete that line if you rely on the replay link alone.
  2. Confirm your personal eligibility and the deadline (sources conflict: see docs/COMPETITION.md and TASKS REL-04).
  3. Confirm the Prize Categories list against what is actually shown in the post and video.
  4. Fill in the AI-assistance disclosure with the tools you actually used.
  5. Decide whether to keep "My Agent Session" (optional) and "The Lazy Payoff" (optional); remove either if unused.
  6. After pushing the release, confirm the new GitHub Actions run passed before keeping "The latest run on `main` passed all three jobs" (last observed: "tests #17" on a4bebb7).
  7. Copy everything below the line into DEV's editor (front matter included), then delete this comment.
Numbers come from evaluation/RESULTS.md (frozen tables), PROGRESS.md and the 2026-10-22 release checks.
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

- **Video:** [VIDEO LINK — not recorded yet]
- **Try it in your browser:** <https://availability-ledger-replay.onrender.com/app>. This is a read-only **replay**: a fictional pantry's week (50 messages, 18 volunteers) with Gemma's answers saved in advance, so it runs on free hosting without a model. Review, history, the chart and both exports work; pasting your own messages is switched off. The free instance sleeps when idle, so the first visit can take about a minute.
- **Read your own messages:** run it locally (below). Live Gemma inference happens only in the local app.

## Code

{% github bipul724/availability-ledger %}

Python standard library only, plain HTML/CSS/JS, MIT licence. A guide with diagrams is at <https://availability-ledger-replay.onrender.com/docs>.

## How I Built It

The design rule is a strict split: **the model proposes, code decides, a person accepts.**

1. **Gemma 4 E2B copies phrases.** Running in Ollama on the laptop (`gemma4:e2b-it-qat`, Apache 2.0), the model fills a JSON schema per message: who, the day words, the time words, available or not, any condition, and a verbatim quote. It never works out a date. On an 8 GB Apple M2 a 50-message week took 131 s end to end in the app, with the model using about 1.6 GB once loaded.
2. **Python decides.** Ordinary code turns "next Tuesday" and "after 3" into dates and times using the message's own timestamp, checks that the quoted words really appear in the message, cross-checks the model against a rule-based reader, keeps the per-day history and does every count. Ambiguities are flagged, never guessed.
3. **You decide.** Accept, edit or reject each suggestion; marking a message reviewed is a separate, explicit step. Only accepted records reach the final sheet.

Three readers are available: *Rules only* (no model), *Model only*, and *Model + rules*, the default.

**Infrastructure I actually used:**

- **Render** hosts the fictional replay. The server runs in a demo mode that refuses any message, roster or week it did not serve, and it never calls a model.
- **GitHub Actions** runs on every push: 116 unit tests (8 tracing tests skip without the optional SDK), a SHA-256 check that the frozen evaluation results are untouched, and a re-score of all three test sets from the saved model outputs. The latest run on `main` passed all three jobs.
- **Sentry Agent Tracing** is opt-in and off by default. When you turn it on, two allowlists in my code reduce every span to structural metadata such as timings, token counts, the model name and stage names; message text, names, quotes, prompts and replies are never sent, and the tests check that a planted fake name never leaves. The traces were useful: in one run four model calls hit Ollama's 300-second timeout, and a later 49-call run took 1.42 minutes with no errors. One honest caveat: the traces Sentry received displayed location (geo) attributes, which my code does not send. After I changed Sentry's settings, the four visible geo values on the chat span and its parent that I inspected appeared filtered. Where that location data comes from, and a complete audit of everything Sentry receives, remain unverified.

## Why Does Open Innovation Matter?

Group-chat availability is personal: names, schedules, family plans, health. An open-weight model that runs on the coordinator's own laptop means those messages are read right there. There is no account, no API key, no per-message bill and no cloud database, and it keeps working offline. Because the model and the code are open, anyone can check exactly what happens to a message. That is the point of the model/code split: the part that can be wrong in creative ways (the model) only copies words, and the part that decides (plain Python) is small enough to read and test.

## How well does it work?

I tested on fictional messages only, written for this project; I wrote sets A and B myself, and an isolated session wrote set C. I froze each set's first score before changing anything.

**Set C** (24 unseen messages, scored once, frozen):

| Reader | Units right | Silent errors | Missed cancellations | Final-sheet slot agreement |
|---|---|---|---|---|
| Rules only | 15/20 | 5 | 4/8 | 0.433 |
| Gemma 4 E2B only | 17/20 | 2 | 4/8 | 0.403 |
| Gemma 4 E2B + rules | 17/20 | 2 | 2/8 | **0.527** |

The units were mostly right, but the sheet was not: two corrections were read with the right times without replacing the earlier answer. I then fixed the causes (explicit dates, replacement cue words, firm follow-ups, an initial-plus-surname match, more negation forms) using new invented messages. Re-scored from the same saved outputs, set C reaches 1.0 slot agreement, but that number is **post-hoc**: the fixes were designed after seeing set C's errors, so it is not independent evidence. On the earlier set B (20 messages), Gemma + rules got 30/35 units with 3 silent errors and 0.776 slot agreement as first scored.

## The Lazy Payoff

I have not measured anyone's time, so I will not claim minutes saved. What I can show: reading is reduced to checking a quote and clicking, corrections and cancellations are reconciled for you, and the things a person must decide are collected in one list. A protocol for a real timing study is in the repo, but no real coordinator has used it yet.

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
- **Best Use of GitHub Copilot** (GitHub Actions route): tests, protected-evidence check and cache-only re-scoring on every push.
- **Best Use of Sentry** (Agent Tracing): opt-in traces that carry no message content from my code; the timeout finding above came from them.

## My Agent Session

<!-- Optional. Remove this section unless you save and embed or link a session. -->

---

*AI assistance: <!-- Owner: name the AI tools you used, e.g. "This project was built with AI coding assistants (…), with every change reviewed and tested by me." -->*
