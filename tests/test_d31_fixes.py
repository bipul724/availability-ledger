"""Reconciliation fixes from D-31 (COR-13 to COR-17). Invented messages only; none copy or paraphrase set A, B or C.
Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ledger import rules  # noqa: E402
from ledger.core import build_ledger, resolve_all  # noqa: E402
from ledger.messages import Message  # noqa: E402
from ledger.names import match_person  # noqa: E402
from ledger.resolve import Calendar, resolve_day  # noqa: E402

CAL = Calendar(date(2026, 11, 9))  # Mon 9 Nov 2026 to Sun 15 Nov 2026
ROSTER = ["Ana Example", "Ben Example"]


def day(text, sent):
    r = resolve_day(text, datetime.fromisoformat(sent), CAL)
    return r.state, [d.isoformat() for d in (r.dates or r.candidates)]


def msg(mid, d, hour, text, sender="Ana Example"):
    return Message(mid, datetime(2026, 11, d, hour), sender, text)


def claim(m, n, day_text, time_text, excerpt, status="available", condition="", source="model", review="pending"):
    return {"id": f"{m}.{n}", "msg": m, "n": n, "source": source, "review": review, "said": {
        "person": "SENDER", "day_text": day_text, "time_text": time_text, "status": status, "condition": condition,
        "replaces_earlier": False, "excerpt": excerpt}}


def sheet_day(msgs, claims, iso):
    L = build_ledger(msgs, resolve_all(msgs, claims, ROSTER, CAL), ROSTER, CAL)
    return [(s["start"], s["end"], s["status"]) for s in L["sheet"]["Ana Example"].get(iso, [])], L


class ExplicitDates(unittest.TestCase):
    """COR-13: an explicit date wins over a weekday word next to it."""

    def test_explicit_date_outside_the_week_is_outside_week(self):
        self.assertEqual(day("Sun 8 Nov", "2026-11-05 10:00"), ("outside_week", ["2026-11-08"]))

    def test_agreeing_weekday_adds_no_second_date(self):
        self.assertEqual(day("Wed 11/11", "2026-11-04 10:00"), ("resolved", ["2026-11-11"]))
        self.assertEqual(day("Thursday, 12 November", "2026-11-04 10:00"), ("resolved", ["2026-11-12"]))
        self.assertEqual(day("Sat the 14th", "2026-11-04 10:00"), ("resolved", ["2026-11-14"]))

    def test_contradicting_weekday_is_ambiguous_with_both(self):
        self.assertEqual(day("Tue 12 Nov", "2026-11-04 10:00"), ("ambiguous", ["2026-11-10", "2026-11-12"]))

    def test_outside_week_claim_is_flagged_not_applied(self):
        msgs = [msg("m1", 5, 10, "can't make Sun 8 Nov, sorry")]
        c = resolve_all(msgs, [claim("m1", 1, "Sun 8 Nov", "", "can't make Sun 8 Nov", status="unavailable")], ROSTER, CAL)[0]
        self.assertEqual((c["date_state"], c["dates"], c["date_candidates"]), ("outside_week", [], ["2026-11-08"]))
        self.assertIn("outside_week", c["flags"])


class FirmFollowUp(unittest.TestCase):
    """COR-14: an untimed available follow-up settles conditional-only time; it is a no-op on available time."""

    def test_follow_up_resolves_a_conditional_offer(self):
        msgs = [msg("m1", 2, 9, "Saturday 2-5 if the van is free"), msg("m2", 4, 9, "van's free, Saturday is on")]
        claims = [claim("m1", 1, "Saturday", "2-5", "Saturday 2-5 if the van is free", status="conditional", condition="if the van is free"),
                  claim("m2", 1, "Saturday", "", "Saturday is on")]
        segs, L = sheet_day(msgs, claims, "2026-11-14")
        self.assertEqual(segs, [("14:00", "17:00", "available")])
        self.assertEqual(L["history"]["Ana Example|2026-11-14"][-1]["what"], "condition resolved")
        self.assertFalse([i for i in L["issues"] if i["kind"] == "condition"])

    def test_still_good_on_available_time_is_a_no_op(self):
        msgs = [msg("m1", 2, 9, "Saturday 2-5"), msg("m2", 4, 9, "Saturday still good")]
        segs, L = sheet_day(msgs, [claim("m1", 1, "Saturday", "2-5", "Saturday 2-5"), claim("m2", 1, "Saturday", "", "Saturday still good")], "2026-11-14")
        self.assertEqual(segs, [("14:00", "17:00", "available")])
        self.assertEqual(L["history"]["Ana Example|2026-11-14"][-1]["what"], "confirmed earlier answer")

    def test_mixed_available_and_conditional_time_is_left_alone(self):
        msgs = [msg("m1", 2, 9, "Saturday 9-12, and 2-5 if the van is free"), msg("m2", 4, 9, "Saturday is on")]
        claims = [claim("m1", 1, "Saturday", "9-12", "Saturday 9-12"),
                  claim("m1", 2, "Saturday", "2-5", "2-5 if the van is free", status="conditional", condition="if the van is free"),
                  claim("m2", 1, "Saturday", "", "Saturday is on")]
        segs, _ = sheet_day(msgs, claims, "2026-11-14")
        self.assertEqual(segs, [("09:00", "12:00", "available"), ("14:00", "17:00", "conditional")])


class ReplacementCues(unittest.TestCase):
    """COR-15: a later explicit range with a change cue replaces the day's earlier answer (model and rules claims)."""

    def test_cue_words_replace_the_earlier_answer(self):
        cases = [("all day", "Wednesday all day", "can we switch Wednesday to 10-1", "10-1", "2026-11-11", [("10:00", "13:00", "available")]),
                 ("9-5", "Thursday 9-5", "make it Thursday 1-3", "1-3", "2026-11-12", [("13:00", "15:00", "available")]),
                 ("9-12", "Friday 9-12", "Friday 2-4 now", "2-4", "2026-11-13", [("14:00", "16:00", "available")])]
        days = {"2026-11-11": "Wednesday", "2026-11-12": "Thursday", "2026-11-13": "Friday"}
        for first_time, first, second, second_time, iso, expected in cases:
            with self.subTest(second=second):
                msgs = [msg("m1", 2, 9, first), msg("m2", 4, 9, second)]
                claims = [claim("m1", 1, days[iso], first_time, first), claim("m2", 1, days[iso], second_time, second)]
                self.assertEqual(sheet_day(msgs, claims, iso)[0], expected)

    def test_also_adds_instead_of_replacing(self):
        msgs = [msg("m1", 2, 9, "Tuesday 2-4"), msg("m2", 4, 9, "Tuesday also 6-8")]
        claims = [claim("m1", 1, "Tuesday", "2-4", "Tuesday 2-4"), claim("m2", 1, "Tuesday", "6-8", "Tuesday also 6-8")]
        self.assertEqual(sheet_day(msgs, claims, "2026-11-10")[0], [("14:00", "16:00", "available"), ("18:00", "20:00", "available")])

    def test_a_first_answer_with_a_cue_word_is_just_an_answer(self):
        msgs = [msg("m1", 2, 9, "Monday 10-2 now")]
        self.assertEqual(sheet_day(msgs, [claim("m1", 1, "Monday", "10-2", "Monday 10-2 now")], "2026-11-09")[0],
                         [("10:00", "14:00", "available")])

    def test_rules_claims_get_the_cue_too(self):
        msgs = [msg("m1", 2, 9, "Wednesday all day"), msg("m2", 4, 9, "Can I move Wednesday to 10-1")]
        raw = [{"id": f"{m.id}.{i}", "msg": m.id, "n": i, "source": "rules", "review": "pending", "said": s}
               for m in msgs for i, s in enumerate(rules.extract(m, ROSTER), 1)]
        self.assertEqual(sheet_day(msgs, raw, "2026-11-11")[0], [("10:00", "13:00", "available")])

    def test_reviewer_added_records_are_not_affected(self):
        msgs = [msg("m1", 2, 9, "Friday 9-12"), msg("m2", 4, 9, "Friday 2-4 now")]
        claims = [claim("m1", 1, "Friday", "9-12", "Friday 9-12"), claim("m2", 1, "Friday", "2-4", "Friday 2-4 now", source="user", review="accepted")]
        self.assertEqual(sheet_day(msgs, claims, "2026-11-13")[0], [("09:00", "12:00", "available"), ("14:00", "16:00", "available")])


