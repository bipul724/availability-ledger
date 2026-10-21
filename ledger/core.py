"""Claims, the ledger and the counts. Ordinary code only; no model calls here.

A claim is one statement such as "Maria is available Tuesday morning". Extractors
(the model, the rules baseline, or a person) supply what was *said*; this module
checks it against the source message, resolves dates and times, and folds every
claim into a per-person, per-day history. Later answers change only the time
they mention, so a Monday correction never touches Wednesday.
"""
from __future__ import annotations

import difflib
import re
from collections import Counter
from datetime import date

from .messages import Message
from .names import SELF_WORDS, match_person, norm_name
from .resolve import _WD, SAME_TIME, Calendar, TimeResolution, _hhmm, _mins, _norm, _wd, resolve_day, resolve_time

SLOT = 15
SLOT_START, SLOT_END = 6 * 60, 23 * 60
N_SLOTS = (SLOT_END - SLOT_START) // SLOT
COUNT_START, COUNT_END, COUNT_STEP = 8 * 60, 22 * 60, 30
STATUSES = ("available", "conditional", "unavailable")
_CAUTION = {"available": 0, "conditional": 1, "unavailable": 2}

# COR-07a (D-25): general-English words that can signal a change to an earlier answer, written from everyday usage,
# not from any fixture. "scratch" and "skip" also occur in set B, so any effect on sets A/B is post-hoc; only the
# frozen set C tests this list independently. A match only raises a warning; it never edits the sheet or the export.
CHANGE_WORDS = re.compile(
    r"\b(?:cancel(?:s|led|ed|ling|ing)?|drop(?:s|ped|ping)?|skip(?:s|ped|ping)?|scratch|off|can'?t|cannot|can not"
    r"|won'?t|no longer|not any ?more|pull(?:ing)? out|back(?:ing)? out|bail(?:s|ed|ing)?|count me out"
    r"|withdraw(?:s|n|ing)?|unable|not able|miss(?:ing)?|rain ?check|change of plans?)\b")

# COR-15 (D-31): general-English cues that a later message changes the day's earlier answer ("change", "instead",
# "now" (covering "only ... now"), "move", "switch", "make it"). Code, not the prompt. Motivated by set C m20/m21, so
# every A/B/C effect is post-hoc. Applied only to model and rules claims that state a time.
REPLACE_CUES = re.compile(r"\b(?:chang(?:e|es|ed|ing)|instead|now|mov(?:e|es|ed|ing)|switch(?:es|ed|ing)?|make it)\b")

_PUNCT = {"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"}


def _norm_map(s: str) -> tuple[str, list[int]]:
    """Lowercase, unify quotes and dashes, collapse spaces; keep an index map."""
    out, idx, space = [], [], False
    for i, ch in enumerate(s or ""):
        c = _PUNCT.get(ch, ch).lower()
        if c.isspace():
            if space or not out:
                continue
            c, space = " ", True
        else:
            space = False
        out.append(c)
        idx.append(i)
    return "".join(out), idx


def locate(excerpt: str, text: str) -> tuple[str, list[int] | None]:
    """Where does the excerpt sit in the message? exact | approx | missing."""
    ne, _ = _norm_map((excerpt or "").strip(" .!?,;:\"'"))
    nt, idx = _norm_map(text)
    if not ne:
        return "missing", None
    k = nt.find(ne)
    if k >= 0:
        return "exact", [idx[k], idx[k + len(ne) - 1] + 1]
    m = difflib.SequenceMatcher(None, nt, ne, autojunk=False).find_longest_match(0, len(nt), 0, len(ne))
    if m.size >= max(8, int(0.8 * len(ne))):
        return "approx", [idx[m.a], idx[m.a + m.size - 1] + 1]
    return "missing", None


def _contains(phrase: str, text: str) -> bool:
    p, _ = _norm_map((phrase or "").strip(" .!?,;:\"'"))
    return not p or p in _norm_map(text)[0]


_MOD_WD = re.compile(rf"\b(?:(next|this|last|coming)\s+)?{_WD}\b")


def _modifier_from_quote(day_text: str, excerpt: str) -> str | None:
    """'Saturday' copied out of 'this Saturday': put the quote's modifier back on that weekday.

    Only when the quote gives the same weekday exactly one modifier and every mention of it
    carries that modifier; otherwise None, so a modifier is never invented.
    """
    quoted: dict[int, set] = {}
    for m in _MOD_WD.finditer(_norm(excerpt)):
        quoted.setdefault(_wd(m[2]), set()).add(m[1])
    changed = False

    def put_back(m):
        nonlocal changed
        mods = quoted.get(_wd(m[2]), set())
        if m[1] or len(mods) != 1 or None in mods:
            return m[0]
        changed = True
        return f"{next(iter(mods))} {m[0]}"

    restored = _MOD_WD.sub(put_back, _norm(day_text))
    return restored if changed else None


