# Decision log

Each entry records why the system is the way it is. Statuses:

- **accepted**: in effect, and the code or evaluation notes show it was chosen deliberately.
- **accepted (implicit)**: in effect in the code, but no discussion of it was recorded.
- **accepted (planning direction)**: owner selected the direction; implementation remains gated and is not claimed complete.
- **proposed**: not built; needs a decision.
- **superseded**: tried and replaced or removed.
- **deferred**: deliberately left out of the current release.

Dates are supported by source/evaluation history or the owner conversation. D-22 records the 2026-10-20 planning direction, not an implementation date.

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
| D-12 | Browser session with transient local server processing | accepted (implicit) |
| D-13 | Hold back unreviewed flagged suggestions from the sheet | superseded |
| D-14 | Collapse duplicate messages | accepted |
| D-15 | Restore day modifiers from the quote | accepted |
| D-16 | "The same" copies times only within one message | accepted |
| D-17 | External services are optional, opt-in and content-free by default | proposed |
| D-18 | ₹0 operating budget | accepted |
| D-19 | Hosted demo replays saved outputs | proposed |
| D-20 | Tune prompts on dev messages only | accepted |
| D-21 | Confirmed final sheet requires explicit message review | accepted |
| D-22 | Coherent multi-category direction with separate product/development/demo roles | accepted (planning direction); Week 3 scope narrowed by D-23 |
| D-23 | Week 3 submission scope: Gemma core, optional Actions CI, other integrations deferred | accepted (project lead, 2026-10-20) |
| D-24 | Set C is frozen outside the public repository | accepted (project lead, 2026-10-20) |
| D-25 | Missed cancellations: warn first, no new extraction vocabulary before C is scored | accepted (project lead, 2026-10-20) |
| D-26 | Duplicate-aware extraction scoring before set C is scored | accepted (project lead, 2026-10-20) |
| D-27 | Documentation economy until submission | accepted (project lead, 2026-10-20) |
| D-28 | Work that cannot bias set C may start before the C freeze | accepted (project lead, 2026-10-20) |
| D-29 | Set C may be written by a fresh, isolated AI session if the owner cannot write it | accepted (project lead, 2026-10-21) |
| D-30 | COR-10: flag unsupported phrases, do not hold them; keep COR-07a | accepted (project lead, 2026-10-21) |
| D-31 | Fix the reconciliation defects set C exposed, labelled post-hoc; set C's first score stays the headline | accepted (project lead, 2026-10-21) |

---

### D-01 Run the model locally

