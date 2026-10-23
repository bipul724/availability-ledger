<!--
REL-05 submission post, v2 rewrite 2026-10-23 (after reading the Week 1 / Weekend winners and the current Week 3 field). NOT PUBLISHED.
Owner checklist before publishing (nothing here has been posted or sent):
  1. IMAGES VERIFIED 2026-10-23: all seven public image URLs return HTTP 200 and match the local PNG files byte for byte.
     Use cover.png in DEV's cover-image field. Body image links are live; you may instead replace each image line with DEV's upload result.
     Check every image in Preview. The exact placements, filenames and captions are in docs/demo/post-image-guide.md.
     There is one cover and six inline screenshots; placement comments are editor instructions, not article text.
  2. AI disclosure (required by DEV guidelines): the last line says what was AI-assisted. Make sure it's true for you, name your coding tools if you want,
     and set the AI-disclosure option in DEV's editor to match. This post was drafted by an AI assistant from the project's records.
  3. Optional, but it strengthens the Sentry category: add ONE redacted Sentry trace screenshot where the comment in "Sentry Agent Tracing" says so.
     No DSN, no location values, no message text. If you don't have a clean one, leave the comment; the text stands on its own.
  4. Optional: save your agent session with DevRelay and add a "My Agent Session" section. Judges like it; it isn't required.
  5. Deadline: the sources conflict. The rules text says 25 Oct 11:59 PM PDT (26 Oct 12:29 PM IST), but the event API's end time is
     2026-10-25T06:59Z = 25 Oct 12:29 PM IST. Publish before 25 Oct 12:29 PM IST to be safe (TASKS REL-04). Confirm your eligibility.
  6. Title alternatives if you prefer a shorter one:
       - "Let AI read, you decide: Gemma 4 turns a week of volunteer chat into a sheet I just say yes to"
       - "Gemma 4 missed Maria's cancellation. A keyword list caught it. That's the whole design."
  7. Copy everything below this comment (front matter included) into DEV's editor, then delete this comment there.
Facts: every number and quote is checked against evaluation/RESULTS.md, fixtures/, ui/ and a local replay of the saved outputs on 2026-10-23 (see PROGRESS "REL-05: post rewrite").
-->
---
title: "Availazy: Gemma 4 reads the volunteer group chat on my laptop, Python does the dates, and I just say yes or no"
published: false
tags: devchallenge, hf26challenge, gemma, opensource
cover_image: https://raw.githubusercontent.com/bipul724/availability-ledger/main/docs/demo/post/cover.png
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

