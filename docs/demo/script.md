# Demo script (DEP-03) · about 4–5 minutes

Version 2, written 2026-10-23. Every on-screen moment below was re-checked that day against the current code, replaying the fictional week from saved Gemma outputs with no model calls; the facts behind each spoken line are listed in [Fact sources](#fact-sources). Everything shown is fictional.

Narration: about 640 words, which is about 4¼ minutes at 150 words a minute and under 5 minutes at a slower 135. Read it with the microphone on while you click (Cmd+Shift+5 → Options → Microphone), one shot at a time, so voice and picture can't drift (D-37: no ElevenLabs). Retake a single shot if you stumble.

---

## Before you record (15 minutes)

1. **Wake the replay.** Open `https://availability-ledger-replay.onrender.com/app` and wait until the fictional week appears. Render's free service sleeps after 15 idle minutes and can take about a minute to wake.
2. **Start the local app for shot 2 (not traced).**
   - In one terminal: `ollama serve` (skip it if Ollama is already running).
   - In another, from the repository: `env -u SENTRY_DSN -u LEDGER_DEMO python3 server.py 8780`, then open `http://127.0.0.1:8780/app`.
3. **Close heavy apps.** The 8 GB Mac ran the model with other apps open, but memory warnings were seen during the slow first traced run.
4. **Dry run shot 2 once.** Use the take only if it gives exactly the expected result.
5. **Browser zoom 110–125%**, so text is readable in the video. Use one browser window and hide bookmarks.

## Shot list and narration

### 1. Cold open · 0:00–0:15
**Screen:** the replay site's landing page (`https://availability-ledger-replay.onrender.com/`), headline "Local AI for Coordinators Who Have Better Things to Do". Scroll slowly once.

> Every week, a volunteer coordinator sends one question: "When can you help?" And every week, the answers come back as dozens of chat messages. This is Availazy.

### 2. The problem, and a live local read · 0:15–0:55
**Screen:** the local app at `127.0.0.1:8780/app`.
- **Settings:** Week starting `2026-11-09`; Reader **Model only**; Model `gemma4:e2b-it-qat`.
- **Volunteers:** `Ana Example`, `Ben Example`, one per line.
- **Messages:**
  ```
  2026-11-09 08:00 | Ana Example | I can help Tuesday 09:00-12:00.
  2026-11-09 08:05 | Ben Example | I can help Thursday 13:00-15:00.
  ```
- Click **Suggest records**. Optionally show `ollama ps` in a terminal corner.
- **Expected (owner-verified 2026-10-23):** Ana Tue 10 Nov 09:00–12:00 and Ben Thu 12 Nov 13:00–15:00, both available, each beside its highlighted quote; nothing under **Needs a decision**.
- **Caption:** "Local app · live Gemma 4 on this laptop · two invented messages".

> Offers, corrections, cancellations, maybes, all mixed together. Turning that into a sheet means reading every message and retyping it, and then reading it again when someone changes their mind. Here are two invented messages. Gemma 4, an open model, reads them live, through Ollama, on this laptop. The messages are read right here, not sent to a cloud AI service. Each suggestion sits next to the exact words it came from.

### 3. A whole week, replayed · 0:55–1:10
**Screen:** switch to the replay tab. Hold on the banner "Replay: fictional messages and saved Gemma 4 outputs…". Keep **Model + rules cross-check**, click **Suggest records**, and let the 50 messages fill in.
- **Caption:** "Hosted replay · fictional week · saved Gemma outputs, no live model".

> For a full week, here's the public replay: fifty fictional messages, with answers Gemma gave earlier on a laptop, saved and replayed. No model runs on this server.

### 4. The model copies words; code decides · 1:10–1:35
**Screen:** message m03, Priya Nair: "Monday after 3 works, and Wednesday afternoon." Show its two cards: Mon 9 Nov 15:00–20:00 and Wed 11 Nov 13:00–17:00, with the quote highlighted.

> Here's the rule that makes it trustworthy. Gemma only copies phrases, like "Monday", "after 3" and "afternoon". Plain Python turns them into dates and hours: "after 3" runs to eight, the end of the planning day, and "afternoon" is one to five. Code checks every phrase against the message, keeps each person's history day by day, and does every count.

### 5. Two readers catch more than one · 1:35–2:05
**Screen:** message m28, Maria Lopez, sent Thu 5 Nov: "Change of plans — Thursday doesn't work anymore, sorry! Tuesday morning still good. I can add Friday 2-5."
- Point at the Thursday card's yellow badge "Added by the rules: possible cancellation the model missed".
- In the **Availability sheet**, point at Maria's Thursday showing **pending change**.
- Click **Accept** on that Thursday card.

> And here's why it reads every message twice. Maria cancels Thursday. Gemma picked up her Tuesday and her new Friday, but it missed the cancellation. A simple keyword reader runs alongside the model, caught it, and added it, flagged, so I can check it. Until I decide, the sheet marks Thursday as a pending change. I accept it, and Thursday won't reach the final sheet.

### 6. Changing minds, kept in order · 2:05–2:25
**Screen:**
- Press Cmd+F and find "shift gets moved". Show m13's Kofi card: Thu 12 Nov 13:00–17:00, conditional ("if my work shift gets moved").
- Find "shift got moved". Show m29's card: Thu 13:00–17:00, available.
- In the right-hand panel, scroll to **Changes over time** and point at the m49 lines for Olu Adeyemi ("marked unavailable, cancelled" on Thu 12 and Sat 14).

This list only shows changes (corrections, cancellations, settled conditions), so Kofi's first "maybe" is shown on its message card instead.

> Every change is kept in order. Kofi's "maybe, if my shift moves" stays conditional until he confirms. Olu drops out "for the rest of this week". He sent that on a Wednesday, so code cancels Wednesday through Sunday, which takes out his Thursday evening and his Saturday morning.

### 7. It doesn't guess · 2:25–2:45
**Screen:** **Needs a decision**. Point at three items:
- m26, Kofi Mensah, sent Wed 4 Nov: 7 Nov is outside the selected week.
- m41, Rui Costa: "Which day? 'next tuesday' sent on Mon 09 Nov could be 10 Nov or 17 Nov".
- m29: "Earlier answer replaced — check".

> When the words don't settle it, it asks instead of guessing. "This Saturday", sent on the fourth, is a different week, so it stays out. "Next Tuesday", sent on a Monday, could be two dates, so I pick. And when a change word replaces an earlier answer, it tells me, so I can check.

### 8. A real model mistake, caught · 2:45–3:05
**Screen:** message m48, Marta Lopes: "Is Maria still doing Tuesday morning? If not I can take it." Show the card filed under **Maria Lopez**, conditional, and Maria's Tuesday conditional on the sheet. Click **Reject**. Maria's Tuesday 09:00–12:00 is firm again.

> Gemma isn't perfect. Marta offers to cover Maria's Tuesday, and the model files the offer under Maria. That's exactly why every suggestion sits beside its message. One click rejects it, and Maria's Tuesday is firm again.

### 9. Review, then export · 3:05–3:30
**Screen:**
1. Click **Accept all suggestions without warnings**; the status line says how many were accepted.
2. Mark m02 and m28 reviewed (**Mark message reviewed**, or **M**).
3. Click **Export final sheet (CSV)** and open the file. Show line 1 (`status=provisional`, the unreviewed message IDs) and the `cell_state` column: Maria's rows (Tue 09:00–12:00 and Fri 14:00–17:00) are `confirmed`, and her Thursday is gone.

> The review is fast because it's decisions, not typing. Once I've checked them, the clean suggestions go in with one button; flagged ones wait for me. Accepting a card and marking a message as read are separate on purpose. The final sheet takes only accepted records, and it calls itself complete only when every message is marked reviewed, nothing is pending and nothing is unresolved. Until then it says "provisional", but it still downloads.

### 10. How we know · 3:30–3:55
**Screen, three quick cuts:**
1. The frozen set C table in `evaluation/RESULTS.md` (Gemma 4 E2B + rules row: 17/20, slot agreement 0.527). Caption: "Frozen first score · fictional set C · before human review".
2. The latest GitHub Actions run on `main`, all three jobs green, with the score table.
3. *(Optional)* One redacted Sentry trace (no DSN, account details or location values). Leave out its line if you don't show it.

> We tested it on twenty-four messages it had never seen, written by a separate AI session and edited by me, then frozen before scoring. It read seventeen of twenty person-days right, but its draft sheet, before any human review, matched the answer key on only about half the time slots. Most of the misses were in our own code, not the model: a correction that didn't replace the old answer, and a dated cancellation put on the wrong Saturday. We kept that first score as it was, fixed the code, and label everything after it as after-the-fact. Every push to main re-checks the frozen evidence on GitHub Actions. *(Optional:)* And with tracing switched on, Sentry showed four model calls hitting the five-minute limit on one run, and none on the next.

### 11. Close · 3:55–4:10
**Screen:** the guide at `/docs` (scroll one diagram), then the replay URL on screen.

> Slow and steady: the model reads, the code reconciles, and you decide. The model is open, it runs on an eight-gigabyte laptop, and your volunteers' messages never go to a cloud AI. Try the replay on the fictional week, or run Availazy on your own computer.

---

## Do not say (each would be false or unproven)
- **Any time saved, or "minutes per week".** No human timing has been measured.
- **"Nothing leaves your machine."** Opt-in tracing sends timing metadata to Sentry, and the replay runs on Render. Say messages are read on your own computer.
- **"The replay runs Gemma."** Its answers were saved earlier.
- **That shot 2 proves accuracy.** It is a two-message check.
- **The post-hoc set C score of 1.0 as the result.** The frozen first score is the result.
- **What caused the four Sentry timeouts.** It was never established.
- **"Only Gemma was tested."** Qwen 3.5 4B was evaluated too; Gemma is the default.

## If something goes wrong on the day
- **Shot 2 gives different times or a warning:** don't use the take. Re-run once; if it differs again, drop shot 2 and start at shot 3 with the replay caption.
- **Render is down:** run the replay locally with `env -u SENTRY_DSN LEDGER_DEMO=1 PORT=8781 python3 server.py` and open `http://127.0.0.1:8781/app`.
  - Caption it "Replay on this laptop · saved Gemma outputs, no live model".
  - It listens on all network interfaces, so stop it (Ctrl+C) right after recording.
  - Drop "Try the replay" from shot 11.
- **Running long:** cut shot 6's Olu line, then shot 10's optional Sentry line.

## Fact sources

| Line | Verified against |
|---|---|
| Two live messages read on the laptop; exact results | Owner run, PROGRESS "CFG-02 / DEP-03: owner manual live-model smoke check passed" (screenshots and both CSVs parsed) |
| Replay uses saved outputs, no model; banner text | `server.py` (`DEMO`, `saved_output`, `status`), `ui/index.html` `#replay-banner`; live `/api/status` returned `"demo": true` on 2026-10-23 |
| Priya m03 → Mon 15:00–20:00, Wed 13:00–17:00 | Replay through current code, 2026-10-23; `ledger/resolve.py` (`after` runs to `day_end` 20:00; afternoon 13:00–17:00) |
| Maria m28: model missed Thursday, rules added it, flagged; pending change; accepting removes Thursday | Replay through current code: Thursday card `added_by_rules`; Model-only replay leaves Thu 09:00–12:00 on the sheet; export with m02 and m28 accepted has no Thursday row |
| Kofi m13 → m29 conditional then available; m29 "Earlier answer replaced — check" | History `Kofi Mensah\|2026-11-12`; issue `cue_replacement` m29 |
| Olu m49 sent Wed 11 Nov → Wed 11–Sun 15 unavailable, removing Thu 17:00–20:00 and Sat 09:00–12:00 | m49 claim dates 2026-11-11 to 2026-11-15; Olu's history (m24, m38, then m49 "cancelled"); `resolve_day` "rest of this week" |
| m26 outside the week; m41 next Tuesday ambiguous | Issues `outside` m26 and `date` m41 |
| m48 filed under Maria; Reject restores Tue 09:00–12:00 available | m48 claim person Maria Lopez, conditional; ledger after rejecting m48 |
| Final sheet: accepted only; complete conditions; provisional still downloads; Maria rows confirmed | `ledger/export.py` `confirmed_export`, `final_csv`; `ui/app.js` `exportFinal`; export check above |
| Set C: 24 messages, separate AI session, owner edits, frozen; 17/20 units; slot agreement 0.527 on the provisional ledger; misses mainly in code (m21 correction not replacing, m13 dated cancellation on the wrong Saturday); later fixes post-hoc | `evaluation/RESULTS.md`, Set C section (frozen table, "Why unit and sheet numbers diverge", post-hoc section) |
| CI on every push re-checks frozen evidence | `.github/workflows/tests.yml` (integrity and cache-only re-score jobs); run #19 on `d322342` succeeded, read from the GitHub API on 2026-10-23 |
| Sentry: four calls hit the 300 s limit on one run, none on the next | `docs/SENTRY_HANDOFF.md`: traces `c26d2afd` (four errors) and `969d7ee9` (49 calls, zero errors) |
| Open model; runs on an 8 GB laptop | `evaluation/RESULTS.md`: Gemma 4 E2B, Apache 2.0, measured on an Apple M2 with 8 GB |
