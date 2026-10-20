# Spec: confirmed final-sheet export (COR-01) and final-sheet scorer (EVAL-06)

Status: **proposed, not implemented.** Written 2026-10-20 as the hand-off for whoever implements COR-01 and EVAL-06. Open decisions are listed at the end; the defaults below apply unless the owner changes them.

Related: [TASKS.md](../../TASKS.md#core-correctness), [API.md](../API.md#csv-export), [MEASUREMENT.md](../../evaluation/MEASUREMENT.md), [DECISIONS.md](../DECISIONS.md) D-07, D-08, D-13.

## Why

- The current export is a log of reviewed records. It has no `replaces_earlier`, so it cannot be replayed into the sheet; `evaluation/score_csv.py` replays it wrongly (both ranges for "Tuesday 10-12" then "Tuesday 2-4 instead").
- The in-app `ledger.sheet` includes **pending** suggestions, so it cannot be exported as confirmed either.
- The timing study needs both conditions (manual and assisted) to produce the **same kind of output**, scored by the same code.

## 1. Message review marks

A message counts as reviewed only when the reviewer **explicitly marks it reviewed**. These do **not** count:
- extraction finishing for the message;
- every suggestion in it being accepted or rejected;
- the evidence gate dropping its suggestions.

Rules:
- The browser keeps `state.reviewedMessages` (a set of message ids) and sends it as `reviewed_messages` with each `/api/resolve` and export request.
- A duplicate message (`duplicate_of` set) is reviewed exactly when its original is; it needs no separate mark.
- Re-running **Suggest records** clears the marks along with everything else (until COR-04 adds sessions).
- UI: a "Mark message reviewed" toggle on each message panel; keyboard `M` on the current card's message; a counter "12 of 48 messages reviewed" above the list.

## 2. Confirmed sheet

Computed in Python (new module `ledger/export.py`), from the resolved claims:

1. Take only claims with `review == "accepted"`, including reviewer-added records (`source: "user"`). Pending, rejected and dropped claims are excluded.
2. Run `build_ledger` on those claims. This replays corrections, including `replaces_earlier`, exactly as the app does.
3. The result's `sheet` is the **confirmed sheet**. Conditional segments stay `conditional`, with their condition text; they are never exported as `available`.

## 3. Export status: complete or provisional

The export is **complete** only when all of these hold:
- every non-duplicate message is marked reviewed;
- no claim is `pending`;
- no blocking issue is open in the confirmed ledger. Blocking kinds: `who`, `date`, `time`, `conflict`. `condition` and `outside` do not block, because an open condition is a legitimate final state and an outside-week claim does not touch the week.

Otherwise the export is **provisional**. A provisional export is always allowed, but it is labelled as such (§4).

## 4. Cell states (person × date)

A cell is `needs_review` when any of these applies:
- a **pending** claim with a resolved person and resolved dates touches it. This includes a pending cancellation over an accepted offer: the offer stays in the confirmed rows, and the cell is marked;
- a **blocking issue** names the person, and the date is among its dates or candidates;
- an **unreviewed message** has a claim with a resolved person and dates that touches it.

**When scope cannot be established**, no cell is marked; the whole export is provisional instead, and the message is listed in the status line (§5) until it is explicitly reviewed. This covers:
- an unreviewed message with no suggestions;
- one whose suggestions were all dropped;
- one with an unresolved person or an unreadable day.

A missed cancellation may hide in exactly such a message, so automatic completion never makes the week complete.

All other cells are `confirmed`.

## 5. File format (single contract for both timing conditions)

UTF-8 CSV, file name `availability-final-<week_start>-<complete|provisional>.csv`.

Line 1 is a status line that starts with `#`:

```
# availability-final v1; week=2026-11-09; status=provisional; unreviewed=m03,m07; pending=2; blocking_issues=1
```

Then a header and one row per confirmed segment:

```csv
volunteer,date,start,end,status,condition,cell_state,sources
Ana Example,2026-11-10,14:00,16:00,available,,confirmed,m01.1;m02.1
Ana Example,2026-11-12,09:00,12:00,available,,needs_review,m01.2
Ben Example,2026-11-14,,,,,needs_review,m05.1
```

Column rules:
- **Cells:**
  - A confirmed cell with no availability has no row.
  - A `needs_review` cell with no confirmed segment gets one row with empty `start`, `end` and `status`, so every `needs_review` cell appears at least once.
- **`status`:** `available` or `conditional`. Unavailable time is the absence of a row.
- **`sources`:** the claim ids behind the segment, `;`-separated. Empty for rows typed by hand.
- **Cell escaping:** every cell is written by one escaping function, so COR-02 (formula neutralising) changes a single place.
- **Manual condition:** the timing study's manual typists use a template with the same status line, pre-filled `status=complete`, and the same columns. They may mark cells `needs_review` themselves. The template is new, in `evaluation/final_sheet_template.csv`, and does not change `fixtures/`.

The existing record-log export stays, renamed in the UI to "Export review log (CSV)". The new export becomes "Export final sheet (CSV)".

## 6. Server interface

New route `POST /api/export`.
- **Body:** the `/api/resolve` body plus `reviewed_messages`.
- **Response:** `{"status": "complete"|"provisional", "unreviewed": [...], "pending": n, "blocking_issues": n, "filename": "...", "csv": "<text>"}`.
- **Download:** the browser saves `csv` under `filename`.
- **Validation:** the same as `/api/resolve`. A `reviewed_messages` id that matches no message is ignored and listed in the response.

`/api/resolve` also returns `confirmed: {status, unreviewed, pending, blocking_issues}`, so the page can show the export state continuously.

## 7. Scorer (EVAL-06)

New `evaluation/score_final.py FILE.csv --set A|B [--allow-provisional]`. The timing study uses **only** this scorer, on final-sheet files from both conditions.

**Reading the file:**
- If the status line or required columns are missing → error, non-zero exit.
- If `status=provisional` → refused with a non-zero exit, unless `--allow-provisional` is given. Then the report carries `"provisional": true` and is not comparable with complete files.

**Scoring:**
- Reference: `final_slots(build_ledger(reference_claims(ref)))`, as today.
- File: each `confirmed` row fills its 15-minute slots with its status.
- Every `needs_review` cell's slots are scored as **disagreement**, whatever the reference says. They are also reported separately as `unresolved_cells` and `unresolved_slots`. They are never dropped from the denominator.
- **Report:** `slot_agreement` (over the union of reference and file slots, with `needs_review` slots included), `missed_withdrawals`, `incorrectly_resolved_conditions`, `unresolved_cells`, `unresolved_slots`, `rows_used`, `provisional`.

`evaluation/score_csv.py` stays for record logs, with a docstring note that it does not replay replacements and must not be used for the timing study.

## 8. Tests (invented messages only)

| Test | Expected |
|---|---|
| Accepted "Tuesday 10-12", accepted "Tuesday 2-4 instead" (`replaces_earlier`), both messages reviewed | one row 14:00–16:00 `confirmed`; status complete |
| Accepted offer + **pending** cancellation on the same day | offer row present with `needs_review`; status provisional |
| Accepted conditional offer | row `conditional` with condition text; not blocking |
| Message with zero suggestions, not marked reviewed | status provisional, `unreviewed` lists it, no cell marked |
| Same message marked reviewed, everything else decided | status complete |
| Duplicate of a reviewed message | not listed as unreviewed |
| Ambiguous-date claim accepted unchanged | `date` issue blocks; candidate cells `needs_review` |
| Rejected claim | no effect on rows or status |
| Scorer: complete file generated from set A reference claims, all accepted, all reviewed | `slot_agreement` 1.0, `unresolved_cells` 0 |
| Scorer: provisional file without the flag | non-zero exit |
| Scorer: file with one `needs_review` cell that matches the reference | that cell's slots count as disagreement and as unresolved |
| Scorer: missing status line | non-zero exit |

The existing 21 tests must keep passing. These changes do not touch extraction, so the cached evaluation numbers should not move; re-run them to confirm.

## 9. Files expected to change

- `ledger/export.py` (new)
- `server.py` (route, `confirmed` summary)
- `ui/app.js`, `ui/index.html`, `ui/style.css` (review marks, counter, `M` key, two export buttons)
- `evaluation/score_final.py` (new) and `evaluation/final_sheet_template.csv` (new)
- `tests/`
- docs: API.md, ARCHITECTURE.md §10, README export section, MEASUREMENT.md, PROGRESS.md, TASKS.md

Not to be touched: fixtures, frozen results, cached runs, the prompt.

## 10. Open decisions (defaults in brackets)

1. Should accepting or rejecting every suggestion in a message offer to mark it reviewed in one action? [Yes, as an explicit "Accept all and mark reviewed" button; never automatic.]
2. Blocking issue kinds. [`who`, `date`, `time`, `conflict`.]
3. Should a provisional export be allowed at all? [Yes, always labelled.]
4. Should pending suggestions also be shown differently on the in-app sheet now (UI-05)? [Separate task; not required for COR-01.]
