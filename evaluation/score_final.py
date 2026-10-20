"""Score a final-sheet CSV (the app's "Export final sheet" or a hand-typed one) against the manual reference.

This is the only scorer for the timing study: both conditions produce the same file format
(docs/specs/final-export.md), read strictly into final slots by ledger.export.parse_final_csv.

    python3 -m evaluation.score_final my_final.csv --set A
    python3 -m evaluation.score_final my_final.csv --set A --allow-provisional   # labelled, not comparable

Metrics describe the final state only. "withdrawal_final_state_errors" counts reference withdrawals whose
interval still shows availability (or is unresolved) in the file; it says nothing about which message was
missed. An unresolved (needs_review) person/day covers all slots 06:00-23:00 and every one of them counts
as disagreement.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ledger.core import _mins, _slot_range, build_ledger, final_slots
from ledger.export import FinalSheetError, parse_final_csv, unresolved_slots

from .fixture import load, reference_claims


def score(final: dict, ref_slots: dict, withdrawals: list[dict], conditions: list[dict]) -> dict:
    unresolved = set(map(tuple, final["unresolved_cells"]))
    open_keys = unresolved_slots(unresolved)
    slots = final["slots"]
    keys = set(ref_slots) | set(slots) | open_keys
    agree = sum(1 for k in keys if k not in open_keys and ref_slots.get(k) == slots.get(k))

    def states(person, d, start, end):
        return {slots.get((person, d, i)) for i in _slot_range(_mins(start), _mins(end))}

    w_errors = []
    for w in withdrawals:
        if (w["person"], w["date"]) in unresolved:
            w_errors.append({**w, "error": "unresolved"})
        elif states(w["person"], w["date"], w["start"], w["end"]) & {"available", "conditional"}:
            w_errors.append({**w, "error": "still available"})
    c_errors = []
    for c in conditions:  # one verdict per reference condition, from every slot of its interval
        got, exp = states(c["person"], c["date"], c["start"], c["end"]), c["expected_final"]
        error = None
        if (c["person"], c["date"]) in unresolved:
            error = "unresolved"
        elif exp == "conditional":
            if "available" in got:
                error = "treated as firm"
            elif got == {None}:
                error = "offer lost"
            elif None in got:
                error = "offer partly lost"
        elif exp == "available":
            if "conditional" in got:
                error = "resolution missed"
            elif got == {None}:
                error = "availability lost"
            elif None in got:
                error = "availability partly lost"
        elif exp == "none" and got & {"available", "conditional"}:
            error = "decline missed"
        if error:
            c_errors.append({**c, "error": error})
    return {
        "status": final["meta"]["status"],
        "provisional": final["meta"]["status"] == "provisional",
        "rows_used": final["rows_used"],
        "slot_agreement": round(agree / len(keys), 3) if keys else 1.0,
        "slots_compared": len(keys),
        "reference_slots": len(ref_slots),
        "unresolved_cells": len(unresolved),
        "unresolved_slots": len(open_keys),
        "withdrawal_final_state_errors": len(w_errors),
        "withdrawal_final_state_errors_unresolved": sum(e["error"] == "unresolved" for e in w_errors),
        "withdrawals_total": len(withdrawals),
        "withdrawal_error_list": [f"{e['msg']} {e['person']} {e['date']} {e['start']}-{e['end']}: {e['error']}" for e in w_errors],
        "condition_final_state_errors": len(c_errors),
        "condition_final_state_errors_unresolved": sum(e["error"] == "unresolved" for e in c_errors),
        "conditions_total": len(conditions),
        "condition_error_list": [f"{e['person']} {e['date']} {e['start']}-{e['end']}: {e['error']}" for e in c_errors],
    }


def score_text(text: str, which: str = "A", allow_provisional: bool = False) -> dict:
    """Parse and score one final-sheet CSV; raises FinalSheetError for anything that must not be scored."""
    messages, roster, cal, ref = load(which)
    final = parse_final_csv(text, roster, cal)
    if final["meta"]["status"] == "provisional" and not allow_provisional:
        raise FinalSheetError("status=provisional: pass --allow-provisional to score it anyway (results are not "
                              "comparable with complete files)")
    ref_slots = final_slots(build_ledger(messages, reference_claims(ref), roster, cal), cal)
    return score(final, ref_slots, ref["withdrawals"], ref["conditions"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--set", default="A", choices=["A", "B"])
    ap.add_argument("--allow-provisional", action="store_true", help="score a provisional file, labelled as such")
    args = ap.parse_args()
    try:
        report = score_text(Path(args.csv).read_text(encoding="utf-8-sig"), args.set, args.allow_provisional)
    except FinalSheetError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
