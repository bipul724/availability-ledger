# YouTube upload kit (DEP-03)

Prepared 2026-10-23 for the owner's recorded demo. Every claim is taken from README, RESULTS, the DEV post draft and the run sheet; see "Fact sources" at the end. YouTube rejects `<` and `>` in titles and descriptions, so the text below uses neither.

## Title (pick one, all under 100 characters)

1. **Availazy: Local Gemma 4 Turns Volunteer Chat into an Availability Sheet You Check** (recommended)
2. Let AI Read, You Decide: Volunteer Availability from Chat with Gemma 4 and Python
3. Volunteer Chat In, Checked Sheet Out | Availazy demo (Gemma 4, open source)

## Description (copy everything inside the box)

```text
Availazy turns a week of volunteer chat messages into an availability sheet you check before you trust it. Let AI read. You decide.

A local open model, Gemma 4 E2B running in Ollama, copies phrases like "next Tuesday", "after 3" or "if my work shift gets moved". Plain Python turns them into dates and times, checks that the quoted words are really in the message, keeps each person's history day by day and does every count. You accept, reject or edit each suggestion beside the message it came from, and only accepted records reach the final sheet.

🔗 LINKS
▶ Try the replay: https://availability-ledger-replay.onrender.com/app
   A fictional week with Gemma's answers saved in advance. No model runs on that server. It is on free hosting that sleeps when idle, so the first visit can take about a minute.
💻 Code (MIT licence): https://github.com/bipul724/availability-ledger
📖 Illustrated guide: https://availability-ledger-replay.onrender.com/docs
📊 Evaluation record: https://github.com/bipul724/availability-ledger/blob/main/evaluation/RESULTS.md
🏆 Built for DEV's Hacktoberfest Open-Source AI Challenge, Week 3 "Slow and Steady": https://dev.to/challenges/hacktoberfest-week3-2026-10-19

⏱ CHAPTERS
0:00 The problem: availability buried in chat
0:28 Gemma 4 reads two invented messages on a laptop
0:55 A full fictional week, replayed
1:10 The model copies words, code decides
1:35 A second reader catches a missed cancellation
2:05 Changes kept in order
2:25 It asks instead of guessing
2:45 A real model mistake, rejected in one click
3:05 Review, then export the final sheet
3:30 How it was tested
3:55 Checks on GitHub Actions, and the guide

WHAT YOU'LL SEE
• A live local read: Gemma 4 reads two invented messages through Ollama on the laptop.
• The hosted replay: 50 fictional messages with saved Gemma outputs.
• A keyword reader runs beside the model and adds a cancellation Gemma missed, flagged for review.
• A conditional offer stays conditional until the person confirms it. "For the rest of this week", sent on a Wednesday, cancels Wednesday to Sunday.
• Dates outside the week and ambiguous phrases like "next Tuesday" sent on a Monday go to a "Needs a decision" list instead of being guessed.
• A real model mistake (an offer filed under the wrong person), rejected with one click.
• The final sheet takes accepted records only. It says "provisional" until every message is marked reviewed, nothing is pending and nothing is unresolved, and it still downloads.

HOW IT WAS TESTED
Set C is 24 fictional messages the system had never seen, frozen before scoring. At its first scoring, Gemma 4 + rules read 17 of 20 person-days right, but its draft sheet, before any human review, matched the answer key on only 0.527 of time slots. We kept that first score unchanged. Fixes made after seeing those errors are labelled post-hoc. Every push to main re-checks the frozen evidence on GitHub Actions.

BUILT WITH
• Gemma 4 E2B (gemma4:e2b-it-qat) in Ollama: the local reader
• Python standard library and plain HTML, CSS and JavaScript
• Render: hosts the fictional replay
• GitHub Actions: unit tests, a frozen-evidence check and a re-score from saved model outputs
• Sentry Agent Tracing: optional and off by default; my code sends timings and structure, not message text

HONEST NOTES
• Every name and message is fictional. No real coordinator has used it yet, and time saved has not been measured.
• The hosted replay is not live inference. To read your own messages, run Availazy on your own computer.
• Up to 20 volunteers. Times are read as written. The review lives only in the browser tab.

#Gemma #OpenSource #LocalAI
```

**Before you paste:**
- **Chapters:** the times follow the run sheet. Scrub your final video and change any time that moved in editing. YouTube needs the first chapter at `0:00`, at least three chapters, and each one at least 10 seconds long. Delete the whole CHAPTERS block if you'd rather skip them.
- **Sentry line:** this keeps the wording general because received traces showed location (geo) attributes that the app's code doesn't send ([SENTRY_HANDOFF](../SENTRY_HANDOFF.md)). Don't change it to "nothing leaves your machine" or "no personal data".
- **DEV post:** after you publish it, add a line under LINKS: `📝 Write-up: ` followed by the post URL.

## Thumbnail

- File: [thumbnail.png](thumbnail.png) (1280 × 720 PNG, about 128 KB; YouTube's limit is 2 MB).
- Source: [thumbnail.html](thumbnail.html). The message text is from the fictional demo week (m02 and m28, exactly as written on the landing page). Maria's three rows are what the replay shows after the run-sheet review: Tue 09:00–12:00 and Fri 14:00–17:00 kept, Thursday cancelled.
- To re-render after editing the HTML, run this from `docs/demo`:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1280,720 --screenshot="$PWD/thumbnail.png" "file://$PWD/thumbnail.html"
  ```
- A custom thumbnail needs a verified YouTube account (phone verification under youtube.com/verify).

## Upload settings

| Setting | Choose |
|---|---|
| Audience | No, it's not made for kids |
| Altered or synthetic content | No (a real screen recording with your own voice) |
| Category | Science & Technology |
| Visibility | Public or Unlisted. Both work for a DEV embed; Unlisted keeps it off search. |
| Tags (optional) | Gemma 4, Ollama, local AI, open source, volunteer coordination, Python, Hacktoberfest |

## Fact sources

| Claim | Source |
|---|---|
| Model copies phrases; Python resolves dates, times, evidence, history, counts | README "A local open model proposes and ordinary code decides"; CLAUDE.md purpose |
| Only accepted records reach the final sheet; complete/provisional rule; still downloads | README capabilities; `ledger/export.py` `confirmed_export`; post draft "What I Built" |
| Replay: fictional, saved outputs, no model on server, about a minute to wake | post draft "Demo"; `home.html` fine print |
| 50 messages; rules-added Maria Thursday cancellation; Kofi m13/m29; Olu m49 Wed–Sun; m26, m41, m48 | run sheet takes B rows, verified by an in-process replay of the saved outputs (PROGRESS DEP-03 entries) |
| Set C 24 messages, frozen first score 17/20 and 0.527, later fixes post-hoc | `evaluation/RESULTS.md` set C tables; post draft "How well does it work?" |
| Actions on pushes to main: unit tests, integrity check, cache-only re-score | `.github/workflows/tests.yml`; TESTING.md |
| Sentry optional and off by default; geo caveat | CLAUDE.md telemetry rule; SENTRY_HANDOFF |
| MIT licence | `LICENSE` |
| Up to 20 volunteers; times read as written; review only in the tab; not tested with real coordinators | README Limitations; post draft "Known limitations" |
| Challenge link | post draft first line |
