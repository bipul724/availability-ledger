"""Opt-in Sentry tracing (INT-03, D-33). Off unless SENTRY_DSN is set and the optional sentry-sdk is installed
(requirements-tracing.txt); otherwise every function here is a no-op and sentry_sdk is never imported.

What leaves the machine is structural metadata only: span names and timings, model name, prompt version, token
counts, load time, JSON-ok flag, claim counts, reader kind, stage name, message position, error category and the
instrumentation version. Never message text, quotes, names, message IDs, prompts, replies or exception text.
Two allowlists, both ours:
- scrub(), run by transaction_hook (the SDK's before_send_transaction), rebuilds each transaction and all its spans. In sentry-sdk 2.72
  the gen_ai.* spans (the chat spans) are still in that transaction at this point; the SDK splits them out into
  streamed v2 span items only afterwards (client.capture_event, after _prepare_event).
- clean_envelope(), in a wrapper around the SDK's transport, is the last step before anything is sent. It rebuilds
  every streamed span item with the same rules (_value, NAME), runs scrub() on transactions again and drops every
  other item type, so the guarantee does not depend on that SDK ordering. Either layer alone stops a leak (tested).
(The SDK's before_send_span hook is not used: in 2.72 it runs only with trace_lifecycle="stream", which is pinned to
"static" here, and never for the streamed gen_ai items.) Breadcrumbs and error events are dropped, and the SDK's
default integrations (logging, HTTP clients, argv, modules, ...) are off.

Span names follow Sentry's manual AI-agent instrumentation (docs.sentry.io/platforms/python/agent-tracing/
manual-instrumentation): op gen_ai.invoke_agent "invoke_agent <agent>", op gen_ai.chat "chat <model>".
"""
from __future__ import annotations

import os
import re
import threading
import time
from contextlib import contextmanager

INSTRUMENTATION_VERSION = "1"
AGENT = "availability-reader"

# Span data kept, with the kind of value allowed. Strings must also match SAFE_STRING.
ALLOWED_DATA = {
    "gen_ai.operation.name": str, "gen_ai.agent.name": str, "gen_ai.provider.name": str,
    "gen_ai.request.model": str, "gen_ai.response.model": str,
    "gen_ai.usage.input_tokens": int, "gen_ai.usage.output_tokens": int, "gen_ai.usage.total_tokens": int,
    "error.type": str,
    "ledger.prompt_version": int, "ledger.load_s": float, "ledger.prompt_s": float, "ledger.output_s": float,
    "ledger.json_ok": bool, "ledger.claim_count": int, "ledger.reader": str, "ledger.stage": str,
    "ledger.message_position": int, "ledger.message_count": int, "ledger.instrumentation_version": str,
}
SAFE_STRING = re.compile(r"^[A-Za-z0-9_.:/\-]{1,100}$")  # identifiers such as model names; no spaces, so no prose
SPAN_KEYS = ("trace_id", "span_id", "parent_span_id", "same_process_as_parent", "op", "description",
             "start_timestamp", "timestamp", "status", "origin")
TRACE_KEYS = ("trace_id", "span_id", "parent_span_id", "op", "status", "origin")
DSC_KEYS = ("trace_id", "environment", "release", "public_key", "org_id", "sample_rate", "sampled", "sample_rand")
NAME = re.compile(r"^(?:invoke_agent|chat|ledger) [A-Za-z0-9_.:/\-]{1,100}$")  # span and transaction names we create
RELEASE = f"availability-ledger-tracing@{INSTRUMENTATION_VERSION}"
HEX16, HEX32 = re.compile(r"^[0-9a-f]{16}$"), re.compile(r"^[0-9a-f]{32}$")
# Streamed (v2) span attributes the SDK adds itself and Sentry uses to place the span; kept only with these values.
STRUCTURAL = {"sentry.op": SAFE_STRING, "sentry.origin": SAFE_STRING, "sentry.release": re.compile(re.escape(RELEASE) + "$"),
              "sentry.environment": re.compile(r"^local$"), "sentry.segment.name": NAME, "sentry.segment.id": HEX16,
              "sentry.sdk.name": SAFE_STRING, "sentry.sdk.version": SAFE_STRING,
              "process.runtime.name": SAFE_STRING, "process.runtime.version": SAFE_STRING}
V2_TYPES = {bool: "boolean", int: "integer", float: "double", str: "string"}
_sdk = None  # the sentry_sdk module once tracing is on


