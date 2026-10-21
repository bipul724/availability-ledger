"""Load the fictional fixture and turn the manual reference into claims."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from ledger.messages import parse_messages, parse_roster
from ledger.resolve import Calendar

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "fixtures"


SETS = {
    "A": ("riverside_week.txt", "roster.txt", "reference.json"),
    "B": ("setB_toolshed.txt", "setB_roster.txt", "setB_reference.json"),
    "C": ("setC_messages.txt", "setC_roster.txt", "setC_reference.json"),
}


def load(which: str = "A"):
    msgs_file, roster_file, ref_file = SETS[which]
    ref = json.loads((FIXTURES / ref_file).read_text())
    messages = parse_messages((FIXTURES / msgs_file).read_text())
    roster = parse_roster((FIXTURES / roster_file).read_text())
    cal = Calendar(date.fromisoformat(ref["week_start"]), ref["timezone"])
    return messages, roster, cal, ref


def reference_claims(ref: dict, include_optional: bool = False) -> list[dict]:
    """Reference claims in the same resolved shape that core.resolve_claim produces."""
    out = []
    for mid, m in ref["messages"].items():
        for i, rc in enumerate(m["claims"], 1):
            if rc.get("optional") and not include_optional:
                continue
            out.append({
                "id": f"{mid}.r{i}", "msg": mid, "n": i, "source": "reference", "review": "accepted",
                "person": rc["person"], "person_state": "resolved" if rc["person"] else "ambiguous",
                "person_candidates": rc.get("person_candidates", []),
                "dates": rc["dates"] or [], "date_state": rc.get("date_state", "resolved"),
                "date_candidates": rc.get("date_candidates", []), "date_note": rc.get("note", ""),
                "start": rc["start"], "end": rc["end"],
                "time_state": "explicit" if rc["start"] else "unstated",
                "status": rc["status"], "condition": "reference" if rc["status"] == "conditional" else "",
                "replaces_earlier": rc.get("replaces_earlier") is True,
                "optional": rc.get("optional", False), "flags": [],
            })
    return out
