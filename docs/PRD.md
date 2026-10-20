# Product requirements: Availability Ledger

Status of this document: describes the current prototype and a proposed next release. Anything under "Proposed" is not built. Status words follow [PROGRESS.md](../PROGRESS.md#status-vocabulary).

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

No real coordinator has used the tool, no interviews have been done, and no real messages have been processed.

## 5. Assumptions and open questions

- A1. Coordinators can export or paste their chats as text. (Untested beyond the WhatsApp line formats in the parser.)
- A2. A laptop with 8 GB of memory is typical; Gemma 4 E2B runs there while other apps are open (measured once, [RESULTS.md](../evaluation/RESULTS.md)).
- A3. Coordinators will review suggestions rather than accept them blindly.
- Q1. Would coordinators rather send a signup link than review messages?
- Q2. Is reviewing actually faster than typing (target: at most 70% of manual time at equal correctness)?
- Q3. What should happen across weeks: should one week's answers carry to the next?
- Q4. Does anyone need the timezone field, or should it be removed (it is not used today)?
- Q5. What licence should the project carry? (None is declared.)

## 6. Scope

### Current scope (prototype, implemented)

Local single-user review tool: paste or upload messages, choose week, timezone label and reader (model + rules, model only, rules only), review suggestions beside source messages, see issues, history, sheet and chart, export reviewed records as CSV. Fictional demo included. See [README.md](../README.md#current-capabilities).

### Proposed next release (not built)

Prioritised in [TASKS.md](../TASKS.md):
In order of work:
1. A confirmed final-sheet export built from accepted records only, and one scoring contract for confirmed final-sheet CSVs (COR-01, EVAL-06).
2. Visible extraction failures (COR-03), and unsupported day/time words kept off the sheet until reviewed (COR-10).
3. CSV protected against formula injection (COR-02).
4. Corrected documentation and evaluation labels (REL-03, done 2026-10-20).
5. A human timing study under the revised protocol (EVAL-02).
- Also: save and reopen a review session (COR-04); a fresh held-out message set written before further code changes (EVAL-01).
- Optional, opt-in, free-tier-only extras: replay-mode hosted demo, demo narration (DEP-02, INT-04).

### Non-goals

- Assigning volunteers to shifts, rotas or notifications to volunteers.
- Sending anything to volunteers or reading chats automatically from WhatsApp or other services.
- Multi-user accounts, cloud sync or a hosted service that processes real messages.
- Paid APIs, paid hosting or any feature that requires spending money (see §9).
- Guessing ambiguous names or dates.

## 7. User journeys

**J1. Weekly reconciliation (main).** Coordinator exports the group chat → pastes it with the roster → picks the Monday of the planning week → clicks **Suggest records** → reviews cards top to bottom (mouse or J/K/A/R) → works through **Needs a decision** → checks the sheet and chart → exports CSV.

**J2. Late change.** A volunteer messages a correction on Thursday. The coordinator adds the new line, runs again, and sees the change in **Changes over time** with a link to the message. (Note: re-running clears earlier review decisions today; see COR-04.)

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
| S9 | No availability: "Thanks! Do I need gloves?"; coordinator's own "still need people Thursday" | "No availability found in this message"; coordinator self-claims dropped | **Implemented.** Partly verified by evaluation. A model JSON failure is not flagged: with model only it looks like "no availability"; with model + rules only the rules' cancellations appear (COR-03) |
| S10 | Human review and confirmed export | only accepted records exported, with source message and warnings | **Partial.** Works, but the export is a record log that cannot reliably be replayed into the final sheet, and pending suggestions already count on the in-app sheet (COR-01) |

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
| FR-15 | Export reviewed records as CSV with source and warnings | Implemented |
| FR-16 | Export a confirmed final sheet built from accepted records only, marking anything pending or unresolved | **Planned** (COR-01) |
| FR-17 | Save and reopen a review session | **Planned** (COR-04) |
| FR-18 | Show a warning when extraction fails for a message | **Planned** (COR-03) |
| FR-19 | Use the selected timezone, or remove the field | **Planned** (COR-05) |
| FR-20 | Day or time words not found in the message never reach the sheet without a reviewer's decision | **Planned** (COR-10) |

### Usability

- USE-01 Every suggestion links to its message and quote (implemented).
- USE-02 Warnings are worded in plain English (implemented, `FLAG_TEXT` in `ui/app.js`).
- USE-03 Review is possible by keyboard (implemented).
- USE-04 Accessibility with screen readers and contrast: **unverified**.

### Privacy

- PRIV-01 Messages never leave the machine in the core workflow (implemented: state is retained in browser memory and processed transiently by the local server; only `127.0.0.1` is contacted; no application persistence).
- PRIV-02 No telemetry by default; if ever added, it must exclude message text, names and model content (proposed rule, [DECISIONS.md](DECISIONS.md) D-17).
- PRIV-03 Any feature that sends content off the device (for example online voice transcription) must say so before use and be opt-in (proposed).

### Performance

- PERF-01 Runs on an 8 GB Mac with other apps open. Recorded once: Gemma 4 E2B ≈ 1.6 GB loaded, median 2.3–3.6 s per message, 50 messages end to end in 131 s with model + rules ([RESULTS.md](../evaluation/RESULTS.md)). Not re-measured since.
- PERF-02 Rules-only mode responds without a model.

### Cost

- COST-01 Additional out-of-pocket spending stays at ₹0. Only free plans, existing local resources or sponsor credits.
- COST-02 No automatic paid upgrades, top-ups, paid fallbacks or renewals. When a free allowance ends, the optional feature stops or degrades; the local workflow keeps working.

## 10. Acceptance criteria for the next release (proposed, not yet met)

- AC-01 The confirmed final export follows the rules in [TASKS.md COR-01](../TASKS.md#core-correctness): accepted records only, corrections replayed, pending or unresolved items marked rather than silently included or dropped; with the set A reference claims accepted it reproduces `expected_sheet` in `fixtures/reference.json`.
- AC-01b A suggestion with invented day/time words never reaches the confirmed export or the sheet without a reviewer's decision (COR-10).
- AC-02 A forced invalid model reply shows a visible warning on that message (COR-03).
- AC-03 Reloading the page after saving a session restores every review decision (COR-04).
- AC-04 On a fresh held-out set written before any further change, Gemma + rules misses no more cancellations on the final sheet than on set B at first scoring (0/5), and silent errors are reported (EVAL-01 freeze, EVAL-07 score once).
- AC-05 A timing study following the revised [MEASUREMENT.md](../evaluation/MEASUREMENT.md) (comparable workloads, balanced order, equivalent final outputs, corrected scorer, more than one participant) is run before any claim of time saved (EVAL-02).

## 11. Success metrics

| Metric | How measured | Current value |
|---|---|---|
| Active review time vs manual typing | revised [MEASUREMENT.md](../evaluation/MEASUREMENT.md) protocol; target ≤ 70% at slot agreement within 2 points, across participants | **Not measured**; not measurable until COR-01 and EVAL-06 are done |
| Cancellations still on the final sheet | `missed_withdrawals` in `evaluation/run.py` on a held-out set | see [PROGRESS.md](../PROGRESS.md#evaluation-status) |
| Silent errors (wrong with no warning) | `silent_errors` in `evaluation/run.py` | see PROGRESS.md |
| Final-sheet slot agreement | `slot_agreement` | see PROGRESS.md |
| Coordinator willingness to use it | interviews or a pilot with consented, anonymised messages | **Not measured** |

The click-count "effort proxy" is not a time measurement and must not be reported as time saved.

## 12. Risks and validation experiments

| Risk | Experiment |
|---|---|
| Nobody wants this; a signup form is enough | Talk to 3–5 coordinators; show the fictional demo and a form; ask which they would use (EVAL-03) |
| Review takes as long as typing | Timing study (EVAL-02) |
| Silent missed cancellations | Fresh held-out set with varied cancellation wording, frozen first and scored once (EVAL-01, EVAL-07) |
| Evaluation is circular (same author wrote fixtures, rules and references) | Have someone else write or check a message set and reference (EVAL-04) |
| Real chats differ from fixtures | One consented, anonymised real week (EVAL-03) |
| A free tier expires or starts charging | All integrations optional and off by default; no stored payment method (D-18) |
