"""Hosted read-only replay (DEP-02, D-33): with LEDGER_DEMO=1 the server serves fictional set A only, answers
suggestions from saved Gemma outputs, never calls the model and refuses anything it did not serve. Without it nothing
changes. Rejected inputs are invented. Run: python3 -m unittest discover -s tests"""
import json
import os
import socket
import subprocess
import sys
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import server  # noqa: E402
from evaluation import run  # noqa: E402
from evaluation.fixture import load  # noqa: E402


class Http:
    def __init__(self):
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def __call__(self, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class DemoMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patches = [mock.patch.object(server, "DEMO", True),
                       mock.patch.object(server.model, "extract", side_effect=AssertionError("model called")),
                       mock.patch.object(server.model, "available_models", side_effect=AssertionError("Ollama asked"))]
        for p in cls.patches:
            p.start()
        cls.http = Http()
        cls.demo = cls.http("/api/demo")[1]
        code, cls.parsed = cls.http("/api/parse", {"text": cls.demo["text"], "roster": cls.demo["roster"]})
        assert code == 200, cls.parsed

    @classmethod
    def tearDownClass(cls):
        cls.http.close()
        for p in cls.patches:
            p.stop()

    def body(self, msg=None, **extra):
        return {"message": msg or self.parsed["messages"][0], "roster": self.parsed["roster"],
                "week_start": self.demo["week_start"], "timezone": self.demo["timezone"], "extractor": "hybrid",
                "model": "gemma4:e2b-it-qat", **extra}

    def test_status_names_the_saved_model_and_never_asks_ollama(self):
        self.assertEqual(self.http("/api/status"), (200, {"models": ["gemma4:e2b-it-qat"], "default_model": "gemma4:e2b-it-qat",
                                                          "demo": True}))

    def test_served_set_a_parses_and_pasted_text_is_refused(self):
        self.assertEqual(len(self.parsed["messages"]), 50)
        for body in ({"text": "2026-11-03 09:00 | Ana Example | Tuesday 10-12 works", "roster": "Ana Example"},
                     {"text": self.demo["text"], "roster": "Ana Example"},
                     {"text": self.demo["text"] + "\n2026-11-03 09:00 | Ana Example | Tuesday 10-12 works", "roster": self.demo["roster"]},
                     {"text": self.demo["text"], "roster": self.demo["roster"], "day_first": True}):
            code, out = self.http("/api/parse", body)
            self.assertEqual(code, 403, out)
            self.assertIn("run the app locally", out["error"])

    def test_unknown_or_altered_messages_other_models_and_other_settings_are_refused(self):
        first = self.parsed["messages"][0]
        refused = [self.body({**first, "id": "m99"}), self.body({**first, "text": "Tuesday 10-12 works"}),
                   self.body({**first, "sender": "Ana Example"}), self.body(model="qwen3.5:4b-q4_K_M"),
                   self.body(roster=["Ana Example"]), self.body(week_start="2026-11-16"), self.body(timezone="UTC"),
                   self.body(coordinators=["Ana Example"])]
        for body in refused:
            code, out = self.http("/api/suggest", body)
            self.assertEqual(code, 403, (body, out))
        payload = {"messages": self.parsed["messages"], "claims": [], "roster": self.parsed["roster"],
                   "week_start": self.demo["week_start"], "timezone": self.demo["timezone"], "reviewed_messages": []}
        for path in ("/api/resolve", "/api/export"):
            self.assertEqual(self.http(path, payload)[0], 200)
            altered = [{**m, "text": "Tuesday 10-12 works"} if i == 3 else m for i, m in enumerate(self.parsed["messages"])]
            self.assertEqual(self.http(path, {**payload, "messages": altered})[0], 403)
            self.assertEqual(self.http(path, {**payload, "messages": self.parsed["messages"][:-1] + [
                {**self.parsed["messages"][0], "id": "m99"}]})[0], 403)
        server.model.extract.assert_not_called()

    def test_replay_equals_a_local_cached_run_for_every_reader_without_a_model_call(self):
        def saved(msg, week, model_name):
            data = json.loads((run.RUNS / "gemma4_e2b_it_qat_prompt3" / f"{msg.id}.json").read_text())
            return data["claims"], dict(data["stats"])

        for kind in ("model", "hybrid", "rules"):
            replay = [self.http("/api/suggest", self.body(m, extractor=kind))[1] for m in self.parsed["messages"]]
            with mock.patch.object(server, "DEMO", False), mock.patch.object(server.model, "extract", side_effect=saved):
                local = [server.suggest(self.body(m, extractor=kind)) for m in self.parsed["messages"]]
            self.assertEqual([r["claims"] for r in replay], [r["claims"] for r in local], kind)
        messages, roster, cal, _ = load("A")
        with mock.patch.object(run.model_mod, "extract", side_effect=AssertionError("model called")):
            raw, _ = run.run_extractor("model", messages, roster, cal, "gemma4:e2b-it-qat", cache_only=True)
        replay = [c for m in self.parsed["messages"] for c in self.http("/api/suggest", self.body(m, extractor="model"))[1]["claims"]]
        self.assertTrue(raw)
        self.assertEqual(replay, raw)
        server.model.extract.assert_not_called()


class LocalDefaultUnchanged(unittest.TestCase):
    def test_pasted_text_is_read_when_demo_mode_is_off(self):
        with mock.patch.object(server, "DEMO", False):
            http = Http()
            try:
                code, out = http("/api/parse", {"text": "2026-11-03 09:00 | Ana Example | Tuesday 10-12 works", "roster": "Ana Example"})
            finally:
                http.close()
        self.assertEqual((code, [m["text"] for m in out["messages"]]), (200, ["Tuesday 10-12 works"]))


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def get(port, path="/"):
    for _ in range(50):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=2) as r:
                return r.read()
        except OSError:
            time.sleep(0.1)
    return None


class Binding(unittest.TestCase):
    """LEDGER_DEMO=1 listens on 0.0.0.0:$PORT; without it PORT is ignored and the server stays on 127.0.0.1."""

    def start(self, env, *args):
        proc = subprocess.Popen([sys.executable, "server.py", *args], cwd=ROOT, stdout=subprocess.PIPE, text=True,
                                env={**{k: v for k, v in os.environ.items() if k not in ("LEDGER_DEMO", "PORT")}, **env, "PYTHONUNBUFFERED": "1"})
        self.addCleanup(proc.wait)
        self.addCleanup(proc.kill)
        return proc

    def test_demo_mode_binds_all_interfaces_on_port(self):
        port = free_port()
        proc = self.start({"LEDGER_DEMO": "1", "PORT": str(port), "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertIn(f"on 0.0.0.0:{port}", proc.stdout.readline())
        self.assertTrue(json.loads(get(port, "/api/status"))["demo"])

    def test_local_default_ignores_port(self):
        port, other = free_port(), free_port()
        proc = self.start({"PORT": str(other), "PYTHONDONTWRITEBYTECODE": "1"}, str(port))
        self.assertIn(f"http://127.0.0.1:{port}", proc.stdout.readline())
        self.assertIn(b"Availability Ledger", get(port))
        with self.assertRaises(OSError):
            urllib.request.urlopen(f"http://127.0.0.1:{other}/", timeout=1)


if __name__ == "__main__":
    unittest.main()
