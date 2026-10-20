"""The confirmed final sheet: accepted records only, with anything unsettled marked. No model calls.

A message counts as reviewed only when the reviewer marks it; finishing extraction or deciding
every suggestion never does. The export is "complete" only when every message is reviewed, nothing
is pending and no blocking issue is open; otherwise it is "provisional". The same file format is
written here and read back strictly by `parse_final_csv`, which the timing-study scorer uses.
"""
from __future__ import annotations

import csv
import io
import re

from .core import N_SLOTS, SLOT, SLOT_END, SLOT_START, _hhmm, _slot_range, build_ledger
from .messages import Message
from .resolve import Calendar

FORMAT = "availability-final v1"
COLUMNS = ["volunteer", "date", "start", "end", "status", "condition", "cell_state", "sources"]
META_KEYS = ("week", "status", "unreviewed", "pending", "blocking_issues")
BLOCKING = ("who", "date", "time", "conflict")
CELL_STATES = ("confirmed", "needs_review")
SUMMARY = ("status", "week", "unreviewed", "pending", "blocking_issues", "needs_review_cells", "unknown_reviewed")


class FinalSheetError(ValueError):
    """A final-sheet CSV that is malformed or contradicts itself."""


FORMULA_START = ("=", "+", "-", "@", "\t", "\r")  # a spreadsheet would run a cell starting with these


def _cell(value) -> str:
    """Every exported cell passes through here: formula-like text gets a leading apostrophe (COR-02)."""
    text = "" if value is None else str(value)
    return "'" + text if text.startswith(FORMULA_START) else text


def _uncell(text: str) -> str:
    """Undo _cell when reading: "'=Eve" is the name "=Eve". A typed value without the apostrophe reads as is."""
    return text[1:] if text[:1] == "'" and text[1:2] in FORMULA_START else text


# ---------------------------------------------------------------- export

def confirmed_export(messages: list[Message], claims: list[dict], roster: list[str], cal: Calendar,
                     reviewed=()) -> dict:
    """Build the confirmed sheet from resolved claims and the reviewer's message marks."""
    ids = {m.id for m in messages}
    marked = set(reviewed) & ids
    unknown = sorted(set(reviewed) - ids)
    unreviewed = [m.id for m in messages if not m.duplicate_of and m.id not in marked]
    week = {d.isoformat() for d in cal.week_dates}
    on_roster = set(roster)

    live = [c for c in claims if c["msg"] in ids]
    accepted = [c for c in live if c.get("review") == "accepted"]
    pending = [c for c in live if c.get("review") == "pending"]
    ledger = build_ledger(messages, accepted, roster, cal)
    blocking = [i for i in ledger["issues"] if i["kind"] in BLOCKING]

    cells: set = set()

    def touch(c: dict):
        people = [c["person"]] if c.get("person_state") == "resolved" else list(c.get("person_candidates") or [])
        days = list(c.get("dates") or []) + list(c.get("date_candidates") or [])
        cells.update((p, d) for p in people if p in on_roster for d in days if d in week)

    by_id = {c["id"]: c for c in live}
    for c in pending:
        touch(c)
    for i in blocking:
        touch(by_id[i["claim"]])
    open_msgs = set(unreviewed)
    for c in live:  # dropped and rejected claims are not evidence of scope; the message itself keeps the file provisional
        if c["msg"] in open_msgs and c.get("review") in ("accepted", "pending"):
            touch(c)

    conds = {c["id"]: c.get("condition") or "" for c in accepted}
    order = {p: i for i, p in enumerate(roster)}
    rows, seen = [], set()
    for person, days in ledger["sheet"].items():
        for d, segs in days.items():
            for s in segs:
                cond = "; ".join(sorted({conds.get(x, "") for x in s["claims"]} - {""})) if s["status"] == "conditional" else ""
                rows.append({"volunteer": person, "date": d, "start": s["start"], "end": s["end"], "status": s["status"],
                             "condition": cond, "cell_state": "needs_review" if (person, d) in cells else "confirmed",
                             "sources": ";".join(s["claims"])})
                seen.add((person, d))
    for person, d in cells - seen:
        rows.append({"volunteer": person, "date": d, "start": "", "end": "", "status": "", "condition": "",
                     "cell_state": "needs_review", "sources": ""})
    rows.sort(key=lambda r: (order.get(r["volunteer"], len(order)), r["date"], r["start"]))

    complete = not unreviewed and not pending and not blocking
    return {
        "status": "complete" if complete else "provisional",
        "week": cal.week_start.isoformat(),
        "unreviewed": unreviewed,
        "pending": len(pending),
        "blocking_issues": len(blocking),
        "needs_review_cells": len(cells),
        "unknown_reviewed": unknown,
        "rows": rows,
    }


