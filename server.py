"""Local review app. Standard library only; binds to 127.0.0.1.

    python3 server.py            # then open http://127.0.0.1:8765
    LEDGER_DEMO=1 PORT=10000 python3 server.py   # hosted read-only replay (DEP-02): binds 0.0.0.0:$PORT

Demo mode replays fictional set A with saved Gemma outputs: it never calls Ollama and refuses any message, roster,
week or model it did not serve itself.

    SENTRY_DSN=... .venv/bin/python server.py   # opt-in tracing (INT-03): structural metadata only, never in demo mode
"""
from __future__ import annotations

import json
import os
import sys
from contextlib import contextmanager
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ledger import hybrid, model, rules, tracing
from ledger.core import build_ledger, resolve_all
from ledger.export import SUMMARY, confirmed_export, final_csv
from ledger.messages import Message, parse_messages, parse_roster
from ledger.resolve import Calendar

ROOT = Path(__file__).resolve().parent
UI = ROOT / "ui"
MAX_VOLUNTEERS = 20
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}
DEMO = os.environ.get("LEDGER_DEMO") == "1"
DEMO_MODEL = "gemma4:e2b-it-qat"
DEMO_RUNS = ROOT / "evaluation" / "runs" / "gemma4_e2b_it_qat_prompt3"  # saved set A outputs, prompt v3


RUNS = tracing.Runs()  # one agent span per browser suggest run when tracing is on (INT-03)


class Forbidden(Exception):
    """A demo-mode request for something the replay did not serve (HTTP 403)."""


def calendar(body: dict) -> Calendar:
    return Calendar(date.fromisoformat(body["week_start"]), body.get("timezone") or "America/New_York")


def saved_output(msg: Message) -> tuple[list, dict]:
    """Demo mode: the saved Gemma reply for a served set A message, in place of a model call."""
    data = json.loads((DEMO_RUNS / f"{msg.id}.json").read_text())
    return data["claims"], {**data["stats"], "saved": True}


def suggest(body: dict) -> dict:
    if DEMO:
        check_demo(body, messages=[body["message"]])
        if (body.get("model") or DEMO_MODEL) != DEMO_MODEL:
            raise Forbidden(f"the replay has saved outputs for {DEMO_MODEL} only")
    kind = body.get("extractor", "hybrid")
    model_name = body.get("model") or model.DEFAULT_MODEL
    run = body.get("run")  # {id, index, total} from the page: a random token and positions, used only for tracing
    parent, last = RUNS.get(run, kind, model_name, model.PROMPT_VERSION)
    try:
        return _suggest(body, kind, model_name, parent, run["index"] if parent.span else None)
    finally:
        if last:
            RUNS.finish(run)


def _suggest(body: dict, kind: str, model_name: str, parent: tracing.Handle, position: int | None) -> dict:
    msg = Message.from_dict(body["message"])
    if msg.duplicate_of:  # same text already read: no extraction call, no suggestions of its own
        return {"claims": [], "stats": {}, "duplicate_of": msg.duplicate_of}
    roster = body["roster"][:MAX_VOLUNTEERS]
    cal = calendar(body)
    week = f"Monday {cal.week_start:%d %B} to Sunday {cal.week_end:%d %B %Y}"
    stats, model_raw, rules_raw = {}, [], []
    if kind in ("model", "hybrid"):
        if DEMO:
            said, stats = saved_output(msg)
        else:
            with tracing.model_call(parent, model_name, position) as span:
                said, stats = model.extract(msg, week, model_name)
                tracing.record_stats(span, stats, model_name, len(said))
        stats.pop("raw", None)
        model_raw = [{"id": f"{msg.id}.{i}", "msg": msg.id, "n": i, "source": "model", "review": "pending", "said": s}
                     for i, s in enumerate(said, 1)]
    if kind in ("rules", "hybrid"):
        rules_raw = [{"id": f"{msg.id}.{i}", "msg": msg.id, "n": i, "source": "rules", "review": "pending", "said": s}
                     for i, s in enumerate(rules.extract(msg, roster), 1)]
    claims = {"model": model_raw, "rules": rules_raw}.get(kind)
    if claims is None:
        with tracing.stage(parent, "hybrid_merge", ledger__message_position=position) as span:
            claims = hybrid.merge([msg], model_raw, rules_raw, roster, cal, body.get("coordinators", []))
            span.set(ledger__claim_count=len(claims))
    return {"claims": claims, "stats": stats}


def _reviewed(body: dict) -> list[str]:
    reviewed = body.get("reviewed_messages") or []
    if not isinstance(reviewed, list) or not all(isinstance(x, str) for x in reviewed):
        raise ValueError("reviewed_messages must be a list of message ids")
    return reviewed


@contextmanager
def _ledger_span(name: str):
    """Ledger work joins the suggest run in progress, if any; otherwise it is its own small transaction."""
    current = RUNS.current()
    if current.span is not None:
        yield current
    else:
        with tracing.transaction(f"ledger.{name}", f"ledger {name}") as h:
            yield h


