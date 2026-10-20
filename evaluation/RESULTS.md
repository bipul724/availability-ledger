# Results so far (measured 20 Oct 2026 on an Apple M2, 8 GB, macOS 26.6.2)

All messages are **fictional**. The same author (the assistant) wrote the fixtures, the references and the rules baseline, and no independent person checked them. These numbers show how the system behaves technically; they say nothing about whether anyone wants it. This file preserves the first-scored historical figures and their provenance; current post-hoc A/B results are in [PROGRESS.md](../PROGRESS.md#evaluation-status).

**Interpretation limits for the agreed sponsor portfolio:** saved-output hosting, narration, CI runs, development checkpoints and optional traces are demonstration/process evidence, not fresh model evaluation, independent validation or measured coordinator time savings. Gemma is the only implemented sponsor use; see [INTEGRATIONS.md](../docs/INTEGRATIONS.md) for the proposed roles and [COMPETITION.md](../docs/COMPETITION.md) for the verified category/history research. Do not present historical measurements as new results from an integration that has not been built.

## Extraction and ledger accuracy (frozen, as first scored)

- **Set A held-out:** 20 messages, 30 reference units.
- **Set B:** a fresh set of 20 messages and 35 units, written and frozen before anything was scored on it.

A "unit" is one person and one day as a message states it. "Silent" means wrong with no warning shown.

**Two different scopes in this table** (label corrected 2026-10-20; the numbers are unchanged):
- *Extraction columns* (units right, silent errors) are computed on **held-out messages only**.
- *Ledger columns* (missed cancellations, wrong conditions, ambiguities flagged, slot agreement) are computed on the **final ledger built from every message in the set**. For set A that means all 50 messages, including the 30 dev messages; for set B all 20 messages, which are all held-out. "Missed cancellations" here means withdrawals still showing on the final sheet, not cancellations missed in their own message. This is the provisional ledger built from resolved suggestions, not the accepted-only final-sheet CSV produced after explicit review.
- **Known metric gap (EVAL-09):** `evaluation/run.py` can miss a partly lost conditional/available interval when it is not wholly empty. Its historical "Wrong conditions" figures may therefore undercount that failure. `score_final.py` checks every slot and has been fixed, but it is a separate final-export scorer. Do not silently replace these frozen values with its numbers.

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

Before further behavior changes, EVAL-01 requires an unseen fictional set C and handwritten reference to be frozen, unscored and committed without implementation agents inspecting it. EVAL-07 scores it once after the planned changes, recording the exact code version. No set C results or real-user time-saving result exists today. A future fictional replay, sponsor trace or demonstration video cannot supply that missing evidence. [MEASUREMENT.md](MEASUREMENT.md) specifies the separate human study and its local-only pilot boundary.

