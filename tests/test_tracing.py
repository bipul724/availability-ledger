"""Opt-in Sentry tracing (INT-03, D-33): off and import-free without SENTRY_DSN or sentry-sdk, never on in demo mode,
and nothing but allowlisted structure leaves the process. Two allowlists guard that: scrub() (before_send_transaction)
and clean_envelope() (the last step before the transport); each is tested alone, and with both off a leak shows. The leak test uses invented sensitive strings, a capturing
test transport and no DSN, so nothing is sent anywhere. It needs sentry-sdk and is skipped without it:
    .venv/bin/python -m unittest tests.test_tracing        # with requirements-tracing.txt installed
Run all: python3 -m unittest discover -s tests"""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ledger import tracing  # noqa: E402

HAS_SDK = importlib.util.find_spec("sentry_sdk") is not None
# Invented, and written so that any copy of message content, names, quotes, replies or error text would show up.
NAME, PHONE, ADDRESS = "Zebulon Quarrington", "+44 7700 900123", "17 Larkspur Mews"
SECRETS = [NAME, PHONE, ADDRESS, "Quarrington", "7700 900123", "Larkspur", "PROMPTSECRET", "REPLYSECRET", "ERRORSECRET",
           "LOGSECRET"]
TEXT = f"Tuesday 10-12 works. {NAME} here, {PHONE}, {ADDRESS}"
SAID = [{"person": "SENDER", "day_text": "Tuesday", "time_text": "10-12", "status": "available", "condition": "",
         "replaces_earlier": False, "excerpt": f"Tuesday 10-12 works. {NAME}"}]
STATS = {"wall_s": 1.5, "prompt_tokens": 1400, "output_tokens": 80, "prompt_s": 0.5, "output_s": 0.9, "load_s": 12.0,
         "json_ok": True, "raw": "REPLYSECRET " + json.dumps({"claims": SAID})}