def init(environ=os.environ, transport=None) -> bool:
    """Turn tracing on if SENTRY_DSN is set (or a test transport is given) and sentry-sdk imports. Returns whether it is on."""
    global _sdk
    dsn = environ.get("SENTRY_DSN") or None
    if not dsn and transport is None:
        return False
    try:
        import sentry_sdk
    except ImportError:
        return False
    sentry_sdk.init(
        dsn=dsn, transport=transport,
        traces_sample_rate=1.0, send_default_pii=False,  # the SDK calls this deprecated; data_collection below is its successor
        data_collection={"user_info": False, "http_bodies": [], "gen_ai": {"inputs": False, "outputs": False},
                         "database_query_data": False, "queues": False, "stack_frame_variables": False,
                         "frame_context_lines": 0},
        default_integrations=False, auto_enabling_integrations=False, integrations=[],
        max_breadcrumbs=0, before_breadcrumb=lambda crumb, hint: None,
        before_send=lambda event, hint: None,  # no error events: their exception text could hold message content
        before_send_transaction=lambda event, hint: transaction_hook(event, hint),
        include_local_variables=False, attach_stacktrace=False, include_source_context=False,
        send_client_reports=False, auto_session_tracking=False, enable_logs=False,
        propagate_traces=False, trace_propagation_targets=[], max_request_body_size="never",
        release=RELEASE, environment="local", server_name="local",
        trace_lifecycle="static",  # whole transactions through before_send_transaction, never span-by-span streaming
    )
    _wrap_transport(sentry_sdk.get_client())
    _sdk = sentry_sdk
    return True


def transaction_hook(event, hint):
    """First allowlist: the SDK's before_send_transaction hook (looked up at call time, so a test can switch it off)."""
    return scrub(event)


def _wrap_transport(client) -> None:
    """Route every envelope through clean_envelope() on its way to the SDK's own transport."""
    from sentry_sdk.transport import Transport

    inner = client.transport
    if inner is None:
        return

    class CleaningTransport(Transport):
        def __init__(self):
            super().__init__()
            self.parsed_dsn = inner.parsed_dsn

        def capture_envelope(self, envelope):
            cleaned = clean_envelope(envelope)  # looked up at call time, so a test can switch it off
            if cleaned is not None:
                inner.capture_envelope(cleaned)

        def flush(self, timeout, callback=None):
            return inner.flush(timeout, callback)

        def kill(self):
            return inner.kill()

        def record_lost_event(self, *args, **kwargs):
            return inner.record_lost_event(*args, **kwargs)

        def is_healthy(self):
            return inner.is_healthy()

    client.transport = CleaningTransport()


def enabled() -> bool:
    return _sdk is not None


def flush(timeout: float = 5.0) -> None:
    if _sdk:
        _sdk.flush(timeout=timeout)


def _value(key, value):
    kind = ALLOWED_DATA.get(key)
    if kind is None or isinstance(value, bool) != (kind is bool):
        return None
    if kind is bool:
        return value
    if kind is str:
        return value if isinstance(value, str) and SAFE_STRING.match(value) else None
    if kind is int:
        return value if isinstance(value, int) else None
    return round(float(value), 3) if isinstance(value, (int, float)) else None


def _data(data) -> dict:
    out = {}
    for k, v in (data or {}).items() if isinstance(data, dict) else ():
        v = _value(k, v)
        if v is not None:
            out[k] = v
    return out


def _span(s: dict) -> dict:
    out = {k: s[k] for k in SPAN_KEYS if k in s}
    if not (isinstance(out.get("description"), str) and NAME.match(out["description"])):
        out["description"] = out.get("op") if isinstance(out.get("op"), str) and SAFE_STRING.match(out["op"]) else "span"
    out["data"] = _data(s.get("data"))
    return out


def _dsc(dsc, name) -> dict:
    """The sampling context the SDK moves into the envelope header: ids, release, rates and our own span name."""
    out = {k: dsc[k] for k in DSC_KEYS if isinstance(dsc, dict) and isinstance(dsc.get(k), str)}
    if isinstance(name, str) and NAME.match(name):
        out["transaction"] = name
    return out


