# Decision log

Each entry records why the system is the way it is. Statuses:

- **accepted**: in effect, and the code or evaluation notes show it was chosen deliberately.
- **accepted (implicit)**: in effect in the code, but no discussion of it was recorded.
- **proposed**: not built; needs a decision.
- **superseded**: tried and replaced or removed.
- **deferred**: deliberately left out of the current release.

No decision has a recorded date except where one is stated in the repository (evaluation notes dated 20 Oct 2026, and the 2026-10-20 code changes). Do not add dates from memory.

## Index

| ID | Title | Status |
|---|---|---|
| D-01 | Run the model locally | accepted |
| D-02 | Gemma 4 E2B as the default model | accepted |
| D-03 | Evaluate Qwen3.5 4B as a comparison only | accepted |
| D-04 | Model copies phrases; code resolves dates and times | accepted |
| D-05 | Model + rules cross-check as the default reader | accepted |
| D-06 | Evidence gate: suggestions must be supported by the message | accepted |
| D-07 | Source-linked review | accepted |
| D-08 | Keep uncertainty visible; never guess | accepted |
| D-09 | Record availability, not assignments | accepted (implicit) |
| D-10 | Synthetic evaluation with frozen held-out sets | accepted |
| D-11 | Python standard library and no external front-end libraries | accepted |
| D-12 | Stateless server, state only in the browser | accepted (implicit) |
| D-13 | Hold back unreviewed flagged suggestions from the sheet | superseded |
| D-14 | Collapse duplicate messages | accepted |
| D-15 | Restore day modifiers from the quote | accepted |
| D-16 | "The same" copies times only within one message | accepted |
| D-17 | External services are optional, opt-in and content-free by default | proposed |
| D-18 | ₹0 operating budget | accepted |
| D-19 | Hosted demo replays saved outputs | proposed |
| D-20 | Tune prompts on dev messages only | accepted |

---

### D-01 Run the model locally