def run_python(code: str, env: dict, python=sys.executable) -> subprocess.CompletedProcess:
    env = {**{k: v for k, v in os.environ.items() if k not in ("SENTRY_DSN", "LEDGER_DEMO", "PORT")}, **env,
           "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([python, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)


class Scrub(unittest.TestCase):
    """The allowlist rebuild, on an event that carries every kind of content it could pick up."""

    def test_only_allowlisted_structure_survives(self):
        event = {
            "type": "transaction", "transaction": TEXT, "server_name": "zebulons-laptop", "user": {"username": NAME},
            "tags": {"who": NAME}, "extra": {"msg": TEXT}, "request": {"data": TEXT}, "modules": {"x": "1"},
            "breadcrumbs": {"values": [{"message": "LOGSECRET " + TEXT}]},
            "contexts": {"trace": {"trace_id": "a" * 32, "span_id": "b" * 16, "op": "gen_ai.invoke_agent",
                                   "data": {"ledger.reader": "hybrid", "gen_ai.input.messages": TEXT, "thread.name": NAME,
                                            "dynamic_sampling_context": None},
                                   "dynamic_sampling_context": {"trace_id": "a" * 32, "transaction": TEXT, "release": "r"}},
                         "os": {"name": "x"}, "device": {"name": NAME}},
            "spans": [{"op": "gen_ai.chat", "description": f"chat {NAME}", "span_id": "c" * 16, "tags": {"q": ADDRESS},
                       "data": {"gen_ai.request.model": "gemma4:e2b-it-qat", "gen_ai.usage.input_tokens": 10,
                                "gen_ai.output.messages": "REPLYSECRET", "gen_ai.system_instructions": "PROMPTSECRET",
                                "error.type": "ERRORSECRET: " + ADDRESS, "ledger.reader": NAME, "ledger.claim_count": "3",
                                "ledger.json_ok": True}}],
        }
        out = tracing.scrub(event)
        text = json.dumps(out)
        for secret in SECRETS + ["zebulons-laptop"]:
            self.assertNotIn(secret, text)
        self.assertEqual(out["spans"][0]["data"], {"gen_ai.request.model": "gemma4:e2b-it-qat", "gen_ai.usage.input_tokens": 10,
                                                   "ledger.json_ok": True})
        self.assertEqual(out["spans"][0]["description"], "gen_ai.chat")  # a name that is not ours is replaced
        self.assertEqual(out["contexts"]["trace"]["data"], {"ledger.reader": "hybrid"})
        self.assertEqual(out["transaction"], "ledger transaction")
        self.assertEqual(set(out), {"type", "event_id", "platform", "transaction", "transaction_info", "start_timestamp",
                                    "timestamp", "release", "environment", "sdk", "contexts", "spans"})

    def test_anything_but_a_transaction_is_dropped(self):
        self.assertIsNone(tracing.scrub({"type": "error", "message": TEXT}))
        self.assertIsNone(tracing.scrub({"message": TEXT}))


class OffByDefault(unittest.TestCase):
    def test_without_a_dsn_nothing_is_imported_and_every_call_is_a_no_op(self):
        r = run_python("import sys\nfrom ledger import tracing\nassert tracing.init() is False and not tracing.enabled()\n"
                       "h, last = tracing.Runs().get({'id': 'x', 'index': 1, 'total': 1}, 'hybrid', 'm', 3)\n"
                       "assert h is tracing.OFF and last is False\n"
                       "with tracing.transaction('gen_ai.invoke_agent', 'invoke_agent a') as t, tracing.model_call(t, 'm', 1) as s:\n"
                       "    s.set(ledger__claim_count=1); tracing.record_stats(s, {}, 'm', 0)\n"
                       "tracing.flush()\nimport server\nprint('sentry_sdk' in sys.modules)", {})
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "False"), r.stderr)

    def test_with_a_dsn_but_sentry_sdk_hidden_the_core_still_runs(self):
        python = str(ROOT / ".venv" / "bin" / "python") if (ROOT / ".venv" / "bin" / "python").exists() else sys.executable
        code = ("import sys\nsys.modules['sentry_sdk'] = None  # hidden: importing it raises ImportError\n"
                "from ledger import tracing\nassert tracing.init() is False\n"
                "import server\n"
                "out = server.suggest({'message': {'id': 'm01', 'sent': '2026-11-03 09:00', 'sender': 'Ana Example',"
                " 'text': 'Tuesday 10-12 works', 'duplicate_of': None}, 'roster': ['Ana Example'], 'week_start': '2026-11-09',"
                " 'timezone': 'Europe/London', 'extractor': 'rules', 'run': {'id': 'x', 'index': 1, 'total': 1}})\n"
                "print(len(out['claims']))")
        r = run_python(code, {"SENTRY_DSN": "https://public@sentry.invalid/1"}, python)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "1"), r.stderr)

    def test_demo_mode_is_never_traced(self):
        # The replay branch of server.py starts before tracing.init(); a DSN in its environment changes nothing.
        src = (ROOT / "server.py").read_text()
        main = src[src.index('if __name__ == "__main__":'):]
        self.assertLess(main.index("if DEMO:"), main.index("tracing.init()"))
        self.assertIn("serve_forever()\n    if tracing.init()", main)