def scrub(event: dict) -> dict | None:
    """Rebuild a transaction from the allowlist. Anything not listed (tags, extra, user, request, breadcrumbs, host
    name, modules, contexts other than the trace) is dropped, and so is any span data key or value not allowed."""
    if not isinstance(event, dict) or event.get("type") != "transaction":
        return None
    trace = (event.get("contexts") or {}).get("trace") or {}
    name = event.get("transaction")
    sdk = event.get("sdk") or {}
    return {
        "type": "transaction", "event_id": event.get("event_id"), "platform": "python",
        "transaction": name if isinstance(name, str) and NAME.match(name) else "ledger transaction",
        "transaction_info": {"source": "custom"},
        "start_timestamp": event.get("start_timestamp"), "timestamp": event.get("timestamp"),
        "release": RELEASE, "environment": "local",
        "sdk": {"name": sdk.get("name"), "version": sdk.get("version")},
        "contexts": {"trace": {**{k: trace[k] for k in TRACE_KEYS if k in trace}, "data": _data(trace.get("data")),
                               **({"dynamic_sampling_context": _dsc(trace["dynamic_sampling_context"], name)}
                                  if "dynamic_sampling_context" in trace else {})}},
        "spans": [_span(s) for s in event.get("spans") or [] if isinstance(s, dict)],
    }


def _v2_attribute(key, attr):
    """One streamed-span attribute ({"value": v, "type": t}) if allowed, else None."""
    value = attr.get("value") if isinstance(attr, dict) else None
    if key in STRUCTURAL:
        return {"value": value, "type": "string"} if isinstance(value, str) and STRUCTURAL[key].match(value) else None
    value = _value(key, value)
    return None if value is None else {"value": value, "type": V2_TYPES[type(value)]}


def _v2_span(span) -> dict | None:
    """Rebuild one streamed (v2) span from the allowlist; None (dropped) if it cannot be cleaned."""
    if not (isinstance(span, dict) and isinstance(span.get("trace_id"), str) and HEX32.match(span["trace_id"])
            and isinstance(span.get("span_id"), str) and HEX16.match(span["span_id"])):
        return None
    attrs = span.get("attributes") if isinstance(span.get("attributes"), dict) else {}
    out = {"trace_id": span["trace_id"], "span_id": span["span_id"],
           "status": "error" if span.get("status") == "error" else "ok", "is_segment": span.get("is_segment") is True}
    if isinstance(span.get("parent_span_id"), str) and HEX16.match(span["parent_span_id"]):
        out["parent_span_id"] = span["parent_span_id"]
    for key in ("start_timestamp", "end_timestamp"):
        if isinstance(span.get(key), (int, float)) and not isinstance(span.get(key), bool):
            out[key] = span[key]
    op = (attrs.get("sentry.op") or {}).get("value") if isinstance(attrs.get("sentry.op"), dict) else None
    name = span.get("name")
    if isinstance(name, str) and NAME.match(name):
        out["name"] = name
    elif isinstance(op, str) and SAFE_STRING.match(op):
        out["name"] = op
    else:
        return None
    out["attributes"] = {k: a for k, a in ((k, _v2_attribute(k, v)) for k, v in attrs.items()) if a is not None}
    return out


def clean_envelope(envelope):
    """The last allowlist before anything is sent: transactions through scrub() again, streamed span items rebuilt
    span by span, every other item type (error events, attachments, sessions, logs, profiles, ...) dropped.
    Returns a new envelope, or None if nothing is left to send."""
    from sentry_sdk.envelope import Envelope, Item, PayloadRef

    items = []
    for item in envelope.items:
        data = item.payload.json
        if item.type == "transaction":
            cleaned = scrub(data)
            if cleaned is not None:
                items.append(Item(payload=PayloadRef(json=cleaned), type="transaction"))
        elif item.type == "span" and isinstance(data, dict) and isinstance(data.get("items"), list):
            spans = [c for c in (_v2_span(sp) for sp in data["items"]) if c is not None]
            if spans:
                items.append(Item(payload=PayloadRef(json={"version": 2, "items": spans}), type="span",
                                  content_type=item.headers.get("content_type"), headers={"item_count": len(spans)}))
    if not items:
        return None
    headers = envelope.headers
    out = {k: headers[k] for k in ("event_id", "sent_at") if isinstance(headers.get(k), str)}
    if isinstance(headers.get("trace"), dict):
        out["trace"] = _dsc(headers["trace"], headers["trace"].get("transaction"))
    return Envelope(headers=out, items=items)


# ---------------------------------------------------------------- handles used at the call sites

class Handle:
    """A span (or transaction) that may be off. set() records allowlisted data; child() opens a nested span."""

    def __init__(self, span=None):
        self.span = span

    def set(self, **data) -> None:
        if self.span is not None:
            for key, value in data.items():
                self.span.set_data(key.replace("__", "."), value)

    @contextmanager
    def child(self, op: str, name: str, **data):
        if self.span is None:
            yield OFF
            return
        with self.span.start_child(op=op, name=name) as span:
            h = Handle(span)
            h.set(**data)
            try:
                yield h
            except Exception as e:  # category only: the exception's text could quote a message
                h.set(error__type=type(e).__name__)
                raise


