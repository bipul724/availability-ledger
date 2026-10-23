# Demo run sheet (DEP-03): what to click, type, show and say

Companion to [script.md](script.md), written 2026-10-23. It records three takes (A, B, C) and joins them in iMovie. Times are positions in the **finished** video, after the waiting is cut. All data is fictional.

## Setup, about 10 minutes before recording

**Terminal 1:**
```bash
ollama serve
```
If it says "address already in use", Ollama is already running. Leave it.

**Terminal 2:**
```bash
cd "/Users/bipulchamoli/Desktop/week 3/availability-ledger" && env -u SENTRY_DSN -u LEDGER_DEMO python3 server.py 8780
```

**Open these Chrome tabs, left to right:**

| Tab | Link | Prepare it like this |
|---|---|---|
| 1 | https://availability-ledger-replay.onrender.com/ | Wait until the page shows. Scroll to the top. |
| 2 | http://127.0.0.1:8780/app | Fill in as below, **but don't click Suggest records yet**. |
| 3 | https://availability-ledger-replay.onrender.com/app | Wait for "Fictional demo week loaded (50 messages). Pick a reader and press Suggest records." **Don't click Suggest records yet.** |
| 4 | https://github.com/bipul724/availability-ledger/blob/main/evaluation/RESULTS.md | Scroll to "Set C: independent, scored once" so the table is on screen. |
| 5 | https://github.com/bipul724/availability-ledger/actions | Click the top run; it should show three green jobs. |
| 6 | https://availability-ledger-replay.onrender.com/docs | Scroll to the top. |

**Fill in tab 2:**
- **Week starting (Monday):** `2026-11-09`
- **Reader:** `Model only`
- **Model:** `gemma4:e2b-it-qat`
- **Volunteers box:**
  ```
  Ana Example
  Ben Example
  ```
- **Messages box:**
  ```
  2026-11-09 08:00 | Ana Example | I can help Tuesday 09:00-12:00.
  2026-11-09 08:05 | Ben Example | I can help Thursday 13:00-15:00.
  ```

**Also before recording:**
- Delete old `availability-final-…csv` files from Downloads.
- Set Chrome zoom to 110% (Cmd and +).
- Hide the bookmarks bar (Cmd+Shift+B).
- Close other heavy apps.

**For each take:** press Cmd+Shift+5 → **Record Selected Portion** → drag over the Chrome window → **Options → Microphone** → **Record**. Stop with ⏹ in the menu bar.

---

## Take A: shots 1–2 · video 0:00–0:55

| Video time | Do this | Say this |
|---|---|---|
| 0:00 | Tab 1 is showing the landing page headline. Scroll down slowly, once. | "Every week, a volunteer coordinator sends one question: 'When can you help?' And every week, the answers come back as dozens of chat messages. This is Availazy." |
| 0:15 | Click **tab 2** (local app, already filled in). Move the mouse over the Messages box. | "Offers, corrections, cancellations, maybes, all mixed together. Turning that into a sheet means reading every message and retyping it, and then reading it again when someone changes their mind." |
| 0:28 | Click **Suggest records**. Wait for the two cards; cut the wait in editing. | "Here are two invented messages. Gemma 4, an open model, reads them live, through Ollama, on this laptop. The messages are read right here, not sent to a cloud AI service." |
| 0:45 | Point at Ana's card (Tue 10, 09:00–12:00) and Ben's card (Thu 12, 13:00–15:00), and their highlighted quotes. | "Each suggestion sits next to the exact words it came from." |

**Check before keeping the take:** Ana is Tue 09:00–12:00 and Ben is Thu 13:00–15:00, both available, with nothing under **Needs a decision**. If not, redo it.

---

## Take B: shots 3–9 · video 0:55–3:30