def _claim_hours(claim: dict, msg: Message, cal: Calendar) -> tuple[str, str] | None:
    """Explicit start and end for a claim: the reviewer's, or time words that are in the message."""
    ov = claim.get("override") or {}
    if "start" in ov or "end" in ov:
        s, e = ov.get("start"), ov.get("end")
        return (s, e) if s and e and _mins(s) < _mins(e) else None
    text = (claim.get("said") or {}).get("time_text", "")
    tr = resolve_time(text, cal)
    return (tr.start, tr.end) if tr.state == "explicit" and _contains(text, msg.text) else None


def _same_hours(claim: dict, siblings, msg: Message, cal: Calendar) -> tuple[str, str, str] | None:
    """'Wednesday the same': hours of the nearest earlier claim in this message, never another message."""
    earlier = [x for x in siblings if x["msg"] == claim["msg"] and x.get("n", 0) < claim.get("n", 0)]
    for x in sorted(earlier, key=lambda x: -x.get("n", 0)):
        if hours := _claim_hours(x, msg, cal):
            return (*hours, x["id"])
    return None


def resolve_claim(claim: dict, msg: Message, roster: list[str], cal: Calendar, coordinators=(),
                  siblings=()) -> dict:
    """Recompute every derived field from what was said plus any human override."""
    said = claim.get("said") or {}
    ov = claim.get("override") or {}
    c = {k: claim[k] for k in ("id", "msg", "source", "review", "said", "override", "n", "hints") if k in claim}
    c.setdefault("review", "pending")
    flags: list[str] = list(claim.get("hints") or [])

    if ov.get("person"):
        c.update(person=ov["person"], person_state="resolved", person_candidates=[], similar=[])
    else:
        pm = match_person(said.get("person", ""), msg.sender, roster)
        c.update(person=pm.name, person_state=pm.state, person_candidates=pm.candidates, similar=pm.similar)
        if pm.state == "ambiguous":
            flags.append("who_ambiguous")
        elif pm.state == "unknown":
            flags.append("who_unknown")
        if pm.similar:
            flags.append("similar_name")

    if ov.get("dates") is not None:
        dates = sorted(ov["dates"])
        inside = [d for d in dates if cal.week_start.isoformat() <= d <= cal.week_end.isoformat()]
        c.update(dates=inside, date_candidates=[], date_note="set by reviewer",
                 date_state="resolved" if inside else "unparsed")
    else:
        restored = None
        if claim.get("source") != "user" and locate(said.get("excerpt", ""), msg.text)[0] != "missing":
            restored = _modifier_from_quote(said.get("day_text", ""), said.get("excerpt", ""))
        dr = resolve_day(restored or said.get("day_text", ""), msg.sent, cal)
        c.update(dates=[d.isoformat() for d in dr.dates], date_state=dr.state,
                 date_candidates=[d.isoformat() for d in dr.candidates], date_note=dr.note)
        if restored:
            c["date_note"] = (dr.note + "; " if dr.note else "") + f"read as '{restored}' from the quote"
            flags.append("day_modifier_from_quote")
    if c["date_state"] == "ambiguous":
        flags.append("date_ambiguous")
    elif c["date_state"] == "outside_week":
        flags.append("outside_week")
    elif c["date_state"] == "unparsed":
        flags.append("date_unreadable")

    if "start" in ov or "end" in ov:
        s, e = ov.get("start") or None, ov.get("end") or None
        if s and e and _mins(s) < _mins(e):
            c.update(start=s, end=e, time_state="explicit", time_note="set by reviewer")
        elif not s and not e:
            c.update(start=None, end=None, time_state="unstated", time_note="set by reviewer")
        else:
            c.update(start=s, end=e, time_state="unparsed", time_note="start must be before end")
    else:
        tr = resolve_time(said.get("time_text", ""), cal)
        if tr.state == "unparsed" and SAME_TIME.search(_norm(said.get("time_text", ""))) \
                and (same := _same_hours(claim, siblings, msg, cal)):
            tr = TimeResolution("explicit", same[0], same[1], note=f"same hours as {same[2]}")
            flags.append("time_from_same_message")
        c.update(start=tr.start, end=tr.end, time_state=tr.state, time_note=tr.note)
    if c["time_state"] == "unparsed":
        flags.append("time_unreadable")
    elif c["time_state"] == "unstated":
        flags.append("time_unstated")

    status = ov.get("status") or said.get("status")
    c["status"] = status if status in STATUSES else "available"
    c["condition"] = ov.get("condition", said.get("condition") or "")
    if c["status"] == "conditional":
        flags.append("conditional")
    c["replaces_earlier"] = bool(said.get("replaces_earlier"))

    if claim.get("source") == "user" and not said.get("excerpt"):
        c["excerpt_state"], c["excerpt_span"] = "user", None
    else:
        c["excerpt_state"], c["excerpt_span"] = locate(said.get("excerpt", ""), msg.text)
        if c["excerpt_state"] != "exact":
            flags.append("excerpt_" + c["excerpt_state"])
        if not (_contains(said.get("day_text", ""), msg.text) and _contains(said.get("time_text", ""), msg.text)):
            flags.append("phrase_not_in_message")
    if ov:
        flags.append("edited")
    c["flags"] = flags

    # The quote must support the claimed days. The quote is verbatim, the day phrase may be a
    # paraphrase: "Whole weekend works" narrows "all week" to Sat-Sun; no overlap at all is dropped.
    if ov.get("dates") is None and claim.get("source") != "user" and c["date_state"] in ("resolved", "ambiguous", "outside_week"):
        quoted = resolve_day(said.get("excerpt", ""), msg.sent, cal)
        support = {d.isoformat() for d in quoted.dates + quoted.candidates}
        claimed = set(c["dates"]) | set(c["date_candidates"])
        if quoted.state != "unparsed" and not claimed <= support:
            if c["date_state"] == "resolved" and claimed & support:
                c["dates"] = sorted(claimed & support)
                c["date_note"] = (c["date_note"] + "; " if c["date_note"] else "") + "narrowed to the days in the quote"
                flags.append("days_narrowed_to_quote")
            else:
                flags.append("days_not_in_quote")

    # Evidence gate: a proposal whose words are not in this message is not applied.
    drop = None
    if "excerpt_missing" in flags and "phrase_not_in_message" in flags:
        drop = "no supporting text in this message"
    elif "days_not_in_quote" in flags:
        drop = "the quoted words do not mention these days"
    elif not ov.get("person") and c["person_state"] != "resolved" and is_coordinator(msg.sender, coordinators) \
            and norm_name(said.get("person", "")) in SELF_WORDS | {""}:
        drop = "the coordinator's own message"
    if drop and c["review"] == "pending":
        c["review"], c["drop_reason"] = "dropped", drop
    return c


