"""Parse pasted or imported chat text into dated messages."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

DUPLICATE_WINDOW = timedelta(hours=24)


@dataclass
class Message:
    id: str
    sent: datetime  # wall-clock time in the selected timezone
    sender: str
    text: str
    duplicate_of: str | None = None  # id of the earliest identical copy from the same sender

    def to_dict(self) -> dict:
        d = asdict(self)
        d["sent"] = self.sent.strftime("%Y-%m-%d %H:%M")
        return d

    @staticmethod
    def from_dict(d: dict) -> "Message":
        return Message(d["id"], datetime.strptime(d["sent"], "%Y-%m-%d %H:%M"), d["sender"], d["text"],
                       d.get("duplicate_of"))


# 2026-11-02 09:41 | Maria Lopez | I can do Tuesday
_PIPE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})[ T](\d{1,2}:\d{2})\s*\|\s*([^|]+?)\s*\|\s?(.*)$")
# WhatsApp Android: 02/11/2026, 09:41 - Maria Lopez: text
_WA_ANDROID = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{2,4}),?\s+(\d{1,2}:\d{2})\s*([AaPp]\.?[Mm]\.?)?\s+-\s+([^:]+?):\s?(.*)$")
# WhatsApp iOS: [02/11/2026, 09:41:03] Maria Lopez: text
_WA_IOS = re.compile(r"^\[(\d{1,2})/(\d{1,2})/(\d{2,4}),?\s+(\d{1,2}:\d{2})(?::\d{2})?\s*([AaPp]\.?[Mm]\.?)?\]\s+([^:]+?):\s?(.*)$")


def _wa_datetime(a: str, b: str, y: str, hm: str, ampm: str | None, day_first: bool) -> datetime:
    day, month = (int(a), int(b)) if day_first else (int(b), int(a))
    year = int(y) + 2000 if len(y) == 2 else int(y)
    hour, minute = (int(x) for x in hm.split(":"))
    if ampm:
        pm = ampm.lower().startswith("p")
        hour = hour % 12 + (12 if pm else 0)
    return datetime(year, month, day, hour, minute)


_PUNCT = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"})


def _same_text_key(sender: str, text: str) -> tuple[str, str]:
    """Case, whitespace, curly quotes and dashes do not make a message different."""
    return " ".join(sender.lower().split()), " ".join(text.translate(_PUNCT).lower().split())


def mark_duplicates(messages: list[Message]) -> None:
    """A repeat of an earlier message (same sender and text, within 24 hours) points at the earliest copy."""
    first: dict[tuple[str, str], Message] = {}
    for msg in messages:
        key = _same_text_key(msg.sender, msg.text)
        orig = first.get(key)
        if orig and msg.sent - orig.sent <= DUPLICATE_WINDOW:
            msg.duplicate_of = orig.id
        else:
            first[key] = msg


def parse_messages(text: str, day_first: bool = False) -> list[Message]:
    """Lines that do not start a new message are appended to the previous one."""
    messages: list[Message] = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        sent = sender = body = None
        if m := _PIPE.match(line):
            sent = datetime.strptime(f"{m[1]} {m[2]}", "%Y-%m-%d %H:%M")
            sender, body = m[3], m[4]
        elif m := (_WA_IOS.match(line) or _WA_ANDROID.match(line)):
            sent = _wa_datetime(m[1], m[2], m[3], m[4], m[5], day_first)
            sender, body = m[6], m[7]
        if sent is None:
            if messages:
                messages[-1].text += "\n" + line.strip()
            continue
        messages.append(Message("", sent, sender.strip(), body.strip()))
    messages.sort(key=lambda msg: msg.sent)  # stable: keeps file order for equal timestamps
    width = max(2, len(str(len(messages))))
    for i, msg in enumerate(messages, 1):
        msg.id = f"m{i:0{width}d}"
    mark_duplicates(messages)
    return messages


def parse_roster(text: str) -> list[str]:
    names = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    seen, out = set(), []
    for n in names:
        if n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return out
