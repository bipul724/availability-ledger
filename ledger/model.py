"""Ask a local open model (through Ollama) what each message says.

The model copies phrases; it never converts them to dates. JSON that parses is
only a proposal: core.resolve_claim checks every phrase against the message.
"""
from __future__ import annotations

import json
import time
import urllib.request

from .messages import Message

OLLAMA = "http://127.0.0.1:11434"
DEFAULT_MODEL = "gemma4:e2b-it-qat"
PROMPT_VERSION = 3  # bump whenever SYSTEM or EXAMPLES change; tuning log in evaluation/TUNING.md

SCHEMA = {
    "type": "object",
    "properties": {"claims": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "person": {"type": "string"},
            "day_text": {"type": "string"},
            "time_text": {"type": "string"},
            "status": {"type": "string", "enum": ["available", "unavailable", "conditional"]},
            "condition": {"type": "string"},
            "replaces_earlier": {"type": "boolean"},
            "excerpt": {"type": "string"},
        },
        "required": ["person", "day_text", "time_text", "status", "condition", "replaces_earlier", "excerpt"],
    }}},
    "required": ["claims"],
}

SYSTEM = """You read one message sent to a volunteer coordinator and list every statement about when a person can or cannot volunteer.

Return one claim per day mentioned. "Tuesday and Thursday mornings" is two claims.
- person: "SENDER" when it is about the writer; otherwise the other person's name exactly as written.
- day_text: copy the exact words that name the day ("Tuesday", "Weds", "tomorrow", "the 12th", "all week", "next Sunday", "one day this weekend"). Never convert to a date.
- time_text: copy the exact time words ("mornings", "9-12", "after 3", "10:30 to 1"), or "" if no time is given for that day.
- status: "available", "unavailable", or "conditional". Conditional means it depends on something unsettled: if..., might, maybe, if needed, one or the other, not sure, will confirm. A reaffirmed offer that was conditional stays conditional.
- condition: copy the words of the condition, or "".
- replaces_earlier: true only when the message changes an earlier answer for that same day (instead, correction, now, only ... now, change).
- excerpt: copy the shortest exact phrase from THIS message that supports the claim.

Only list what THIS message says.
An exception is its own claim: "all week except Friday" is an available claim for "all week" plus an unavailable claim for "Friday". Short negatives such as "Not Tuesday" or "Friday's off" are unavailable claims.
Politeness is not a condition: "just let me know", "if that helps", "hope that's ok" leave the status available.
Someone who offers to take another person's slot is talking about themselves (SENDER). A name that is only mentioned gets no claim.
"Still on for Saturday" with no time has time_text "".

Not availability, so no claim: questions about logistics, thanks, reminders, past events ("last Saturday"), deadlines ("will know by Tuesday"), and coordinator messages that describe shifts or say which days still need people."""

# Invented examples; none come from the evaluation fixture.
EXAMPLES = [
    ("Jamie Park", "Thursday 5 March 2026 18:02",
     "Tuesday 2-4 works, but not Thursday. Saturday maybe, if my sister can babysit.",
     [{"person": "SENDER", "day_text": "Tuesday", "time_text": "2-4", "status": "available", "condition": "",
       "replaces_earlier": False, "excerpt": "Tuesday 2-4 works"},
      {"person": "SENDER", "day_text": "Thursday", "time_text": "", "status": "unavailable", "condition": "",
       "replaces_earlier": False, "excerpt": "not Thursday"},
      {"person": "SENDER", "day_text": "Saturday", "time_text": "", "status": "conditional",
       "condition": "if my sister can babysit", "replaces_earlier": False,
       "excerpt": "Saturday maybe, if my sister can babysit"}]),
    ("Chris (organiser)", "Friday 6 March 2026 09:15",
     "Passing on Robin's text: 'I can do Friday morning.' Also, who has the van keys?",
     [{"person": "Robin", "day_text": "Friday", "time_text": "morning", "status": "available", "condition": "",
       "replaces_earlier": False, "excerpt": "I can do Friday morning"}]),
    ("Chris (organiser)", "Friday 6 March 2026 16:30",
     "Still short on Thursday afternoon and Saturday morning, anyone?",
     []),
    ("Jamie Park", "Saturday 7 March 2026 11:40",
     "Actually make Tuesday 3-4 instead. Loved last week's debrief!",
     [{"person": "SENDER", "day_text": "Tuesday", "time_text": "3-4", "status": "available", "condition": "",
       "replaces_earlier": True, "excerpt": "make Tuesday 3-4 instead"}]),
    ("Kim Osei", "Saturday 7 March 2026 12:01",
     "Is Jo still covering Friday evening? If not, I can do it. Could I also come Monday morning? Let me know!",
     [{"person": "SENDER", "day_text": "Friday", "time_text": "evening", "status": "conditional",
       "condition": "If not", "replaces_earlier": False, "excerpt": "If not, I can do it"},
      {"person": "SENDER", "day_text": "Monday", "time_text": "morning", "status": "available", "condition": "",
       "replaces_earlier": False, "excerpt": "Could I also come Monday morning?"}]),
    ("Dana Lee", "Saturday 7 March 2026 12:05",
     "Thanks! Do I need to bring gloves on Sunday?",
     []),
]


def _user_prompt(msg: Message, week: str, sent_label: str | None = None) -> str:
    return "\n".join([f"The coordinator is planning the week of {week}.",
                      f"Message sent {sent_label or msg.sent.strftime('%A %d %B %Y %H:%M')} by {msg.sender}.",
                      "Message:", f'"""{msg.text}"""'])


def build_messages(msg: Message, week: str) -> list[dict]:
    chat = [{"role": "system", "content": SYSTEM}]
    for sender, sent, text, claims in EXAMPLES:
        chat.append({"role": "user", "content": _user_prompt(Message("x", msg.sent, sender, text), "Monday 9 March 2026", sent)})
        chat.append({"role": "assistant", "content": json.dumps({"claims": claims})})
    chat.append({"role": "user", "content": _user_prompt(msg, week)})
    return chat


def extract(msg: Message, week: str, model: str = DEFAULT_MODEL,
            num_ctx: int = 4096, timeout: float = 300) -> tuple[list[dict], dict]:
    payload = {
        "model": model, "messages": build_messages(msg, week), "format": SCHEMA,
        "stream": False, "think": False, "keep_alive": "30m",
        "options": {"temperature": 0, "seed": 7, "num_ctx": num_ctx},
    }
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read())
    wall = time.time() - t0
    content = body.get("message", {}).get("content", "")
    stats = {
        "wall_s": round(wall, 2),
        "prompt_tokens": body.get("prompt_eval_count"),
        "output_tokens": body.get("eval_count"),
        "prompt_s": round((body.get("prompt_eval_duration") or 0) / 1e9, 2),
        "output_s": round((body.get("eval_duration") or 0) / 1e9, 2),
        "load_s": round((body.get("load_duration") or 0) / 1e9, 2),
        "raw": content,
    }
    try:
        claims = json.loads(content).get("claims", [])
        stats["json_ok"] = True
    except json.JSONDecodeError:
        claims, stats["json_ok"] = [], False
    return [c for c in claims if isinstance(c, dict)], stats


def available_models() -> list[str]:
    try:
        with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=2) as r:
            return [m["name"] for m in json.loads(r.read()).get("models", [])]
    except OSError:
        return []