> 🦥 **TL;DR.** Paste a week of volunteer chat messages. **Gemma 4**, running locally in Ollama, copies the words that matter ("Tuesday", "after 3", "if my work shift gets moved"). Plain **Python** turns them into dates, times and a day-by-day history. You **accept or reject** each suggestion beside the message it came from, and only what you accept reaches the final sheet.
>
> ▶️ [5:48 demo](https://www.youtube.com/watch?v=Qlq_kEsDr4g) · 🧪 [Try the replay in your browser](https://availability-ledger-replay.onrender.com/app) · 💻 [Code, MIT licence](https://github.com/bipul724/availability-ledger)

## Thursday, 9:10 a.m.

On Monday, Maria posts in the volunteer group chat:

> I can do Tuesday and Thursday mornings.

On Thursday she posts again:

> Change of plans — Thursday doesn't work anymore, sorry! Tuesday morning still good. I can add Friday 2-5.

There are 48 more messages that week. Priya can do "Monday after 3". Kofi "might be able to do Thursday afternoon if my work shift gets moved". Rui writes "Next Tuesday" on a Monday, which could mean tomorrow or the Tuesday after. Somebody has to read all of it, remember who changed their mind, and type it into a sheet. Then somebody changes their mind again.

Riverside Community Pantry doesn't exist. The pantry, its 18 volunteers and all 50 messages are invented, so this could be built and tested without touching anyone's real chat. But if you've ever coordinated volunteers, you've lived this week.

## What I Built

**Availazy** is a local review tool for the person who asks "when can you help?" and then has to make sense of the answers.

<!-- IMAGE 1: upload landing.png immediately below this paragraph. Keep the caption below the uploaded image. -->
![Availazy landing page: Local AI for Coordinators Who Have Better Things to Do](https://raw.githubusercontent.com/bipul724/availability-ledger/main/docs/demo/post/landing.png)

*Availazy turns volunteer messages into suggestions you can review beside their source.*

You paste dated chat messages (or a WhatsApp text export) and your volunteer list, pick the week, and Availazy:

- 📝 **suggests availability records**, each shown beside its message with the quoted words highlighted;
- 🔁 **keeps everyone's history day by day**, so a correction replaces the earlier answer, a cancellation removes it, and a "maybe" stays a maybe until the person confirms;
- ✋ **refuses to guess.** Anything the words don't settle goes on a **Needs a decision** list;
- ✅ **exports a final sheet built only from what you accepted.** It says *complete* only when every message is marked reviewed, nothing is pending and nothing is unresolved. Otherwise it says *provisional*, and it still downloads.

It records **availability**, not shift assignments. The person who gets to be lazy is the coordinator: they stop retyping and start deciding.

## Demo

{% embed https://www.youtube.com/watch?v=Qlq_kEsDr4g %}

The video opens with the local app: Gemma 4 reads two invented messages live, through Ollama, on my laptop. Then it switches to the hosted replay for the full week.

**Try it yourself:** <https://availability-ledger-replay.onrender.com/app>. This is a **replay**, not live inference. It serves the fictional week with Gemma's answers saved in advance, so it runs on free hosting without a model. Reviewing, history, the chart and both exports all work; pasting your own messages is switched off. Free hosting sleeps when idle, so the first visit can take about a minute.

There's also an illustrated guide with diagrams at [/docs](https://availability-ledger-replay.onrender.com/docs).

## Gemma missed Maria's cancellation. That's the point.

When Gemma read Maria's Thursday message in the saved run, it got her Tuesday right and her new Friday right, and it **missed the cancellation completely**.

So Availazy doesn't trust one reader. In the default mode, a plain keyword reader reads every message alongside the model. When the rules see a cancellation the model didn't, the app adds it, **flagged**, so I can check it:

<!-- IMAGE 2: upload maria-change-of-plans.png here, before the paragraph beginning "Until I accept it". -->
![Maria's "change of plans" message. Two cards come from the model; the third, Thursday unavailable, is marked "Added by the rules: possible cancellation the model missed"](https://raw.githubusercontent.com/bipul724/availability-ledger/main/docs/demo/post/maria-change-of-plans.png)

*Gemma found Tuesday and Friday. The rules added the Thursday cancellation for review.*

Until I accept it, the sheet shows Thursday as a *pending change*. One click on **Accept** and Thursday is gone from the final sheet. In **Model only** mode, the same replay leaves Maria on Thursday morning. That one message is the whole argument for running two readers.

## How I Built It: the model reads, code decides

The design is one strict split:

```text
message ──▶ Gemma 4 E2B (Ollama, local) ──▶ copied words + a proposed status
        └─▶ keyword rules ─────────────────▶ a second opinion
                         │
                         ▼
     Python: who, which date, which hours, does the quote exist,
             what does this replace, what is still unsure
                         │
                         ▼
     You: accept / reject / edit, mark each message reviewed
                         │
                         ▼
     Final sheet (accepted records only) + review log
```

**1. Gemma copies words; it doesn't do dates.** For each message, Gemma fills a JSON schema that Ollama enforces. This is its real saved answer for Maria's "Tuesday morning still good":

```json
{"person": "SENDER", "day_text": "Tuesday", "time_text": "morning",
 "status": "available", "condition": "", "replaces_earlier": false,
 "excerpt": "Tuesday morning still good"}
```

No date and no hours, just the words. Gemma didn't even mark it as a replacement (`"replaces_earlier": false`). Python spotted "Change of plans" and marked Maria's new answers as replacing her old ones, with a visible note on each card. **Python** also works out that "Tuesday", sent on Thursday 5 November for the week of 9 November, means **10 November**, and that "morning" means a fixed window:

```python
DEFAULT_PERIODS = {
    "morning": ("09:00", "12:00"),
    "afternoon": ("13:00", "17:00"),
    "evening": ("17:00", "20:00"),
}
```

Open ranges are code too. "After 3" runs to 20:00, the end of the planning day, and the card says so:

<!-- IMAGE 3: upload priya-after-3.png here, after the explanation of the 20:00 cutoff. -->
![Priya's message "Monday after 3 works, and Wednesday afternoon." becomes Mon 9 15:00–20:00 and Wed 11 13:00–17:00, with the note "'after 3' runs to 20:00"](https://raw.githubusercontent.com/bipul724/availability-ledger/main/docs/demo/post/priya-after-3.png)

*“After 3” becomes 15:00–20:00, with the assumption written on the card.*

**2. Every quote is checked against the message.** If the model's quote *and* its day/time words are both missing from the message, the suggestion is **not applied** unless you choose "Use it anyway". If only some words are missing, it's flagged.

**3. History is kept in order.** Later messages change only the days and times they mention. Kofi's "if my work shift gets moved" stays *conditional* until his later "my shift got moved, so Thursday afternoon is a yes". Olu's "I have to drop out for the rest of this week", sent on a Wednesday, cancels Wednesday through Sunday, taking out his Thursday evening and Saturday morning:

<!-- IMAGE 4: upload changes-over-time.png here, at the end of point 3 and before point 4. -->
![An excerpt of the change history, with replacements and cancellations linked to their source messages](https://raw.githubusercontent.com/bipul724/availability-ledger/main/docs/demo/post/changes-over-time.png)

*An excerpt of the change history, with replacements and cancellations linked to their source messages.*

**4. When the words don't settle it, it asks.** "Next Tuesday" sent on a Monday could be two dates. "This Saturday" sent the week before is outside the week. A name that matches nobody on the roster isn't guessed:

<!-- IMAGE 5: upload needs-a-decision.png here, at the end of point 4 and before point 5. -->
![Needs a decision: ten items, including "Which day? 'next tuesday' sent on Mon 09 Nov could be 10 Nov or 17 Nov" and "2026-11-07 is outside the selected week"](https://raw.githubusercontent.com/bipul724/availability-ledger/main/docs/demo/post/needs-a-decision.png)

*Ambiguous dates, unmatched names and unresolved conditions stay on the decision list.*

**5. The calm wrong answer.** Marta asks: *"Is Maria still doing Tuesday morning? If not I can take it."* Gemma filed Marta's offer **under Maria**, as a conditional Tuesday. It's wrong, and it looks perfectly reasonable. That's why every suggestion sits beside its message, and why this one carries "Only one of the two readers found this":

<!-- IMAGE 6: upload m48-wrong-person.png here, before "One click on Reject". -->
![m48 from Marta Lopes, with the model's suggestion filed under Maria Lopez as conditional Tuesday 09:00–12:00 and the flag "Only one of the two readers found this"](https://raw.githubusercontent.com/bipul724/availability-ledger/main/docs/demo/post/m48-wrong-person.png)

*Marta wrote the message, but Gemma assigned the offer to Maria. Reviewing the source makes the mistake visible.*

One click on **Reject** and Maria's Tuesday is firm again.

**6. Only accepted records reach the sheet.** Here are the first rows of the real export from the replay, after I accepted Maria's cancellation, rejected the m48 mix-up, accepted the 39 warning-free suggestions and marked two messages reviewed:

```text
# availability-final v1; week=2026-11-09; status=provisional; unreviewed=m01 m03 … m50; pending=21; blocking_issues=0
volunteer,date,start,end,status,condition,cell_state,sources
Maria Lopez,2026-11-10,09:00,12:00,available,,confirmed,m28.1
Maria Lopez,2026-11-13,14:00,17:00,available,,confirmed,m28.2
Marta Lopes,2026-11-09,09:00,12:00,available,,needs_review,m17.1
```

*(The `unreviewed` list is shortened here.)* Maria has Tuesday and Friday, and no Thursday. Her messages are marked reviewed, so her cells are `confirmed`. Everyone else is `needs_review`, and the whole file honestly says `provisional`.

**The stack is boring on purpose:** a Python standard-library server, plain HTML/CSS/JS with no framework or CDN, and Ollama on `127.0.0.1`. The only optional dependency is `sentry-sdk`, for opt-in tracing.

## The Lazy Payoff 🦥

Here's the fictional week, by the numbers, from the replay:

| | |
|---|---|
| Messages | **50** (one exact repeat is collapsed automatically) |
| Suggestions, each beside its quote | **67** |
| Accepted with **one click** (no warnings) | **39** |
| Left for a real decision (a warning, or not applied) | **28** |
| Items on the *Needs a decision* list | **10** |
| Gemma + rules reading the week on my 8 GB Apple M2 | **131 s** end to end (one dated run, not a benchmark) |

So the work shifts from reading 50 messages and typing a sheet to **checking 28 flagged suggestions**, each with its quote right next to it. The model reads the whole week in about two minutes: long enough to make a cup of tea.

I haven't timed a real coordinator, so I won't claim minutes saved. The repo has a written protocol for that study; it hasn't been run.

## How well does it work?

I didn't want to grade my own homework, so a **separate ChatGPT session wrote a test week I'd never seen** (set C: 24 fictional messages; I rewrote five of them). Its files were frozen by hash before any implementing agent saw them, and then it was **scored once**. That first score is kept exactly as it came out:

| Reader | Person-days right | Silent errors | Cancellations missed on the sheet | Sheet agreement with the answer key |
|---|---|---|---|---|
| Keyword rules only | 15/20 | 5 | 4/8 | 0.433 |
| Gemma 4 E2B only | 17/20 | 2 | 4/8 | 0.403 |
| **Gemma 4 E2B + rules** | **17/20** | **2** | **2/8** | **0.527** |

All suggestions were left pending and nobody reviewed them: this scores the draft sheet *before* a human touches it.

**Four things I didn't expect:**

1. **The keyword list earned its seat.** On the sheet, rules alone (0.433) actually beat Gemma alone (0.403). Gemma read more person-days right, but each reader caught things the other missed. Together they halved the missed cancellations.
2. **"Mostly right" can still make a wrong sheet.** Gemma + rules read 17 of 20 person-days right, yet the sheet matched only about half the time slots. The biggest culprit was *"Please change my availability on monday to 1-4 pm"*. The hours were right, but nothing treated it as a *replacement*, because "change" wasn't one of my replacement words. So the old all-day Monday stayed underneath.
3. **Every fix went into Python, not the prompt.** The prompt is the same version that was scored. Five deterministic fixes followed: explicit dates beat weekday words, "change" became a replacement cue, a firm follow-up settles a maybe, "T. Vekar" is an ambiguity rather than a stranger, and the rules learned more negations. Re-scored from the *same saved Gemma outputs*, set C now reaches 1.0, but I label that **post-hoc**: I fixed what I'd seen, so it proves little about new messages.
4. **Honest numbers are less impressive and more useful.** An earlier set B (20 messages) scored 30/35 person-days and 0.776 sheet agreement on its first scoring. Every frozen table, every caveat and every after-the-fact change is in [RESULTS.md](https://github.com/bipul724/availability-ledger/blob/main/evaluation/RESULTS.md).

## Built with

- 🧠 **Gemma 4 E2B** ([`gemma4:e2b-it-qat`](https://ollama.com/library/gemma4:e2b-it-qat), Apache 2.0) in **Ollama**. About a 4.3 GB download and about 1.6 GB of memory once loaded on my 8 GB Mac, so it runs alongside a browser. It's the reader in the local app, and it produced every saved answer in the replay.
- ☁️ **Render** hosts the [fictional replay](https://availability-ledger-replay.onrender.com/app), so judges can click through a full week without installing anything. The server runs in a demo mode that refuses any message, roster or week it didn't serve, and it never calls a model.
- ✅ **GitHub Actions** runs on every push and pull request to `main`, with three jobs: 116 unit tests (8 tracing tests skip without the optional SDK); a SHA-256 check that the frozen evaluation results haven't been touched; and a re-score of all three test sets from the saved model outputs, with no model calls. [Run #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754) passed all three jobs for the release.
- 🔭 **Sentry Agent Tracing** is opt-in and off by default. When on, two allowlists in my adapter limit what's sent to structure: timings, token counts, model and stage names. Message text, names, quotes, prompts and replies are excluded, and offline tests check that planted fake content never appears. The traces earned their keep. In one run, **four model calls hit the 300-second client deadline** waiting for Ollama. A later run made **49 calls in 1.42 minutes with no errors**. (The traces don't say *why* the earlier calls stalled, and I won't pretend they do.) One caveat I found: received traces showed location (geo) attributes that my code doesn't send. After a settings change, the four I inspected appeared filtered, but I haven't audited everything Sentry receives ([dated evidence](https://github.com/bipul724/availability-ledger/blob/main/docs/SENTRY_HANDOFF.md)).

<!-- OPTIONAL IMAGE 7 (not captured): one real redacted Sentry trace goes here, immediately after the Sentry bullet and before the GitHub embed. Show model-call duration/status only; exclude DSN, location values and message text. Caption only what that trace shows. Omit this image if unavailable; do not use a mock dashboard. -->

{% github bipul724/availability-ledger %}

## Why Does Open Innovation Matter?

Volunteer availability is quietly personal. "I'm at a wedding." "If my work shift gets moved." Read together, a week of these messages maps people's families, jobs and lives. Here's what an open model on the coordinator's own laptop makes possible:

1. **The messages stay on the computer.** In the local app they go only to Ollama on `127.0.0.1`. There's no cloud AI service in the loop, and optional tracing is off unless you turn it on.
2. **No account, no API key, no per-message bill.** Once Ollama and the model are installed, it works offline. A small food pantry can afford "free forever".
3. **It fits the hardware people actually have.** An 8 GB laptop is enough, so the volunteer coordinator doesn't need a GPU or a budget.
4. **It can be checked.** The prompt, the schema, the rules, the test sets and the frozen scores are all in the repo. Anyone can re-score them from the saved outputs without running a model, which is exactly what CI does.
5. **It can be swapped.** The model is a menu choice of whatever Ollama has installed. I also evaluated Qwen3.5 4B against the same answer keys.

A hosted API might be smarter. But the right answer to "where do my volunteers' messages go?" should be "nowhere".

## What it can't do (yet)

- It has only seen **fictional** messages. No real coordinator has used it, and the test sets share an author with the code, except set C.
- Times are read as written; the timezone field is stored but not converted. "At 9" isn't read.
- Up to 20 volunteers, one browser tab, and nothing is saved between sessions.
- The keyword reader still misreads some phrasings. It read "Saturday 9–12 if it isn't raining" as *unavailable* instead of *conditional*, which is exactly why every suggestion sits beside its message.
- Not tested in Safari, Firefox or with a screen reader.

## Prize Categories

- **Best Use of Gemma**: Gemma 4 E2B is the local reader, held to a strict "copy the words, code does the maths" contract, measured against a rules baseline and a frozen test set written by a separate AI session.
- **Best Use of Render**: the interactive replay that lets anyone review a full fictional week without installing a model.
- **Best Use of GitHub Copilot** (via GitHub Actions): unit tests, a frozen-evidence integrity check and a cache-only re-score of every test set on every push and pull request.
- **Best Use of Sentry Agent Tracing**: opt-in, content-free model-call traces that surfaced the 300-second timeouts.

---

Slow and steady: the model reads, the code reconciles, and a person decides. If you coordinate volunteers, how do you collect availability today, and what's the message that always breaks your spreadsheet? 🦥

*AI assistance: I built Availazy with AI coding assistants, and this post was drafted with an AI assistant from the project's own records. I reviewed and edited it, and every number links back to the repo.*
