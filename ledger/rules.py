"""Baseline: keywords and regular expressions, roughly what an hour of rule writing gives.

It emits the same claim shape as the model so both run through identical
resolution, ledger and scoring code.
"""
from __future__ import annotations

import re

from .messages import Message
from .names import match_person

_WD = r"(?:mon(?:day)?s?|tue(?:s(?:day)?)?s?|wed(?:s|nesday)?s?|thu(?:r(?:s(?:day)?)?)?s?|fri(?:day)?s?|sat(?:urday)?s?|sun(?:day)?s?)"
DAY = re.compile(
    rf"\b(?:(?:next|this|last|coming)\s+)?{_WD}\b"
    r"|\b(?:today|tonight|tomorrow|this (?:morning|afternoon|evening))\b"
    r"|\b(?:the )?rest of (?:this|the) week\b|\b(?:all|whole) week\b|\bweekdays\b"
    r"|\b(?:this |next |the )?weekend\b|\b\d{1,2}/\d{1,2}\b|\bthe \d{1,2}(?:st|nd|rd|th)\b", re.I)
_T = r"\d{1,2}(?::\d{2})?(?:\s*[ap]m)?"
TIME = re.compile(
    rf"(?:from\s+)?{_T}\s*(?:-|–|to|until|till)\s*{_T}"
    rf"|\b(?:after|from|until|till|before)\s+{_T}"
    r"|\b(?:all day|mornings?|afternoons?|evenings?|tonight)\b", re.I)
NEG = re.compile(r"\b(?:can'?t|can’t|cannot|can not|won'?t|not|no good|doesn'?t work|isn'?t|unavailable"
                 r"|busy|away|off|out of town|drop out|cancel(?:s|led|ed|ling|ing|lation)?"
                 r"|i'?m out|i’m out|i am out|out all day)\b", re.I)  # COR-17: word forms; "out" only in these phrases
COND = re.compile(r"\b(?:if|might|maybe|possibly|probably|not sure|either|one or the other|depending|unless"
                  r"|will confirm)\b", re.I)
REPLACE = re.compile(r"\b(?:instead|correction|actually|change of plans|update|now)\b", re.I)
QUESTION_START = re.compile(r"^\W*(?:where|did|who|what|when|how|is|are|does|do|has|have)\b", re.I)
SPLIT = re.compile(r"(?<=[.!?;])\s+|\s+[—–]\s+")


def extract(msg: Message, roster: list[str]) -> list[dict]:
    if match_person("SENDER", msg.sender, roster).state != "resolved":
        return []  # coordinator or unknown sender
    replaces = bool(REPLACE.search(msg.text))
    claims = []
    for sentence in SPLIT.split(msg.text):
        if QUESTION_START.match(sentence):
            continue
        for k, part in enumerate(re.split(r"\bexcept\b", sentence, maxsplit=1, flags=re.I)):
            days = [m.group(0) for m in DAY.finditer(part)]
            if not days:
                continue
            t = TIME.search(part)
            cond = COND.search(part)
            status = "unavailable" if k == 1 or NEG.search(part) else "conditional" if cond else "available"
            for d in days:
                claims.append({
                    "person": "SENDER", "day_text": d, "time_text": t.group(0) if t else "",
                    "status": status, "condition": cond.group(0) if cond and status == "conditional" else "",
                    "replaces_earlier": replaces, "excerpt": part.strip(),
                })
    return claims
