# Demo script (DEP-03)

Target length: about 2 min 30 s. Everything shown is fictional: the Ana/Ben live example and the "Riverside Community Pantry" replay (set A). Script/source audit refreshed 2026-10-23; no new recording or model run was made by that audit.

**Where to record.**
- **Shot 1:** the local app with live Gemma through Ollama (which you start yourself), reading the **two invented Ana/Ben messages** of the owner's verified check (CFG-02, 2026-10-23: Model only, `gemma4:e2b-it-qat`). It shows the model running on the laptop. Caption it **"Local app · live Gemma 4 on this laptop · two invented messages"**. This two-message flow has explicit person/date/time/source-quote and provisional/complete-export verification. Earlier full-week live runs exist in the Sentry history, but their resulting availability was not checked end to end for correctness; do not present trace completion as full-week or hybrid accuracy validation. Use the two-message live opening.
- **Shots 2–8:** the Render replay at `https://availability-ledger-replay.onrender.com/app` (deployed; DEP-02). It uses saved Gemma outputs. Caption the first replay shot **"Hosted replay · fictional week · saved Gemma outputs, no live model"**. The site root is the landing page (usable for shot 8). Open the replay early: [Render's free-service policy](https://render.com/docs/free), checked 2026-10-23, says it sleeps after 15 idle minutes and takes about one minute to wake; that is not a guaranteed maximum.
- If Render is down on recording day, run the same replay on the laptop instead of a live run: `env -u SENTRY_DSN LEDGER_DEMO=1 PORT=8781 python3 server.py`, then `http://127.0.0.1:8781/app`. It serves the same saved outputs and never calls the model, but it listens on all network interfaces (0.0.0.0), so use a trusted network and stop it (Ctrl+C) after recording. Caption it **"Replay on this laptop · saved Gemma outputs, no live model"**.

**The moments below** were re-checked on 2026-10-22 on the replay code path (`LEDGER_DEMO=1`, saved Gemma 4 E2B outputs, Model + rules, no model calls): 67 suggestions from the 50 messages (one exact repeat is collapsed); 10 items under Needs a decision, including m26 (outside the week), m41 (which Tuesday) and m29 (earlier answer replaced); Changes over time lists m28 replacing Maria's Thursday and m29 replacing Kofi's Thursday; rejecting m48's suggestion turns Maria's Tuesday 09:00–12:00 from conditional back to available. REL-02 on 2026-10-23 matched nine served front-end files to pushed release `d4b2f76`, verified 67 suggestions and passed 22 bounded live replay checks covering review, history and both exports. This checks public behavior and served UI files, not deployed server source. Glance at the intended scenes before recording. Shot 1's expected result is the owner's verified live run (2026-10-23), not the replay. [tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754) passed all three jobs on that release.

**Tools (₹0):**
- macOS screen recording (Cmd+Shift+5).
- iMovie to join the shots and add captions.
- **Narration (D-37, ElevenLabs dropped):** in the Cmd+Shift+5 toolbar choose **Options → Microphone**, and read each shot's lines aloud while you click. Voice and video are recorded together, so they can't drift. Retake a single shot if you stumble. Or record silently and put the lines on screen as iMovie titles.

---

## Shots and narration

### 1. The problem (0:00–0:20) — local app, live run
**Before recording:** `ollama serve` in one terminal (skip if Ollama is already running), then from the repository run `env -u SENTRY_DSN -u LEDGER_DEMO python3 server.py 8780` and open `http://127.0.0.1:8780/app`. This explicitly starts the local untraced mode without reading `.env`. Leave an existing server alone if the port is occupied; use another free port consistently. No `.env` is needed for this shot.

**Screen:** Reader **Model only**, Model `gemma4:e2b-it-qat`, Week starting **2026-11-09**. Roster:

```
Ana Example
Ben Example
```

Messages:

```
2026-11-09 08:00 | Ana Example | I can help Tuesday 09:00-12:00.
2026-11-09 08:05 | Ben Example | I can help Thursday 13:00-15:00.
```

Click **Suggest records**. Show the Ollama model running (`ollama ps` in a terminal corner, or the status line); speed up any wait and caption it "sped up". Expected, as verified: Ana Example, Tue 10 Nov, 09:00–12:00, available; Ben Example, Thu 12 Nov, 13:00–15:00, available; each beside its highlighted quote, nothing under Needs a decision. If either differs, stop and don't use the take. Optional, if time allows: accept both, then mark both messages reviewed; the status line then says the final sheet would be complete (also verified, including both CSVs).

> Every week, a volunteer coordinator asks: "When can you help?" The answers arrive as chat messages: offers, corrections, cancellations, maybes. Availazy turns them into a sheet you can check. Here are two invented messages, read live by Gemma 4, an open model, through Ollama on this laptop, so your messages are read right here, not by a cloud service.

### 2. Model proposes, code decides (0:20–0:40)
**Screen:** switch to the hosted replay. Hold on its banner ("Replay: fictional messages and saved Gemma 4 outputs…"), then one message with its suggestion card and the highlighted quote, e.g. Priya's "Monday after 3 works, and Wednesday afternoon."

> From here on this is the public replay: fifty fictional messages with Gemma's answers saved earlier. Gemma proposes copied phrases, status and replacement hints. Plain code turns "Monday" and "after 3" into dates and times, checks source evidence, and keeps each person's history. The model never does the arithmetic.

### 3. History: a cancellation and a settled condition (0:40–1:05)
**Screen:** open **Changes over time**. Show Maria Lopez on Thu 12 Nov: her first offer, then the m28 entry "Thu 12 replaced earlier answer for this day" after "Change of plans — Thursday doesn't work anymore"; the provisional sheet shows **pending change** while the cancellation is pending. Check its source and click **Accept** on the cancellation before explaining its effect on the accepted-only export. Then show Kofi Mensah on Thu 12 Nov: conditional ("if my work shift gets moved", m13), then available after "my shift got moved, so Thursday afternoon is a yes" (m29). Distinguish the provisional display from decisions already accepted.

> Messages change their minds, and the ledger keeps the history. Check Maria's cancellation and accept it: her earlier Thursday offer no longer reaches the final export. Kofi's "maybe, if my shift moves" stays conditional until he confirms, and only then does it become a firm yes.

### 4. It doesn't guess (1:05–1:25)
**Screen:** **Needs a decision**. Point at Kofi's "this Saturday" sent on Wed 4 Nov flagged as outside the selected week (m26). Point at Rui's "next Tuesday" sent on Monday, flagged as ambiguous between two Tuesdays (m41). Point at the "Earlier answer replaced — check" item on Kofi's Thursday (m29).

> When a message is unclear, the ledger asks instead of guessing. "This Saturday", sent on the fourth, is a different week, so it stays out. "Next Tuesday", sent on a Monday, could mean two dates, so you pick. When a change word replaces an earlier answer, it tells you so you can check.

### 5. A real model mistake, caught (1:25–1:50)
**Screen:** m48, Marta Lopes: "Is Maria still doing Tuesday morning? If not I can take it." The model's suggestion puts the conditional offer on **Maria** Lopez, the wrong person, and the sheet shows Maria's Tuesday as conditional. Click **Reject**. Maria's Tuesday returns to a firm morning.

> Gemma isn't perfect. Here Marta offers to cover Maria's Tuesday, and the model files the offer under Maria. That's exactly why every suggestion sits beside its message. One click rejects it, and Maria's Tuesday is firm again.

### 6. Review and the final sheet (1:50–2:10)
**Screen:** only after reading and checking the affected suggestions, use **Accept all suggestions without warnings**, then mark a few actually read messages reviewed with **M** (or **Mark message reviewed**). Warning-free does not establish correctness. Point out that accepting a suggestion and marking its message reviewed are separate steps, and show the status line count the reviewed messages. Click **Export final sheet**: it still downloads while provisional. Open the CSV in Numbers and show the first line (`status=provisional`, the unreviewed message IDs) and the `cell_state` column.

> You review by deciding, not retyping: accept suggestions you've checked, decide the flagged ones, and mark each message once you've read it. Only accepted records reach the final sheet. The file says "complete" only when every message, apart from exact repeats, is marked reviewed, nothing is pending and no blocking issue is open. Until then it says "provisional", and it still downloads.

### 7. How we know it works (2:10–2:25)
**Screen:** [GitHub Actions tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754) on `d4b2f76`, with the score table (INT-11). Then the frozen set C table from `evaluation/RESULTS.md`, with its slot agreement of 0.527, if showing the number. Caption that score **"Frozen fictional set C · provisional ledger before human review"**; it does not score the owner's accepted-only CSV. The isolated ChatGPT session wrote C and the owner rewrote five messages; no independent reference review was done.

> An isolated AI session wrote new fictional messages, with owner edits, frozen before scoring. The first result stays published with its mistakes. It measures the provisional ledger before human review. Pushes to main re-check saved-output scores on GitHub Actions.

### 8. Close (2:25–2:35)
**Screen:** the repo README, then the replay URL.

> Slow and steady: the model reads, the code reconciles, and you decide. Try the replay on the fictional week, or run Availazy locally to read your own messages on your own computer.

---

## Optional lines (only with real evidence on screen)
- **Sentry (INT-03), after shot 7:** show one owner-selected, redacted trace screenshot (no DSN, account details or location values) and say only what that trace showed. Recorded evidence: an early traced run had four model calls hit the 300-second timeout; a later 49-call run took 1.42 minutes with no errors ([Sentry handoff](../SENTRY_HANDOFF.md)). Say tracing is opt-in and off by default, and never call the received data fully audited. If location comes up, say only this: received traces displayed geo attributes; after a settings change, four visible geo values on one inspected chat span and its parent appeared filtered; where that enrichment comes from, and a complete audit of the received data, are unverified.
- **Render:** if the replay is down on recording day, drop "Try the replay" from shot 8.
- **Captions instead of voice (D-37):** every narration line above can be an iMovie title; keep the two captions that say which shots are the local live app and which are the hosted replay.

## Honesty rules for the recording
- Say "fictional" on screen (the replay banner does this) and don't claim time saved: no human timing has been measured.
- Don't say "nothing leaves your machine": optional tracing sends timing metadata to Sentry when turned on, and the replay runs on Render. Say messages are read on your own computer in the local app.
- Don't call the replay live inference: its Gemma answers were saved earlier.
- Don't present shot 1 as general accuracy evidence: it is a two-message check. Historical full-week/hybrid trace delivery exists, but full-week availability and review/export correctness were not validated end to end.
- Don't show the post-hoc 1.0 set C score as the headline. If set C appears at all, show the frozen first score.
- Don't hide the model mistake in shot 5. It's the clearest evidence that review matters.