@unittest.skipUnless(HAS_SDK, "sentry-sdk is not installed (optional: .venv with requirements-tracing.txt)")
class NoContentLeaves(unittest.TestCase):
    """Real server and evaluation code paths, traced into a capturing transport; every byte of every envelope is searched."""

    @classmethod
    def setUpClass(cls):
        from sentry_sdk.transport import Transport

        class Capture(Transport):
            def __init__(self):
                super().__init__({})
                self.envelopes = []

            def capture_envelope(self, envelope):
                self.envelopes.append(envelope)

        cls.transport = Capture()
        assert tracing.init({}, transport=cls.transport)  # no DSN: the test transport is the only destination

    @classmethod
    def tearDownClass(cls):
        import sentry_sdk
        sentry_sdk.init()  # back to a client with no destination
        tracing._sdk = None

    def test_server_run_and_ledger_send_structure_only(self):
        import logging
        import server
        sys.path.insert(0, str(ROOT / "tests"))
        from test_demo_mode import Http

        messages = [{"id": f"m0{i}", "sent": f"2026-11-03 0{i}:00", "sender": NAME, "text": TEXT.replace("10-12", f"{i}-{i + 2}"),
                     "duplicate_of": None} for i in (1, 2, 3)]
        base = {"roster": [NAME], "week_start": "2026-11-09", "timezone": "Europe/London", "model": "gemma4:e2b-it-qat"}
        calls = iter([(SAID, dict(STATS)), ValueError(f"ERRORSECRET {NAME} {ADDRESS}"), (SAID, {**STATS, "json_ok": False})])

        def extract(msg, week, model_name):
            import sentry_sdk
            logging.getLogger("ledger").warning("LOGSECRET %s", msg.text)  # a log line must not become a breadcrumb
            # Careless instrumentation, as a future change might add it: the allowlists must still stop all of it.
            span = sentry_sdk.get_current_span()  # the chat span, which the SDK sends as a streamed v2 item
            assert span.op == "gen_ai.chat"
            tracing.Handle(span).set(custom__key=msg.text, ledger__note=NAME)  # unapproved keys through Handle.set
            span.set_data("custom.raw", msg.text)  # ... and through raw set_data
            span.set_data("ledger.reader", msg.text)  # an approved key with a message-text value
            span.set_data("gen_ai.input.messages", "PROMPTSECRET " + msg.text)
            span.set_data("gen_ai.output.messages", STATS["raw"])
            span.set_tag("sender", msg.sender)
            sentry_sdk.set_user({"username": NAME, "email": "zq@example.invalid"})
            sentry_sdk.set_extra("message", msg.text)
            sentry_sdk.set_tag("address", ADDRESS)
            sentry_sdk.add_breadcrumb(message="LOGSECRET " + msg.text)
            sentry_sdk.capture_message("ERRORSECRET " + msg.text)
            nxt = next(calls)
            if isinstance(nxt, Exception):
                raise nxt
            return nxt

        before = len(self.transport.envelopes)
        http = Http()
        try:
            with mock.patch.object(server.model, "extract", side_effect=extract), \
                    contextlib.redirect_stderr(io.StringIO()):
                codes = [http("/api/suggest", {**base, "message": m, "extractor": "hybrid",
                                               "run": {"id": "run-1", "index": i, "total": 3}})[0]
                         for i, m in enumerate(messages, 1)]
                claims = [{"id": "m01.1", "msg": "m01", "n": 1, "source": "model", "review": "accepted", "said": SAID[0]}]
                payload = {**base, "messages": messages, "claims": claims, "reviewed_messages": ["m01"]}
                resolve, export = http("/api/resolve", payload), http("/api/export", payload)
        finally:
            http.close()
        self.assertEqual(codes, [200, 400, 200])
        self.assertIn(NAME, export[1]["csv"])  # the content really went through the traced code paths
        self.assertEqual(resolve[0], 200)

        tracing.flush()
        envelopes = self.transport.envelopes[before:]
        text = b"".join(e.serialize() for e in envelopes).decode("utf-8", "replace")
        for secret in SECRETS + ["m01", "m02", "m03", "run-1", "zq@example.invalid", "custom.key", "custom.raw", "ledger.note"]:
            self.assertNotIn(secret, text)
        items = [(i.type, i.payload.json) for e in envelopes for i in e.items]
        self.assertNotIn("event", [t for t, _ in items])  # no error events
        agent = [p for t, p in items if t == "transaction" and p["transaction"] == "invoke_agent availability-reader"]
        self.assertEqual(len(agent), 1)  # one agent span for the whole run
        self.assertEqual({s["op"] for s in agent[0]["spans"]}, {"ledger.hybrid_merge"})
        chats = [s for t, p in items if t == "span" for s in p["items"] if s["name"] == "chat gemma4:e2b-it-qat"]
        self.assertEqual(len(chats), 3)
        a = chats[0]["attributes"]
        self.assertEqual((a["gen_ai.usage.input_tokens"]["value"], a["gen_ai.usage.total_tokens"]["value"],
                          a["ledger.load_s"]["value"], a["ledger.json_ok"]["value"], a["ledger.message_position"]["value"]),
                         (1400, 1480, 12.0, True, 1))
        failed = [s for s in chats if s["status"] == "error"]
        self.assertEqual([s["attributes"]["error.type"]["value"] for s in failed], ["ValueError"])
        ledger = [p for t, p in items if t == "transaction" and p["transaction"] == "ledger request"]
        self.assertEqual(len(ledger), 2)  # resolve and export after the run, each its own small transaction
        self.assertEqual([s["op"] for s in ledger[1]["spans"]], ["ledger.resolve", "ledger.confirmed_export", "ledger.export"])

    def test_evaluation_run_sends_structure_only(self):
        from evaluation import run
        from ledger.messages import parse_messages
        from ledger.resolve import Calendar
        from datetime import date

        msgs = parse_messages(f"2026-11-03 09:00 | {NAME} | {TEXT}\n")
        ref = {"split": {"heldout": []}, "withdrawals": [], "conditions": [], "ambiguities": [], "expected_sheet": {},
               "messages": {"m01": {"category": ["basic"], "claims": [
                   {"person": NAME, "dates": ["2026-11-10"], "start": "10:00", "end": "12:00", "status": "available"}]}}}
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(run, "RUNS", Path(tmp) / "runs"), \
                mock.patch.object(run, "load", return_value=(msgs, [NAME], Calendar(date(2026, 11, 9)), ref)), \
                mock.patch.object(run, "MemorySampler", side_effect=AssertionError("not with --cache-only")), \
                mock.patch.object(run.model_mod, "extract", return_value=(SAID, dict(STATS))), \
                mock.patch.object(sys, "argv", ["run", "--extractor", "hybrid", "--cache-only", "--out", tmp]), \
                contextlib.redirect_stdout(io.StringIO()):
            (Path(tmp) / "runs" / "gemma4_e2b_it_qat_prompt3").mkdir(parents=True)
            (Path(tmp) / "runs" / "gemma4_e2b_it_qat_prompt3" / "m01.json").write_text(json.dumps({"claims": SAID, "stats": STATS}))
            before = len(self.transport.envelopes)
            run.main()
        text = b"".join(e.serialize() for e in self.transport.envelopes[before:]).decode()
        for secret in SECRETS + ["m01"]:
            self.assertNotIn(secret, text)
        t = [i.payload.json for e in self.transport.envelopes[before:] for i in e.items if i.type == "transaction"]
        self.assertEqual([x["transaction"] for x in t], ["invoke_agent availability-reader"])
        self.assertEqual([s["op"] for s in t[0]["spans"]], ["ledger.hybrid_merge", "ledger.score", "ledger.build_ledger"])
        self.assertEqual(t[0]["contexts"]["trace"]["data"]["ledger.reader"], "hybrid")



