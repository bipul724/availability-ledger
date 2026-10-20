# Spec: confirmed final-sheet export (COR-01) and final-sheet scorer (EVAL-06)

Status: **implemented 2026-10-20.** Code: `ledger/export.py`, `server.py` (`/api/export` and the `confirmed` summary in `/api/resolve`), `ui/app.js`, `evaluation/score_final.py`, `evaluation/final_sheet_template.csv`. Tests: `tests/test_export.py`.

This file is the canonical description of the file format and the scoring contract. Optional sponsor tools and the proposed public fictional replay must preserve this distinction between provisional display and confirmed export; see [INTEGRATIONS.md](../INTEGRATIONS.md). No hosting, tracing or narration integration is implemented by this spec. Related: [API.md](../API.md#final-sheet-csv), [MEASUREMENT.md](../../evaluation/MEASUREMENT.md), [DECISIONS.md](../DECISIONS.md) D-21.

## Why

- The record-log export has no `replaces_earlier`, so it cannot be replayed into the sheet. `evaluation/score_csv.py` replays it wrongly: "Tuesday 10-12" then "Tuesday 2-4 instead" scores as both ranges.
- The in-app `ledger.sheet` includes **pending** suggestions, so it cannot be exported as confirmed either.
- The timing study needs both conditions (manual and assisted) to produce the **same kind of output**, scored by the same code.

## Settled decisions (owner, 2026-10-20)

1. **No inferred review.** A message counts as reviewed only when the reviewer explicitly marks it. None of these count: extraction finishing, every suggestion being decided, or the evidence gate dropping suggestions.
2. **"Accept all and mark reviewed"** is an explicit action. It is offered only when every undecided suggestion in the message (pending or dropped) is eligible: pending, only informational flags, person and day resolved, and a readable time. A message with any flagged, dropped or unresolved suggestion must be decided suggestion by suggestion, then marked reviewed.
3. **Blocking issue kinds:** `who`, `date`, `time`, `conflict`. `condition` and `outside` do not block.
4. **Provisional exports are allowed**, always labelled in the status line and the file name.
5. **UI-05** (showing pending suggestions differently on the in-app sheet and chart) is a separate task.

"Informational flags" are the same set as for "Accept all suggestions without warnings": `time_unstated`, `conditional`, `edited`, `replace_cue`, `similar_name`, `time_from_same_message`.

## 1. Message review marks

- The browser keeps `state.reviewed` (message ids marked by the reviewer) and sends it as `reviewed_messages` to `/api/resolve` and `/api/export`.
- **Controls:**
  - Each message panel has a "Mark message reviewed" toggle, shown as "✓ Reviewed" once marked.
  - "Accept all and mark reviewed" appears when settled decision 2 allows it.
  - Keyboard `M` toggles the mark on the current card's message.
  - The line above the list shows "N of M messages marked reviewed. Final sheet export: complete | provisional (reasons)."
- **Duplicates:** a duplicate message is covered by its original's mark and is never listed as unreviewed.
- **Reset:** a **successful** run of **Suggest records** commits the new week, timezone, messages and roster together and clears claims and marks. A run that fails validation (week not a Monday), fails to parse, or finds no dated messages changes nothing: the previous session, its marks and its export stay exactly as they were (fixed 2026-10-20; browser check `tests/browser/session_rerun.mjs`).
- Statistics count marks (`marks`) and bulk actions (`bulk`).
- **Limitation:** J/K move between suggestion cards, so a message with no suggestions can only be marked with its button (Tab or mouse).

## 2. Confirmed sheet

1. Take only claims with `review == "accepted"`, which includes reviewer-added records. Pending, rejected and dropped claims are excluded.
2. Run the ordinary `build_ledger` on them. This replays corrections, including `replaces_earlier`, exactly as the app does.
3. Conditional segments stay `conditional`, with their condition text; they are never exported as `available`.

## 3. Export status

The export is **complete** only when all of these hold:
- every non-duplicate message is marked reviewed;
- no claim is pending;
- no blocking issue is open in the confirmed ledger.

Otherwise it is **provisional**.

## 4. Cell states (person × date)

A cell is `needs_review` when it is touched by any of the following:
- a **pending** claim. A pending cancellation over an accepted offer keeps the offer in the rows and marks the cell;
- the claim behind a **blocking issue**;
- an **accepted or pending** claim of an **unreviewed message**. Dropped and rejected claims never create or mark cells (fixed 2026-10-20).

"Touches" means the claim's resolved person (or its candidate people, if unresolved) on its resolved dates (or its candidate dates inside the week).

**When scope cannot be established**, no cell is marked, the whole export stays provisional, and the message is listed as unreviewed until it is explicitly reviewed. This covers:
- an unreviewed message with no suggestions;
- one whose suggestions were all dropped or rejected;
- one whose suggestions have no resolvable person or day.

All other cells are `confirmed`.

## 5. File format, `availability-final v1`

UTF-8 CSV named `availability-final-<week_start>-<complete|provisional>.csv`.

Line 1 is a status line. Its items are separated by `;`, and message ids are separated by **spaces**, so that a spreadsheet keeps the whole line in one cell:

```
# availability-final v1; week=2026-11-09; status=provisional; unreviewed=m03 m07; pending=2; blocking_issues=1
volunteer,date,start,end,status,condition,cell_state,sources
Ana Example,2026-11-10,14:00,16:00,available,,confirmed,m01.1;m02.1
Ana Example,2026-11-12,09:00,12:00,available,,needs_review,m01.2
Ben Example,2026-11-14,,,,,needs_review,
```

- **Rows:** one row per confirmed segment, sorted by roster order, date and start.
  - A cell with no availability has no row.
  - A `needs_review` cell with no confirmed segment gets one row with empty times and status, so every unresolved cell appears.
- **`status`:** `available` or `conditional`; unavailable time is simply absent.
- **`sources`:** the claim ids behind the segment, `;`-separated. Empty in hand-typed files.
- **CSV quoting:** every data cell goes through `ledger.export._cell`, the intended change point for COR-02, before `csv.writer` quotes it as needed. `_cell` currently only converts values to strings: spreadsheet-formula protection remains unimplemented. The status line is written verbatim. The browser-built review log has its own writer and also needs protection.
- **Manual condition:** typists use `evaluation/final_sheet_template.csv`. They replace `YYYY-MM-DD` with the set's week and may mark uncertain cells `needs_review`, which then requires `status=provisional`.

The record log stays available as **Export review log (CSV)** (`availability-log-<week>.csv`).

## 6. Server interface

| Route | Body | Response |
|---|---|---|
| `POST /api/resolve` | as before, plus optional `reviewed_messages` (list of ids) | as before, plus `confirmed`: `{status, week, unreviewed, pending, blocking_issues, needs_review_cells, unknown_reviewed}` |
| `POST /api/export` | same as `/api/resolve` | the `confirmed` fields plus `rows`, `filename`, `csv` |

- Clients send `reviewed_messages` as a list of strings. Current server behavior treats omission or a JSON value falsy under Python (`null`, `false`, `0`, `""`, `[]`, `{}`) as no marks; a truthy non-list value or a list containing a non-string → 400. This follows `body.get("reviewed_messages") or []`; it never infers a review mark.
- Ids that match no message are ignored and returned in `unknown_reviewed`.

## 7. Strict reader and scorer

`ledger.export.parse_final_csv(text, roster, cal)` reads a file **directly into final slots**, without going through claims or `build_ledger`. It raises `FinalSheetError` for any of the following.

**Status line and header:**
- The status line is missing, or doesn't start with `# availability-final v1`.
- An item isn't `key=value`, or a key appears more than once (even with the same value). A repeated key is rejected before any value is used, so it cannot turn a provisional file into a complete one, and `--allow-provisional` does not override it.
- `week`, `status`, `unreviewed`, `pending` or `blocking_issues` is missing.
- `week` differs from the set's week.
- `status` is not `complete` or `provisional`.
- The counts are not whole numbers.
- The header does not contain exactly the eight column names above, each once. Column order may differ; values are mapped by name.

Tolerated: a BOM, blank rows, and empty trailing cells that spreadsheets add. Unknown status-line keys are currently ignored after duplicate-key validation; the five required keys still have to be present.

**Rows:**
- A volunteer is not on the roster.
- A date is outside the week.
- A `cell_state` other than `confirmed` or `needs_review`.
- A confirmed row without status `available` or `conditional`, or without a valid interval.
- Times that are not `HH:MM`, not on a 15-minute boundary, or outside `06:00 ≤ start < end ≤ 23:00`.
- Values beyond the last column.

**Contradictions:**
- Overlapping rows for the same person and day with **different** statuses. Same-status overlaps are merged.
- `status=complete` together with any `needs_review` row, a non-empty `unreviewed`, `pending > 0` or `blocking_issues > 0`.

**Scoring** (`evaluation/score_final.py FILE.csv --set A|B [--allow-provisional]`):
- **Exit codes:** a malformed file → exit 2 with the reason. A provisional file → exit 2 unless `--allow-provisional` is given; the report then carries `"provisional": true` and is not comparable with complete files.
- **Unresolved cells:** an unresolved person/day covers the whole grid, 06:00–23:00, which is **68 fifteen-minute slots**. Cells are de-duplicated, however many rows they have. Every unresolved slot is in the denominator and counts as **disagreement**, even where the file's rows happen to match the reference.
- **`slot_agreement`:** agreeing slots divided by the union of reference slots, file slots and unresolved slots.
- **Final-state errors.** These measure the final sheet, not which message a reader missed:
  - `withdrawal_final_state_errors`: a reference withdrawal whose interval still shows availability, or whose cell is unresolved. The unresolved part is reported separately.
  - `condition_final_state_errors`: a reference condition whose final state is wrong anywhere in its interval: treated as firm, offer lost, offer partly lost, resolution missed, availability lost, availability partly lost, decline missed; or unresolved. Every slot is checked, and each reference condition counts at most once. The unresolved part is reported separately.
- **Also reported:** `slots_compared`, `reference_slots`, `unresolved_cells`, `unresolved_slots`, `rows_used`, and the error lists.

`evaluation/score_csv.py` remains for record logs only and is documented as unfit for timing.

**What the scorer does not establish:** it compares availability/conditional final-slot states against the fictional reference. It does not assess the correctness of condition prose, source ids, actual human review, extraction provenance, user usefulness or time saved. Passing the parser and a perfect synthetic score are not independent real-world validation. The older `evaluation/run.py` ledger metric still misses partial condition loss (EVAL-09); only `score_final.py` has the every-slot fix described above. Frozen historical results must stay unchanged.

A future public replay may demonstrate review and final export using labelled fictional saved outputs; its results are separate from fresh model runs, held-out evaluation, private pilot data and the timed conditions in [MEASUREMENT.md](../../evaluation/MEASUREMENT.md).

## 8. Verification (2026-10-20)

- 28 tests in `tests/test_export.py` (49 in total, all passing), including 8 added on 2026-10-20 for unreviewed scope (dropped-only, rejected-only, mixed), partial condition loss (available and conditional) and duplicate status-line keys (parser, scorer, CLI). Before those fixes, 7 of the 8 failed; the eighth guards the unchanged condition outcomes. The original four deliberate code breakages in a scratch copy were each caught by the intended test:
  - accepting a contradictory `complete` file;
  - counting unresolved slots as agreement;
  - ignoring unreviewed messages' claims;
  - allowing contradictory overlaps.
- On fictional set A and set B:
  - A complete file typed from `expected_sheet` scores `slot_agreement` 1.0 with 0 final-state errors.
  - The export built from the reference claims is provisional (3 blocking issues on A, 1 on B), because the references deliberately leave ambiguities unresolved. It is refused without `--allow-provisional`.
- The blank template is rejected until its week is filled in.
- The cached evaluation comparison table is unchanged (0 fresh model calls).
- **Headless Chrome:**
  - The bulk button appeared only on fully eligible messages (40 on the rules-only demo, none on flagged ones).
  - Marking, `M`, the counter, a provisional demo export and a complete export on an invented week all work.
  - The log export still works, with no console errors.
