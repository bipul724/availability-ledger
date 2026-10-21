"""CI re-score safeguards (INT-11): --cache-only never calls the model, --out keeps results away from the committed and
protected folders, and the CI summary fails on any score difference. Invented messages only.
Run: python3 -m unittest discover -s tests"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation import ci_summary, run  # noqa: E402
from ledger.messages import parse_messages  # noqa: E402
from ledger.resolve import Calendar  # noqa: E402

CAL = Calendar(date(2026, 11, 9))
ROSTER = ["Ana Example", "Ben Example"]
TEXT = ("2026-11-03 09:00 | Ana Example | Tuesday 10-12 works\n"
        "2026-11-03 10:00 | Ben Example | Wednesday afternoon is fine\n")
SAID = {"person": "SENDER", "day_text": "Tuesday", "time_text": "10-12", "status": "available", "condition": "",
        "replaces_earlier": False, "excerpt": "Tuesday 10-12 works"}
REF = {"week_start": "2026-11-09", "timezone": "Europe/London", "split": {"heldout": ["m02"]},
       "messages": {"m01": {"category": ["basic"], "claims": [
                        {"person": "Ana Example", "dates": ["2026-11-10"], "start": "10:00", "end": "12:00", "status": "available"}]},
                    "m02": {"category": ["basic"], "claims": [
                        {"person": "Ben Example", "dates": ["2026-11-11"], "start": "13:00", "end": "17:00", "status": "available"}]}},
       "withdrawals": [], "conditions": [], "ambiguities": [],
       "expected_sheet": {"Ana Example": {"2026-11-10": [["10:00", "12:00", "available"]]},
                          "Ben Example": {"2026-11-11": [["13:00", "17:00", "available"]]}}}


def save(runs: Path, mid: str, claims: list):
    folder = runs / "test_model_prompt3"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{mid}.json").write_text(json.dumps({"claims": claims, "stats": {"wall_s": 1.0, "json_ok": True}}))


class CacheOnly(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.runs = Path(self.tmp.name) / "runs"
        self.messages = parse_messages(TEXT)
        patches = [mock.patch.object(run, "RUNS", self.runs),
                   mock.patch.object(run.model_mod, "PROMPT_VERSION", 3),
                   mock.patch.object(run.model_mod, "extract", side_effect=AssertionError("model called"))]
        self.extract = [p.start() for p in patches][-1]
        for p in patches:
            self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)

    def extractor(self, kind):
        return run.run_extractor(kind, self.messages, ROSTER, CAL, "test:model", cache_only=True)

    def test_a_missing_output_names_the_message_and_path_and_never_reaches_the_model(self):
        save(self.runs, "m01", [SAID])  # m02 is not saved
        for kind in ("model", "hybrid"):
            with self.assertRaises(run.CacheMissError) as caught:
                self.extractor(kind)
            self.assertIn("message m02", str(caught.exception))
            self.assertIn(str(self.runs / "test_model_prompt3" / "m02.json"), str(caught.exception))
        self.extract.assert_not_called()
        self.assertFalse((self.runs / "test_model_prompt3" / "m02.json").exists())

    def test_saved_outputs_are_used_without_a_model_call(self):
        save(self.runs, "m01", [SAID])
        save(self.runs, "m02", [])
        raw, stats = self.extractor("model")
        self.assertEqual([c["id"] for c in raw], ["m01.1"])
        self.assertTrue(all(s["cached"] for s in stats.values()))
        self.extract.assert_not_called()

    def main(self, *argv):
        with mock.patch.object(sys, "argv", ["run", *argv]), mock.patch.object(run, "load", return_value=(
                self.messages, ROSTER, CAL, REF)), contextlib.redirect_stdout(io.StringIO()):
            run.main()

    def test_main_writes_to_out_skips_memory_sampling_and_reports_no_fresh_calls(self):
        save(self.runs, "m01", [SAID])
        save(self.runs, "m02", [])
        out = Path(self.tmp.name) / "out"
        with mock.patch.object(run, "MemorySampler", side_effect=AssertionError("sampler started")), \
                mock.patch.object(run, "ollama_ps", side_effect=AssertionError("Ollama asked")):
            self.main("--extractor", "hybrid", "--model", "test:model", "--cache-only", "--out", str(out))
        report = json.loads((out / "setA_hybrid_test_model_prompt3.json").read_text())
        self.assertEqual((report["speed"]["fresh_calls"], "memory" in report), (0, False))
        self.assertEqual(report["all"]["correct_units"], 1)
        self.extract.assert_not_called()

    def test_main_exits_with_the_error_on_a_miss(self):
        with self.assertRaises(SystemExit) as caught:
            self.main("--extractor", "model", "--model", "test:model", "--cache-only", "--out", self.tmp.name)
        self.assertIn("message m01", str(caught.exception.code))
        self.extract.assert_not_called()

    def test_out_refuses_protected_folders_and_refresh_contradicts_cache_only(self):
        for argv in (["--out", str(run.RESULTS / "frozen")], ["--out", str(run.RESULTS / "frozen-setC" / "x")],
                     ["--out", str(run.RESULTS / "tuning")], ["--cache-only", "--refresh"]):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                self.main("--extractor", "rules", *argv)
        self.assertEqual(list(Path(self.tmp.name).iterdir()), [])


class Summary(unittest.TestCase):
    """The step summary compares scores only; run time, speed and memory may differ."""

    def report(self, correct=1, fresh=0, wall=1.0):
        return {"set": "A", "extractor": "model", "model": "gemma4:e2b-it-qat", "wall_s": wall,
                "speed": {"fresh_calls": fresh}, "memory": {"samples": 3},
                "heldout": {"correct_units": correct, "reference_units": 2},
                "ledger": {"missed_withdrawals": 0, "withdrawals_total": 1, "slot_agreement": 0.9}}

    def summary(self, new, committed):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            (Path(a) / "setA_x.json").write_text(json.dumps(new))
            if committed is not None:
                (Path(b) / "setA_x.json").write_text(json.dumps({k: v for k, v in committed.items() if k != "memory"}))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = ci_summary.main([a, "--against", b])
            return code, out.getvalue()

    def test_same_scores_pass_even_when_run_time_differs(self):
        code, text = self.summary(self.report(), self.report(wall=99.0))
        self.assertEqual(code, 0, text)
        self.assertIn("| A | Gemma 4 E2B only | 1/2 | 0/1 | 0.9 | 0 | yes |", text)

    def test_score_difference_fresh_call_or_missing_file_fails(self):
        for new, committed, reason in ((self.report(correct=2), self.report(), "scores differ"),
                                       (self.report(fresh=1), self.report(), "1 fresh model calls"),
                                       (self.report(), None, "no committed file")):
            code, text = self.summary(new, committed)
            self.assertEqual(code, 1, text)
            self.assertIn(reason, text)


if __name__ == "__main__":
    unittest.main()
