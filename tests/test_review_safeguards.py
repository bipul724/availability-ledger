"""Review safeguards: COR-10 (flag suggestions whose day/time words are not in the message, D-30) and COR-07a
(warn about a possible change nobody applied). Invented messages only. Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ledger.core import build_ledger, resolve_all  # noqa: E402
from ledger.export import confirmed_export  # noqa: E402
from ledger.messages import Message  # noqa: E402
from ledger.resolve import Calendar  # noqa: E402

CAL = Calendar(date(2026, 11, 9))
ROSTER = ["Ana Example", "Ben Example"]


def msg(mid, day, hour, text, sender="Ana Example"):
    return Message(mid, datetime(2026, 11, day, hour), sender, text)


def claim(m, n, day_text, time_text, excerpt, review="pending", status="available", hints=()):
    return {"id": f"{m}.{n}", "msg": m, "n": n, "source": "model", "review": review, "hints": list(hints), "said": {
        "person": "SENDER", "day_text": day_text, "time_text": time_text, "status": status, "condition": "",
        "replaces_earlier": False, "excerpt": excerpt}}


def ledger(msgs, claims):
    resolved = resolve_all(msgs, claims, ROSTER, CAL)
    return resolved, build_ledger(msgs, resolved, ROSTER, CAL)


def tuesday(L):
    return [(s["start"], s["end"]) for s in L["sheet"]["Ana Example"].get("2026-11-10", [])]


class FlagUnsupportedPhrases(unittest.TestCase):
    """COR-10 per D-30: a pending suggestion flagged phrase_not_in_message is NOT held. It counts on the provisional
    sheet as before, keeps its flag, and is listed as a non-blocking "check the wording" item; the final export
    still takes accepted claims only."""

    happy = [msg("m1", 2, 9, "Happy to help")]

    def test_counts_provisionally_flagged_and_listed_and_stays_out_of_the_export_until_accepted(self):
        resolved, L = ledger(self.happy, [claim("m1", 1, "Tuesday", "2-4", "Happy to help")])
        self.assertEqual(resolved[0]["review"], "pending")
        self.assertIn("phrase_not_in_message", resolved[0]["flags"])
        self.assertNotIn("held", resolved[0]["flags"])
        self.assertEqual(tuesday(L), [("14:00", "16:00")])
        self.assertEqual([e["claim"] for e in L["history"]["Ana Example|2026-11-10"]], ["m1.1"])
        self.assertEqual([(i["kind"], i["claim"]) for i in L["issues"]], [("check_wording", "m1.1")])
        exp = confirmed_export(self.happy, resolved, ROSTER, CAL, ["m1"])
        self.assertEqual((exp["status"], exp["pending"], exp["blocking_issues"], [r["status"] for r in exp["rows"]]),
                         ("provisional", 1, 0, [""]))  # nothing confirmed; the pending claim only marks its cell

        resolved, L = ledger(self.happy, [claim("m1", 1, "Tuesday", "2-4", "Happy to help", review="accepted")])
        self.assertEqual(tuesday(L), [("14:00", "16:00")])
        self.assertEqual(L["issues"], [])
        exp = confirmed_export(self.happy, resolved, ROSTER, CAL, ["m1"])
        self.assertEqual((exp["status"], [(r["start"], r["end"], r["cell_state"]) for r in exp["rows"]]),
                         ("complete", [("14:00", "16:00", "confirmed")]))

    def test_check_wording_is_not_a_blocking_kind(self):
        from ledger.export import BLOCKING
        self.assertNotIn("check_wording", BLOCKING)
        self.assertNotIn("unanswered_change", BLOCKING)

    def test_other_flags_raise_no_wording_item(self):
        msgs = [msg("m1", 2, 9, "Tuesday 2-4 works")]
        resolved, L = ledger(msgs, [claim("m1", 1, "Tuesday", "2-4", "Tuesday 2-4 works", hints=["readers_disagree", "one_reader"])])
        self.assertEqual(tuesday(L), [("14:00", "16:00")])
        self.assertEqual(L["issues"], [])

    def test_dropped_and_rejected_raise_no_wording_item(self):
        msgs = [msg("m1", 2, 9, "Happy to help")]
        dropped = claim("m1", 1, "Tuesday", "2-4", "I can do Tuesday 2-4")  # quote missing too: the evidence gate drops it
        rejected = claim("m1", 2, "Tuesday", "2-4", "Happy to help", review="rejected")
        resolved, L = ledger(msgs, [dropped, rejected])
        self.assertEqual([c["review"] for c in resolved], ["dropped", "rejected"])
        self.assertEqual((L["issues"], L["sheet"]["Ana Example"]), ([], {}))


class UnansweredChange(unittest.TestCase):
    """COR-07a: a later message with a change word naming a day that still has open time, but no claim on that day."""

    offer = [msg("m1", 2, 9, "Thursday 9-12 works")]
    offer_claim = [claim("m1", 1, "Thursday", "9-12", "Thursday 9-12 works", review="accepted")]

    def warnings(self, msgs, claims):
        _, L = ledger(msgs, claims)
        return L, [i for i in L["issues"] if i["kind"] == "unanswered_change"]

    def test_change_word_on_an_open_day_without_a_claim_warns(self):
        msgs = self.offer + [msg("m2", 4, 18, "Sorry, I have to cancel Thursday")]
        L, warn = self.warnings(msgs, self.offer_claim)
        self.assertEqual([(w["msg"], w["person"], w["date"]) for w in warn], [("m2", "Ana Example", "2026-11-12")])
        self.assertTrue(warn[0]["text"].startswith("Possible change not applied (m2 mentions Thu 12 Nov)"), warn[0]["text"])
        self.assertEqual([(s["start"], s["end"]) for s in L["sheet"]["Ana Example"]["2026-11-12"]], [("09:00", "12:00")])

    def test_no_change_word_does_not_warn(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12 works"), msg("m2", 4, 18, "Tuesday still good")]
        _, warn = self.warnings(msgs, [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12 works", review="accepted")])
        self.assertEqual(warn, [])

    def test_change_word_on_a_day_without_open_time_does_not_warn(self):
        _, warn = self.warnings(self.offer + [msg("m2", 4, 18, "Can't do Friday")], self.offer_claim)
        self.assertEqual(warn, [])

    def test_day_already_handled_by_a_claim_does_not_warn(self):
        msgs = self.offer + [msg("m2", 4, 18, "Can't do Thursday after all")]
        L, warn = self.warnings(msgs, self.offer_claim + [claim("m2", 1, "Thursday", "", "Can't do Thursday", status="unavailable")])
        self.assertEqual(warn, [])
        self.assertNotIn("2026-11-12", L["sheet"]["Ana Example"])

    def test_another_person_does_not_inherit_the_change(self):
        _, warn = self.warnings(self.offer + [msg("m2", 4, 18, "I have to cancel Thursday", sender="Ben Example")], self.offer_claim)
        self.assertEqual(warn, [])

    def test_warning_never_changes_the_sheet_or_the_export(self):
        before = self.offer
        after = self.offer + [msg("m2", 4, 18, "Sorry, I have to cancel Thursday")]
        _, L0 = ledger(before, self.offer_claim)
        resolved, L1 = ledger(after, self.offer_claim)
        self.assertEqual((L0["sheet"], L0["counts"]), (L1["sheet"], L1["counts"]))
        exp = confirmed_export(after, resolved, ROSTER, CAL, ["m1", "m2"])
        self.assertEqual((exp["status"], [(r["date"], r["start"], r["end"]) for r in exp["rows"]]),
                         ("complete", [("2026-11-12", "09:00", "12:00")]))


if __name__ == "__main__":
    unittest.main()