@unittest.skipUnless(HAS_SDK, "sentry-sdk is not installed (optional: .venv with requirements-tracing.txt)")
class EachAllowlistAlone(unittest.TestCase):
    """A chat span carrying unapproved keys and message text, with each allowlist switched off in turn."""

    def capture(self, scrub_on=True, clean_on=True):
        from sentry_sdk.transport import Transport

        class Capture(Transport):
            def __init__(self):
                super().__init__({})
                self.envelopes = []

            def capture_envelope(self, envelope):
                self.envelopes.append(envelope)

        t = Capture()
        with mock.patch.object(tracing, "transaction_hook", tracing.transaction_hook if scrub_on else (lambda e, h: e)), \
                mock.patch.object(tracing, "clean_envelope", tracing.clean_envelope if clean_on else (lambda e: e)):
            tracing._sdk = None
            tracing.init({}, transport=t)
            with tracing.transaction("gen_ai.invoke_agent", f"invoke_agent {tracing.AGENT}") as run_h:
                with tracing.model_call(run_h, "gemma4:e2b-it-qat", 1) as h:
                    tracing.record_stats(h, STATS, "gemma4:e2b-it-qat", 1)
                    h.set(custom__key=TEXT, ledger__note=NAME, ledger__reader=TEXT)
                    h.span.set_data("custom.raw", TEXT)
                    h.span.set_data("gen_ai.input.messages", "PROMPTSECRET " + TEXT)
            tracing.flush()
        text = b"".join(e.serialize() for e in t.envelopes).decode("utf-8", "replace")
        chats = [s for e in t.envelopes for i in e.items if i.type == "span" for s in i.payload.json["items"]]
        return text, chats

    @classmethod
    def tearDownClass(cls):
        import sentry_sdk
        sentry_sdk.init()
        tracing._sdk = None

    def leaked(self, text):
        return [x for x in SECRETS + ["custom.key", "custom.raw", "ledger.note", "Tuesday 10-12"] if x in text]

    def test_both_on(self):
        text, chats = self.capture()
        self.assertEqual(self.leaked(text), [])
        self.assertEqual(len(chats), 1)  # the chat span still goes out as a streamed item (Agents view)
        a = chats[0]["attributes"]
        self.assertEqual((a["gen_ai.usage.input_tokens"]["value"], a["ledger.load_s"]["value"], a["ledger.message_position"]["value"]),
                         (1400, 12.0, 1))
        self.assertNotIn("ledger.reader", a)  # approved key, but a prose value: dropped
        self.assertLessEqual(set(a), set(tracing.ALLOWED_DATA) | set(tracing.STRUCTURAL))

    def test_transport_cleaner_alone_stops_streamed_span_leaks(self):
        text, chats = self.capture(scrub_on=False)
        self.assertEqual(self.leaked(text), [])
        self.assertEqual(chats[0]["attributes"]["gen_ai.usage.output_tokens"]["value"], 80)

    def test_scrub_alone_covers_chat_spans_in_this_sdk(self):
        # sentry-sdk 2.72 splits gen_ai spans out of the transaction only after before_send_transaction. If a future
        # SDK sends them some other way, this canary fails (and clean_envelope still protects).
        text, chats = self.capture(clean_on=False)
        self.assertEqual(self.leaked(text), [])
        self.assertEqual(len(chats), 1)

    def test_with_both_off_the_leak_is_detected(self):
        text, _ = self.capture(scrub_on=False, clean_on=False)
        self.assertIn(NAME, text)  # so the assertions above would catch a leak: the SDK itself does not drop these
        self.assertIn("custom.raw", text)

    def test_clean_envelope_output_directly(self):
        from sentry_sdk.envelope import Envelope, Item, PayloadRef
        good = {"trace_id": "a" * 32, "span_id": "b" * 16, "parent_span_id": "c" * 16, "name": "chat gemma4:e2b-it-qat",
                "status": "ok", "is_segment": False, "start_timestamp": 1.0, "end_timestamp": 2.0, "user": NAME,
                "attributes": {"sentry.op": {"value": "gen_ai.chat", "type": "string"},
                               "gen_ai.usage.input_tokens": {"value": 10, "type": "integer"},
                               "ledger.json_ok": {"value": True, "type": "boolean"},
                               "ledger.reader": {"value": TEXT, "type": "string"},
                               "custom.key": {"value": TEXT, "type": "string"},
                               "user.name": {"value": NAME, "type": "string"},
                               "sentry.release": {"value": "something-else", "type": "string"},
                               "sentry.segment.name": {"value": TEXT, "type": "string"},
                               "thread.name": {"value": NAME, "type": "string"}}}
        renamed = {**good, "span_id": "d" * 16, "name": f"chat {NAME}"}
        unnamed = {**good, "span_id": "e" * 16, "name": TEXT, "attributes": {}}
        bad_ids = {**good, "trace_id": NAME}
        env = Envelope(headers={"event_id": "f" * 32, "sent_at": "2026-10-21T00:00:00Z", "dsn": "x", "user": NAME,
                                "trace": {"trace_id": "a" * 32, "transaction": TEXT, "release": "r", "user_id": NAME}},
                       items=[Item(payload=PayloadRef(json={"version": 2, "items": [good, renamed, unnamed, bad_ids]}), type="span"),
                              Item(payload=PayloadRef(json={"message": TEXT}), type="event"),
                              Item(payload=TEXT.encode(), type="attachment")])
        out = tracing.clean_envelope(env)
        self.assertNotIn(NAME, out.serialize().decode())
        self.assertEqual(out.headers, {"event_id": "f" * 32, "sent_at": "2026-10-21T00:00:00Z",
                                       "trace": {"trace_id": "a" * 32, "release": "r"}})
        self.assertEqual([i.type for i in out.items], ["span"])
        spans = out.items[0].payload.json["items"]
        self.assertEqual([(sp["span_id"], sp["name"]) for sp in spans], [("b" * 16, "chat gemma4:e2b-it-qat"), ("d" * 16, "gen_ai.chat")])
        self.assertEqual(spans[0]["attributes"], {"sentry.op": {"value": "gen_ai.chat", "type": "string"},
                                                  "gen_ai.usage.input_tokens": {"value": 10, "type": "integer"},
                                                  "ledger.json_ok": {"value": True, "type": "boolean"}})
        self.assertEqual(set(spans[0]) - {"attributes"}, {"trace_id", "span_id", "parent_span_id", "name", "status", "is_segment",
                                                          "start_timestamp", "end_timestamp"})
        self.assertIsNone(tracing.clean_envelope(Envelope(items=[Item(payload=PayloadRef(json={"m": TEXT}), type="event")])))

    def test_static_lifecycle_and_no_span_hook(self):
        import sentry_sdk
        self.capture()
        options = sentry_sdk.get_client().options
        self.assertEqual((options["trace_lifecycle"], options["before_send_span"], options["stream_gen_ai_spans"]),
                         ("static", None, True))
        self.assertEqual(type(sentry_sdk.get_client().transport).__name__, "CleaningTransport")


if __name__ == "__main__":
    unittest.main()
