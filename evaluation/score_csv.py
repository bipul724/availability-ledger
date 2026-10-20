"""Score a record log (the app's "Export review log (CSV)") against the manual reference.

Not for the timing study. Every row is replayed with replaces_earlier=False, so "Tuesday 10-12" followed by
"Tuesday 2-4 instead" scores as both ranges. The timing study scores final-sheet files with
evaluation/score_final.py (docs/specs/final-export.md).

    python3 -m evaluation.score_csv my_sheet.csv --set A
"""
from __future__ import annotations

import argparse
import csv
import json

from ledger.core import build_ledger, final_slots

from .fixture import load, reference_claims
from .run import ledger_checks


def rows_to_claims(path: str, messages) -> list[dict]:
    order = {m.id: i for i, m in enumerate(messages)}
    claims = []
    with open(path, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f), 1):
            if not row.get("volunteer") or not row.get("date"):
                continue  # unresolved notes do not change the sheet
            start, end = (row.get("start") or "").strip(), (row.get("end") or "").strip()
            msg = row.get("message_id") or (messages[-1].id if messages else "m01")
            claims.append({
                "id": f"csv{i}", "msg": msg if msg in order else messages[-1].id, "n": i, "review": "accepted",
                "person": row["volunteer"].strip(), "person_state": "resolved", "person_candidates": [],
                "dates": [row["date"].strip()], "date_state": "resolved", "date_candidates": [],
                "start": start or None, "end": end or None, "time_state": "explicit" if start and end else "unstated",
                "status": (row.get("status") or "available").strip(), "condition": row.get("condition", ""),
                "replaces_earlier": False, "flags": [],
            })
    return claims


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--set", default="A", choices=["A", "B"])
    args = ap.parse_args()
    messages, roster, cal, ref = load(args.set)
    claims = rows_to_claims(args.csv, messages)
    _, checks = ledger_checks(messages, roster, cal, ref, claims)
    ref_slots = final_slots(build_ledger(messages, reference_claims(ref), roster, cal), cal)
    print(json.dumps({"rows_used": len(claims), "reference_slots": len(ref_slots),
                      **{k: v for k, v in checks.items() if k != "ambiguity_detail"}}, indent=1))


if __name__ == "__main__":
    main()
