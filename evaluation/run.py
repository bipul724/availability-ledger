"""Run an extractor over the fictional fixture and score it against the manual reference.

    python3 -m evaluation.run --extractor rules
    python3 -m evaluation.run --extractor model --only m02,m05,m08,m13,m20   # small benchmark
    python3 -m evaluation.run --extractor model                              # full run (cached per message)
    python3 -m evaluation.run --extractor hybrid --cache-only --out /tmp/x   # CI: saved outputs only, never Ollama
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
import threading
import time
import urllib.request
from collections import Counter
from pathlib import Path

from ledger import hybrid
from ledger import model as model_mod
from ledger import rules
from ledger.core import _mins, _slot_range, build_ledger, effective_units, final_slots, resolve_all

from .fixture import ROOT, load, reference_claims

RUNS = ROOT / "evaluation" / "runs"
RESULTS = ROOT / "evaluation" / "results"
PROTECTED = [RESULTS / "frozen", RESULTS / "frozen-setC", RESULTS / "tuning", RUNS]  # never written by a run (--out)
# Flags that point a reviewer at the content of a suggestion. "similar_name" is excluded on purpose:
# it marks identity, not the day/time/status, so an error under it still counts as silent.
WARNING_FLAGS = {"who_ambiguous", "who_unknown", "date_ambiguous", "outside_week", "date_unreadable",
                 "time_unreadable", "excerpt_missing", "excerpt_approx", "phrase_not_in_message",
                 "readers_disagree", "one_reader", "added_by_rules", "days_not_in_quote", "days_narrowed_to_quote"}


# ---------------------------------------------------------------- memory

def _memory_sample() -> dict:
    ps = subprocess.run(["ps", "-axo", "rss=,comm="], capture_output=True, text=True).stdout
    rss_kb = sum(int(line.split()[0]) for line in ps.splitlines() if "ollama" in line.lower())
    swap = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout
    used = re.search(r"used = ([\d.]+)M", swap)
    mp = subprocess.run(["memory_pressure", "-Q"], capture_output=True, text=True).stdout
    free = re.search(r"(\d+)%", mp)
    level = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"], capture_output=True, text=True).stdout
    vm = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    swapouts = re.search(r"Swapouts:\s+(\d+)", vm)
    return {"t": time.time(), "ollama_rss_mb": round(rss_kb / 1024), "swap_used_mb": float(used[1]) if used else None,
            "free_pct": int(free[1]) if free else None, "pressure_level": int(level or 0),
            "swapouts": int(swapouts[1]) if swapouts else 0}


class MemorySampler(threading.Thread):
    def __init__(self, every: float = 1.0):
        super().__init__(daemon=True)
        self.every, self.samples, self._stop_evt = every, [], threading.Event()

    def run(self):
        while not self._stop_evt.is_set():
            self.samples.append(_memory_sample())
            self._stop_evt.wait(self.every)

    def stop(self) -> dict:
        self._stop_evt.set()
        self.join()
        s = self.samples or [_memory_sample()]
        levels = Counter(x["pressure_level"] for x in s)
        return {
            "samples": len(s),
            "ollama_rss_peak_mb": max(x["ollama_rss_mb"] for x in s),
            "swap_used_start_mb": s[0]["swap_used_mb"], "swap_used_peak_mb": max(x["swap_used_mb"] or 0 for x in s),
            "free_pct_min": min(x["free_pct"] for x in s if x["free_pct"] is not None),
            "pressure_level_share": {{1: "normal", 2: "warn", 4: "critical"}.get(k, str(k)): round(v / len(s), 2)
                                     for k, v in sorted(levels.items())},
            "swapout_pages_during_run": s[-1]["swapouts"] - s[0]["swapouts"],
        }


def ollama_ps() -> list[dict]:
    try:
        with urllib.request.urlopen(f"{model_mod.OLLAMA}/api/ps", timeout=2) as r:
            return [{"name": m["name"], "size_mb": round(m["size"] / 2**20), "size_vram_mb": round(m.get("size_vram", 0) / 2**20),
                     "context_length": m.get("context_length")} for m in json.loads(r.read()).get("models", [])]
    except OSError:
        return []


# ---------------------------------------------------------------- extraction

def _shown(path: Path):
    return path.relative_to(ROOT) if ROOT in path.parents else path


class CacheMissError(RuntimeError):
    """--cache-only and a model output is not saved: fail instead of calling the model (INT-11)."""


def run_extractor(kind, messages, roster, cal, model_name, only=None, refresh=False, set_name="A", cache_only=False):
    if kind == "hybrid":
        model_raw, stats = run_extractor("model", messages, roster, cal, model_name, only, refresh, set_name, cache_only)
        rules_raw, _ = run_extractor("rules", messages, roster, cal, model_name, only, refresh, set_name)
        return hybrid.merge([m for m in messages if not only or m.id in only], model_raw, rules_raw, roster, cal), stats
    week = f"Monday {cal.week_start:%d %B} to Sunday {cal.week_end:%d %B %Y}"
    tag = re.sub(r"[^a-z0-9.]+", "_", model_name.lower()) + f"_prompt{model_mod.PROMPT_VERSION}" + \
        ("" if set_name == "A" else f"_set{set_name}")
    raw, stats = [], {}
    for msg in messages:
        if only and msg.id not in only:
            continue
        if msg.duplicate_of:
            continue  # repeats of an earlier message are not read again (core.build_ledger records them)
        if kind == "rules":
            said, st = rules.extract(msg, roster), {}
        else:
            cache = RUNS / tag / f"{msg.id}.json"
            if cache.exists() and not refresh:
                data = json.loads(cache.read_text())
                said, st = data["claims"], {**data["stats"], "cached": True}
            elif cache_only:
                raise CacheMissError(f"no saved model output for message {msg.id} (set {set_name}): "
                                     f"{_shown(cache)} is missing and --cache-only forbids a model call")
            else:
                said, st = model_mod.extract(msg, week, model_name)
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps({"claims": said, "stats": st}, indent=1, ensure_ascii=False))
                print(f"  {msg.id} {st['wall_s']:>5.1f}s  claims={len(said)}  {msg.text[:60]}")
        for i, s in enumerate(said, 1):
            raw.append({"id": f"{msg.id}.{i}", "msg": msg.id, "n": i, "source": kind, "review": "pending", "said": s})
        stats[msg.id] = st
    return raw, stats


# ---------------------------------------------------------------- scoring

def _statuses(u: dict) -> set:
    s = {seg[0] for seg in u["open"]} | set(u["unstated"]) | set(u["unreadable"])
    return s | ({"unavailable"} if u["unavailable"] else set())


def _classify(r: dict, p: dict) -> str:
    rs, ps = _statuses(r), _statuses(p)
    if rs == ps:
        return "time_error"
    if "conditional" in rs and "conditional" not in ps and "available" in ps:
        return "condition_treated_as_firm"
    if "available" in rs and "conditional" in ps and "available" not in ps:
        return "false_condition"
    if "unavailable" in rs and "unavailable" not in ps:
        return "missed_negation"
    if "unavailable" in ps and "unavailable" not in rs:
        return "false_negation"
    return "status_error"


def _prior_open(ref_claims, messages) -> dict:
    """For each reference unit: did the person already have open availability that day?"""
    order = [m.id for m in messages]
    open_days, prior = set(), {}
    for mid in order:
        units = effective_units([c for c in ref_claims if c["msg"] == mid and not c["optional"]])
        for key, u in units.items():
            prior[(mid, key)] = key in open_days
        for key, u in units.items():
            if u["open"] or u["unstated"]:
                open_days.add(key)
            elif u["unavailable"] and not u["open"]:
                open_days.discard(key)
    return prior


def _manual_cost(key, u, had_prior) -> int:
    """Keystroke-level proxy for typing the same record into a spreadsheet by hand."""
    person, d = key
    if person.startswith("?") or d.startswith("?") or d.startswith("outside") or d == "unreadable":
        return 1  # a note to follow up
    if u["open"]:
        if had_prior:
            return 2  # edit an existing row's times or status
        return 6 + any(seg[0] == "conditional" for seg in u["open"])  # new row: person, date, start, end, status (+condition)
    if u["unstated"]:
        return 0 if had_prior else 6
    return 2 if (u["unavailable"] and had_prior) else 0  # cancelling means editing a row


def condition_error(got: set, expected: str) -> str | None:
    """Final-state verdict for one reference condition from the statuses found in every slot of its interval."""
    if expected == "conditional":
        if "available" in got:
            return "treated as firm"
        if got == {None}:
            return "offer lost"
        if None in got:
            return "offer partly lost"
    elif expected == "available":
        if "conditional" in got:
            return "resolution missed"
        if got == {None}:
            return "availability lost"
        if None in got:
            return "availability partly lost"
    elif expected == "none" and got & {"available", "conditional"}:
        return "decline missed"
    return None


def score(messages, roster, cal, ref, raw, ids):
    resolved = resolve_all(messages, raw, roster, cal)
    refc = reference_claims(ref, include_optional=True)
    prior = _prior_open(refc, messages)
    cats = {mid: m["category"] for mid, m in ref["messages"].items()}
    errors, per_msg = [], {}
    manual = assisted = assisted_bulk = silent = correct = total_ref = flagged_units = false_alarms = 0
    # A duplicate is never extracted (D-14), so its reference units are excluded from both sides (D-26, EVAL-10).
    duplicates = {m.id for m in messages if m.duplicate_of}
    dup_ids = [mid for mid in ids if mid in duplicates]
    dup_units = sum(len(effective_units([c for c in refc if c["msg"] == mid and not c["optional"]])) for mid in dup_ids)
    for mid in ids:
        if mid in duplicates:
            continue
        r_units = effective_units([c for c in refc if c["msg"] == mid and not c["optional"]])
        o_units = effective_units([c for c in refc if c["msg"] == mid and c["optional"]])
        pred = [c for c in resolved if c["msg"] == mid and c["review"] not in ("rejected", "dropped")]
        p_units = effective_units(pred)
        warned = {key for c in pred if WARNING_FLAGS & set(c["flags"])
                  for key in effective_units([c]).keys()}
        extras = [k for k in p_units if k not in r_units and k not in o_units]
        flagged_units += sum(1 for k in p_units if k in warned)
        false_alarms += sum(1 for k in p_units if k in warned and r_units.get(k) == p_units[k])
        msg_errors = []
        for key, r in r_units.items():
            total_ref += 1
            cost_manual = _manual_cost(key, r, prior.get((mid, key), False))
            manual += cost_manual
            p = p_units.get(key)
            if p is not None and p == r:
                correct += 1
                assisted += 1
                continue
            guessed = []
            if p is not None:
                kind = _classify(r, p)
                cost = 3  # open the suggestion, change up to two fields
            else:
                person, d = key
                guessed = [k for k in extras if k[0] == person and d.startswith("?") and k[1] in d] or \
                          [k for k in extras if person.startswith("?") and k[0] in person and k[1] == d] or \
                          [k for k in extras if d.startswith("outside") and k[0] == person]
                if guessed:
                    kind = "ambiguity_guessed" if not d.startswith("outside") else "outside_week_applied"
                    for k in guessed:
                        extras.remove(k)
                    cost = len(guessed) + 1
                else:
                    kind = "missed_" + ("cancellation" if r["unavailable"] and prior.get((mid, key)) else
                                        "condition" if "conditional" in _statuses(r) else
                                        "ambiguity_flag" if (key[0].startswith("?") or key[1].startswith(("?", "outside"))) else
                                        "unavailability" if r["unavailable"] and not r["open"] else "availability")
                    cost = cost_manual + (1 if cost_manual else 0)
            assisted += cost
            is_silent = not any(k in warned for k in guessed) if guessed else (p is None or key not in warned)
            silent += is_silent
            msg_errors.append({"msg": mid, "key": list(key), "kind": kind, "silent": is_silent,
                               "expected": r, "got": p})
        for key in extras:
            p = p_units[key]
            kind = "claim_from_unrelated_message" if "unrelated" in cats[mid] else "extra_" + "/".join(sorted(_statuses(p)))
            assisted += 1
            silent += key not in warned
            msg_errors.append({"msg": mid, "key": list(key), "kind": kind, "silent": key not in warned, "expected": None, "got": p})
        errors += msg_errors
        per_msg[mid] = len(msg_errors)
    assisted_bulk = 1 + sum(1 + 2 for e in errors if not e["silent"])  # one bulk accept, then fix flagged errors only
    return resolved, {
        "messages": len(ids), "duplicate_messages_excluded": len(dup_ids), "duplicate_units_excluded": dup_units,
        "reference_units": total_ref, "correct_units": correct,
        "extraction_errors": len(errors), "error_kinds": dict(Counter(e["kind"] for e in errors)),
        "silent_errors": silent,
        "flagged_units": flagged_units, "flagged_but_correct": false_alarms,
        "effort_proxy": {"manual_actions": manual, "assisted_actions_full_review": assisted,
                         "ratio_full_review": round(assisted / manual, 2) if manual else None,
                         "assisted_actions_bulk_accept": assisted_bulk,
                         "ratio_bulk_accept": round(assisted_bulk / manual, 2) if manual else None},
        "errors": errors, "errors_per_message": per_msg,
    }


def ledger_checks(messages, roster, cal, ref, resolved):
    ref_ledger = build_ledger(messages, reference_claims(ref), roster, cal)
    pred_ledger = build_ledger(messages, resolved, roster, cal)
    rs, ps = final_slots(ref_ledger, cal), final_slots(pred_ledger, cal)
    keys = set(rs) | set(ps)
    agree = sum(rs.get(k) == ps.get(k) for k in keys)

    def interval_states(slots, person, d, start, end):
        return {slots.get((person, d, i)) for i in _slot_range(_mins(start), _mins(end))}

    missed_withdrawals = [w for w in ref["withdrawals"]
                          if interval_states(ps, w["person"], w["date"], w["start"], w["end"]) & {"available", "conditional"}]
    cond_errors = []  # every slot of the interval counts (EVAL-09); one verdict per reference condition
    for c in ref["conditions"]:
        error = condition_error(interval_states(ps, c["person"], c["date"], c["start"], c["end"]), c["expected_final"])
        if error:
            cond_errors.append({**c, "error": error})
    issues = {(i["msg"], i["kind"]) for i in pred_ledger["issues"]}
    amb = {a["msg"]: ((a["msg"], {"person": "who", "date": "date", "outside_week": "outside"}[a["kind"]]) in issues)
           for a in ref["ambiguities"]}
    count_diff = []
    for rd, pd in zip(ref_ledger["counts"]["days"], pred_ledger["counts"]["days"]):
        count_diff += [abs(a - b) for a, b in zip(rd["available"], pd["available"])]
    return pred_ledger, {
        "slot_agreement": round(agree / len(keys), 3) if keys else 1.0,
        "slots_compared": len(keys),
        "missed_withdrawals": len(missed_withdrawals), "withdrawals_total": len(ref["withdrawals"]),
        "missed_withdrawal_list": [f"{w['msg']} {w['person']} {w['date']} {w['start']}-{w['end']}" for w in missed_withdrawals],
        "incorrectly_resolved_conditions": len(cond_errors), "conditions_total": len(ref["conditions"]),
        "condition_error_list": [f"{c['person']} {c['date']} {c['start']}-{c['end']}: {c['error']}" for c in cond_errors],
        "ambiguities_flagged": sum(amb.values()), "ambiguities_total": len(amb), "ambiguity_detail": amb,
        "count_chart_abs_error_sum": sum(count_diff), "count_chart_max_error": max(count_diff) if count_diff else 0,
        "count_chart_slots_wrong": sum(1 for x in count_diff if x),
    }


def form_analysis(ref) -> dict:
    """Which final records fit a reusable checkbox form (day x morning/afternoon/evening)?"""
    shifts = {("09:00", "12:00"), ("13:00", "17:00"), ("17:00", "20:00"), ("13:00", "20:00"), ("09:00", "20:00")}
    fit = misfit = 0
    reasons = Counter()
    for person, days in ref["expected_sheet"].items():
        for d, segs in days.items():
            for start, end, status in segs:
                if status == "conditional":
                    misfit += 1
                    reasons["conditional offer needs free text"] += 1
                elif (start, end) in shifts:
                    fit += 1
                else:
                    misfit += 1
                    reasons["partial hours do not match a shift box"] += 1
    return {"final_records": fit + misfit, "fit_checkbox_form": fit, "need_free_text": misfit, "reasons": dict(reasons)}


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extractor", choices=["rules", "model", "hybrid"], default="rules")
    ap.add_argument("--model", default=model_mod.DEFAULT_MODEL)
    ap.add_argument("--set", default="A", choices=["A", "B", "C"], help="A = original 50 (dev + held-out), B = fresh held-out, C = independent, scored once")
    ap.add_argument("--only", default="", help="comma-separated message ids (small benchmark)")
    ap.add_argument("--refresh", action="store_true", help="ignore cached model outputs")
    ap.add_argument("--label", default="", help="suffix for the results file")
    ap.add_argument("--cache-only", action="store_true",
                    help="use saved model outputs only; a missing one is an error, Ollama is never called (CI)")
    ap.add_argument("--out", default="", help="directory for the results file (default evaluation/results)")
    args = ap.parse_args()
    if args.cache_only and args.refresh:
        ap.error("--cache-only and --refresh contradict each other")
    out_dir = Path(args.out).resolve() if args.out else RESULTS
    if any(out_dir == p or p in out_dir.parents for p in PROTECTED):
        ap.error(f"--out {args.out} is inside a protected folder")

    messages, roster, cal, ref = load(args.set)
    only = set(filter(None, args.only.split(","))) or None
    uses_model = args.extractor != "rules"
    # Memory sampling uses macOS tools and measures Ollama; with --cache-only there is no model work to measure.
    sampler = MemorySampler() if uses_model and not args.cache_only else None
    if sampler:
        sampler.start()
    t0 = time.time()
    try:
        raw, stats = run_extractor(args.extractor, messages, roster, cal, args.model, only, args.refresh, args.set,
                                   args.cache_only)
    except CacheMissError as e:
        if sampler:
            sampler.stop()
        sys.exit(f"error: {e}")
    wall = time.time() - t0
    loaded = ollama_ps() if sampler else []
    memory = sampler.stop() if sampler else None

    heldout = set(ref["split"]["heldout"])
    all_ids = [m.id for m in messages if not only or m.id in only]
    report = {"set": args.set, "extractor": args.extractor, "model": args.model if args.extractor != "rules" else None,
              "prompt_version": model_mod.PROMPT_VERSION if args.extractor != "rules" else None,
              "messages_run": len(all_ids), "wall_s": round(wall, 1)}
    if uses_model:
        fresh = [s for s in stats.values() if not s.get("cached")]
        report["speed"] = {
            "fresh_calls": len(fresh),
            "median_s_per_message": statistics.median([s["wall_s"] for s in fresh]) if fresh else None,
            "max_s_per_message": max([s["wall_s"] for s in fresh], default=None),
            "output_tokens_per_s": round(sum(s["output_tokens"] or 0 for s in fresh) / max(1e-9, sum(s["output_s"] for s in fresh)), 1) if fresh else None,
            "prompt_tokens_per_s": round(sum(s["prompt_tokens"] or 0 for s in fresh) / max(1e-9, sum(s["prompt_s"] for s in fresh)), 1) if fresh else None,
            "json_parse_failures": sum(1 for s in stats.values() if not s.get("json_ok", True)),
            "first_load_s": max((s["load_s"] for s in fresh), default=None),
        }
    if sampler:
        report["memory"] = {**memory, "ollama_ps": loaded}
    for name, ids in (("dev", [i for i in all_ids if i not in heldout]), ("heldout", [i for i in all_ids if i in heldout]),
                      ("all", all_ids)):
        if ids:
            _, s = score(messages, roster, cal, ref, raw, ids)
            report[name] = s
    if not only:
        resolved, _ = score(messages, roster, cal, ref, raw, all_ids)
        _, report["ledger"] = ledger_checks(messages, roster, cal, ref, resolved)
        report["form_analysis"] = form_analysis(ref)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"set{args.set}_{args.extractor}" + ("" if args.extractor == "rules" else
                                                 "_" + re.sub(r"[^a-z0-9.]+", "_", args.model.lower()) + f"_prompt{model_mod.PROMPT_VERSION}")
    out = out_dir / f"{name}{'_' + args.label if args.label else ('_subset' if only else '')}.json"
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=list))
    brief = {k: v for k, v in report.items() if k not in ("dev", "heldout", "all")}
    for split in ("dev", "heldout", "all"):
        if split in report:
            brief[split] = {k: v for k, v in report[split].items() if k not in ("errors", "errors_per_message")}
    print(json.dumps(brief, indent=1, ensure_ascii=False, default=list))
    print(f"\nwrote {_shown(out)}")


if __name__ == "__main__":
    main()
