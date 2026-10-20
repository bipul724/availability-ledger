# Product requirements: Availability Ledger

Status of this document: describes the current prototype, planned core work and optional conditional integrations as of 2026-10-20. Future directions are not implemented features. Status words follow [PROGRESS.md](../PROGRESS.md#status-vocabulary). Start with [context.md](../context.md) and [CLAUDE.md](../CLAUDE.md); technology contracts are in [INTEGRATIONS.md](INTEGRATIONS.md) and verified competition research is in [COMPETITION.md](COMPETITION.md).

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
- Q5. What licence should the project carry? (None is declared.)

## 6. Scope

### Current scope (prototype, implemented)

Local single-user review tool: paste or upload messages, choose week, timezone label and reader (model + rules, model only, rules only), review suggestions beside source messages, explicitly mark messages reviewed, see issues, history, sheet and chart, export an accepted-only reconciled final-sheet CSV plus a separate review-log CSV. The in-app sheet/chart remain provisional because they include pending claims. Fictional demo included. See [README.md](../README.md#current-capabilities).

### Planned core release and conditional supporting integrations

Core order, with task ownership and completion criteria in [TASKS.md](../TASKS.md):

1. **Freeze unseen set C first (EVAL-01).** At least 20 new fictional messages and handwritten references must be frozen, unscored and committed before further behavior changes. Implementation agents must not inspect that set. No set C is present at this audit.
2. Show extraction failures (COR-03), and keep unsupported day/time suggestions off the sheet until reviewed (COR-10).
3. Protect both CSV exports against formula injection (COR-02).
4. Score C once after planned behavior changes (EVAL-07), recording the exact code version. Validate the coordinator workflow, seek independent reference review and run the matched timing study (EVAL-02/EVAL-03/EVAL-04). Feedback can proceed in parallel; time savings remain unmeasured until the protocol is followed.

The confirmed final export and final-sheet scorer (COR-01/EVAL-06), atomic re-run preservation and strict-reader follow-ups already exist. Documentation/evaluation labeling REL-03 is done. Save/reopen (COR-04), provisional-sheet clarity (UI-05) and the older evaluation metric fix (EVAL-09) remain separate tasks. If cancellation extraction work COR-07 is undertaken, develop on newly invented examples without opening C; score C once afterward (EVAL-07), recording the exact version.

The agreed supporting portfolio has distinct roles: genuine Copilot development/review plus Actions CI; genuine future Entire sessions; conditional metadata-only Sentry diagnostics; a Render-hosted fictional replay; the owner's domain as its address; ElevenLabs narration; and optional Backboard R-CLI development if useful and locally compatible. **Only Gemma is implemented.** None of these plans authorizes installing tools, claiming credits, deploying services or changing code in this documentation task. Gates and evidence contracts are centralized in [INTEGRATIONS.md](INTEGRATIONS.md).

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
| S3 | Later correction or cancellation: "can't do Thursday after all" | Thursday availability removed; history says "cancelled" | **Partial.** Ledger logic verified; extraction misses some cancellations. Gemma alone left 7 of 12 set A cancellations on the final sheet; Gemma + rules 0 of 12 (fictional) |
| S4 | Correction to one day keeps another: "Actually Monday 10-11 instead" after "Monday and Wednesday mornings" | Monday 10–11; Wednesday unchanged | **Implemented, Verified** (unit test) |
| S5 | Conditional: "Saturday maybe, if my sister can babysit" | conditional segment, listed in Needs a decision until a later message resolves or declines it | **Implemented, Verified** in evaluation (Gemma + rules got 2 of 7 set A conditions wrong) |
| S6 | Similar names: "Maria Lopez" and "Marta Lopes"; "Sam" with Sam Okafor and Samira Haddad on the roster | similar name flagged; ambiguous short name not applied; a prefix matching only one roster name resolves to that person | **Implemented, Verified** (unit tests) |
| S7 | Duplicate message sent twice within 24 h | second copy greyed, "Same as mXX", no separate suggestions, history "repeated" | **Implemented, Verified** (unit tests and a headless-browser check, 2026-10-20) |
| S8 | Ambiguous date: "Next Friday" sent on a Monday; "one day this weekend" | both candidate dates shown; not applied until the reviewer picks | **Implemented, Verified** (unit tests) |
| S8b | Ambiguous or unreadable time: "at 9", "the same" with nothing earlier | not applied; issue shown | **Implemented, Verified** (unit tests) |
| S9 | No availability: "Thanks! Do I need gloves?"; coordinator's own "still need people Thursday" | "No availability found in this message"; coordinator self-claims dropped when the sender is off the volunteer roster | **Implemented.** Partly verified by evaluation. Since COR-03 (2026-10-20) a request error or unreadable model reply is shown as a per-message warning instead of "no availability" |
| S10 | Human review and confirmed export | only accepted records in the final sheet, corrections replayed; complete only when every message is explicitly reviewed | **Implemented, Verified** (unit tests, headless Chrome, 2026-10-20). The in-app sheet and chart still include pending suggestions (UI-05) |

## 9. Requirements

### Functional

| ID | Requirement | Status |
|---|---|---|
| FR-01 | Parse `YYYY-MM-DD HH:MM \| Sender \| text` lines and WhatsApp Android/iOS exports, including multi-line messages | Implemented, Verified (fixtures) |
| FR-02 | Accept a roster of up to 20 names | Implemented (extras silently dropped; should warn) |
| FR-03 | Offer three readers: model + rules (default), model only, rules only | Implemented, Verified |
| FR-04 | The model only copies phrases; code resolves dates and times | Implemented, Verified |
| FR-05 | Drop suggestions when neither the quote nor the day/time words are in the message, with a visible reason and a "Use it anyway" option | Implemented, Verified. **Partial guarantee:** a real quote with invented day/time words is flagged but applied provisionally (FR-20) |
| FR-06 | Never guess ambiguous people or dates; show candidates | Implemented, Verified |
| FR-07 | Keep per-person, per-day history; later answers change only the time they mention | Implemented, Verified |
| FR-08 | Keep conditional offers conditional until a later message resolves or declines them | Implemented, Verified |
| FR-09 | Show each suggestion beside its message with the supporting words highlighted | Implemented |
| FR-10 | Let the reviewer accept, reject, edit (volunteer, days, times, status, condition), reset, add records | Implemented |
| FR-11 | Bulk-accept suggestions without warnings | Implemented |
| FR-12 | Keyboard review: J/K/A/R/E/Esc, not while typing | Implemented, Verified (headless Chrome, 2026-10-20) |
| FR-13 | Collapse duplicate messages (same sender, same normalised text, within 24 h) | Implemented, Verified |
| FR-14 | Show Needs a decision, the sheet, a half-hourly chart and Changes over time | Implemented |
| FR-15 | Export reviewed records as a review-log CSV with source and warnings | Implemented |
| FR-16 | Export a confirmed final sheet built from accepted records only, marking anything pending or unresolved, complete only after explicit message review | Implemented, Verified ([specs/final-export.md](specs/final-export.md)) |
| FR-17 | Save and reopen a review session | **Planned** (COR-04) |
| FR-18 | Show a warning when extraction fails for a message | **Implemented** (COR-03, 2026-10-20; browser check `tests/browser/extraction_failures.mjs`) |
| FR-19 | Use the selected timezone, or remove the field | **Planned** (COR-05) |
| FR-20 | Day or time words not found in the message never reach the sheet without a reviewer's decision | **Planned** (COR-10) |

### Usability

- USE-01 Every suggestion links to its message and quote (implemented).
- USE-02 Warnings are worded in plain English (implemented, `FLAG_TEXT` in `ui/app.js`).
- USE-03 Review is possible by keyboard (implemented).
- USE-04 Accessibility with screen readers and contrast: **unverified**.

### Privacy

- PRIV-01 Messages never leave the machine in the core workflow (implemented: state is retained in browser memory and processed transiently by the local server; only `127.0.0.1` is contacted; no application persistence).
- PRIV-02 No telemetry is implemented. Proposed Sentry diagnostics must be opt-in, off by default and allow-list non-sensitive operational metadata; exclude message text, names, quotes, prompts/replies and raw sensitive exceptions. A dependency/network/privacy decision is required before implementation ([INTEGRATIONS.md](INTEGRATIONS.md), [DECISIONS.md](DECISIONS.md) D-17).
- PRIV-03 Any external data transfer must be disclosed before use. Demo narration uses a fictional script; in-app transcription is not selected. Development sessions and issues shared through sponsor tools must exclude private pilot data, secrets and credentials.
- PRIV-04 A real pilot requires written owner confirmation of consent and prior anonymisation, storage outside version control, local-only processing and aggregate-only reporting. Public hosting/demo fixtures remain fictional.

### Performance

- PERF-01 Target: usable on an 8 GB Mac. Historical runs report Gemma allocation about 1.59 GB and prompt-v3 median 2.45 s/message on A, 2.30 s on B; an earlier 50-message hybrid run was reported at 131 s ([RESULTS.md](../evaluation/RESULTS.md)). Allocation is not total machine memory; other-app behavior and current end-to-end performance have not been remeasured.
- PERF-02 Rules-only mode responds without a model.

### Cost

- COST-01 Additional out-of-pocket spending stays at ₹0. Only free plans, existing local resources or sponsor credits.
- COST-02 No automatic paid upgrades, top-ups, paid fallbacks or renewals. When a free allowance ends, the optional feature stops or degrades; the local workflow keeps working.

## 10. Acceptance criteria for the next release (proposed, not yet met)

- AC-01 (met 2026-10-20) The confirmed final export follows [specs/final-export.md](specs/final-export.md): accepted records only, corrections replayed, pending or unresolved items marked, complete only after explicit review; with the set A reference claims accepted its rows reproduce `expected_sheet` in `fixtures/reference.json`.
- AC-01b A suggestion with invented day/time words never reaches the confirmed export or the sheet without a reviewer's decision (COR-10).
- AC-02 A forced invalid model reply shows a visible warning on that message (COR-03).
- AC-03 Reloading the page after saving a session restores every review decision (COR-04).
- AC-04 On a fresh held-out set written before any further change, Gemma + rules misses no more cancellations on the final sheet than on set B at first scoring (0/5), and silent errors are reported (EVAL-01 freeze, EVAL-07 score once).
- AC-05 A timing study following the revised [MEASUREMENT.md](../evaluation/MEASUREMENT.md) (comparable workloads, balanced order, equivalent final outputs, corrected scorer, more than one participant) is run before any claim of time saved (EVAL-02).

## 11. Success metrics

| Metric | How measured | Current value |
|---|---|---|
| Active review time vs manual typing | revised [MEASUREMENT.md](../evaluation/MEASUREMENT.md) protocol; target ≤ 70% at slot agreement no more than 2 percentage points below manual, across participants | **Not measured**; required final export/scorer exist, but the study has not run |
| Cancellations still on the final sheet | `missed_withdrawals` in `evaluation/run.py` over the complete message set (A includes dev; B is all held-out) | see [PROGRESS.md](../PROGRESS.md#evaluation-status) |
| Silent errors (wrong with no warning) | `silent_errors` in `evaluation/run.py` | see PROGRESS.md |
| Final-sheet slot agreement | `evaluation/run.py` for existing benchmark tables; `evaluation/score_final.py` for both timing-study outputs | see PROGRESS.md; study unmeasured |
| Coordinator willingness to use it | interviews or a pilot with consented, anonymised messages | **Not measured** |

The click-count "effort proxy" is not a time measurement and must not be reported as time saved. Current A/B values are post-hoc; preserve frozen results. EVAL-09 remains open because the older `evaluation/run.py` condition metric misses partial loss; the final-sheet timing scorer detects it. Unresolved person/day cells count as 68 disagreeing 15-minute slots, once per cell.

## 12. Risks and validation experiments

| Risk | Experiment |
|---|---|
| Nobody wants this; a signup form is enough | Talk to 3–5 coordinators; show the fictional demo and a form; ask which they would use (EVAL-03) |
| Review takes as long as typing | Timing study (EVAL-02) |
| Silent missed cancellations | Fresh held-out set with varied cancellation wording, frozen first and scored once (EVAL-01, EVAL-07) |
| Evaluation is circular (same author wrote fixtures, rules and references) | Have someone else write or check a message set and reference (EVAL-04) |
| Real chats differ from fixtures | One consented, anonymised real week (EVAL-03) |
| A free tier expires or starts charging | Optional runtime services off by default; verify allowances and cost controls before activation, stop/degrade rather than charge, and do not add a payment method under this plan (D-18) |


## 13. Competition strategy and product boundaries

The owner's objective is to maximize legitimate winning opportunities while retaining Gemma and the ₹0 additional-spending limit. Keep **Overall + Gemma** as the current implemented fit, then add only categories backed by completed, meaningful use. The contest theme is **Slow and Steady**; sponsor categories are optional awards, not separate product requirements. The rules permit entry into multiple genuinely used categories, with at most one prize. Eligibility, the deadline conflict, all sponsor categories, Week 1 winners and Week 2 submissions are sourced in [COMPETITION.md](COMPETITION.md).

Historical winning posts provide useful examples of concrete use, technical decisions and candid evaluation. They do not establish that CI/narration alone is a strong winning lane, that any category is easier, or that integrating more services raises our probability of winning. No reliable category entrant totals or judge scorecards are available in the recorded research. Writing quality has the highest published judging weight, so a clear, truthful explanation is part of the release work.

Our practical priorities remain correctness, a reviewed final artifact, independent evaluation and coordinator validation. Human review, corrections and local processing are not unique by themselves; claims of originality must address specific behavior and evidence. Do not add a feature just to resemble a historical winner or promote a planned integration, fictional benchmark or demonstration replay into a production capability.
