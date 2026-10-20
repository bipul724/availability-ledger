"""Deterministic date and time resolution.

The model only copies day and time phrases out of a message. This module turns
those phrases into dates and times using the message timestamp and the selected
week. When the phrase and context do not settle the answer, the result stays
ambiguous instead of being guessed.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

DEFAULT_PERIODS = {
    "morning": ("09:00", "12:00"),
    "afternoon": ("13:00", "17:00"),
    "evening": ("17:00", "20:00"),
}


@dataclass
class Calendar:
    week_start: date  # a Monday
    timezone: str = "America/New_York"
    day_start: str = "09:00"
    day_end: str = "20:00"
    periods: dict = field(default_factory=lambda: dict(DEFAULT_PERIODS))

    def __post_init__(self):
        if self.week_start.weekday() != 0:
            raise ValueError("week_start must be a Monday")

    @property
    def week_end(self) -> date:
        return self.week_start + timedelta(days=6)

    @property
    def week_dates(self) -> list[date]:
        return [self.week_start + timedelta(days=i) for i in range(7)]

    def in_week(self, d: date) -> bool:
        return self.week_start <= d <= self.week_end


@dataclass
class DayResolution:
    state: str  # resolved | ambiguous | outside_week | unparsed
    dates: list[date] = field(default_factory=list)  # inside the selected week
    candidates: list[date] = field(default_factory=list)
    note: str = ""


@dataclass
class TimeResolution:
    state: str  # explicit | period | open | unstated | unparsed
    start: str | None = None
    end: str | None = None
    note: str = ""


def _norm(text: str) -> str:
    t = (text or "").lower()
    t = t.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    t = re.sub(r"a\.m\.?", "am", t)
    t = re.sub(r"p\.m\.?", "pm", t)
    t = re.sub(r"[^a-z0-9:/' -]", " ", t)
    return " ".join(t.split())


def _monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


# ---------------------------------------------------------------- days

_WD = r"(mon(?:day)?s?|tue(?:s(?:day)?)?s?|wed(?:s|nesday)?s?|thu(?:r(?:s(?:day)?)?)?s?|fri(?:day)?s?|sat(?:urday)?s?|sun(?:day)?s?)"
_WD_INDEX = {"mo": 0, "tu": 1, "we": 2, "th": 3, "fr": 4, "sa": 5, "su": 6}
_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
_MONTH_RE = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*"


def _wd(token: str) -> int:
    return _WD_INDEX[token[:2]]


class _Atoms:
    """Collects date readings found in a phrase."""

    def __init__(self):
        self.fixed: list[date] = []
        self.ambiguous: list[list[date]] = []
        self.notes: list[str] = []

    def add(self, *ds: date):
        self.fixed.extend(ds)

    def either(self, options: list[date], note: str):
        self.ambiguous.append(sorted(set(options)))
        self.notes.append(note)


def resolve_day(text: str, sent: datetime, cal: Calendar) -> DayResolution:
    t = _norm(text)
    if not t:
        return DayResolution("unparsed", note="no day given")
    today = sent.date()
    this_mon = _monday(today)
    atoms = _Atoms()
    choice = bool(re.search(r"\b(one day|one of|either|whichever|not sure which)\b", t) or re.search(r"\bor\b", t))

    def consume(pattern: str, fn):
        nonlocal t
        for m in list(re.finditer(pattern, t)):
            fn(m)
        t = re.sub(pattern, " ", t)

    # relative words
    consume(r"\bday after tomorrow\b", lambda m: atoms.add(today + timedelta(days=2)))
    consume(r"\b(tomorrow|tmrw|tmr)\b", lambda m: atoms.add(today + timedelta(days=1)))
    consume(r"\b(today|tonight|this (morning|afternoon|evening))\b", lambda m: atoms.add(today))

    # week ranges
    consume(r"\b(the )?rest of (this|the) week\b",
            lambda m: atoms.add(*[today + timedelta(days=i) for i in range(7 - today.weekday())]))
    consume(r"\b(all|whole|entire) (of )?(the )?week\b|\bevery day\b|\bany day\b|\ball days\b",
            lambda m: atoms.add(*cal.week_dates))
    consume(r"\bweekdays\b", lambda m: atoms.add(*cal.week_dates[:5]))
    consume(r"\bnext week\b", lambda m: atoms.add(*[this_mon + timedelta(days=7 + i) for i in range(7)]))
    consume(r"\bthis week\b", lambda m: atoms.add(*[this_mon + timedelta(days=i) for i in range(7)]))

    def next_weekend(m):
        sat_next = today + timedelta(days=((5 - today.weekday()) % 7) or 7)
        a = [sat_next, sat_next + timedelta(days=1)]
        b = [this_mon + timedelta(days=12), this_mon + timedelta(days=13)]
        if a == b:
            atoms.add(*a)
        else:
            atoms.either(a + b, "'next weekend' could mean either of two weekends")

    consume(r"\bnext weekend\b", next_weekend)
    consume(r"\bthis weekend\b", lambda m: atoms.add(this_mon + timedelta(days=5), this_mon + timedelta(days=6)))
    consume(r"\b(the |over the |at the )?weekend\b", lambda m: atoms.add(cal.week_dates[5], cal.week_dates[6]))

    # numeric dates such as 11/12 or 11/12/2026
    def numeric(m):
        a, b = int(m[1]), int(m[2])
        year = int(m[3]) + (2000 if m[3] and len(m[3]) == 2 else 0) if m[3] else today.year
        readings = []
        for month, day, label in ((a, b, "M/D"), (b, a, "D/M")):
            try:
                readings.append((date(year, month, day), label))
            except ValueError:
                pass
        in_week = sorted({d for d, _ in readings if cal.in_week(d)})
        if len(in_week) == 1:
            atoms.add(in_week[0])
            if len({d for d, _ in readings}) > 1:
                atoms.notes.append(f"'{m[0]}' read as {[l for d, l in readings if d == in_week[0]][0]} because only that date is in the selected week")
        elif readings:
            atoms.add(*sorted({d for d, _ in readings}))

    consume(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", numeric)

    def month_day(month_token: str, day_token: str):
        month, day = _MONTHS[month_token[:3]], int(day_token)
        try:
            d = date(today.year, month, day)
        except ValueError:
            return
        if d < today - timedelta(days=180):
            d = date(today.year + 1, month, day)
        atoms.add(d)

    consume(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+(?:of\s+)?{_MONTH_RE}\b", lambda m: month_day(m[2], m[1]))
    consume(rf"\b{_MONTH_RE}\s+(\d{{1,2}})(?:st|nd|rd|th)?\b", lambda m: month_day(m[1], m[2]))

    def ordinal(m):
        day = int(m[1])
        y, mo = today.year, today.month
        if day < today.day:
            y, mo = (y + 1, 1) if mo == 12 else (y, mo + 1)
        try:
            atoms.add(date(y, mo, day))
        except ValueError:
            pass

    consume(r"\b(?:the\s+)?(\d{1,2})(?:st|nd|rd|th)\b", ordinal)

    # weekday ranges: thu-sat, thursday to saturday
    def wd_range(m):
        a, b = _wd(m[1]), _wd(m[2])
        if b >= a:
            atoms.add(*[cal.week_start + timedelta(days=i) for i in range(a, b + 1)])

    consume(rf"\b{_WD}\s*(?:-|to|through|thru|till|until)\s*{_WD}\b", wd_range)

    # single weekdays with optional modifier
    def weekday(m):
        mod = {"coming": "next"}.get(m[1], m[1])
        token, idx = m[2], _wd(m[2])
        if mod == "next":
            delta = (idx - today.weekday()) % 7 or 7
            a = today + timedelta(days=delta)
            b = this_mon + timedelta(days=7 + idx)
            if a == b:
                atoms.add(a)
            else:
                atoms.either([a, b], f"'next {token}' sent on {today:%a %d %b} could be {a:%d %b} or {b:%d %b}")
        elif mod == "last":
            delta = (today.weekday() - idx) % 7 or 7
            atoms.add(today - timedelta(days=delta))
        elif mod == "this":
            d = this_mon + timedelta(days=idx)
            if d < today:
                atoms.either([d, d + timedelta(days=7)], f"'this {token}' has already passed")
            else:
                atoms.add(d)
        else:
            d = cal.week_start + timedelta(days=idx)
            if (cal.in_week(today) and d < today) or today > cal.week_end:
                atoms.either([d, d + timedelta(days=7)], f"'{token}' was sent after that day had passed")
            else:
                atoms.add(d)

    consume(rf"\b(?:(next|this|last|coming)\s+)?{_WD}\b", weekday)

    if not atoms.fixed and not atoms.ambiguous:
        return DayResolution("unparsed", note=f"could not read a day in '{text}'")
    fixed = sorted(set(atoms.fixed))
    if atoms.ambiguous:
        cands = sorted(set(fixed).union(*map(set, atoms.ambiguous)))
        return DayResolution("ambiguous", candidates=cands, note="; ".join(atoms.notes))
    if choice and len(fixed) > 1:
        return DayResolution("ambiguous", candidates=fixed, note="the message offers one of these days, not all of them")
    inside = [d for d in fixed if cal.in_week(d)]
    outside = [d for d in fixed if not cal.in_week(d)]
    note = "; ".join(atoms.notes)
    if inside:
        if outside:
            note = (note + "; " if note else "") + "ignored dates outside the selected week: " + ", ".join(f"{d:%d %b}" for d in outside)
        return DayResolution("resolved", dates=inside, note=note)
    return DayResolution("outside_week", candidates=outside, note=note or "outside the selected week")


# ---------------------------------------------------------------- times

_TOK = r"(noon|midday|\d{1,2}(?::\d{2})?\s*(?:am|pm)?)"
SAME_TIME = re.compile(r"\b(the same|same time|same times|same hours)\b")


def _tok_minutes(tok: str) -> tuple[int, bool]:
    tok = tok.strip()
    if tok in ("noon", "midday"):
        return 12 * 60, True
    m = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", tok)
    hour, minute, ampm = int(m[1]), int(m[2] or 0), m[3]
    if ampm == "pm" and hour < 12:
        hour += 12
    elif ampm == "am" and hour == 12:
        hour = 0
    elif not ampm and 1 <= hour <= 7:
        hour += 12  # "2-5" at a volunteer shift means the afternoon
    return hour * 60 + minute, bool(ampm)


def _hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _mins(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def resolve_time(text: str, cal: Calendar) -> TimeResolution:
    t = _norm(text)
    if not t:
        return TimeResolution("unstated")
    if re.search(r"\b(all day|all-day|full day|whole day|any ?time|all of it)\b", t):
        return TimeResolution("period", cal.day_start, cal.day_end)

    m = re.search(rf"\bbetween\s+{_TOK}\s+and\s+{_TOK}", t) or \
        re.search(rf"{_TOK}\s*(?:-|to|until|till|til|thru|through)\s*{_TOK}", t)
    if m:
        s, _ = _tok_minutes(m[1])
        e, e_explicit = _tok_minutes(m[2])
        if e <= s and not e_explicit and e + 720 <= 24 * 60:
            e += 720  # "6-9" in the evening
        if 0 <= s < e <= 24 * 60:
            return TimeResolution("explicit", _hhmm(s), _hhmm(e))
        return TimeResolution("unparsed", note=f"time range '{m[0]}' does not make sense")

    if m := re.search(rf"\b(?:after|from|since|starting(?: at)?)\s+{_TOK}", t) or \
            re.search(rf"\b{_TOK}\s*onwards?\b", t):
        s, _ = _tok_minutes(m[1])
        return TimeResolution("open", _hhmm(s), cal.day_end, note=f"'{m[0]}' runs to {cal.day_end}")
    if m := re.search(rf"\b(?:until|till|til|before|up to)\s+{_TOK}", t):
        e, _ = _tok_minutes(m[1])
        return TimeResolution("open", cal.day_start, _hhmm(e), note=f"'{m[0]}' starts at {cal.day_start}")

    spans = []
    for word, key in (("morning", "morning"), ("afternoon", "afternoon"), ("evening", "evening"),
                      ("tonight", "evening"), ("night", "evening")):
        if re.search(rf"\b{word}s?\b", t):
            spans.append(cal.periods[key])
    if spans:
        return TimeResolution("period", min(s for s, _ in spans), max(e for _, e in spans))
    if SAME_TIME.search(t):  # core copies the hours from another claim in the same message
        return TimeResolution("unparsed", note="'the same' needs a time earlier in this message")
    return TimeResolution("unparsed", note=f"could not read a time in '{text}'")
