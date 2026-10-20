"""Print a comparison table.  python3 -m evaluation.compare [frozen]"""
import json
import sys

from .fixture import ROOT

RESULTS = ROOT / "evaluation" / "results" / (sys.argv[1] if len(sys.argv) > 1 else "")


def row(name, r, split):
    s, L = r[split], r.get("ledger", {})
    e = s["effort_proxy"]
    return (f"| {name} | {split} | {s['correct_units']}/{s['reference_units']} | {s['extraction_errors']} | "
            f"{s['silent_errors']} | {s['flagged_units']} ({s['flagged_but_correct']} fine) | "
            f"{L.get('missed_withdrawals', '-')}/{L.get('withdrawals_total', '-')} | "
            f"{L.get('incorrectly_resolved_conditions', '-')}/{L.get('conditions_total', '-')} | "
            f"{L.get('ambiguities_flagged', '-')}/{L.get('ambiguities_total', '-')} | "
            f"{L.get('slot_agreement', '-')} | {e['ratio_full_review']} |")


def main():
    print("| Extractor | Split | Units right | Errors | Silent errors | Flagged units | Missed cancellations* | "
          "Wrong conditions* | Ambiguities flagged* | Slot agreement* | Effort proxy (full review / manual) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for f in sorted(RESULTS.glob("set*.json")):
        r = json.loads(f.read_text())
        label = r["extractor"] + (f" ({r['model']}, prompt v{r['prompt_version']})" if r.get("model") else "")
        for split in ("dev", "heldout") if r["set"] == "A" else ("heldout",):
            if split in r:
                print(row(f"Set {r['set']}: {label}", r, split))
    print("\n*ledger-level columns are computed over the whole set (all its messages), not per split.")


if __name__ == "__main__":
    main()
