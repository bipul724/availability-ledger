# Results so far (measured 20 Oct 2026 on an Apple M2, 8 GB, macOS 26.6.2)

All messages are **fictional**. For sets A and B, the same author (the assistant) wrote the fixtures, references and rules baseline. Set C was written by an isolated ChatGPT session and edited by the owner, as described below; no independent reference review or human timing study has been completed. These numbers show technical behaviour, not demand or measured time saved. The heading's 20 October date applies to the original A/B measurements; set C was first scored on 21 October. This file preserves the first-scored historical figures and their provenance, followed by explicitly post-hoc corrections. Current post-hoc A/B results are in [PROGRESS.md](../PROGRESS.md#evaluation-status).

**Interpretation limits:** Gemma is the local model reader; the Render replay, GitHub Actions and optional Sentry tracing are also implemented. Saved-output hosting, CI and traces provide demonstration/process evidence, not fresh model evaluation, independent validation or measured coordinator time savings. ElevenLabs narration was dropped (D-37); the demo uses the owner's voice or captions. See [INTEGRATIONS.md](../docs/INTEGRATIONS.md) for actual roles and boundaries, and [COMPETITION.md](../docs/COMPETITION.md) for dated category research. Do not present these historical measurements as new integration results.

## Extraction and ledger accuracy (frozen, as first scored)

- **Set A held-out:** 20 messages, 30 reference units.
- **Set B:** a fresh set of 20 messages and 35 units, written and frozen before anything was scored on it.

A "unit" is one person and one day as a message states it. "Silent" means wrong with no warning shown.

**Two different scopes in this table** (label corrected 2026-10-20; the numbers are unchanged):
- *Extraction columns* (units right, silent errors) are computed on **held-out messages only**.
- *Ledger columns* (missed cancellations, wrong conditions, ambiguities flagged, slot agreement) are computed on the **final ledger built from every message in the set**. For set A that means all 50 messages, including the 30 dev messages; for set B all 20 messages, which are all held-out. "Missed cancellations" here means withdrawals still showing on the final sheet, not cancellations missed in their own message. This is the provisional ledger built from resolved suggestions, not the accepted-only final-sheet CSV produced after explicit review.
- **Historical metric gap (EVAL-09):** the original A/B evaluator could miss a partly lost conditional/available interval when it was not wholly empty, so its frozen "Wrong conditions" figures may undercount that failure. EVAL-09 fixed this before set C was scored (commit `36b9345`); the current evaluator and `score_final.py` share the per-slot `condition_error` verdict, covered by `tests/test_evaluation.py`. Their input contracts still differ: the evaluator scores the all-pending provisional ledger, while `score_final.py` reads the accepted-only final-sheet CSV used by the timing study. Do not rewrite these frozen values with corrected-scorer numbers.

| Reader | Units right A / B | Silent errors A / B | Missed cancellations A / B | Wrong conditions A / B | Ambiguities flagged A / B | Final-sheet slot agreement A / B |
|---|---|---|---|---|---|---|
| Rules only | 20/30 · 17/35 | 10 · 18 | 0/12 · 3/5 | 2/7 · 1/2 | 2/4 · 1/1 | 0.787 · 0.570 |
| Gemma 4 E2B only | 20/30 · 28/35 | 9 · 5 | 7/12 · 1/5 | 2/7 · 0/2 | 1/4 · 0/1 | 0.775 · 0.731 |
| Gemma 4 E2B + rules cross-check | 26/30 · 30/35 | 3 · 3 | 0/12 · 0/5 ‡ | 2/7 · 0/2 | 3/4 · 1/1 | 0.851 · 0.776 |
| Qwen3.5 4B only | 24/30 · 31/35 | 5 · 3 | 5/12 · 0/5 | 0/7 · 0/2 | 2/4 · 0/1 | 0.902 · 0.409 † |
| Qwen3.5 4B + rules cross-check | 29/30 · 32/35 | 0 · 1 | 0/12 · 0/5 | 0/7 · 0/2 | 4/4 · 1/1 | 0.973 · 0.409 † |