def _confirmed(body: dict, parent: tracing.Handle):
    if DEMO:
        check_demo(body, messages=body["messages"])
    messages = [Message.from_dict(m) for m in body["messages"]]
    roster = body["roster"][:MAX_VOLUNTEERS]
    cal = calendar(body)
    with tracing.stage(parent, "resolve", ledger__message_count=len(messages), ledger__claim_count=len(body["claims"])):
        resolved = resolve_all(messages, body["claims"], roster, cal, body.get("coordinators", []))
    with tracing.stage(parent, "confirmed_export"):
        exp = confirmed_export(messages, resolved, roster, cal, _reviewed(body))
    return messages, roster, cal, resolved, exp


def resolve(body: dict) -> dict:
    with _ledger_span("request") as parent:
        messages, roster, cal, resolved, exp = _confirmed(body, parent)
        with tracing.stage(parent, "build_ledger"):
            ledger = build_ledger(messages, resolved, roster, cal)
    return {"claims": resolved, "ledger": ledger, "confirmed": {k: exp[k] for k in SUMMARY}}


def export(body: dict) -> dict:
    with _ledger_span("request") as parent:
        *_, exp = _confirmed(body, parent)
        with tracing.stage(parent, "export"):
            filename, text = final_csv(exp)
    return {**{k: exp[k] for k in SUMMARY}, "rows": len(exp["rows"]), "filename": filename, "csv": text}


def demo() -> dict:
    fx = ROOT / "fixtures"
    ref = json.loads((fx / "reference.json").read_text())
    return {"text": (fx / "riverside_week.txt").read_text(), "roster": (fx / "roster.txt").read_text(),
            "week_start": ref["week_start"], "timezone": ref["timezone"]}


_served = None


def served() -> dict:
    """What demo mode serves: set A's parsed messages by id, its roster, week and timezone."""
    global _served
    if _served is None:
        d = demo()
        _served = {**d, "messages": {m.id: m.to_dict() for m in parse_messages(d["text"])},
                   "roster_list": parse_roster(d["roster"])[:MAX_VOLUNTEERS]}
    return _served


def check_demo(body: dict, messages: list) -> None:
    """Demo mode accepts only messages it served, unchanged, with the served roster, week and timezone."""
    s = served()
    for m in messages:
        if not isinstance(m, dict) or s["messages"].get(m.get("id")) != {k: m.get(k) for k in Message.__dataclass_fields__}:
            raise Forbidden("the replay only reads the fictional messages it served")
    if body.get("roster") != s["roster_list"] or body.get("week_start") != s["week_start"] \
            or body.get("timezone") != s["timezone"] or body.get("coordinators"):
        raise Forbidden("the replay only uses the fictional roster and week it served")


def parse(body: dict) -> dict:
    if DEMO and (body.get("text") != served()["text"] or body.get("roster") != served()["roster"] or body.get("day_first")):
        raise Forbidden("the replay does not read pasted messages; run the app locally to use your own")
    msgs = parse_messages(body.get("text", ""), bool(body.get("day_first")))
    return {"messages": [m.to_dict() for m in msgs], "roster": parse_roster(body.get("roster", ""))[:MAX_VOLUNTEERS]}


def status() -> dict:
    if DEMO:  # never contacts Ollama
        return {"models": [DEMO_MODEL], "default_model": DEMO_MODEL, "demo": True}
    return {"models": model.available_models(), "default_model": model.DEFAULT_MODEL}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json")

    def do_GET(self):
        if self.path == "/api/demo":
            return self._json(demo())
        if self.path == "/api/status":
            return self._json(status())
        name = "index.html" if self.path in ("/", "") else self.path.lstrip("/").split("?")[0]
        f = (UI / name).resolve()
        if UI in f.parents and f.is_file() and f.suffix in TYPES:
            return self._send(200, f.read_bytes(), TYPES[f.suffix])
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if self.path == "/api/parse":
                return self._json(parse(body))
            if self.path == "/api/suggest":
                return self._json(suggest(body))
            if self.path == "/api/resolve":
                return self._json(resolve(body))
            if self.path == "/api/export":
                return self._json(export(body))
            self._json({"error": "unknown endpoint"}, 404)
        except Forbidden as e:
            self._json({"error": str(e)}, 403)
        except Exception as e:  # report to the page instead of dropping the connection
            self._json({"error": f"{type(e).__name__}: {e}"}, 400)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    if DEMO:  # hosted replay: the host chooses the port and the server must listen on every interface
        port = int(os.environ.get("PORT") or port)
        print(f"Availability Ledger replay (fictional set A, saved Gemma outputs) on 0.0.0.0:{port}", flush=True)
        ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
    if tracing.init():  # the replay above is never traced: it makes no model calls
        print("Sentry tracing on: timings, token counts and model name only; no message text, names or replies")
    print(f"Availability Ledger on http://127.0.0.1:{port}  (Ctrl+C to stop)")
    try:
        ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
    finally:
        tracing.flush()