class InitialAndSurname(unittest.TestCase):
    """COR-16: an initial plus a surname matches roster entries with that surname and first initial."""

    roster = ["Mira Okonjo", "Milo Okonjo", "Nadia Fenn", "Ola Fenwick"]

    def test_initial_and_surname(self):
        m = match_person("M. Okonjo", "x", self.roster)
        self.assertEqual((m.state, m.candidates), ("ambiguous", ["Mira Okonjo", "Milo Okonjo"]))
        self.assertEqual(match_person("N Fenn", "x", self.roster).name, "Nadia Fenn")
        self.assertEqual(match_person("O. Fenwick", "x", self.roster).name, "Ola Fenwick")
        self.assertEqual(match_person("Q Fenn", "x", self.roster).state, "unknown")
        self.assertEqual(match_person("N. Okonjo", "x", self.roster).state, "unknown")


class RulesNegationForms(unittest.TestCase):
    """COR-17: rules negation covers word forms and 'I'm out' without catching unrelated 'out'."""

    def statuses(self, text):
        return [(c["day_text"], c["status"]) for c in rules.extract(msg("m1", 4, 9, text), ROSTER)]

    def test_word_forms_and_out_phrases(self):
        self.assertEqual(self.statuses("I'm cancelling Thursday, sorry"), [("Thursday", "unavailable")])
        self.assertEqual(self.statuses("Friday is cancelled for me"), [("Friday", "unavailable")])
        self.assertEqual(self.statuses("I'm out Monday"), [("Monday", "unavailable")])
        self.assertEqual(self.statuses("out all day Wednesday"), [("Wednesday", "unavailable")])

    def test_unrelated_out_is_not_negation(self):
        self.assertEqual(self.statuses("Can sort out the van Tuesday 2-4"), [("Tuesday", "available")])
        self.assertEqual(self.statuses("Tuesday about 2-4"), [("Tuesday", "available")])


if __name__ == "__main__":
    unittest.main()
