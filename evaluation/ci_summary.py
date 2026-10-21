"""Markdown score table for a cache-only re-score, checked against the committed results (INT-11).

    python3 -m evaluation.ci_summary DIR [--against evaluation/results] >> "$GITHUB_STEP_SUMMARY"

Exits 1 if a re-scored file made a fresh model call, has no committed counterpart, or differs from it in any
scoring field. Run time, speed and memory are measurements of the machine, not scores, so they are not compared.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .fixture import ROOT

RUNTIME = {"wall_s", "speed", "memory"}
READERS = {"rules": "Rules only", "model": "Gemma 4 E2B only", "hybrid": "Gemma 4 E2B + rules"}


def scores(report: dict) -> dict:
    return {k: v for k, v in report.items() if k not in RUNTIME}


def row(r: dict, verdict: str) -> str:
    u, L = r["heldout"], r["ledger"]
    fresh = r.get("speed", {}).get("fresh_calls", 0)
    reader = READERS[r["extractor"]] if r["model"] in (None, "gemma4:e2b-it-qat") else f"{r['extractor']} ({r['model']})"
    return (f"| {r['set']} | {reader} | {u['correct_units']}/{u['reference_units']} | "
            f"{L['missed_withdrawals']}/{L['withdrawals_total']} | {L['slot_agreement']} | {fresh} | {verdict} |")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="folder of re-scored set*.json files")
    ap.add_argument("--against", default=str(ROOT / "evaluation" / "results"), help="committed results folder")
    args = ap.parse_args(argv)
    files = sorted(Path(args.dir).glob("set*.json"))
    order = {"rules": 0, "model": 1, "hybrid": 2}
    reports = sorted(((f, json.loads(f.read_text())) for f in files), key=lambda x: (x[1]["set"], order[x[1]["extractor"]]))
    lines, failures = [], []
    for f, r in reports:
        committed = Path(args.against) / f.name
        if r.get("speed", {}).get("fresh_calls", 0):
            failures.append(f"{f.name}: {r['speed']['fresh_calls']} fresh model calls")
        if not committed.exists():
            verdict = "no committed file"
            failures.append(f"{f.name}: no committed file in {args.against}")
        elif scores(json.loads(committed.read_text())) != scores(r):
            verdict = "**differs**"
            failures.append(f"{f.name}: scores differ from the committed file")
        else:
            verdict = "yes"
        lines.append(row(r, verdict))
    print("### Cache-only re-score (saved Gemma outputs, no model calls)\n")
    print("| Set | Reader | Units right (held-out messages) | Missed cancellations (final sheet) | Slot agreement (final sheet) "
          "| Fresh model calls | Matches committed results |")
    print("|---|---|---|---|---|---|---|")
    print("\n".join(lines))
    print("\nUnits right counts held-out messages only (set A: 20 of 50; sets B and C: all). Missed cancellations and slot "
          "agreement are on the provisional final sheet built from every message in the set. All suggestions are "
          "unreviewed. Fictional messages; set C's independent first score is frozen in `evaluation/results/frozen-setC/` "
          "and these are post-hoc. Run time and memory are not compared.")
    if not reports:
        failures.append(f"no set*.json files in {args.dir}")
    if failures:
        print("\n**Failed:**\n" + "\n".join(f"- {x}" for x in failures))
        return 1
    print(f"\nAll {len(reports)} re-scored files match the committed results.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
