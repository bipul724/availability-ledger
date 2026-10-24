"""Match names in messages to the roster. Similar names are flagged, never guessed."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

SELF_WORDS = {"sender", "me", "i", "myself", "self"}


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return " ".join(s.split())


def _distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


@dataclass
class PersonMatch:
    state: str  # resolved | ambiguous | unknown
    name: str | None = None
    candidates: list[str] = field(default_factory=list)
    similar: list[str] = field(default_factory=list)


def similar_names(name: str, roster: list[str]) -> list[str]:
    n = norm_name(name)
    return [r for r in roster if r != name and _distance(n, norm_name(r)) <= 2]


def match_person(text: str, sender: str, roster: list[str]) -> PersonMatch:
    raw = (text or "").strip()
    if not raw or norm_name(raw) in SELF_WORDS:
        raw = sender
    n = norm_name(raw)
    by_norm = {norm_name(r): r for r in roster}
    if n in by_norm:
        name = by_norm[n]
        return PersonMatch("resolved", name, similar=similar_names(name, roster))
    words = n.split()
    if not words:
        return PersonMatch("unknown")
    first = words[0]
    if len(first) == 1 and len(words) > 1:  # COR-16: "T. Vekar" / "T Vekar" = first initial + surname
        cands = [r for rn, r in by_norm.items() if rn.split()[-1] == words[-1] and rn.split()[0].startswith(first)]
        if len(cands) == 1:
            return PersonMatch("resolved", cands[0], similar=similar_names(cands[0], roster))
        if cands:
            return PersonMatch("ambiguous", None, candidates=cands)
    last_initial = words[1][0] if len(words) > 1 else None
    exact, prefix = [], []
    for rn, r in by_norm.items():
        r_first, r_last = rn.split()[0], rn.split()[-1]
        if last_initial and not r_last.startswith(last_initial):
            continue
        if r_first == first:
            exact.append(r)
        elif len(first) >= 3 and r_first.startswith(first):
            prefix.append(r)  # "Sam" may be short for "Samira"
    cands = exact + prefix
    if len(cands) == 1:
        return PersonMatch("resolved", cands[0], similar=similar_names(cands[0], roster))
    if cands:
        return PersonMatch("ambiguous", None, candidates=cands)
    return PersonMatch("unknown")


def named_in(text: str, roster: list[str]) -> list[str]:
    """COR-20: roster entries whose first name appears in the text as a whole word (accents and case ignored)."""
    words = set(norm_name(text).split())
    return [r for r in roster if norm_name(r).split() and norm_name(r).split()[0] in words]
