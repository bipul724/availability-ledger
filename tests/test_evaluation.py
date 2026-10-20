"""Evaluation metric definitions (EVAL-09, EVAL-10). Invented messages and references only.
Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation import run  # noqa: E402
from ledger.core import resolve_all  # noqa: E402
from ledger.messages import parse_messages  # noqa: E402
from ledger.resolve import Calendar  # noqa: E402

CAL = Calendar(date(2026, 11, 9))
ROSTER = ["Ana Example", "Ben Example"]


def said(mid, n, day_text, time_text, excerpt, status="available"):
    return {"id": f"{mid}.{n}", "msg": mid, "n": n, "source": "rules", "review": "pending", "said": {
        "person": "SENDER", "day_text": day_text, "time_text": time_text, "status": status, "condition": "",
        "replaces_earlier": False, "excerpt": excerpt}}


def ref_claim(start, end, status="available"):
    return {"person": "Ana Example", "dates": ["2026-11-10"], "start": start, "end": end, "status": status}


class DuplicateAwareUnits(unittest.TestCase):
    """EVAL-10: a duplicate message is not extracted (D-14), so its reference units are not counted (D-26)."""

    def test_duplicate_units_are_excluded_from_both_sides(self):
        messages = parse_messages("2026-11-03 09:00 | Ana Example | Tuesday 10-12 works\n"
                                  "2026-11-03 10:00 | Ana Example | Tuesday 10-12 works\n")
        self.assertEqual(messages[1].duplicate_of, "m01")
        ref = {"messages": {"m01": {"category": ["basic"], "claims": [ref_claim("10:00", "12:00")]},
                            "m02": {"category": ["duplicate"], "claims": [ref_claim("10:00", "12:00")]}}}
        raw = [said("m01", 1, "Tuesday", "10-12", "Tuesday 10-12 works")]
        _, s = run.score(messages, ROSTER, CAL, ref, raw, ["m01", "m02"])
        self.assertEqual((s["reference_units"], s["correct_units"], s["extraction_errors"], s["silent_errors"]), (1, 1, 0, 0))
        self.assertEqual((s["duplicate_messages_excluded"], s["duplicate_units_excluded"]), (1, 1))
        self.assertNotIn("m02", s["errors_per_message"])

    def test_split_without_duplicates_is_unchanged(self):
        messages = parse_messages("2026-11-03 09:00 | Ana Example | Tuesday 10-12 works\n")
        ref = {"messages": {"m01": {"category": ["basic"], "claims": [ref_claim("10:00", "12:00")]}}}
        _, s = run.score(messages, ROSTER, CAL, ref, [said("m01", 1, "Tuesday", "10-12", "Tuesday 10-12 works")], ["m01"])
        self.assertEqual((s["reference_units"], s["correct_units"], s["duplicate_units_excluded"]), (1, 1, 0))


class ConditionIntervals(unittest.TestCase):
    """EVAL-09: every slot of a reference condition's interval must hold the expected final status."""

    def errors(self, expected, ref_status, time_text, status):
        messages = parse_messages("2026-11-03 09:00 | Ana Example | Tuesday afternoon if the bus runs\n")
        ref = {"messages": {"m01": {"category": ["conditional"], "claims": [ref_claim("14:00", "16:00", ref_status)]}},
               "withdrawals": [], "ambiguities": [],
               "conditions": [{"msg": "m01", "person": "Ana Example", "date": "2026-11-10", "start": "14:00", "end": "16:00",
                               "expected_final": expected}]}
        claims = [said("m01", 1, "Tuesday", time_text, "Tuesday afternoon if the bus runs", status)] if time_text else []
        resolved = resolve_all(messages, claims, ROSTER, CAL)
        _, checks = run.ledger_checks(messages, ROSTER, CAL, ref, resolved)
        return checks["incorrectly_resolved_conditions"], checks["condition_error_list"]

    def test_partial_loss_is_an_error_for_available_and_conditional(self):
        self.assertEqual(self.errors("available", "available", "2-3", "available"),
                         (1, ["Ana Example 2026-11-10 14:00-16:00: availability partly lost"]))
        self.assertEqual(self.errors("conditional", "conditional", "3-4", "conditional"),
                         (1, ["Ana Example 2026-11-10 14:00-16:00: offer partly lost"]))

    def test_full_matches_and_existing_errors_are_unchanged(self):
        cases = [("available", "available", "2-4", "available", 0, None),
                 ("conditional", "conditional", "2-4", "conditional", 0, None),
                 ("conditional", "conditional", "2-4", "available", 1, "treated as firm"),
                 ("conditional", "conditional", "", "available", 1, "offer lost"),
                 ("available", "available", "", "available", 1, "availability lost"),
                 ("available", "available", "2-3", "conditional", 1, "resolution missed")]
        for expected, ref_status, time_text, status, n, kind in cases:
            with self.subTest(expected=expected, time_text=time_text, status=status):
                got_n, errs = self.errors(expected, ref_status, time_text, status)
                self.assertEqual(got_n, n, errs)
                if kind:
                    self.assertTrue(errs[0].endswith(kind), errs)

    def test_scorers_share_one_verdict(self):
        verdict = run.condition_error
        self.assertEqual(verdict({"available", None}, "available"), "availability partly lost")
        self.assertEqual(verdict({"conditional", None}, "conditional"), "offer partly lost")
        self.assertEqual(verdict({"available"}, "none"), "decline missed")
        self.assertIsNone(verdict({None}, "none"))


if __name__ == "__main__":
    unittest.main()
