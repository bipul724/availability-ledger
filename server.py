"""Local review app. Standard library only; binds to 127.0.0.1.

    python3 server.py            # then open http://127.0.0.1:8765
"""
from __future__ import annotations

import json
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ledger import hybrid, model, rules
from ledger.core import build_ledger, resolve_all
from ledger.messages import Message, parse_messages, parse_roster
from ledger.resolve import Calendar

ROOT = Path(__file__).resolve().parent
UI = ROOT / "ui"
MAX_VOLUNTEERS = 20
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}


def calendar(body: dict) -> Calendar:
    return Calendar(date.fromisoformat(body["week_start"]), body.get("timezone") or "America/New_York")


def suggest(body: dict) -> dict:
    msg = Message.from_dict(body["message"])
    if msg.duplicate_of:  # same text already read: no extraction call, no suggestions of its own
        return {"claims": [], "stats": {}, "duplicate_of": msg.duplicate_of}
    roster = body["roster"][:MAX_VOLUNTEERS]
    cal = calendar(body)
    kind = body.get("extractor", "hybrid")
    week = f"Monday {cal.week_start:%d %B} to Sunday {cal.week_end:%d %B %Y}"
    stats, model_raw, rules_raw = {}, [], []
    if kind in ("model", "hybrid"):
        said, stats = model.extract(msg, week, body.get("model") or model.DEFAULT_MODEL)
        stats.pop("raw", None)
        model_raw = [{"id": f"{msg.id}.{i}", "msg": msg.id, "n": i, "source": "model", "review": "pending", "said": s}
                     for i, s in enumerate(said, 1)]
    if kind in ("rules", "hybrid"):
        rules_raw = [{"id": f"{msg.id}.{i}", "msg": msg.id, "n": i, "source": "rules", "review": "pending", "said": s}
                     for i, s in enumerate(rules.extract(msg, roster), 1)]
    claims = {"model": model_raw, "rules": rules_raw}.get(kind) or \
        hybrid.merge([msg], model_raw, rules_raw, roster, cal, body.get("coordinators", []))
    return {"claims": claims, "stats": stats}


def resolve(body: dict) -> dict:
    messages = [Message.from_dict(m) for m in body["messages"]]
    roster = body["roster"][:MAX_VOLUNTEERS]
    cal = calendar(body)
    resolved = resolve_all(messages, body["claims"], roster, cal, body.get("coordinators", []))
    return {"claims": resolved, "ledger": build_ledger(messages, resolved, roster, cal)}


def demo() -> dict:
    fx = ROOT / "fixtures"
    ref = json.loads((fx / "reference.json").read_text())
    return {"text": (fx / "riverside_week.txt").read_text(), "roster": (fx / "roster.txt").read_text(),
            "week_start": ref["week_start"], "timezone": ref["timezone"]}


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
            return self._json({"models": model.available_models(), "default_model": model.DEFAULT_MODEL})
        name = "index.html" if self.path in ("/", "") else self.path.lstrip("/").split("?")[0]
        f = (UI / name).resolve()
        if UI in f.parents and f.is_file() and f.suffix in TYPES:
            return self._send(200, f.read_bytes(), TYPES[f.suffix])
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if self.path == "/api/parse":
                msgs = parse_messages(body.get("text", ""), bool(body.get("day_first")))
                return self._json({"messages": [m.to_dict() for m in msgs],
                                   "roster": parse_roster(body.get("roster", ""))[:MAX_VOLUNTEERS]})
            if self.path == "/api/suggest":
                return self._json(suggest(body))
            if self.path == "/api/resolve":
                return self._json(resolve(body))
            self._json({"error": "unknown endpoint"}, 404)
        except Exception as e:  # report to the page instead of dropping the connection
            self._json({"error": f"{type(e).__name__}: {e}"}, 400)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"Availability Ledger on http://127.0.0.1:{port}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