def is_coordinator(sender: str, coordinators=()) -> bool:
    n = norm_name(sender)
    return "coordinator" in n.split() or n in {norm_name(x) for x in coordinators}


def resolve_all(messages: list[Message], claims: list[dict], roster: list[str], cal: Calendar,
                coordinators=()) -> list[dict]:
    by_id = {m.id: m for m in messages}
    by_msg: dict[str, list] = {}
    for c in claims:
        by_msg.setdefault(c["msg"], []).append(c)
    return [resolve_claim(c, by_id[c["msg"]], roster, cal, coordinators, by_msg[c["msg"]])
            for c in claims if c["msg"] in by_id]


# ---------------------------------------------------------------- ledger

def _span(c: dict, cal: Calendar, slots: list) -> tuple[int, int] | None:
    """Minutes covered by a claim on one day; None means 'confirmation only'."""
    if c["time_state"] != "unstated":
        return _mins(c["start"]), _mins(c["end"])
    if c["status"] == "unavailable":
        return SLOT_START, SLOT_END
    if any(s and s[0] != "unavailable" for s in slots):
        return None  # "Sunday still good": keep the earlier hours
    return _mins(cal.day_start), _mins(cal.day_end)


def _slot_range(a: int, b: int) -> range:
    return range(max(0, (a - SLOT_START) // SLOT), min(N_SLOTS, (b - SLOT_START + SLOT - 1) // SLOT))


def _segments(slots: list) -> list[dict]:
    segs: list[dict] = []
    for i, s in enumerate(slots):
        if s is None:
            continue
        t = SLOT_START + i * SLOT
        if segs and segs[-1]["status"] == s[0] and segs[-1]["_end"] == t:
            segs[-1]["_end"] = t + SLOT
            if s[1] not in segs[-1]["claims"]:
                segs[-1]["claims"].append(s[1])
        else:
            segs.append({"status": s[0], "_start": t, "_end": t + SLOT, "claims": [s[1]]})
    for seg in segs:
        seg["start"], seg["end"] = _hhmm(seg.pop("_start")), _hhmm(seg.pop("_end"))
    return segs


def _spec(c: dict) -> int:
    return len(c["dates"]) if c["date_state"] == "resolved" else 0


def build_ledger(messages: list[Message], claims: list[dict], roster: list[str], cal: Calendar) -> dict:
    order = {m.id: i for i, m in enumerate(messages)}
    sent = {m.id: m.sent.strftime("%a %d %b %H:%M") for m in messages}
    live = [c for c in claims if c.get("review") not in ("rejected", "dropped") and c["msg"] in order]
    live.sort(key=lambda c: (order[c["msg"]], -_spec(c), c.get("n", 0)))
    cue_msgs = {m.id for m in messages if REPLACE_CUES.search(_norm(m.text))}

    state: dict[tuple, list] = {}
    history: dict[tuple, list] = {}
    issues: list[dict] = []
    review_marks: dict[tuple, list[str]] = {}
    cleared: set = set()
    conflicts_seen: set = set()

    def issue(kind, c, text, **extra):
        issues.append({"kind": kind, "msg": c["msg"], "claim": c["id"], "person": c.get("person"), "text": text, **extra})

    # A repeated message has no claims of its own; its history entry echoes what the original applied.
    applied: dict[str, list] = {}
    echoes = [m for m in messages if m.duplicate_of in order]

    def echo_until(pos):
        while echoes and order[echoes[0].id] < pos:
            dup = echoes.pop(0)
            for oc in (x for x in live if x["msg"] == dup.duplicate_of):
                for key, span in applied.get(oc["id"], []):
                    history[key].append({"msg": dup.id, "sent": sent[dup.id], "claim": oc["id"], "status": oc["status"],
                                         "what": "repeated", "span": span, "duplicate_of": dup.duplicate_of})

    # COR-07a: a later message from the same person with a change word that names a day on which they still have open
    # time, while none of that message's live claims touches the day. Checked just before that message's claims apply.
    change_msgs = [m for m in messages if not m.duplicate_of and CHANGE_WORDS.search(_norm(m.text))]
    claims_of: dict[str, list] = {}
    for c in live:
        claims_of.setdefault(c["msg"], []).append(c)

    def check_changes_until(pos):
        while change_msgs and order[change_msgs[0].id] <= pos:
            m = change_msgs.pop(0)
            pm = match_person("SENDER", m.sender, roster)
            if pm.state != "resolved":
                continue
            dr = resolve_day(m.text, m.sent, cal)
            touched = {d for c in claims_of.get(m.id, [])
                       if pm.name in ([c["person"]] if c["person_state"] == "resolved" else c.get("person_candidates") or [])
                       for d in list(c.get("dates") or []) + list(c.get("date_candidates") or [])}
            for d in sorted({x.isoformat() for x in dr.dates + dr.candidates if cal.in_week(x)}):
                slots = state.get((pm.name, d))
                if d in touched or not slots or not any(s and s[0] != "unavailable" for s in slots):
                    continue
                issues.append({"kind": "unanswered_change", "msg": m.id, "claim": None, "person": pm.name, "date": d,
                               "text": f"Possible change not applied ({m.id} mentions {date.fromisoformat(d):%a %d %b}): "
                                       f"{pm.name} still has open time that day and nothing from {m.id} changes it"})

    for c in live:
        echo_until(order[c["msg"]])
        check_changes_until(order[c["msg"]])
        who = c["person"] or "/".join(c.get("person_candidates") or []) or "unknown sender"
        if c["person_state"] != "resolved":
            issue("who", c, f"Who is this about? Candidates: {', '.join(c['person_candidates']) or 'none on the roster'}")
            for cand in c.get("person_candidates") or []:
                for d in c["dates"]:
                    review_marks.setdefault((cand, d), []).append(f"{c['msg']}: unresolved name may mean {cand}")
            continue
        if c["date_state"] == "ambiguous":
            issue("date", c, f"Which day? {c['date_note']}", candidates=c["date_candidates"])
            for d in c["date_candidates"]:
                review_marks.setdefault((c["person"], d), []).append(f"{c['msg']}: possibly {c['status']} ({c['date_note']})")
            continue
        if c["date_state"] == "outside_week":
            issue("outside", c, f"{who}: {', '.join(c['date_candidates'])} is outside the selected week", candidates=c["date_candidates"])
            continue
        if c["date_state"] != "resolved":
            issue("date", c, f"{who}: could not read a day ({c['date_note']})")
            continue
        if c["time_state"] == "unparsed":
            issue("time", c, f"{who}: could not read a time ({c['time_note']}); not applied")
            continue

        for d in c["dates"]:
            key = (c["person"], d)
            slots = state.setdefault(key, [None] * N_SLOTS)
            hist = history.setdefault(key, [])
            span = _span(c, cal, slots)
            event = {"msg": c["msg"], "sent": sent[c["msg"]], "claim": c["id"], "status": c["status"]}
            if span is None:
                # COR-14: a firm, untimed follow-up settles a day that so far holds only conditional time from earlier
                # messages; with any available time already there it is just a confirmation.
                cond = [i for i, s in enumerate(slots) if s and s[0] == "conditional" and s[2] != c["msg"]]
                if c["status"] == "available" and cond and not any(s and s[0] == "available" for s in slots):
                    for i in cond:
                        slots[i] = ("available", c["id"], c["msg"], _spec(c))
                    done = f"{_hhmm(SLOT_START + cond[0] * SLOT)}-{_hhmm(SLOT_START + (cond[-1] + 1) * SLOT)}"
                    hist.append({**event, "what": "condition resolved", "span": done})
                    applied.setdefault(c["id"], []).append((key, done))
                else:
                    hist.append({**event, "what": "confirmed earlier answer", "span": ""})
                    applied.setdefault(c["id"], []).append((key, ""))
                continue
            replaces = c["replaces_earlier"] or (c.get("source") in ("model", "rules") and c["msg"] in cue_msgs
                                                 and c["time_state"] != "unstated" and c["status"] in ("available", "conditional"))
            if replaces and (c["msg"], key) not in cleared and any(s and s[2] != c["msg"] for s in slots):
                removed = _segments([s if s and s[2] != c["msg"] else None for s in slots])
                for i, s in enumerate(slots):
                    if s and s[2] != c["msg"]:
                        slots[i] = None
                cleared.add((c["msg"], key))
                hist.append({**event, "what": "replaced earlier answer for this day", "span": ""})
                if not c["replaces_earlier"]:  # COR-18 (D-32): replaced only because of a cue word; make it visible
                    gone = ", ".join(f"{g['start']}-{g['end']} {g['status']}" for g in removed)
                    issue("cue_replacement", c, f"{c['person']} {date.fromisoformat(d):%a %d %b}: {c['msg']} contains a change word, "
                          f"so it replaced the earlier answer ({gone}); check that the message really changes it",
                          date=d, removed=[[g["start"], g["end"], g["status"]] for g in removed])
            changes: Counter = Counter()
            new = (c["status"], c["id"], c["msg"], _spec(c))
            for i in _slot_range(*span):
                prev = slots[i]
                if prev and prev[2] == c["msg"] and prev[3] == new[3] and prev[0] != new[0]:
                    pair = (prev[1], c["id"])
                    if pair not in conflicts_seen:
                        conflicts_seen.add(pair)
                        issue("conflict", c, f"{c['person']} {d}: the same message says both {prev[0]} and {new[0]}")
                    if _CAUTION[prev[0]] >= _CAUTION[new[0]]:
                        continue  # keep the more cautious reading until a person decides
                if prev is None:
                    kind = "marked unavailable" if new[0] == "unavailable" else "added"
                elif prev[2] == c["msg"]:
                    kind = "refined"
                elif prev[0] == new[0]:
                    kind = "repeated"
                elif new[0] == "unavailable":
                    kind = "cancelled" if prev[0] == "available" else "condition declined"
                elif prev[0] == "conditional" and new[0] == "available":
                    kind = "condition resolved"
                elif prev[0] == "unavailable":
                    kind = "now " + new[0]
                else:
                    kind = "now conditional"
                slots[i] = new
                changes[kind] += 1
            hist.append({**event, "what": ", ".join(changes) or "no change", "span": f"{_hhmm(span[0])}-{_hhmm(span[1])}"})
            applied.setdefault(c["id"], []).append((key, hist[-1]["span"]))
    echo_until(len(order))
    check_changes_until(len(order))
    # COR-10 per D-30: a pending suggestion whose day or time words are not in the message still counts provisionally
    # (holding it removed correct, reworded suggestions), but is listed for a wording check. Not a blocking kind.
    for c in live:
        if c.get("review") == "pending" and "phrase_not_in_message" in (c.get("flags") or []):
            who = c["person"] or "/".join(c.get("person_candidates") or []) or "unknown sender"
            issue("check_wording", c, f"{who}: some day or time words are not in this message; check the wording before accepting")

    sheet: dict[str, dict] = {p: {} for p in roster}
    for (person, d), slots in sorted(state.items()):
        segs = [s for s in _segments(slots) if s["status"] != "unavailable"]
        for s in segs:
            s["review"] = review_marks.get((person, d), [])
            if s["status"] == "conditional":
                conds = sorted({c["condition"] for c in live if c["id"] in s["claims"] and c["condition"]})
                issues.append({"kind": "condition", "msg": s["claims"][-1].split(".")[0], "claim": s["claims"][-1],
                               "person": person, "text": f"{person} {d} {s['start']}-{s['end']} is still conditional"
                               + (f": {'; '.join(conds)}" if conds else "")})
        if segs:
            sheet.setdefault(person, {})[d] = segs
    review_notes = {f"{p}|{d}": notes for (p, d), notes in sorted(review_marks.items())
                    if cal.week_start.isoformat() <= d <= cal.week_end.isoformat()}

    counts = []
    for d in cal.week_dates:
        avail, cond = [], []
        for t in range(COUNT_START, COUNT_END, COUNT_STEP):
            idx = list(_slot_range(t, t + COUNT_STEP))
            a = m = 0
            for person in roster:
                slots = state.get((person, d.isoformat()))
                if not slots:
                    continue
                sts = [slots[i][0] if slots[i] else None for i in idx]
                if all(s == "available" for s in sts):
                    a += 1
                elif all(s in ("available", "conditional") for s in sts):
                    m += 1
            avail.append(a)
            cond.append(m)
        counts.append({"date": d.isoformat(), "available": avail, "conditional": cond})

    return {
        "sheet": sheet,
        "review_notes": review_notes,
        "history": {f"{p}|{d}": h for (p, d), h in sorted(history.items())},
        "issues": issues,
        "counts": {"start": _hhmm(COUNT_START), "end": _hhmm(COUNT_END), "step": COUNT_STEP, "days": counts},
    }


# ---------------------------------------------------------------- evaluation helpers

def effective_units(claims: list[dict]) -> dict:
    """What one message says per (person, day), after in-message precedence.

    Used to compare extractors with the reference. Keys for unresolved people or
    dates carry their candidate lists, so guessing a single answer does not match.
    """
    units: dict = {}
    for c in sorted(claims, key=lambda c: -_spec(c)):
        person = c["person"] if c["person_state"] == "resolved" else "?" + "|".join(sorted(c.get("person_candidates") or []))
        if c["date_state"] == "resolved":
            keys = [(person, d) for d in c["dates"]]
        elif c["date_state"] in ("ambiguous", "outside_week"):
            tag = "?" if c["date_state"] == "ambiguous" else "outside:"
            keys = [(person, tag + "|".join(sorted(c["date_candidates"])))]
        else:
            keys = [(person, "unreadable")]
        for key in keys:
            u = units.setdefault(key, {"slots": [None] * N_SLOTS, "unstated": set(), "unreadable": set()})
            if c["time_state"] == "unparsed":
                u["unreadable"].add(c["status"])
            elif c["time_state"] == "unstated" and c["status"] != "unavailable":
                u["unstated"].add(c["status"])
            else:
                a, b = (SLOT_START, SLOT_END) if c["time_state"] == "unstated" else (_mins(c["start"]), _mins(c["end"]))
                for i in _slot_range(a, b):
                    u["slots"][i] = (c["status"], c["id"], c["msg"], 0)
    out = {}
    for key, u in units.items():
        segs = _segments(u["slots"])
        out[key] = {
            "open": tuple((s["status"], s["start"], s["end"]) for s in segs if s["status"] != "unavailable"),
            "unavailable": any(s["status"] == "unavailable" for s in segs),
            "unstated": tuple(sorted(u["unstated"])),
            "unreadable": tuple(sorted(u["unreadable"])),
        }
    return out


def final_slots(ledger: dict, cal: Calendar) -> dict:
    """(person, date, slot index) -> 'available' | 'conditional' for the evaluation."""
    out = {}
    for person, days in ledger["sheet"].items():
        for d, segs in days.items():
            for s in segs:
                for i in _slot_range(_mins(s["start"]), _mins(s["end"])):
                    out[(person, d, i)] = s["status"]
    return out