def final_csv(export: dict) -> tuple[str, str]:
    """(file name, CSV text). Line 1 is the status line; it is written verbatim, not as escaped cells."""
    meta = (f"# {FORMAT}; week={export['week']}; status={export['status']}; "
            f"unreviewed={' '.join(export['unreviewed'])}; pending={export['pending']}; "
            f"blocking_issues={export['blocking_issues']}")
    buf = io.StringIO()
    buf.write(meta + "\n")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUMNS)
    for r in export["rows"]:
        w.writerow([_cell(r[k]) for k in COLUMNS])
    return f"availability-final-{export['week']}-{export['status']}.csv", buf.getvalue()


# ---------------------------------------------------------------- strict reader

_HHMM = re.compile(r"^(\d{2}):(\d{2})$")


def _minutes(text: str, where: str) -> int:
    m = _HHMM.match(text)
    if not m or int(m[1]) > 23 or int(m[2]) > 59:
        raise FinalSheetError(f"{where}: '{text}' is not a HH:MM time")
    t = int(m[1]) * 60 + int(m[2])
    if t % SLOT:
        raise FinalSheetError(f"{where}: '{text}' is not on a {SLOT}-minute boundary")
    return t


def _interval(start: str, end: str, where: str) -> tuple[int, int]:
    a, b = _minutes(start, where), _minutes(end, where)
    if not SLOT_START <= a < b <= SLOT_END:
        raise FinalSheetError(f"{where}: {start}-{end} must satisfy {_hhmm(SLOT_START)} <= start < end <= {_hhmm(SLOT_END)}")
    return a, b


def _status_line(row: list[str], cal: Calendar) -> dict:
    if not row or not row[0].lstrip().startswith("#") or any(x.strip() for x in row[1:]):
        raise FinalSheetError(f"line 1 must be the status line '# {FORMAT}; week=...; status=...'")
    parts = [p.strip() for p in row[0].lstrip()[1:].split(";")]
    if parts[0] != FORMAT:
        raise FinalSheetError(f"status line must start with '# {FORMAT}', found '{parts[0]}'")
    meta = {}
    for p in filter(None, parts[1:]):
        k, sep, v = p.partition("=")
        if not sep:
            raise FinalSheetError(f"status line item '{p}' is not key=value")
        if k.strip() in meta:
            raise FinalSheetError(f"status line repeats '{k.strip()}'; each item may appear only once")
        meta[k.strip()] = v.strip()
    missing = [k for k in META_KEYS if k not in meta]
    if missing:
        raise FinalSheetError(f"status line is missing {', '.join(missing)}")
    if meta["week"] != cal.week_start.isoformat():
        raise FinalSheetError(f"status line week={meta['week']} does not match the week {cal.week_start.isoformat()}")
    if meta["status"] not in ("complete", "provisional"):
        raise FinalSheetError(f"status must be complete or provisional, not '{meta['status']}'")
    for k in ("pending", "blocking_issues"):
        if not meta[k].isdigit():
            raise FinalSheetError(f"{k} must be a whole number, not '{meta[k]}'")
    return {"week": meta["week"], "status": meta["status"], "unreviewed": meta["unreviewed"].split(),
            "pending": int(meta["pending"]), "blocking_issues": int(meta["blocking_issues"])}