- **‡ The 0/5 is partly luck.** "Scratch Wednesday" was missed silently. The sheet only came out right because an earlier, flagged problem (Wednesday's "the same" hours) had kept Wednesday off it.
- **† One hallucination caused Qwen's set B score.** For "Whole weekend works", Qwen proposed "all week" plus "Friday unavailable", copying my prompt's example. It was flagged but still counted.
- **How independent each figure is:**
  - The Gemma prompt was tuned on the 30 set A dev messages only (`TUNING.md`).
  - I designed the cross-check after reading the set A held-out errors, so its set A figures are not independent; its set B figures are.
  - Qwen was never tuned.

### Post-hoc change (designed after seeing set B, so not independent evidence)

The quote must support the claimed days. A claim is narrowed to the days its verbatim quote names, and dropped if the quote names none of them. This changed only Qwen on set B, where slot agreement went from 0.409 to 0.776 and errors from 9 to 4. No other figure moved.

A second idea, holding back unreviewed flagged suggestions from the sheet, held 15 correct suggestions against 3 wrong ones, so I removed it.

## Speed and memory (measured with the Claude desktop app and a browser open)

Provenance (added 2026-10-20): only runs that made **fresh** model calls measured anything. Files with fresh calls and memory samples: `results/frozen/setA_model_qwen3.5_4b_q4_k_m_prompt3.json` (50 calls, 438 samples), `results/frozen/setB_model_qwen3.5_4b_q4_k_m_prompt3.json` (20 calls, 201 samples), `results/frozen/setB_model_gemma4_e2b_it_qat_prompt3.json` (20 calls, 55 samples) and the three Gemma dev runs in `results/tuning/`. Every other frozen file replayed cached outputs and holds a single memory sample, so its memory fields describe the machine at replay time, not a model run. Per-message timings are also stored in `evaluation/runs/*/m*.json`.

| | Gemma 4 E2B (`gemma4:e2b-it-qat`) | Qwen3.5 4B (`qwen3.5:4b-q4_K_M`) |
|---|---|---|
| Licence | Apache 2.0 | Apache 2.0 |
| Download | 4.3 GB | 3.3 GB |
| Memory once loaded (Ollama `/api/ps`) | 1.59 GB | 2.95 GB |
| First call, including model load | 36 s (27 s of it loading) | 15.8 s |
| Median per message | 2.3–3.4 s | 8.7–11.0 s |
| Slowest message | 9.2 s | 17.8 s |
| Output speed | 26–33 tokens/s | 12–14 tokens/s |
| JSON parse failures | 0 | 0 |
| Lowest free memory during a run | 14–15% (fresh runs: dev tuning and set B); an earlier note of "2% during the first load" has no backing file and is unverified | 7% |
| macOS memory pressure | "warn" in every sample | "warn" 97%, "critical" 1% |
| Swap-out **traffic** during a run (pages written to swap × 16 KB) | up to about 1.9 GB (`tuning/…prompt1_dev.json`, 25 fresh calls); 0.15 GB on set B | about 15 GB over 50 messages (set A), 4.4 GB over 20 (set B) |
| Growth in **occupied** swap during a run | 0.25–0.84 GB (tuning runs); ≈ 0 on set B | about 1.2 GB (6,653 → 7,896 MB, set A); 0.19 GB (set B) |

Swap-out traffic counts every page written to swap, including pages written repeatedly; it is not how much swap was occupied. The earlier notes "swap grew about 4 GB on first load" (Gemma) and "2% during the first load" are not backed by any result file and should be treated as unverified. "Memory once loaded" is the model's own allocation as reported by Ollama; "lowest free memory" and pressure are system-wide.

In the app, end to end with Gemma + rules, 50 messages took **131 s**.

Both models fit in 8 GB. Gemma E2B is usable with other apps open. Qwen 4B runs but makes the Mac swap heavily.

## Effort (a proxy, not human time)

This counts clicks and typed fields for a full review, relative to typing every record by hand. It leaves out reading and checking, which are probably most of the work.

Snapshot (label added 2026-10-20): these are **unarchived historical notes**. They matched the `evaluation/results/*.json` files as those stood after the quote-supports-days rule and before the 2026-10-20 changes. Those files were overwritten by the 2026-10-20 re-run, and no copy is kept in the repository, so the attribution cannot be re-checked from repository artifacts. The retained frozen values are in brackets where they differ; current values are in [PROGRESS.md](../PROGRESS.md#evaluation-status).

| Held-out set | Rules | Gemma + rules | Qwen + rules |
|---|---|---|---|
| A | 0.49 | 0.46 [frozen 0.47] | 0.37 [frozen 0.38] |
| B | 0.48 | 0.40 | 0.39 [frozen 0.44] |

All of these are under 0.70, but the proxy cannot test the 30% target. The real difference between readers shows up in silent errors (rules 18 vs Gemma + rules 3 on set B), not in clicks. `MEASUREMENT.md` has the human timing protocol.

## A reusable signup form (analysis, not measured)

I checked the reference final records against a form with morning, afternoon and evening boxes for each day:

- Set A: 18 of 31 fit.
- Set B: 7 of 11 fit.
- The 17 that don't fit need free text: 13 partial-hour offers and 4 conditional offers.

This reflects how I wrote the fixtures. It says nothing about whether real volunteers would use a link.

## Post-hoc changes on 2026-10-20 (not independent evidence)

Four code changes were made on 2026-10-20: duplicate messages are collapsed, day modifiers dropped by the model are restored from its quote, "4 onwards" is read, and "the same" copies times from earlier in the same message. The modifier and "the same" changes were motivated by held-out messages (set A m26, set B m18 and set B's "the same"), so every changed set B figure is **post-hoc (code changed after set B was seen)**. Frozen figures above are unchanged. Current figures, an ablation of each change, and the regressions they caused (fewer units right because duplicates no longer produce units; more cancellations left on the set B final sheet once previously unreadable offers were applied) are in [PROGRESS.md](../PROGRESS.md#evaluation-status).

The next step at that historical point was EVAL-01's unseen set C freeze, followed by EVAL-07's one-time first scoring. Both were completed on 21 October, as recorded below. Later fixes informed by C are post-hoc; a new independent check would require fresh data (EVAL-11), not another replay of C. Human time saved remains unmeasured. A fictional replay, sponsor trace or demonstration video cannot establish it. [MEASUREMENT.md](MEASUREMENT.md) specifies the separate human study and its local-only pilot boundary.

## Set C: independent, scored once (2026-10-21, code 56e38bd + set registration)

**Provenance.** Set C (24 fictional messages, 12-name roster, week of Mon 23 Nov 2026, every message held-out) was written by an isolated ChatGPT session; the owner rewrote 5 messages. Its files were frozen by hash in `fixtures/setC.manifest` (commit 688c50d) before any implementing agent saw them, and the copy used here matched the manifest (`shasum -a 256 -c`: all three OK). Code: HEAD 56e38bd plus one change, registering set C in `evaluation/fixture.py` and `evaluation/run.py`. Scored **once as an independent first test**, on 2026-10-21 at about 03:34–03:36 IST, with the rules reader, Gemma 4 E2B (`gemma4:e2b-it-qat`, prompt v3, 23 fresh calls, one per non-duplicate message) and Gemma + rules (reusing the same model outputs). Qwen was not run. Results are frozen read-only in `evaluation/results/frozen-setC/` (committed in `9327e30`; set registration in `deaefed`). The EVAL-09 (partial condition loss) and EVAL-10 (duplicates excluded from unit counts) metric definitions apply. Nothing had been tuned on C before this first scoring. It independently tested the preceding changes (duplicates, day modifiers, time phrases, COR-03, COR-02, COR-10 flag only, COR-07a). Subsequent deterministic fixes were designed after reading C's failures and are explicitly post-hoc below. The same caveats as A/B apply: fictional messages, no independent reference review, and no human review in the scoring (all suggestions are pending).

| Reader | Units right | Errors | Silent | Duplicate units excluded | Missed cancellations (final sheet) | Wrong conditions | Ambiguities flagged | Slot agreement | Chart slots wrong |
|---|---|---|---|---|---|---|---|---|---|
| Rules only | 15/20 | 5 | 5 | 1 | 4/8 | 1/2 | 1/3 | 0.433 | 32 |
| Gemma 4 E2B only | 17/20 | 3 | 2 | 1 | 4/8 | 1/2 | 2/3 | 0.403 | 44 |
| Gemma 4 E2B + rules | 17/20 | 3 | 2 | 1 | 2/8 | 1/2 | 2/3 | 0.527 | 26 |

Unit metrics are per message; the other columns are final-sheet (ledger) metrics over all 24 messages. Effort proxy (clicks, not time): 0.35 / 0.30 / 0.30.

**Why unit and sheet numbers diverge.** Unit scoring compares each message's days and times but not whether a suggestion replaces the person's earlier answer. Two corrections were read with the right times but not as replacements, so the old availability stayed on the sheet while the units counted as right.

**Errors, by message (preserved first-score record; later fixes are described separately below):**

| Message | Readers | Visible? | What went wrong |
|---|---|---|---|
| m13 "can't do Sat 21 Nov, away that day" (sent 19 Nov) | all three | silent | Date resolution: "Sat" is read as the selected week's Saturday (28 Nov) and the explicit 21 Nov is discarded as outside the week, so an outside-week cancellation becomes a silent "unavailable" on Sat 28 Nov and the outside-week ambiguity is not raised. Likely bug in `ledger/resolve.py` (weekday plus explicit date); not fixed here. |
| m15 "I am cancelling my plan for the Monday morning…" | rules | silent | The rules' negation word is `cancel`, which does not match "cancelling"; read as available, so Monday morning stays on the sheet. |
| m16 "…i'm out all Tuesday, sorry" | rules | silent | "out" alone is not a rules negation word; read as an untimed confirmation, so Tuesday stays. |
| m19 "lab swap went thru, Friday is definite now" | all three | silent | No time was extracted (the reference carries 15:00–20:00 forward), and the ledger treats an untimed follow-up on a day with an earlier answer as "confirmed earlier answer" without changing its status, so Friday stays **conditional** (the one wrong condition for every reader). |
| m20 "Sunday only 10:15-12:45 now…" | Gemma only | silent (sheet) | Times right, but not marked as replacing the all-day Sunday offer, so 09:00–10:15 and 12:45–20:00 stay (2 missed cancellations). Gemma + rules fixes it through the "now" cue. |
| m21 "Please change my availability on monday to 1-4 pm" | all three | silent (sheet) | Times right, but no reader marks it as a replacement ("change" is not one of the cue words), so 13:00–16:00 is laid over the earlier all-day Monday and 09:00–13:00 and 16:00–20:00 stay (2 missed cancellations, the largest source of slot disagreement). |
| m23 coordinator relays "'T. Vekar': 'Sunday for an hour, 10-11 works'. which T tho" | all three | rules silent; Gemma flagged | Rules ignore coordinator messages, so the ambiguity is missed. Gemma proposes "T. Vekar", which matches no roster name as a whole and is too short a first name for prefix matching, so it becomes an **unknown** person (flagged, not applied) instead of an ambiguity between Taren and Tarin Vekar. |

The duplicate (m05 repeats m03) was handled correctly by all readers.

**COR-07a warnings:** 0 for every reader: no true-positive warnings and no false-positive warnings. This does not mean there were no missed cancellations; those are counted in the frozen table. No message in set C combined a change word with a day that still had open time and no suggestion touching that day. The warning could not catch C's actual failures by design: in m15/m16 (rules) a wrong-polarity suggestion touched the day, and in m20/m21 the correction touched the day without replacing the earlier answer; "change" is also not in the word list ("change of plans" is).

**COR-10 `phrase_not_in_message` flags:** rules 0; Gemma 4 and Gemma + rules 4 (m07 "Fri", m08 "sat", m11 "wed", m12 "thurs"). All 4 are harmless rewording of an abbreviated day; each suggestion is correct. 0 real problems, consistent with D-30 (flag only).

**Speed and memory (Gemma run, fresh calls, measured with other apps open):** 23 calls, 0 JSON failures; median 1.78 s per message; slowest 56.1 s, which includes a 47.9 s cold model load (next slowest 2.46 s); output about 42 tokens/s; whole run 94 s. Ollama reports the model at 1,561 MB. System-wide during the run: lowest free memory 4%, pressure "warn" in 82% and "critical" in 18% of 45 samples, occupied swap grew by about 4.1 GB (5,035 → 9,176 MB, mostly the cold load), swap-out traffic about 8.5 GiB.

### Set C, post-hoc after D-31 fixes (2026-10-21; not independent evidence)

The frozen table above is set C's independent result and is unchanged. The fixes below (COR-13 to COR-17, D-31) were designed after seeing set C's errors and tested with invented messages, so every number here is **post-hoc**. Re-scored from the same cached Gemma outputs (0 fresh calls); `frozen-setC/` untouched.

| Reader | Units right | Silent | Missed cancellations | Wrong conditions | Ambiguities flagged | Slot agreement | Chart slots wrong |
|---|---|---|---|---|---|---|---|
| Rules only | 15/20 → 17/20 | 5 → 3 | 4/8 → 0/8 | 1/2 → 0/2 | 1/3 | 0.433 → 1.0 | 32 → 0 |
| Gemma 4 E2B only | 17/20 → 19/20 | 2 → 1 | 4/8 → 0/8 | 1/2 → 0/2 | 2/3 → 3/3 | 0.403 → 1.0 | 44 → 0 |
| Gemma 4 E2B + rules | 17/20 → 19/20 | 2 → 1 | 2/8 → 0/8 | 1/2 → 0/2 | 2/3 → 3/3 | 0.527 → 1.0 | 26 → 0 |

Which fix moved what (each fix scored in turn): **COR-13** (explicit dates) m13 is now outside-week and flagged for both Gemma readers; **COR-14** (firm follow-up) m19 settles Friday for all readers; **COR-15** (replacement cues) m20/m21 replace the earlier answers (the largest slot gain); **COR-16** (initial + surname) m23 becomes an ambiguity between the two Vekars for both Gemma readers; **COR-17** (rules negation forms) m15/m16 for the rules reader.

Still wrong after the fixes: m19 for every reader (no time extracted, a unit-level error, though the sheet is now right); m13 for rules ("Sat" alone still reads as Sat 28 Nov, so the evidence gate now drops it as unsupported by the quote; the outside-week ambiguity is missed, silently); m23 for rules (coordinator messages are ignored). A perfect slot agreement on 24 fictional messages after fixing their own failures says little about new messages; an independent check would need a fresh set (EVAL-11, D-31).

