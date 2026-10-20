"""Two readers: the model proposes, the rules baseline cross-checks.

Decided after held-out set A showed the model dropping cancellations, and frozen
before set B was scored:
  1. Explicit replacement words ("instead", "correction", "actually", "update",
     "change of plans", "now") mark the model's positive claims as replacing earlier answers.
  2. A day the rules read as *unavailable* but the model did not mention at all is
     added from the rules, flagged, so a cancellation cannot vanish silently.
  3. Where both readers mention a day but disagree, the model's claims are flagged.
  4. Days only one reader mentions are flagged as single-reader.
"""
from __future__ import annotations

import copy

from .core import effective_units, resolve_all
from .rules import REPLACE


def merge(messages, model_raw: list[dict], rules_raw: list[dict], roster, cal, coordinators=()) -> list[dict]:
    m_res = {c["id"]: c for c in resolve_all(messages, model_raw, roster, cal, coordinators)}
    r_res = {c["id"]: c for c in resolve_all(messages, rules_raw, roster, cal, coordinators)}
    out = []
    for msg in messages:
        mine = [copy.deepcopy(c) for c in model_raw if c["msg"] == msg.id]
        theirs = [c for c in rules_raw if c["msg"] == msg.id]
        live_m = [m_res[c["id"]] for c in mine if m_res[c["id"]]["review"] != "dropped"]
        live_r = [r_res[c["id"]] for c in theirs if r_res[c["id"]]["review"] != "dropped"]
        cue = bool(REPLACE.search(msg.text))
        for c in mine:
            c.setdefault("hints", [])
            if cue and c["said"].get("status") in ("available", "conditional") and not c["said"].get("replaces_earlier"):
                c["said"]["replaces_earlier"] = True
                c["hints"].append("replace_cue")
        mu = {k: v for k, v in effective_units(live_m).items()}
        ru = {k: v for k, v in effective_units(live_r).items()}
        keys_of = lambda claims: {c["id"]: set(effective_units([c]).keys()) for c in claims}  # noqa: E731
        m_keys, r_keys = keys_of(live_m), keys_of(live_r)
        for c in mine:
            ks = m_keys.get(c["id"], set())
            if any(k in ru and ru[k] != mu[k] for k in ks):
                c["hints"].append("readers_disagree")
            elif ks and not any(k in ru for k in ks):
                c["hints"].append("one_reader")
        n = len(mine)
        for rc in theirs:
            ks = r_keys.get(rc["id"], set())
            missing = [k for k in ks if k not in mu and ru[k]["unavailable"] and not ru[k]["open"]]
            if missing:
                n += 1
                add = copy.deepcopy(rc)
                add.update(id=f"{msg.id}.{n}", n=n, source="rules", hints=["added_by_rules"])
                out.append(add)
        out.extend(mine)
    return out
