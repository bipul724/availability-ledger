# Prompt tuning log

Forward rule: tune only on development messages. Keep new held-out messages unseen by implementation agents and score them once after the planned changes. The historical tables below explicitly record departures: some code changes followed inspection of A/B errors and are **post-hoc**, so A/B no longer independently validates those changes.

**Current gate:** before further behavior changes, freeze and commit at least 20 new fictional set C messages plus a handwritten reference, unscored (EVAL-01); implementation agents must not open them. Use new invented development examples, then score C once at an identified code version (EVAL-07). C does not exist today. See [TASKS.md](../TASKS.md#evaluation-and-validation).

**Sponsor boundary:** the agreed [integration plan](../docs/INTEGRATIONS.md) preserves the local phrase-copying Gemma/Python boundary. No new provider, prompt change, hosted inference, fine-tuning or in-product voice capability is authorized merely by a category target. Any real prompt change needs the `PROMPT_VERSION` bump, separate cache identity and a log entry. Saved-output replay, CI results, development sessions and optional traces are not new accuracy results and must not be labelled as independent tests. Keep consented real pilot data local, outside git and all external development/demo/telemetry artifacts.

## v1 → v2 (from the 30 dev messages, gemma4:e2b-it-qat)

| Dev error (v1) | Message | Change in v2 |
|---|---|---|
| Coordinator's shift description and "still need people" turned into claims | m01, m34 | Coordinator messages that describe shifts or list needs are not availability |
| Claims copied from the sender's earlier messages (context) | m23, m39 | "Only list what THIS message says"; excerpt must come from this message |
| "all week except Friday" lost the exception | m08 | Exceptions become a separate unavailable claim |
| "Not Tuesday" dropped | m17 | Short negatives are unavailable claims |
| "Just let me know" read as a condition | m30 | Politeness is not a condition |
| Marta's offer to take Maria's slot attributed to "Maria" | m48 | Offers to take another person's slot are about SENDER; mentioned names get no claim |

No few-shot examples changed. The rules baseline was not tuned after its first run.

## v2 → v3 (dev still showed 9 errors, 3 silent)

| Dev error (v2) | Message | Change |
|---|---|---|
| Claims repeated from earlier-message context | m23 | Removed earlier messages from the prompt entirely (code handles "still"/confirmations) |
| Coordinator "still need people" and shift list still extracted | m01, m34 | Invented example of a coordinator request with no claims; **code rule**: a coordinator's self-claim is dropped when the coordinator does not resolve to a roster name (a coordinator on the roster is retained) |
| "Just let me know" still read as a condition; Marta's offer still given to "Maria" | m30, m48 | One invented example combining "If not, I can do it" (SENDER, conditional) and "Could I also…? Let me know!" (available) |
| Any proposal whose excerpt and phrases are absent from the message | (general) | **Code rule (evidence gate)**: dropped with a visible reason, never applied. This does not cover an exact quote paired with invented day/time words: those may remain pending and affect the provisional sheet today (COR-10) |

## After held-out scoring (post-hoc; not independent evidence)

| What | Why | Kept? |
|---|---|---|
| Model + rules cross-check (`ledger/hybrid.py`) | Held-out set A showed Gemma dropping negatives and never marking replacements | Kept. Set B was written and frozen afterwards so this design has one independent test |
| Quote must support the claimed days: narrow to the quote's days, drop if none match | Set B: Qwen turned "Whole weekend works" into "all week" | Kept. Only Qwen on set B changed (slot agreement 0.409 → 0.776) |
| Unreviewed flagged suggestions may remove but not add availability | Same Qwen case | **Removed.** It held 15 correct suggestions vs 3 wrong ones |
| Restore modifiers the model drops ("this Saturday" → "Saturday", "Next Friday" → "Friday") | Set A m26, set B m18 | **Built 2026-10-20** (`core._modifier_from_quote`, flag `day_modifier_from_quote`), tested with invented messages only. Its held-out gains are post-hoc; a fresh held-out set is still needed (TASKS EVAL-01 freeze, EVAL-07 score once) |
| Read "the same" as the hours of an earlier claim in the same message; read "4 onwards" | Set B "Wednesday the same" | **Built 2026-10-20**, tested with invented messages. Post-hoc. Side effect: newly applied offers exposed cancellations both readers miss |
| Collapse duplicate messages (same sender and text within 24 h) | Set A m11/m12 (from the task description) | **Built 2026-10-20**. Lowers "units right" because the references count a duplicate's units; final sheets unchanged |