def parse_final_csv(text: str, roster: list[str], cal: Calendar) -> dict:
    """Read a final-sheet CSV straight into final slots, rejecting anything malformed or contradictory.

    Returns {"meta", "slots": {(person, date, slot): status}, "unresolved_cells": [(person, date)], "rows_used"}.
    Slots of needs_review cells are left out of "slots"; the scorer counts them as unresolved.
    """
    reader = csv.reader(io.StringIO(text.lstrip("﻿")))
    meta = header = None
    week = {d.isoformat() for d in cal.week_dates}
    on_roster = set(roster)
    entries = []
    for r in reader:
        if not any(x.strip() for x in r):
            continue
        where = f"line {reader.line_num}"
        if meta is None:
            meta = _status_line(r, cal)
            continue
        if header is None:
            header = [h.strip() for h in r]
            while header and not header[-1]:
                header.pop()
            if sorted(header) != sorted(COLUMNS):
                raise FinalSheetError(f"{where}: columns must be exactly {', '.join(COLUMNS)}")
            idx = {h: i for i, h in enumerate(header)}
            continue
        if any(x.strip() for x in r[len(header):]):
            raise FinalSheetError(f"{where}: values beyond the last column")
        get = lambda k: _uncell((r[idx[k]] if idx[k] < len(r) else "").strip())  # noqa: E731
        person, d, state, status = get("volunteer"), get("date"), get("cell_state"), get("status")
        start, end = get("start"), get("end")
        if person not in on_roster:
            raise FinalSheetError(f"{where}: '{person}' is not on the roster")
        if d not in week:
            raise FinalSheetError(f"{where}: '{d}' is not a date in the week of {cal.week_start.isoformat()}")
        if state not in CELL_STATES:
            raise FinalSheetError(f"{where}: cell_state must be confirmed or needs_review, not '{state}'")
        if state == "confirmed":
            if status not in ("available", "conditional"):
                raise FinalSheetError(f"{where}: a confirmed row needs status available or conditional, not '{status}'")
            span = _interval(start, end, where)
        elif start or end or status:
            if status not in ("available", "conditional"):
                raise FinalSheetError(f"{where}: status must be available or conditional, not '{status}'")
            span = _interval(start, end, where)
        else:
            span = None  # an unresolved cell with nothing else known
        entries.append((person, d, state, status, span, where))
    if meta is None or header is None:
        raise FinalSheetError("missing status line or header row")

    unresolved = {(p, d) for p, d, state, *_ in entries if state == "needs_review"}
    if meta["status"] == "complete":
        problems = []
        if unresolved:
            problems.append(f"{len(unresolved)} needs_review cell(s)")
        if meta["unreviewed"]:
            problems.append(f"unreviewed={' '.join(meta['unreviewed'])}")
        if meta["pending"]:
            problems.append(f"pending={meta['pending']}")
        if meta["blocking_issues"]:
            problems.append(f"blocking_issues={meta['blocking_issues']}")
        if problems:
            raise FinalSheetError(f"status=complete contradicts {'; '.join(problems)}")

    filled: dict = {}
    for person, d, state, status, span, where in entries:
        if span is None:
            continue
        for i in _slot_range(*span):
            prev = filled.get((person, d, i))
            if prev and prev != status:
                raise FinalSheetError(f"{where}: {person} {d} {_hhmm(SLOT_START + i * SLOT)} is both {prev} and {status}")
            filled[(person, d, i)] = status
    slots = {k: v for k, v in filled.items() if (k[0], k[1]) not in unresolved}
    return {"meta": meta, "slots": slots, "unresolved_cells": sorted(unresolved), "rows_used": len(entries)}


def unresolved_slots(cells) -> set:
    """An unresolved person/day covers the whole slot grid (06:00-23:00, N_SLOTS fifteen-minute slots)."""
    return {(p, d, i) for p, d in set(map(tuple, cells)) for i in range(N_SLOTS)}