| Video time | Do this | Say this |
|---|---|---|
| 0:55 | Click **tab 3** (replay). Hold on the yellow banner at the top, "Replay: fictional messages and saved Gemma 4 outputs…". | "For a full week, here's the public replay: fifty fictional messages, with answers Gemma gave earlier on a laptop, saved and replayed. No model runs on this server." |
| 1:05 | Check **Reader** says `Model + rules cross-check`. Click **Suggest records**. Wait until it says "Replayed 50 messages in … s from saved outputs." (cut the wait). | *(silence, or keep talking over the next line)* |
| 1:10 | Press **Cmd+F**, type `Monday after 3`, press Enter, then Esc. Point at Priya's two cards: Mon 9, 15:00–20:00 and Wed 11, 13:00–17:00. | "Here's the rule that makes it trustworthy. Gemma only copies phrases, like 'Monday', 'after 3' and 'afternoon'. Plain Python turns them into dates and hours: 'after 3' runs to eight, the end of the planning day, and 'afternoon' is one to five. Code checks every phrase against the message, keeps each person's history day by day, and does every count." |
| 1:35 | **Cmd+F**, type `Change of plans`, Enter, Esc. This is Maria's message m28. Point at the **Thursday** card's yellow badge, "Added by the rules: possible cancellation the model missed". | "And here's why it reads every message twice. Maria cancels Thursday. Gemma picked up her Tuesday and her new Friday, but it missed the cancellation. A simple keyword reader runs alongside the model, caught it, and added it, flagged, so I can check it." |
| 1:52 | In the right-hand panel, scroll to **Availability sheet**. Point at Maria Lopez's Thursday cell showing **pending change**. Then click **Accept** on the Thursday card. | "Until I decide, the sheet marks Thursday as a pending change. I accept it, and Thursday won't reach the final sheet." |
| 2:05 | **Cmd+F**, type `shift gets moved`, Enter, Esc. Point at Kofi's card: Thu 12, 13:00–17:00, conditional. Then **Cmd+F**, `shift got moved`, Enter, Esc, and point at the m29 card: Thu 13:00–17:00, available. | "Every change is kept in order. Kofi's 'maybe, if my shift moves' stays conditional until he confirms." |
| 2:15 | In the right panel, scroll to **Changes over time**. Point at the two m49 lines for Olu Adeyemi (Thu 12 and Sat 14, "marked unavailable, cancelled"). | "Olu drops out 'for the rest of this week'. He sent that on a Wednesday, so code cancels Wednesday through Sunday, which takes out his Thursday evening and his Saturday morning." |
| 2:25 | In the right panel, scroll up to **Needs a decision**. Point at three lines in turn: the m26 Kofi line ("2026-11-07 is outside the selected week"); the m41 line ("Which day? 'next tuesday'…"); and the m29 line ("Earlier answer replaced — check"). | "When the words don't settle it, it asks instead of guessing. 'This Saturday', sent on the fourth, is a different week, so it stays out. 'Next Tuesday', sent on a Monday, could be two dates, so I pick. And when a change word replaces an earlier answer, it tells me, so I can check." |
| 2:45 | In **Needs a decision**, click the **m48** link (Maria Lopez … still conditional). This is Marta's message. Point at the card filed under **Maria Lopez**, conditional. | "Gemma isn't perfect. Marta offers to cover Maria's Tuesday, and the model files the offer under Maria." |
| 2:55 | Click **Reject** on that card. Scroll the right panel to **Availability sheet** and show Maria's Tuesday back to **09:00–12:00** without the "?". | "That's exactly why every suggestion sits beside its message. One click rejects it, and Maria's Tuesday is firm again." |
| 3:05 | Scroll the left side to the top. Click **Accept all suggestions without warnings**. Point at the message under **Suggest records**: "Accepted … suggestions that had no warnings." | "The review is fast because it's decisions, not typing. Once I've checked them, the clean suggestions go in with one button; flagged ones wait for me." |
| 3:12 | **Cmd+F**, `Tuesday and Thursday mornings`, Enter, Esc, then click **Mark message reviewed** on that message (m02). **Cmd+F**, `Change of plans`, Enter, Esc, and click **Mark message reviewed** (m28). Point at the line above the messages: "2 of 49 messages marked reviewed. Final sheet export: provisional…". | "Accepting a card and marking a message as read are separate on purpose." |
| 3:18 | In the right panel, scroll to the bottom. Click **Export final sheet (CSV)**. Open the downloaded file from Chrome's download bar (it opens in Numbers). Show line 1 (`status=provisional`), then Maria's two rows (Tue 09:00–12:00 and Fri 14:00–17:00) with `cell_state` `confirmed` and no Thursday. | "The final sheet takes only accepted records, and it calls itself complete only when every message is marked reviewed, nothing is pending and nothing is unresolved. Until then it says 'provisional', but it still downloads." |

**If you click the wrong thing:** stop, reload tab 3 (Cmd+R), and record take B again from the start. A reload resets everything.

---

## Take C: shots 10–11 · video 3:30–4:15

| Video time | Do this | Say this |
|---|---|---|
| 3:30 | Click **tab 4** (RESULTS.md, already on the set C table). Point at the **Gemma 4 E2B + rules** row: 17/20 and 0.527. | "We tested it on twenty-four messages it had never seen, written by a separate AI session and edited by me, then frozen before scoring. It read seventeen of twenty person-days right, but its draft sheet, before any human review, matched the answer key on only about half the time slots." |
| 3:43 | Stay on tab 4; scroll down a little to the "Errors, by message" table. | "Most of the misses were in our own code, not the model: a correction that didn't replace the old answer, and a dated cancellation put on the wrong Saturday. We kept that first score as it was, fixed the code, and label everything after it as after-the-fact." |
| 3:55 | Click **tab 5** (the Actions run). Show the three green jobs, then scroll to the score table. | "Every push to main re-checks the frozen evidence on GitHub Actions." |
| 4:02 | Click **tab 6** (`/docs`). Scroll slowly through one diagram. Then click **tab 3** so the replay address shows. | "Slow and steady: the model reads, the code reconciles, and you decide. The model is open, it runs on an eight-gigabyte laptop, and your volunteers' messages never go to a cloud AI. Try the replay on the fictional week, or run Availazy on your own computer." |
| 4:15 | Stop recording. | — |

**Optional Sentry line** (only with a redacted trace from your own Sentry account): add a tab after tab 5. At about 4:00, show the trace and say: "And with tracing switched on, Sentry showed four model calls hitting the five-minute limit on one run, and none on the next."

---

## Joining in iMovie
1. **File → New Movie**, then drag in takes A, B and C, in that order.
2. Trim each clip's start and end by dragging its edges.
3. Cut the waits: put the playhead where the wait starts and press **Cmd+B**, do the same where it ends, select the middle piece and press Delete. There are two waits: take A at 0:28 (live model) and take B at 1:05 (replay loading).
4. **Titles** (the T button), placed over the start of each take:
   - Take A at 0:15: "Local app · live Gemma 4 on this laptop · two invented messages"
   - Take B at 0:55: "Hosted replay · fictional week · saved Gemma outputs, no live model"
   - Take C at 3:30: "Frozen first score · fictional set C · before human review"
5. **File → Share → File → 1080p**, then save and upload (YouTube, unlisted is fine).