- **Status:** accepted
- **Context:** Messages contain volunteers' names, plans and sometimes personal reasons. Coordinators of small groups have no budget for APIs.
- **Decision:** Inference runs in Ollama on the coordinator's computer (`ledger/model.py`, `http://127.0.0.1:11434`). The server binds to `127.0.0.1`.
- **Alternatives:** hosted LLM APIs; a hosted open model.
- **Rationale:** privacy ("Nothing leaves the machine", README) and zero cost.
- **Tradeoffs:** needs Ollama and a 4 GB model download; slower than hosted models; limited by laptop memory.
- **Revisit if:** coordinators cannot install Ollama, or a free private hosted option appears that keeps messages local.
- **References:** [ARCHITECTURE.md §5](ARCHITECTURE.md#5-model-integration), [RESULTS.md](../evaluation/RESULTS.md) speed and memory.

### D-02 Gemma 4 E2B as the default model

- **Status:** accepted
- **Context:** Target hardware is an 8 GB Mac with other apps open.
- **Decision:** `DEFAULT_MODEL = "gemma4:e2b-it-qat"`.
- **Alternatives:** Qwen3.5 4B (D-03).
- **Rationale:** recorded ≈ 1.6 GB loaded (Ollama `/api/ps`), median 2.3–3.4 s per message, and usable with other apps open. Qwen used ≈ 2.95 GB and made the Mac swap heavily. Licence recorded as Apache 2.0 in RESULTS.md (not re-checked here).
- **Tradeoffs:** Gemma alone misses cancellations (7 of 12 still on the set A final sheet); it needs the rules cross-check (D-05).
- **Revisit if:** the target hardware changes, or a fresh held-out set shows Gemma + rules missing cancellations that Qwen + rules catches.
- **References:** [RESULTS.md](../evaluation/RESULTS.md).

### D-03 Evaluate Qwen3.5 4B as a comparison only

- **Status:** accepted
- **Context:** Needed to know whether a larger small model reads messages much better.
- **Decision:** Qwen3.5 4B was scored on both sets with the same prompt (never tuned) and kept as a selectable model, not the default.
- **Rationale:** it reads better (set A held-out 29/30 units with rules at first scoring) but costs memory and speed on 8 GB.
- **Tradeoffs:** one Qwen hallucination ("all week" for "Whole weekend works") drove the post-hoc quote rule (D-06).
- **Revisit if:** the hardware target rises to 16 GB.
- **References:** [RESULTS.md](../evaluation/RESULTS.md), [TUNING.md](../evaluation/TUNING.md).

### D-04 Model copies phrases; code resolves dates and times

- **Status:** accepted
- **Context:** Small models make arithmetic and calendar mistakes, and their output cannot be checked against the text if they paraphrase.
- **Decision:** The model returns copied words (`day_text`, `time_text`, `excerpt`). `ledger/resolve.py` turns them into dates and times using the send time and the selected week; `ledger/core.py` does history, conflicts and counts.
- **Alternatives:** have the model output ISO dates and times.
- **Rationale:** deterministic, testable and explainable ("next Tuesday sent on Monday 9 Nov could be 10 or 17 Nov").
- **Tradeoffs:** every new phrase type needs code (for example "4 onwards" and "the same" added on 2026-10-20); the model can drop words ("this Saturday" → "Saturday"), which needed D-15.
- **Revisit if:** phrase coverage becomes the main error source on fresh data.
- **References:** `ledger/resolve.py`, `tests/test_ledger.py`.

### D-05 Model + rules cross-check as the default reader

- **Status:** accepted (designed after reading set A held-out errors; set B, written afterwards, is its one independent test)
- **Context:** Held-out set A showed Gemma dropping negatives and never marking replacements.
- **Decision:** `ledger/hybrid.py` runs both readers. Replacement words mark the model's positive claims as replacing earlier answers; a day the rules read as unavailable but the model never mentioned is added and flagged; disagreements are flagged.
- **Alternatives:** model only; rules only; prompt changes only.
- **Rationale:** at first scoring, set B final-sheet missed cancellations went from 1/5 (Gemma only) to 0/5 (Gemma + rules).
- **Tradeoffs:** the 0/5 was partly luck (RESULTS.md ‡). After the 2026-10-20 time-phrase changes it is 1/5: "Scratch Wednesday" is still missed silently (Gemma missed it, and the rules have no "scratch" keyword).
- **Revisit if:** a fresh held-out set shows the rules adding more false cancellations than true ones.
- **References:** [RESULTS.md](../evaluation/RESULTS.md), [PROGRESS.md](../PROGRESS.md#evaluation-status).

### D-06 Evidence gate: suggestions must be supported by the message

- **Status:** accepted (the quote-supports-days part is post-hoc, designed after seeing set B)
- **Decision:** A suggestion is dropped (with a visible reason and "Use it anyway") when neither its quote nor its phrases are in the message, when its quote names none of the claimed days, or when it is a coordinator's own self-claim and the coordinator is not on the roster. Claimed days are narrowed to the quoted days when they partly overlap.
- **Alternatives:** trust the model's JSON.
- **Rationale:** stops claims copied from examples or other messages.
- **Tradeoffs:** a correct claim with a badly copied quote can be dropped; the reviewer must restore it. The reverse gap also exists: a claim is dropped only when **both** the quote and the phrases are missing, so a real quote ("Happy to help") with invented day/time words ("Tuesday", "2-4") is only flagged and is applied to the provisional sheet (COR-10).
- **References:** `ledger/core.py` `resolve_claim`, [TUNING.md](../evaluation/TUNING.md).

### D-07 Source-linked review

- **Status:** accepted
- **Decision:** Every card sits beside its message with the supporting words highlighted; issues and changes link back to the message; the export keeps message id, time, sender and quote.
- **Rationale:** the reviewer can check each suggestion without searching the chat; trust comes from evidence, not from the model.
- **Tradeoffs:** a long message list is long to scroll; keyboard review (J/K) and bulk accept mitigate this.

### D-08 Keep uncertainty visible; never guess

- **Status:** accepted
- **Decision:** Ambiguous people and dates are not applied and show candidates; similar names are flagged, never merged; conditional offers stay conditional until a later message settles them; same-message conflicts keep the more cautious reading; unreadable times are not applied.
- **Alternatives:** pick the most likely reading.
- **Tradeoffs:** more items in "Needs a decision".
- **References:** `ledger/names.py`, `ledger/core.py`.

### D-09 Record availability, not assignments

- **Status:** accepted (implicit: the code has no shift or assignment concept; no discussion recorded)
- **Decision:** The output is when people can or cannot help. Who works which shift is decided elsewhere.
- **Revisit if:** coordinators ask for shift filling; that would be a separate component built on top of the ledger, not a change to it.

### D-10 Synthetic evaluation with frozen held-out sets

- **Status:** accepted
- **Context:** No real messages could be used.
- **Decision:** Fictional set A (50 messages: 30 dev, 20 held-out) and set B (20 held-out, written and frozen before scoring), with hand-written references. First-scored results are kept in `evaluation/results/frozen/` and never overwritten.
- **Tradeoffs:** the same author wrote fixtures, references and rules, and no independent person checked them; the results show technical behaviour only, not demand or time saved. Every change made after reading held-out errors is labelled post-hoc.
- **Revisit if:** real consented messages or an independent reviewer become available (EVAL-03, EVAL-04).
- **Label correction (2026-10-20):** extraction metrics are held-out only; ledger metrics are computed over every message in a set (all 50 for set A, including dev). RESULTS.md now states both scopes and which snapshot each table comes from.
- **References:** [RESULTS.md](../evaluation/RESULTS.md), [TUNING.md](../evaluation/TUNING.md), [MEASUREMENT.md](../evaluation/MEASUREMENT.md).

### D-11 Python standard library and no external front-end libraries

- **Status:** accepted
- **Decision:** No pip packages, no CDN or JS libraries; network calls only to local Ollama.
- **Rationale:** nothing to install beyond Python and Ollama; nothing to leak data.
- **Tradeoffs:** hand-written HTTP server and chart; SDK-based integrations (for example Sentry's SDK) would break this rule and need their own decision.

### D-12 Stateless server, state only in the browser

- **Status:** accepted (implicit)
- **Decision:** The browser holds all state and sends it to `/api/resolve` each time; nothing is stored.
- **Tradeoffs:** reload loses work (COR-04). Simple and private.

### D-13 Hold back unreviewed flagged suggestions from the sheet

- **Status:** superseded (removed)
- **Context:** Tried after the Qwen "all week" case.
- **Decision recorded:** removed, because it held back 15 correct suggestions for every 3 wrong ones. Pending suggestions count on the sheet; the chart hint says so.
- **References:** [TUNING.md](../evaluation/TUNING.md), [RESULTS.md](../evaluation/RESULTS.md).

### D-14 Collapse duplicate messages

- **Status:** accepted (implemented 2026-10-20 on request)
- **Decision:** Same sender + same text (ignoring case, whitespace, quote and dash style) within 24 h of the earliest copy → `duplicate_of`; no extraction call, no suggestions, history entry "repeated".
- **Tradeoffs:** the reference fixtures count a duplicate's units separately, so "units right" fell by 1–2 on held-out sets; final sheets were unaffected. A re-sent message after an intervening cancellation is still treated as a repeat (it does not re-apply).
- **References:** `ledger/messages.py`, [PROGRESS.md](../PROGRESS.md#evaluation-status).

### D-15 Restore day modifiers from the quote

- **Status:** accepted (post-hoc: motivated by set A m26 and set B m18, both held-out)
- **Decision:** If the model's `day_text` lacks "next/this/last/coming" but its quote has exactly one such modifier for the same weekday, re-resolve with it and flag `day_modifier_from_quote`. Never invent a modifier.
- **References:** `ledger/core.py` `_modifier_from_quote`, unit tests.

### D-16 "The same" copies times only within one message

- **Status:** accepted (post-hoc: motivated by set B)
- **Decision:** "the same / same time / same hours" copies the explicit range of the nearest earlier claim in the same message; otherwise it stays unparsed. Never across messages.
- **Tradeoffs:** once readable, these claims reach the sheet, which exposed a cancellation both readers miss (D-05).

### D-17 External services are optional, opt-in and content-free by default

- **Status:** proposed (nothing external is implemented)
- **Proposal:** Any integration (Sentry tracing, ElevenLabs, hosting) must be off by default, work on a free tier or existing credits only, and stop or degrade when the allowance ends. Telemetry must not contain message text, names, quotes or model replies; timings, token counts and error types only. Any feature that sends content off the device (for example voice-note transcription) must say so before each use.
- **Revisit:** when the first integration is designed.

### D-18 ₹0 operating budget

- **Status:** accepted (stated by the project owner)
- **Decision:** Additional out-of-pocket spending stays at ₹0. Free plans, existing local resources or sponsor credits only. No automatic upgrades, top-ups, paid fallbacks or renewals. The core local workflow must never depend on a paid service. The existing domain `bipulchamoli.tech` may be pointed at free hosting; do not buy another.
- **Consequence:** the Hacktoberfest .tech category's domain "renews at $29.99 a year" per the challenge page (read 2026-10-20); auto-renew must be off, or the category skipped.

### D-19 Hosted demo replays saved outputs

- **Status:** proposed
- **Proposal:** If a public demo is needed, host a replay mode that serves the cached model outputs for the fictional fixtures, clearly labelled, on a free hosting plan (for example Render). The existing domain can point at that host; the domain itself does not host anything. Free hosting cannot run Gemma and cannot reach Ollama on a laptop.
- **References:** [ARCHITECTURE.md §15](ARCHITECTURE.md#15-deployment), TASKS DEP-02.

### D-20 Tune prompts on dev messages only

- **Status:** accepted
- **Decision:** Prompt changes (v1 → v3) were motivated only by the 30 set A dev messages; held-out sets are scored once per prompt version. `SYSTEM`, `EXAMPLES` and `PROMPT_VERSION = 3` are frozen; any change bumps the version.
- **References:** [TUNING.md](../evaluation/TUNING.md).
