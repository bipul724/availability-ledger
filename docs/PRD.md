# Product requirements: Availazy (formerly Availability Ledger)

Status of this document: product requirements and their implementation status, rechecked against source on 2026-10-23. Targets and unmet acceptance criteria are not implemented guarantees. Dated evaluation figures retain their original provenance; current test evidence is in [TESTING.md](../TESTING.md). Status words follow [PROGRESS.md](../PROGRESS.md#status-vocabulary). Start with [context.md](../context.md) and [CLAUDE.md](../CLAUDE.md); technology contracts are in [INTEGRATIONS.md](INTEGRATIONS.md) and dated competition research is in [COMPETITION.md](COMPETITION.md).

## 1. Problem

Volunteer coordinators for small community groups collect availability through ordinary messages: WhatsApp, SMS, email. People answer in their own words ("after 3", "next Tuesday", "maybe Saturday if my sister can babysit"), change their minds later ("actually make it 10-11"), cancel ("can't do Thursday after all") and repeat themselves. The coordinator reconciles all of it by hand into a spreadsheet, re-reading threads to find out who is free when.

The error that matters most is a **silent** one: a cancellation or a condition that never reaches the sheet, so the coordinator counts on someone who is not coming.

**Availability is not assignment.** This product records when people say they can or cannot help. Deciding who works which shift stays with the coordinator and is out of scope.

## 2. Users and current workaround

- **Primary user:** one volunteer coordinator (non-technical) planning a week of shifts for up to about 20 volunteers, on their own laptop.
- **Current workaround (assumed):** read each message, type or edit rows in a spreadsheet, scroll back through the chat when someone changes an answer. Some groups use a signup form instead; the fixtures suggest many answers would not fit fixed form boxes (see §4).
- **Volunteers** are not users of the tool. They keep messaging the way they already do.

## 3. Jobs to be done

1. Turn a week's worth of messages into a list of who is available, when, without retyping.
2. Notice every cancellation, correction and condition, and see which message caused it.
3. Resolve unclear cases (which Sam? which Friday?) without the tool guessing.
4. See how many people are available in each part of each day.
5. Hand on a reviewed list (CSV) for planning shifts elsewhere.
6. Keep messages private.

## 4. Evidence

| Claim | Evidence | Strength |
|---|---|---|
| Coordinators reconcile message-based availability by hand, weekly | Anecdotal: one public post in r/nonprofit, "Volunteer scheduling help" (https://www.reddit.com/r/nonprofit/comments/1apjpbc/volunteer_scheduling_help/), describing weekly manual reconciliation. Found in an earlier review; this document's author could not re-open the page (fetch blocked). | **Anecdotal** (one source) |
| The time spent is meaningful and a tool would reduce it | No interviews, surveys or real-user validation. | **Unverified** |
| Free-text answers do not fit a fixed signup form | `form_analysis` over the fictional references: set A 18 of 31 final records fit morning/afternoon/evening boxes, set B 7 of 11 ([RESULTS.md](../evaluation/RESULTS.md)) | Weak: reflects how the fixtures were written |
| A small local model can read these messages | Set B held-out (fictional): Gemma 4 E2B + rules 30/35 units right at first scoring ([RESULTS.md](../evaluation/RESULTS.md)) | Technical only; fictional data written by the same author as the references |
| Generalisation remains uncertain | First-scored independent set C: Gemma + rules 17/20 units, 0.527 slot agreement and 2/8 missed final-sheet cancellations; subsequent fixes are post-hoc ([RESULTS.md](../evaluation/RESULTS.md)) | Small fictional set written by an isolated AI session plus owner edits; not real-chat validation |
| The local end-to-end workflow runs with the installed model | Owner's 2026-10-23 Ana/Ben Model-only check matched two invented messages and their quotes, then produced the expected provisional and complete CSVs (CFG-02 in [PROGRESS](../PROGRESS.md#cfg-02--dep-03-owner-manual-live-model-smoke-check-passed-2026-10-23)) | Bounded smoke check, not a full-week/hybrid accuracy benchmark |
| The tool saves human time | Not measured. Only a click-count proxy exists. Protocol in [MEASUREMENT.md](../evaluation/MEASUREMENT.md) | **Unverified** |

No real-coordinator use, interviews or processing of real messages is recorded in the project evidence. Any later pilot must meet the consent, anonymisation and local-only rules in [CLAUDE.md](../CLAUDE.md).

## 5. Assumptions and open questions

- A1. Coordinators can export or paste their chats as text. (Untested beyond the WhatsApp line formats in the parser.)
- A2. An 8 GB laptop is adequate for the target coordinator. Gemma has recorded runs on an 8 GB Mac, but typical coordinator hardware and behavior with other apps open are unverified. Ollama-reported model allocation is not total machine memory ([RESULTS.md](../evaluation/RESULTS.md)).
- A3. Coordinators will review suggestions rather than accept them blindly.
- Q1. Would coordinators rather send a signup link than review messages?
- Q2. Is reviewing actually faster than typing (target: at most 70% of manual time at equal correctness)?
- Q3. What should happen across weeks: should one week's answers carry to the next?
- Q4. Does anyone need the timezone field, or should it be removed (it is not used today)?
- Q5. The code/documentation licence was settled as MIT on 2026-10-21 ([LICENSE](../LICENSE)); the model's licence is separate. This is no longer an open product question.

## 6. Scope

### Current scope (prototype, implemented)

Local single-user review tool: paste or upload supported dated text/WhatsApp exports, choose week, timezone label and reader (model + rules, model only, rules only), review suggestions beside source messages, explicitly mark messages reviewed, see issues, history, sheet and chart, export an accepted-only reconciled final-sheet CSV plus a separate review-log CSV. The in-app sheet/chart include pending claims, visibly distinguish them, and show Provisional until the export's completeness conditions are met. Fictional local demo, hosted saved-output replay, landing page, user guide and optional opt-in tracing are implemented. See [README.md](../README.md#current-capabilities).

### Completed release work and remaining validation

Current status, with ownership and completion criteria in [TASKS.md](../TASKS.md):

1. **EVAL-01/EVAL-07 completed:** set C was written outside the implementation context, frozen by committed manifest, then copied into the repository and first-scored once on 2026-10-21. Frozen scores remain protected; current A/B/C results are post-hoc after COR-13–COR-18.
2. **COR-03/COR-10 completed:** failures are visible per message. Under D-30, unsupported day/time wording is flagged and listed for review, but still affects the provisional sheet while pending. The proposed holdback was rejected after it suppressed correct reworded suggestions; do not describe it as implemented.
3. **COR-02/UI-05/EVAL-09 completed:** both CSV writers neutralise formula-like cells; pending display is explicit; both scorers share the every-slot condition verdict. The final export/scorer and atomic failed-rerun preservation also exist.
4. **Remaining validation:** coordinator feedback/consented pilot, independent reference review and matched timing study (EVAL-02/EVAL-03/EVAL-04) remain unfinished. A fresh optional set D would test the post-hoc fixes independently (EVAL-11). The two-message model smoke check and dated full-week Sentry demonstration runs do not replace these studies.

Save/reopen (COR-04), timezone semantics (COR-05), an explicit roster-limit warning (COR-06), exact mixed-segment review provenance (UI-06), Rules negation inside a condition (COR-19) and screen-reader follow-ups (UI-22) remain separate proposed/deferred tasks. Future behavior changes need invented development examples and honest post-hoc labels; set C cannot become unseen again.

Implemented supporting uses are **GitHub Actions** (unit/integrity/cache-only CI), **Render** (fictional replay) and **opt-in Sentry tracing** (source allowlists, real received traces and a bounded privacy check; wider questions remain open). No verified Copilot coding-agent, Entire, domain connection or Backboard R-CLI use is recorded. ElevenLabs was dropped (D-37); demo narration uses owner voice or captions. Runtime, development and public-demo roles stay distinct. These statuses do not authorize new installations, accounts, external data transfers or deployment changes. Gates and evidence are centralized in [INTEGRATIONS.md](INTEGRATIONS.md).

### Non-goals

- Assigning volunteers to shifts, rotas or notifications to volunteers.
- Sending anything to volunteers or reading chats automatically from WhatsApp or other services.
- Multi-user accounts, cloud sync or a hosted service that processes real messages.
- In-app voice, online transcription, a cloud database or a new orchestration/provider stack merely to enter a prize category. These are not selected features.
- Paid APIs, paid hosting or any feature that requires spending money (see §9).
- Guessing ambiguous names or dates.

## 7. User journeys

**J1. Weekly reconciliation (main).** Coordinator exports the group chat → pastes it with the roster → picks the Monday of the planning week → clicks **Suggest records** → reviews cards top to bottom (mouse or J/K/A/R) → works through **Needs a decision** → explicitly marks each message reviewed → checks the provisional sheet/chart → exports the final-sheet CSV and checks its complete/provisional status. The original review mark covers duplicate messages.

**J2. Late change.** A volunteer messages a correction on Thursday. The coordinator adds the new line, runs again, and sees the change in **Changes over time** with a link to the message. (A successful re-run replaces earlier review decisions; invalid settings, failed parsing or no dated messages preserve the existing session. Save/reopen remains COR-04.)

**J3. Try without a model.** On a machine without Ollama, choose **Rules only**; everything except the model reader works.

## 8. Scenarios and current status

| # | Scenario (fictional example) | Expected behaviour | Status today |
|---|---|---|---|
| S1 | Initial availability: "I can do Tuesday and Thursday mornings" | two records, 09:00–12:00 each | **Implemented, Verified** (reference-sheet test; evaluation) |
| S2 | Partial day: "Monday after 3", "10:30 to 1", "4 onwards" | 15:00–20:00, 10:30–13:00, 16:00–20:00 | **Implemented, Verified** (unit tests). Point times ("at 9") are deliberately left unread |
| S3 | Later correction or cancellation: "can't do Thursday after all" | Thursday availability removed; history says "cancelled" | **Partial.** Ledger logic verified; extraction still misses some cancellations. Frozen first-scored set A: Gemma alone left 7/12; Gemma + rules 0/12. Frozen set C: Gemma + rules missed 2/8. Current fixes and scores are post-hoc; see RESULTS |
| S4 | Correction to one day keeps another: "Actually Monday 10-11 instead" after "Monday and Wednesday mornings" | Monday 10–11; Wednesday unchanged | **Implemented, Verified** (unit test) |
| S5 | Conditional: "Saturday maybe, if my sister can babysit" | conditional segment, listed in Needs a decision until a later message resolves or declines it | **Implemented with limitations.** Ledger transitions are tested, including untimed firm follow-ups on conditional-only days (COR-14). Extraction can misread conditions; Rules negation inside a condition is COR-19. Historical frozen set A Gemma + rules got 2/7 conditions wrong |
| S6 | Similar names: "Maria Lopez" and "Marta Lopes"; "Sam" with Sam Okafor and Samira Haddad on the roster | similar name flagged; ambiguous short name not applied; a prefix matching only one roster name resolves to that person | **Implemented, Verified** (unit tests) |
| S7 | Duplicate message sent twice within 24 h | second copy greyed, "Same as mXX", no separate suggestions, history "repeated" | **Implemented, Verified** (unit tests and a headless-browser check, 2026-10-20) |
| S8 | Ambiguous date: "Next Friday" sent on a Monday; "one day this weekend" | both candidate dates shown; not applied until the reviewer picks | **Implemented, Verified** (unit tests) |
| S8b | Ambiguous or unreadable time: "at 9", "the same" with nothing earlier | not applied; issue shown | **Implemented, Verified** (unit tests) |
| S9 | No availability: "Thanks! Do I need gloves?"; coordinator's own "still need people Thursday" | "No availability found in this message"; coordinator self-claims dropped when the sender is off the volunteer roster | **Implemented.** Partly verified by evaluation. Since COR-03 (2026-10-20) a request error or unreadable model reply is shown as a per-message warning instead of "no availability" |
| S10 | Human review and confirmed export | only accepted records in the final sheet, corrections replayed; complete only when every non-duplicate message is explicitly reviewed, no claim is pending and no blocking issue remains | **Implemented, Verified** (unit/browser tests; owner two-message CSV check 2026-10-23). In-app sheet/chart include pending suggestions with distinct styling (UI-05); provisional export still downloads |

## 9. Requirements

### Functional

| ID | Requirement | Status |
|---|---|---|
| FR-01 | Parse `YYYY-MM-DD HH:MM \| Sender \| text` lines and supported WhatsApp Android/iOS exports, including multi-line messages | Implemented; pipe fixtures/unit tests and a recorded day-first upload check. Support for every locale/export variant is not established |
| FR-02 | Accept a roster of up to 20 names | Implemented (extras silently dropped; should warn) |
| FR-03 | Offer three readers: model + rules (default), model only, rules only | Implemented, Verified |
| FR-04 | The model copies phrases and proposes status/replacement hints; code resolves dates, times, history and counts | Implemented, Verified |
| FR-05 | Drop suggestions when neither the quote nor the day/time words are in the message, with a visible reason and a "Use it anyway" option | Implemented, Verified. **Partial guarantee:** a real quote with invented day/time words is flagged but applied provisionally (FR-20) |
| FR-06 | Never guess ambiguous people or dates; show candidates | Implemented, Verified |
| FR-07 | Keep per-person, per-day history; later answers change only the time they mention | Implemented, Verified |
| FR-08 | Keep conditional offers conditional until a later message resolves or declines them | Implemented ledger transitions; reader accuracy remains partial (COR-19 and recorded evaluation errors) |
| FR-09 | Show each suggestion beside its message with the supporting words highlighted | Implemented |
| FR-10 | Let the reviewer accept, reject, edit (volunteer, days, times, status, condition), reset, add records | Implemented |
| FR-11 | Bulk-accept suggestions without warnings | Implemented |
| FR-12 | Keyboard review: J/K/A/R/E/M/Esc, not while typing; M toggles the current card's message mark | Implemented, Verified in recorded Chrome checks |
| FR-13 | Collapse duplicate messages (same sender, same normalised text, within 24 h) | Implemented, Verified |
| FR-14 | Show Needs a decision, the sheet, a half-hourly chart and Changes over time | Implemented |
| FR-15 | Export reviewed records as a review-log CSV with source and warnings | Implemented |
| FR-16 | Export accepted records through reconciliation, marking scoped unsettled cells; complete only after non-duplicate message review, no pending claims and no blocking issues | Implemented, Verified; provisional downloads allowed ([specs/final-export.md](specs/final-export.md)) |
| FR-17 | Save and reopen a review session | **Planned** (COR-04) |
| FR-18 | Show a warning when extraction fails for a message | **Implemented** (COR-03, 2026-10-20; browser check `tests/browser/extraction_failures.mjs`) |
| FR-19 | Use the selected timezone, or remove the field | **Planned** (COR-05) |
| FR-20 | Unsupported day/time wording stays flagged, outside warning-free bulk acceptance, and visible in Needs a decision | **Implemented, Verified** (COR-10 flag-only, D-30). The earlier holdback requirement was superseded; pending claims still affect the provisional sheet, final time ranges require acceptance |

### Usability

- USE-01 Every suggestion links to its message and quote (implemented).
- USE-02 Warnings are worded in plain English (implemented, `FLAG_TEXT` in `ui/app.js`).
- USE-03 Review is possible by keyboard (implemented).
- USE-04 **Partially verified:** UI-02 recorded automated Chrome labels/focus/light-theme contrast/narrow-layout checks and a skip link to the summary. Screen readers, Firefox/Safari and UI-22 follow-ups remain unverified; this is not a complete accessibility certification.

### Privacy

- PRIV-01 Messages never leave the machine in the core workflow (implemented: state is retained in browser memory and processed transiently by the local server; only `127.0.0.1` is contacted; no application persistence).
- PRIV-02 **Implemented, with explicit limits:** optional Sentry tracing is off unless `SENTRY_DSN` is set and the optional SDK is installed (D-33). Two allowlists exclude message text, names, quotes, prompts/replies and raw exception text from application transmissions. Received location attributes have an unverified origin; a full received-data audit and account checks remain open ([SENTRY_HANDOFF.md](SENTRY_HANDOFF.md)). Hosted replay never initializes tracing.
- PRIV-03 Any external data transfer must be disclosed before use. The hosted replay processes packaged fictional data over the internet; do not send private data through direct API claim/override fields. Demo video uses fictional examples and owner voice/captions; in-app transcription is not selected. Development artifacts must exclude private pilot data, secrets and credentials.
- PRIV-04 A real pilot requires written owner confirmation of consent and prior anonymisation, storage outside version control, local-only processing and aggregate-only reporting. Public hosting/demo fixtures remain fictional.

### Performance

- PERF-01 Target: usable on an 8 GB Mac. Historical runs report Gemma allocation about 1.59 GB and prompt-v3 median 2.45 s/message on A, 2.30 s on B; an earlier 50-message hybrid run was reported at 131 s ([RESULTS.md](../evaluation/RESULTS.md)). Later owner-run full-week tracing demonstrations, including timeouts and an 86-second retry, are recorded in [SENTRY_HANDOFF](SENTRY_HANDOFF.md). Allocation is not total machine memory; these uncontrolled observations do not establish performance on typical coordinator hardware or a controlled current benchmark.
- PERF-02 Rules-only mode responds without a model.

### Cost

- COST-01 Additional out-of-pocket spending stays at ₹0. Only free plans, existing local resources or sponsor credits.
- COST-02 No automatic paid upgrades, top-ups, paid fallbacks or renewals. When a free allowance ends, the optional feature stops or degrades; the local workflow keeps working.

## 10. Acceptance criteria and actual outcomes

- AC-01 (met 2026-10-20) The confirmed final export follows [specs/final-export.md](specs/final-export.md): accepted records only, corrections replayed, pending or unresolved items marked, complete only after explicit review; with the set A reference claims accepted its rows reproduce `expected_sheet` in `fixtures/reference.json`.
- AC-01b **Superseded by D-30:** the proposed unsupported-word holdback was removed. The implemented acceptance criterion is a visible warning/non-blocking wording issue, exclusion from warning-free bulk acceptance, and accepted-only final time ranges (COR-10).
- AC-02 **Met in tests:** a forced invalid model reply shows a visible warning on that message, reading continues and no retry occurs (COR-03).
- AC-03 **Not implemented:** reloading after saving would restore review decisions; session save/load remains COR-04.
- AC-04 **Original target not met:** the first independent set C score was recorded with silent errors, but Gemma + rules missed 2/8 cancellations, above the target of zero. Post-hoc fixes reaching zero on C do not retroactively meet the unseen-data target (EVAL-01/EVAL-07).
- AC-05 **Not run:** a timing study following [MEASUREMENT.md](../evaluation/MEASUREMENT.md) (comparable workloads, balanced order, equivalent final outputs, corrected scorer, more than one participant) is required before any time-saved claim (EVAL-02).

## 11. Success metrics

| Metric | How measured | Current value |
|---|---|---|
| Active review time vs manual typing | revised [MEASUREMENT.md](../evaluation/MEASUREMENT.md) protocol; target ≤ 70% at slot agreement no more than 2 percentage points below manual, across participants | **Not measured**; required final export/scorer exist, but the study has not run |
| Cancellations still on the final sheet | `missed_withdrawals` in `evaluation/run.py` over the complete message set (A includes dev; B is all held-out) | see [PROGRESS.md](../PROGRESS.md#evaluation-status) |
| Silent errors (wrong with no warning) | `silent_errors` in `evaluation/run.py` | see PROGRESS.md |
| Final-sheet slot agreement | `evaluation/run.py` for existing benchmark tables; `evaluation/score_final.py` for both timing-study outputs | see PROGRESS.md; study unmeasured |
| Coordinator willingness to use it | interviews or a pilot with consented, anonymised messages | **Not measured** |

The click-count "effort proxy" is not a time measurement and must not be reported as time saved. Current A/B/C values are post-hoc; preserve frozen results. EVAL-09 is implemented: `evaluation/run.py` and the final-sheet scorer share the every-slot condition verdict, including partial loss. Frozen historical values retain their original metric/code provenance. Unresolved person/day cells in the final-sheet scorer count as 68 disagreeing 15-minute slots, once per cell.

## 12. Risks and validation experiments

| Risk | Experiment |
|---|---|
| Nobody wants this; a signup form is enough | Talk to 3–5 coordinators; show the fictional demo and a form; ask which they would use (EVAL-03) |
| Review takes as long as typing | Timing study (EVAL-02) |
| Silent missed cancellations | EVAL-01/EVAL-07's first-scored C exposed misses; future independent validation requires a fresh set, not retuning C (optional EVAL-11) |
| Evaluation is circular (same author wrote fixtures, rules and references) | Have someone else write or check a message set and reference (EVAL-04) |
| Real chats differ from fixtures | One consented, anonymised real week (EVAL-03) |
| A free tier expires or starts charging | Optional runtime services off by default; verify allowances and cost controls before activation, stop/degrade rather than charge, and do not add a payment method under this plan (D-18) |


## 13. Competition strategy and product boundaries

The owner's objective is to maximize legitimate winning opportunities while retaining Gemma and the ₹0 additional-spending limit. The recorded portfolio includes Overall/Gemma plus implemented Render replay, Actions automation and opt-in Sentry evidence; organizer eligibility and the final submitted categories remain owner checks. The contest theme is **Slow and Steady**; sponsor categories are optional awards, not separate product requirements. The recorded rules permit multiple qualifying categories with at most one prize; current eligibility/deadline confirmation belongs in [COMPETITION.md](COMPETITION.md), alongside dated historical research.

Historical winning posts provide useful examples of concrete use, technical decisions and candid evaluation. They do not establish that CI/narration alone is a strong winning lane, that any category is easier, or that integrating more services raises our probability of winning. No reliable category entrant totals or judge scorecards are available in the recorded research. Writing quality has the highest published judging weight, so a clear, truthful explanation is part of the release work.

Our practical priorities remain correctness, a reviewed final artifact, independent evaluation and coordinator validation. Human review, corrections and local processing are not unique by themselves; claims of originality must address specific behavior and evidence. Do not add a feature just to resemble a historical winner or promote a planned integration, fictional benchmark or demonstration replay into a production capability.