OFF = Handle()


def _start(op: str, name: str, **data) -> Handle:
    t = _sdk.start_transaction(op=op, name=name, source="custom")
    h = Handle(t)
    if op.startswith("gen_ai."):
        data.setdefault("gen_ai__operation__name", op.removeprefix("gen_ai."))
    h.set(ledger__instrumentation_version=INSTRUMENTATION_VERSION, **data)
    return h


@contextmanager
def transaction(op: str, name: str, **data):
    """A top-level span for work that is not part of a browser suggest run (an evaluation run, a lone request)."""
    if not _sdk:
        yield OFF
        return
    h = _start(op, name, **data)
    try:
        yield h
    except Exception as e:
        h.set(error__type=type(e).__name__)
        h.span.set_status("internal_error")
        raise
    finally:
        h.span.finish()


def agent_run(reader: str, model: str | None, message_count: int, prompt_version: int) -> Handle:
    """Open the agent span for one suggest run (gen_ai.invoke_agent)."""
    if not _sdk:
        return OFF
    data = {"gen_ai__agent__name": AGENT, "ledger__reader": reader, "ledger__message_count": message_count}
    if reader != "rules":
        data.update(gen_ai__request__model=model, ledger__prompt_version=prompt_version)
    return _start("gen_ai.invoke_agent", f"invoke_agent {AGENT}", **data)


class Runs:
    """The browser reads a week as one request per message. The page sends a random run token with the message's
    position and the number of requests, so those requests share one agent span. Content-free by construction."""

    STALE_S = 600

    def __init__(self):
        self.lock, self.open = threading.Lock(), {}

    def get(self, run, reader, model, prompt_version) -> tuple[Handle, bool]:
        """(handle, last): the run's span, and whether this request is its last."""
        if not _sdk or not isinstance(run, dict) or not isinstance(run.get("id"), str):
            return OFF, False
        index, total = run.get("index"), run.get("total")
        if not (isinstance(index, int) and isinstance(total, int) and 1 <= index <= total):
            return OFF, False
        with self.lock:
            now = time.time()
            for key, (h, seen) in list(self.open.items()):
                if key != run["id"] and (index == 1 or now - seen > self.STALE_S):  # abandoned: close, marked cancelled
                    h.span.set_status("cancelled")
                    h.span.finish()
                    del self.open[key]
            if run["id"] not in self.open:
                self.open[run["id"]] = (agent_run(reader, model, total, prompt_version), now)
            h = self.open[run["id"]][0]
            self.open[run["id"]] = (h, now)
            return h, index == total

    def current(self) -> Handle:
        """The run in progress, if any (resolve calls during a run belong to it)."""
        with self.lock:
            return next(iter(self.open.values()))[0] if self.open else OFF

    def finish(self, run) -> None:
        with self.lock:
            h, _ = self.open.pop(run["id"], (OFF, 0))
        if h.span is not None:
            h.span.finish()


def model_call(parent: Handle, model: str, position: int | None):
    """The gen_ai.chat span around one model call; the caller adds the returned stats with record_stats."""
    data = {"gen_ai__provider__name": "ollama", "gen_ai__request__model": model}
    if position is not None:
        data["ledger__message_position"] = position
    return parent.child("gen_ai.chat", f"chat {model}", gen_ai__operation__name="chat", **data)


def record_stats(h: Handle, stats: dict, model: str, claims: int) -> None:
    i, o = stats.get("prompt_tokens"), stats.get("output_tokens")
    h.set(gen_ai__response__model=model, ledger__claim_count=claims, ledger__json_ok=bool(stats.get("json_ok")),
          ledger__load_s=stats.get("load_s"), ledger__prompt_s=stats.get("prompt_s"), ledger__output_s=stats.get("output_s"))
    if isinstance(i, int) and isinstance(o, int):
        h.set(gen_ai__usage__input_tokens=i, gen_ai__usage__output_tokens=o, gen_ai__usage__total_tokens=i + o)


def stage(parent: Handle, name: str, **data):
    """A ledger stage: hybrid_merge, resolve, build_ledger, export."""
    return parent.child(f"ledger.{name}", f"ledger {name}", ledger__stage=name, **data)