- **Status:** accepted
- **Context:** Messages contain volunteers' names, plans and sometimes personal reasons. Coordinators of small groups have no budget for APIs.
- **Decision:** Inference runs in Ollama on the coordinator's computer (`ledger/model.py`, `http://127.0.0.1:11434`). The server binds to `127.0.0.1`.
- **Alternatives:** hosted LLM APIs; a hosted open model.
- **Rationale:** privacy ("Nothing leaves the machine", README) and zero cost.
- **Tradeoffs:** needs Ollama and a 4 GB model download; slower than hosted models; limited by laptop memory.
- **Revisit if:** coordinators cannot install Ollama, or a separately approved design changes the local privacy boundary. A hosted inference service does not keep inference local merely because access is free.
- **References:** [ARCHITECTURE.md §5](ARCHITECTURE.md#5-model-integration), [RESULTS.md](../evaluation/RESULTS.md) speed and memory.

### D-02 Gemma 4 E2B as the default model

- **Status:** accepted
- **Context:** Target hardware is an 8 GB Mac with other apps open.
- **Decision:** `DEFAULT_MODEL = "gemma4:e2b-it-qat"`.
- **Alternatives:** Qwen3.5 4B (D-03).
- **Rationale:** recorded ≈ 1.6 GB loaded (Ollama `/api/ps`), median 2.3–3.4 s per message, and usable with other apps open. Qwen used ≈ 2.95 GB and made the Mac swap heavily. The [official Ollama tag listing](https://ollama.com/library/gemma4:e2b-it-qat) identifies Apache 2.0 (checked 2026-10-20); this is separate from the application licence decision.
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

### D-12 Browser session with transient local server processing

- **Status:** accepted (implicit)
- **Decision:** Session state lives in browser memory and is processed transiently by the local server for resolve/export. No application persistence is implemented.
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

- **Status:** proposed implementation; safety constraints accepted in D-18/D-22 (nothing external is implemented)
- **Proposal:** Optional runtime diagnostics must be opt-in/off by default, use verified free access and stop/degrade without blocking local review when allowance ends. Telemetry excludes message text, names, quotes, replies, private identifiers and raw sensitive errors. Start with fictional data and a metadata allowlist. Development evidence and demo assets have separate boundaries. Public replay/narration use fictional data; in-app voice/transcription is deferred. See [INTEGRATIONS.md](INTEGRATIONS.md).
- **Revisit:** when the first integration is designed.

### D-18 ₹0 operating budget

- **Status:** accepted (stated by the project owner)
- **Decision:** Additional out-of-pocket spending stays at ₹0. Free plans, existing local resources or sponsor credits only. No automatic upgrades, top-ups, paid fallbacks or renewals. The core local workflow must never depend on a paid service. The existing domain `bipulchamoli.tech` may be pointed at free hosting; do not buy another.
- **Consequence:** the Hacktoberfest .tech category's domain "renews at $29.99 a year" per the challenge page (read 2026-10-20); auto-renew must be off, or the category skipped.

### D-19 Hosted demo replays saved outputs

- **Status:** planning direction selected in D-22; replay implementation/deployment remains proposed.
- **Proposal:** Host a useful interactive replay using fixed fictional saved outputs, clearly labelled, on a verified free host such as Render. The domain points at the host; it does not host the app. No hosted Gemma resources are provisioned, and a remote host cannot use the laptop localhost Ollama. A future replay spec must define permitted inputs/APIs and exclude private-data uploads. A truthful local video remains a valid alternative.
- **References:** [ARCHITECTURE.md §15](ARCHITECTURE.md#15-deployment), [INTEGRATIONS.md](INTEGRATIONS.md), TASKS DEP-02.

### D-20 Tune prompts on dev messages only

- **Status:** accepted
- **Decision:** Prompt changes (v1 → v3) were motivated only by the 30 set A dev messages; first-scored held-out results are frozen, while later reruns after inspecting A/B errors are explicitly post-hoc. New C must stay unseen and be scored once after planned behavior changes. `SYSTEM`, `EXAMPLES` and `PROMPT_VERSION = 3` are frozen; any change bumps the version.
- **References:** [TUNING.md](../evaluation/TUNING.md).

### D-21 Confirmed final sheet requires explicit message review

- **Status:** accepted (owner decisions recorded 2026-10-20; implemented the same day)
- **Context:** The record log could not be replayed into the sheet, the in-app sheet includes pending suggestions, and a cancellation the readers missed can sit in a message that produced no suggestions.
- **Decision:** The final-sheet export uses accepted records only and is `complete` only when every message is explicitly marked reviewed, nothing is pending and no `who`/`date`/`time`/`conflict` issue is open. Review is never inferred from extraction or from deciding suggestions. "Accept all and mark reviewed" is offered only for eligible pending suggestions with resolved identity/day, readable time and no blocking warning; approved informational flags are specified in the export contract/UI. Provisional exports are allowed and labelled. The timing study scores final-sheet files from both conditions with one strict scorer, counting unresolved cells as disagreement.
- **Alternatives:** export `ledger.sheet` directly (would export pending suggestions as confirmed); add `replaces_earlier` to the record log and keep replaying it (two contracts, and still blind to unreviewed messages); infer review when all suggestions are decided (cannot see missed cancellations).
- **Tradeoffs:** one more click per message; a message with no suggestions must be marked with its button (J/K move between cards).
- **Revisit if:** the timing study shows marking costs significant time, or coordinators want per-day rather than per-message review.
- **References:** [specs/final-export.md](specs/final-export.md), `ledger/export.py`, `evaluation/score_final.py`, `tests/test_export.py`.

### D-22 Coherent multi-category direction with separate product/development/demo roles

- **Date:** 2026-10-20 (owner direction and all-doc alignment).
- **Status:** accepted (planning direction); optional uses remain unimplemented and conditional.
- **Context:** The owner wants genuine winning opportunities beyond Gemma while retaining the useful local workflow, ₹0 additional spending and privacy. Historical research separates meaningful sponsor evidence from cheap eligibility; reliable category odds are unknown.
- **Decision:** Gemma/Ollama stays local phrase extraction; Python and human review determine the final sheet. Pursue genuine Copilot development/review and Actions CI as distinct evidence routes; Entire captures real upcoming sessions. Consider narrowly scoped Sentry diagnostics only after privacy/dependency/free-budget gates. Plan a useful fictional saved-output Render replay, conditional domain routing and ElevenLabs demo narration. Backboard R-CLI is an optional bounded development trial if genuinely useful and locally compatible.
- **Boundaries:** No in-app voice, cloud database, authentication, public-web retrieval, orchestration engine or fine-tuning is selected merely to add a category. Development/demo tools are not application dependencies. Only completed qualifying uses may be listed in the submission.
- **Prerequisites:** Freeze unseen C before behavior changes; finish visible extraction failures/unsupported evidence and CSV protection; preserve frozen/post-hoc labels; validate usefulness and measure human time before claiming savings.
- **Implementation scope:** This is not the specific D-11 SDK/network exception, service activation, install, download, credit claim, data sharing, deployment or publishing authorization. Follow the owner's actual scoped request and existing session authorization without asking twice.
- **Tradeoffs:** Multiple categories cannot stack prizes and do not establish higher odds. Integrations consume time and may weaken the story if they displace correctness, independent evaluation, coordinator validation or the heavily weighted write-up.
- **References:** [INTEGRATIONS.md](INTEGRATIONS.md) (roles/contracts/rollout), [COMPETITION.md](COMPETITION.md) (rules/history/strategy), [TASKS.md](../TASKS.md) (status/dependencies), [context.md](../context.md) (handoff).

### D-23 Week 3 submission scope: Gemma core, optional Actions CI, other integrations deferred

- **Date:** 2026-10-20, 20:45 IST (project-lead takeover). **Status:** accepted. It narrows D-22 for the Week 3 submission; D-22 stays as the longer-term direction. The owner can override.
- **Context:** About 4.6 days remain before the earlier deadline reading (25 Oct, 12:29 IST). The listed effort estimates for optional work in [COMPETITION.md](COMPETITION.md#recommended-portfolio--revised-using-historical-evidence-still-proposed) add up to roughly 15–35 hours: Sentry 6–12 h, Render 4–8 h, narration 2–4 h, Entire 1–3 h, R-CLI 1–3 h, Actions 1–3 h. The core is unfinished: COR-03, COR-10, COR-02, unseen C, and a known silent missed-cancellation weakness. An entry can win at most one prize; writing quality is weighted most heavily; the inspected Week 1 winners showed deep, concrete use of their sponsor.
- **Decision:** the Week 3 entry targets **overall + Gemma**. **GitHub Actions CI** (running the existing offline tests on push) is the only addition, and only if the core is finished by Thursday 22 Oct, 14:00 IST. **Deferred until after submission:** Sentry (it needs a network/SDK exception that weakens the local-privacy story), the Render replay and `.tech` routing (a new deployment surface; a local video is enough), ElevenLabs narration, Entire, Copilot agent work and the R-CLI trial.
- **Evidence and uncertainty:** no per-category entrant data exists, so this is not a win-probability calculation. The judgement is that finished correctness, an independent evaluation and a candid write-up beat several thinly evidenced categories. Effort figures are hypotheses.
- **Consequence:** INT-02, -03, -04, -07, -08 and -09 and DEP-02 are deferred; INT-06 (Copilot agent) is deferred; INT-10 (Actions) is optional with a deadline. Only completed qualifying uses may be named in the post.

### D-24 Set C is frozen outside the public repository

- **Date:** 2026-10-20. **Status:** accepted.
- **Context:** The GitHub repository [bipul724/availability-ledger](https://github.com/bipul724/availability-ledger) is public (GitHub API, 2026-10-20). Implementation agents also work in the same folder. Committing C, as the earlier EVAL-01 wording required, would show it to those agents and to the public before it is scored.
- **Decision:** C is written and stored in `~/Documents/availability-setC/`, outside every repository. Only a SHA-256 manifest (`fixtures/setC.manifest`) is committed at freeze time, which shows C has not changed since. The files enter `fixtures/` only at EVAL-07, after their hashes are verified. The project owner writes C; an optional fresh steward session converts the notes into the reference schema. The planning lead and implementation agents never see it. Brief: [specs/eval-01-setC-brief.md](specs/eval-01-setC-brief.md).
- **Tradeoff:** the manifest proves C is unchanged but not that nobody read it, so the isolation rests on the stated rules.

### D-25 Missed cancellations: warn first, no new extraction vocabulary before C is scored

- **Date:** 2026-10-20. **Status:** accepted.
- **Context:** On set B, Gemma + rules silently missed "scratch Wednesday" (PROGRESS known defect 6). Adding the missing words to the rules or the prompt would be tuned to set B wording.
- **Decision:** COR-07 becomes **COR-07a**, a code-level warning. When a later message from a person mentions a day on which they still have open availability and contains a change word from a general-English list, but no live claim from that message touched that day, the app raises an `unanswered_change` issue. It never edits the sheet. Vocabulary changes to the rules or the prompt (COR-07b) are deferred until after C is scored.
- **Why:** a warning keeps the human in the loop, reaches the reviewer even when extraction misses entirely, and generalises beyond set B's phrasing. Its false-alarm rate on C is part of EVAL-07.

### D-26 Duplicate-aware extraction scoring before set C is scored

- **Date:** 2026-10-20. **Status:** accepted.
- **Context:** Duplicates are no longer extracted (D-14), but `evaluation/run.py` still counts a duplicate's reference units, which turns correct behaviour into apparent misses (context §8).
- **Decision:** EVAL-10 excludes messages with `duplicate_of` from both reference and predicted unit counts, reports how many units were excluded, and leaves ledger-level metrics unchanged. This must land before EVAL-07; historical tables stay as they were, and changed current A/B numbers are labelled.

### D-27 Documentation economy until submission

- **Date:** 2026-10-20. **Status:** accepted.
- **Context:** Project docs exceed 2,500 lines across 18 files, and each task has updated most of them. Documentation now competes with the core work and the write-up for the time left.
- **Decision:** until submission, each task updates **its own TASKS row**, adds **one dated PROGRESS entry** (what changed, which checks were run, results), and updates the affected spec only if a contract changes. context.md changes only when the plan or a material state changes. No new research documents. The standing rule to record every task still holds; this limits how much is written, not whether it is recorded.

### D-28 Work that cannot bias set C may start before the C freeze

- **Date:** 2026-10-20, about 21:30 IST. **Status:** accepted.
- **Context:** The implementation agent correctly stopped because the C manifest does not exist yet. An earlier brief named it `setC.sha256`; the canonical name is now `fixtures/setC.manifest` (D-24). Waiting for C would idle the agent for half a day.
- **Decision:** the freeze protects C as an independent test of changes to **what is extracted and what reaches the sheet**. COR-10 and COR-07a change exactly that, so they still wait. COR-03 (visible extraction failures and continuing after them), COR-02 (CSV formula protection), EVAL-09 and EVAL-10 (metric definitions fixed from invented inputs) do not change any reader's claims or the ledger, so they may start now. Their acceptance tests use invented messages only, and they must not touch `ledger/model.py`, `ledger/rules.py`, `ledger/hybrid.py`, `ledger/resolve.py`, or claim and ledger logic in `ledger/core.py`.
- **Check:** after these tasks, a cached re-run of A/B must leave every extraction and ledger number unchanged, except metrics EVAL-09 and EVAL-10 intentionally redefine, which are reported separately and labelled. Any other change means the work crossed the boundary and must be reverted or re-planned.

### D-29 Set C may be written by a fresh, isolated AI session if the owner cannot write it

- **Date:** 2026-10-21, about 01:00 IST. **Status:** accepted.
- **Context:** The owner asked whether their coding agent could write set C. Waiting for a human writer puts C on the critical path.
- **Decision:** **Not the coding agent.** It has seen the code and the A/B failures, and it will implement COR-10 and COR-07a, so a C it wrote would not test its own changes independently. A **brand-new AI session** may write C instead, under these conditions:
  - it is started only for this task and never used afterwards for this project's code, planning or briefs;
  - it works only in `~/Documents/availability-setC/`;
  - it does not read the project's code, tests, docs (other than the brief), set A/B messages or results;
  - it gets the reference format from the brief and its own reading of `fixtures/reference.json`.
  The owner then reads every message and **rewrites at least 5 of them in their own words** before freezing, and spot-checks the reference answers.
- **Consequence:** C is recorded as "written by an isolated AI session, edited by the owner". That is weaker than human-written, because a model may write in ways models read easily, and the write-up must say so. It is still independent of the code changes, which is what EVAL-07 needs.
- **Addendum (2026-10-21, about 01:15 IST):** the owner chose to use **ChatGPT** as the isolated writer. A model from a different provider is acceptable, and arguably more independent of the code's author. C is fictional, so sending it to that service raises no privacy issue; it must stay within the free tier (₹0). ChatGPT cannot read local files, so the owner pastes a self-contained prompt, saves its outputs into `~/Documents/availability-setC/` and runs the local consistency check from the brief. The owner-edit rule (at least 5 messages) still applies.

### D-30 COR-10: flag unsupported phrases, do not hold them; keep COR-07a

- **Date:** 2026-10-21, about 03:15 IST. **Status:** accepted.
- **Evidence (post-hoc, A/B):** COR-10 as specified held **28 suggestions, every one correct, 0 wrong**. The model had rewritten the wording without changing the meaning ("Wed" → "Wednesday", "from 2 until 6" → "2-6"). Slot agreement fell in seven configurations (e.g. B Qwen + rules 1.0 → 0.810), and missed cancellations rose in three. That is worse than the 15:3 record that removed D-13. The case that motivated COR-10, a real quote with invented **days**, is already covered by the quote-day gate (`days_narrowed_to_quote` / `days_not_in_quote`, D-06). Neither A nor B shows an invented **time**.
- **Decision:** option (b). Revert the hold. A `phrase_not_in_message` suggestion counts on the provisional sheet as before, keeps its visible flag, stays excluded from bulk accept (as before), and is listed under Needs a decision as a **non-blocking** "check the wording" item. The final export still takes accepted claims only, so nothing unreviewed reaches it.
- **Rejected for now:** option (c), meaning-based time checking. It is plausible, but there is no observed failure to fix, it would be a new post-hoc design, and there is no time to validate it before EVAL-07.
- **COR-07a kept:** 13 warnings on A/B, all real missed cancellations, 0 false alarms (post-hoc; word list fixed before the run). Its independent test is EVAL-07 on set C.

### D-31 Fix the reconciliation defects set C exposed, labelled post-hoc; set C's first score stays the headline

- **Date:** 2026-10-21, about 03:45 IST. **Status:** accepted.
- **Evidence (independent, set C, scored once at `56e38bd`):** Gemma + rules scored 17/20 units but only **0.527** final-sheet slot agreement, with 2 of 8 cancellations missed. The lead re-checked this from `evaluation/results/frozen-setC/`. The causes are mostly **deterministic code**, not the model:
  - **m13:** "Sat 21 Nov" was resolved to the planning week's Saturday, giving a silent wrong-day cancellation.
  - **m19:** "definite now" with no time did not settle a conditional offer.
  - **m20/m21:** corrections ("only … now", "change … to") were not applied as replacements.
  - **m23:** "T. Vekar" (initial plus surname) became an unknown person instead of an ambiguity.
  - **m15/m16 (rules only):** "cancelling" and "out" were missed.
  COR-07a raised 0 warnings, because in each failure some suggestion had touched the day.
- **Decision:** fix these as general rules, using invented development messages (COR-13 to COR-17). Every set C (and A/B) number after a fix is **post-hoc** and reported beside, never instead of, the frozen first score. The write-up leads with the frozen set C table and explains what the independent test found.
- **Optional independent check:** if the owner has about 45 minutes, a small fresh **set D** (≥ 12 messages, the same isolated-writer process, D-24/D-29) scored once after the fixes (EVAL-11) would test them independently. Without it, the fixes are claimed only as post-hoc corrections plus unit tests.
- **Why not stop here:** the defects produce silent wrong sheets, which is the product's core failure mode. They are cheap, deterministic fixes, and the time to submission allows them.

### D-32 Accept D-31 as delivered; make cue-only replacements visible (COR-18); accept the B rules regression

- **Date:** 2026-10-21, about 12:00 IST. **Status:** accepted.
- **Review of D-31 (lead, re-run):** 81 unit tests pass on Python 3.15 and 3.12; fixtures, `runs/`, `frozen/`, `frozen-setC/`, `tuning/` and `ledger/model.py` have no diff; RESULTS.md keeps the frozen set C table and adds a separate post-hoc subsection. The code diff matches the five TASKS rows.
- **Risk found (COR-15):** `REPLACE_CUES` is matched against the **whole message**, not the claim's own wording. With invented messages, an earlier "Sat 10-12" was removed from the sheet in three cases where it should have stayed: a cue in another sentence ("Moving my Fri slot to 2-4 instead. Also free Sat 6-8."), "now" used for an addition ("I can now also do Sat 6-8") and "move" as an activity ("help move tables Sat 6-8 too"). "Also free Sat 6-8" (no cue) correctly kept both. The removal is shown only in that day's history ("replaced earlier answer for this day"), not as an issue, so a reviewer reading the sheet would not see it.
- **Decision:** keep COR-15 (it fixed real set C and set A misses) and add **COR-18**: when a replacement comes only from `REPLACE_CUES` (the reader did not set `replaces_earlier`), raise a review issue naming the time that was removed. Warning only: sheet, chart, export and scores unchanged. Narrowing the cue to the claim's own sentence is deferred: it would change scores again and would need fresh data to judge.
- **COR-14 regression on set B rules (chart slots wrong 58 → 64):** accepted and documented, not fixed. The cause is the rules reader's missing negation word in a held-out message; any fix designed from it would be tuning on held-out data.
- **Set D (EVAL-11), if run:** the brief should ask for a few messages that use "now", "move", "change" or "instead" without changing an earlier answer.

### D-33 Owner override of D-23: add Copilot (Actions), Render, Sentry and ElevenLabs

- **Date:** 2026-10-21, about 13:00 IST. **Status:** accepted (owner request; plan by the project lead).
- **Owner request:** enter as many categories as possible by adding Render, Sentry, ElevenLabs and GitHub Copilot to the existing system.
- **Official routes** (HF26 hub, read 2026-10-21):
  - **Copilot:** "automate your project with GitHub Actions" is a listed route.
  - **Render:** "host an agent's front end".
  - **Sentry Agent Tracing:** show setup, performance (latency, tokens, cost), what you found and how you debugged it, with traces or screenshots.
  - **ElevenLabs:** "generate narration for your demo".
- **Deadline unchanged:** the event API says 25 Oct 06:59 UTC (12:29 IST); the written rules say 25 Oct 11:59 PM PDT (26 Oct 12:29 IST). Plan for the earlier one. Internal publish target stays Sat 24 Oct 21:00 IST.
- **Scope per category (smallest genuine use):**
  - **INT-11 Copilot via Actions:** extend CI with a protected-files integrity check and a cache-only re-score that writes the score table to the job summary. Needs a new `--cache-only` flag that fails on a cache miss instead of calling the model.
  - **DEP-02/INT-02 Render:** a read-only hosted replay of fictional set A with saved Gemma outputs. Demo mode is on only via an env var: no paste box, no model calls, a banner saying it is a replay. The local default (127.0.0.1, live model) is unchanged.
  - **INT-03 Sentry:** opt-in tracing (off unless `SENTRY_DSN` is set), using the optional `sentry-sdk` package. One span per model call with model name, duration, load time and token counts, plus spans for resolve, ledger and export. No message text, names, quotes, prompts or replies; an allowlist scrubber is tested with invented sensitive strings. `ledger/model.py` and the prompt are not changed: spans wrap the call sites. Real traces on fictional data; the finding is whatever the traces show.
  - **INT-04 ElevenLabs:** narration of the demo video from the lead's script, made in the owner's account with a stock voice. No code and no runtime dependency.
- **D-11 exception:** the core stays standard-library only. `sentry-sdk` is optional (`requirements-tracing.txt`), imported only when `SENTRY_DSN` is set. Tracing sends content-free timing metadata to Sentry's cloud, and the post says so.
- **Order and gates:**
  - **Wed 21:** INT-11.
  - **Thu 22:** DEP-02 Render; deployed by 22:00 IST.
  - **Fri 23:** INT-03 Sentry; real traces by 18:00 IST.
  - **Sat 24 morning:** record and narrate.
  - **Sat 24 evening:** post.
  - Any category that misses its gate is dropped from the post, not rushed. Core quality and the write-up come first.
- **Owner-only steps:** create accounts (Render, Sentry, ElevenLabs), redeem offers, enter keys in dashboards or a local `.env`, deploy, and confirm free-tier terms (no card, no paid fallback). Keys are never committed or pasted into chat.
