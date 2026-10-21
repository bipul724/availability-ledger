# Demo script (DEP-03) with ElevenLabs narration (INT-04)

Target length: about 2 min 30 s. Narration is about 330 words at a calm pace. Everything shown is fictional ("Riverside Community Pantry", set A).

**Where to record.**
- **Shot 1:** the local app with live Gemma through Ollama. It proves the model runs on the laptop.
- **Shots 2–8:** the Render replay (DEP-02), which uses the saved Gemma outputs. They are deterministic, so the moments below appear exactly as described.
- If the replay isn't deployed by Fri 23 Oct, record shots 2–8 locally with **Model + rules**. Do one dry run first, because live model output can differ from the saved outputs: if a moment below doesn't appear, skip it and its narration line.

**The moments below** were checked against the saved Gemma 4 E2B outputs with the Model + rules reader on 2026-10-21. There are 67 suggestions from the 50 messages (one exact repeat is collapsed), and 11 items under Needs a decision. In shot 5, rejecting m48's suggestion was checked to turn Maria's Tuesday 09:00–12:00 from conditional back to available. Re-check on the replay before recording.

**Tools (₹0):**
- macOS screen recording (Cmd+Shift+5).
- iMovie to lay the narration over the video.
- ElevenLabs (your Hacktoberfest offer, a stock voice, never a cloned real voice) to generate one MP3 per shot, so each clip lines up with its shot.

---

## Shots and narration

### 1. The problem (0:00–0:20) — local app, live run
**Screen:** the message panel filled with the Riverside week. Choose the week of 9 Nov, keep **Model + rules**, click **Suggest**. Show the Ollama model running (`ollama ps` in a terminal corner, or the status line). Speed the wait up and caption it "sped up".

> Every week, a volunteer coordinator asks: "When can you help?" The answers arrive as fifty chat messages: offers, corrections, cancellations, maybes. Availability Ledger turns them into a sheet you can trust. It runs on your own laptop, with Gemma 4, an open model, through Ollama. Nothing leaves your machine.

### 2. Model proposes, code decides (0:20–0:40)
**Screen:** the replay banner, then one message with its suggestion card and the highlighted quote, e.g. Priya's "Monday after 3 works, and Wednesday afternoon."

> Gemma only copies phrases: "Monday", "after 3", "Wednesday afternoon". Plain code turns them into dates and times, checks that every phrase really is in the message, and keeps each person's history day by day. The model never does the arithmetic.

### 3. History: a cancellation and a settled condition (0:40–1:05)
**Screen:** open **Changes over time**. Show Maria Lopez on Thu 12 Nov: added from her first message, then marked unavailable after "Change of plans — Thursday doesn't work anymore" (m28). Then Kofi Mensah on Thu 12 Nov: conditional ("if my work shift gets moved", m13), then available after "my shift got moved, so Thursday afternoon is a yes" (m29).

> Messages change their minds, and the ledger keeps up. Maria cancels Thursday, so Thursday comes off her sheet, and the history shows why. Kofi's "maybe, if my shift moves" stays conditional until he confirms, and only then does it become a firm yes.

### 4. It doesn't guess (1:05–1:25)
**Screen:** **Needs a decision**. Point at Kofi's "this Saturday" sent on Wed 4 Nov flagged as outside the selected week (m26). Point at Rui's "next Tuesday" sent on Monday, flagged as ambiguous between two Tuesdays (m41). Point at the "Earlier answer replaced — check" item on Kofi's Thursday (m29).

> When a message is unclear, the ledger asks instead of guessing. "This Saturday", sent on the fourth, is a different week, so it stays out. "Next Tuesday", sent on a Monday, could mean two dates, so you pick. When a change word replaces an earlier answer, it tells you so you can check.

### 5. A real model mistake, caught (1:25–1:50)
**Screen:** m48, Marta Lopes: "Is Maria still doing Tuesday morning? If not I can take it." The model's suggestion puts the conditional offer on **Maria** Lopez, the wrong person, and the sheet shows Maria's Tuesday as conditional. Click **Reject**. Maria's Tuesday returns to a firm morning.

> Gemma isn't perfect. Here Marta offers to cover Maria's Tuesday, and the model files the offer under Maria. That's exactly why every suggestion sits beside its message. One click rejects it, and Maria's Tuesday is firm again.

### 6. Review and the final sheet (1:50–2:10)
**Screen:** use **Accept all suggestions without warnings**, then mark a few messages reviewed with **M**. Show the status line move from provisional towards complete. Click **Export final sheet** and open the CSV in Numbers.

> You review in minutes, not by retyping: accept the clean suggestions in bulk, decide the flagged ones, mark each message reviewed. Only accepted records reach the final sheet, and it says "provisional" until every message is reviewed.

### 7. How we know it works (2:10–2:25)
**Screen:** the GitHub Actions run summary with the score table (INT-11). Then the frozen set C table from `evaluation/RESULTS.md`, with its slot agreement of 0.527, if you want the honest number on screen.

> We tested it on messages it had never seen, written separately and frozen before scoring. The first score is published as it was, with what it got wrong. Every push re-checks the scores on GitHub Actions.

### 8. Close (2:25–2:35)
**Screen:** the repo README, then the replay URL.

> Slow and steady: the model reads, the code reconciles, and you decide. Try the replay, or run it locally on your own messages.

---

## Lines to add only if the integration is real by recording day
- **Sentry (INT-03), after shot 7:** show one trace and say only what the trace showed. For example: "Sentry traces show where the time goes: the first call loads the model, then each message takes about N seconds." Fill in N from the real trace; never invent it.
- **Render:** if the replay isn't live, drop "Try the replay" from shot 8.

## Honesty rules for the recording
- Say "fictional" on screen (the replay banner does this) and don't claim time saved: no human timing has been measured.
- Don't show the post-hoc 1.0 set C score as the headline. If set C appears at all, show the frozen first score.
- Don't hide the model mistake in shot 5. It's the clearest evidence that review matters.
