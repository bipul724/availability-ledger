"""Checks for the deterministic layer. Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation.fixture import load, reference_claims  # noqa: E402
from ledger.core import build_ledger, resolve_all, resolve_claim  # noqa: E402
from ledger.messages import Message, parse_messages  # noqa: E402
from ledger.names import match_person  # noqa: E402
from ledger.resolve import Calendar, resolve_day, resolve_time  # noqa: E402

CAL = Calendar(date(2026, 11, 9))


def day(text, sent):
    r = resolve_day(text, datetime.fromisoformat(sent), CAL)
    return r.state, [d.isoformat() for d in (r.dates or r.candidates)]


class Days(unittest.TestCase):
    def test_bare_weekday_means_selected_week(self):
        self.assertEqual(day("Tuesday", "2026-11-02 09:41"), ("resolved", ["2026-11-10"]))

    def test_next_weekday_resolves_only_when_both_readings_agree(self):
        self.assertEqual(day("Next Tuesday", "2026-11-03 12:40"), ("resolved", ["2026-11-10"]))
        self.assertEqual(day("Next Tuesday", "2026-11-09 07:50"), ("ambiguous", ["2026-11-10", "2026-11-17"]))
        self.assertEqual(day("Next Sunday", "2026-11-08 20:30"), ("resolved", ["2026-11-15"]))

    def test_this_saturday_before_the_week_is_outside(self):
        self.assertEqual(day("this Saturday", "2026-11-04 18:10"), ("outside_week", ["2026-11-07"]))

    def test_numeric_date_uses_calendar_context(self):
        self.assertEqual(day("11/12", "2026-11-03 14:02"), ("resolved", ["2026-11-12"]))

    def test_relative_words(self):
        self.assertEqual(day("tonight", "2026-11-10 08:05"), ("resolved", ["2026-11-10"]))
        self.assertEqual(day("Tomorrow morning", "2026-11-10 09:20"), ("resolved", ["2026-11-11"]))
        self.assertEqual(day("the rest of this week", "2026-11-11 08:40")[1][0], "2026-11-11")

    def test_one_day_this_weekend_stays_open(self):
        self.assertEqual(day("one day this weekend", "2026-11-10 11:00"), ("ambiguous", ["2026-11-14", "2026-11-15"]))

    def test_weekday_inside_a_word_is_not_a_day(self):
        self.assertEqual(day("at a wedding", "2026-11-04 18:10")[0], "unparsed")


class Times(unittest.TestCase):
    def t(self, text):
        r = resolve_time(text, CAL)
        return r.start, r.end

    def test_ranges(self):
        self.assertEqual(self.t("10:30 to 1"), ("10:30", "13:00"))
        self.assertEqual(self.t("from 2 until 6"), ("14:00", "18:00"))
        self.assertEqual(self.t("like 6-9"), ("18:00", "21:00"))
        self.assertEqual(self.t("9-12"), ("09:00", "12:00"))

    def test_open_and_periods(self):
        self.assertEqual(self.t("after 3"), ("15:00", "20:00"))
        self.assertEqual(self.t("mornings"), ("09:00", "12:00"))
        self.assertEqual(self.t("all day"), ("09:00", "20:00"))

    def test_point_time_is_not_guessed(self):
        self.assertEqual(resolve_time("at 9", CAL).state, "unparsed")


class Names(unittest.TestCase):
    roster = ["Sam Okafor", "Samira Haddad", "Lena Fischer", "Lina Fisher", "Tomás Ruiz"]

    def test_short_name_shared_by_two_people_is_ambiguous(self):
        self.assertEqual(match_person("Sam", "Grace Kim", self.roster).state, "ambiguous")

    def test_accent_and_similar_names(self):
        self.assertEqual(match_person("SENDER", "Tomas Ruiz", self.roster).name, "Tomás Ruiz")
        self.assertIn("Lina Fisher", match_person("Lena", "x", self.roster).similar)


class Ledger(unittest.TestCase):
    def test_reference_claims_reproduce_the_hand_written_sheet(self):
        for which in ("A", "B"):
            messages, roster, cal, ref = load(which)
            ledger = build_ledger(messages, reference_claims(ref), roster, cal)
            got = {p: {d: [[s["start"], s["end"], s["status"]] for s in segs] for d, segs in days.items()}
                   for p, days in ledger["sheet"].items()}
            self.assertEqual(got, ref["expected_sheet"], which)

    def test_monday_correction_keeps_wednesday(self):
        cal = CAL
        msgs = [Message("m1", datetime(2026, 11, 2, 9), "Ana", "Monday and Wednesday mornings"),
                Message("m2", datetime(2026, 11, 3, 9), "Ana", "Actually Monday 10-11 instead")]
        said = [("m1", "Monday", "mornings", False), ("m1", "Wednesday", "mornings", False), ("m2", "Monday", "10-11", True)]
        claims = [resolve_claim({"id": f"{m}.{i}", "msg": m, "n": i, "said": {
            "person": "SENDER", "day_text": d, "time_text": t, "status": "available", "condition": "",
            "replaces_earlier": r, "excerpt": d}}, msgs[0] if m == "m1" else msgs[1], ["Ana"], cal)
            for i, (m, d, t, r) in enumerate(said)]
        sheet = build_ledger(msgs, claims, ["Ana"], cal)["sheet"]["Ana"]
        self.assertEqual([(s["start"], s["end"]) for s in sheet["2026-11-09"]], [("10:00", "11:00")])
        self.assertEqual([(s["start"], s["end"]) for s in sheet["2026-11-11"]], [("09:00", "12:00")])


def said(msg, n, day_text, excerpt, time_text="", status="available"):
    return {"id": f"{msg}.{n}", "msg": msg, "n": n, "source": "model", "review": "pending", "said": {
        "person": "SENDER", "day_text": day_text, "time_text": time_text, "status": status, "condition": "",
        "replaces_earlier": False, "excerpt": excerpt}}


class Duplicates(unittest.TestCase):
    roster = ["Ana Silva", "Ben Ode"]

    def test_repeat_gets_one_set_of_suggestions_and_one_edit(self):
        import server
        msgs = parse_messages("2026-11-03 09:00 | Ana Silva | Tuesday 2-5 works, I’m in\n"
                              "2026-11-03 21:30 | Ana Silva | tuesday  2–5 works, I'm in\n")
        self.assertEqual([m.duplicate_of for m in msgs], [None, "m01"])
        self.assertEqual(msgs[1].to_dict()["duplicate_of"], "m01")
        body = {"roster": self.roster, "week_start": "2026-11-09", "extractor": "rules"}
        claims = [c for m in msgs for c in server.suggest({**body, "message": m.to_dict()})["claims"]]
        self.assertEqual({c["msg"] for c in claims}, {"m01"})
        claims[0]["override"] = {"start": "15:00", "end": "16:00"}
        ledger = build_ledger(msgs, resolve_all(msgs, claims, self.roster, CAL), self.roster, CAL)
        self.assertEqual(ledger["sheet"]["Ana Silva"]["2026-11-10"],
                         [{"status": "available", "start": "15:00", "end": "16:00", "claims": ["m01.1"], "review": []}])
        self.assertEqual([e["what"] for e in ledger["history"]["Ana Silva|2026-11-10"]], ["added", "repeated"])

    def test_other_sender_or_a_day_later_is_not_merged(self):
        msgs = parse_messages("2026-11-03 09:00 | Ana Silva | Tuesday 2-5 works\n"
                              "2026-11-03 09:05 | Ben Ode | Tuesday 2-5 works\n"
                              "2026-11-04 09:01 | Ana Silva | Tuesday 2-5 works\n")
        self.assertEqual([m.duplicate_of for m in msgs], [None, None, None])


class DayModifierFromQuote(unittest.TestCase):
    def resolve(self, sent, text, day_text, excerpt):
        msg = Message("m1", datetime.fromisoformat(sent), "Ana", text)
        return resolve_claim(said("m1", 1, day_text, excerpt, status="unavailable"), msg, ["Ana"], CAL)

    def test_this_saturday_before_the_week_stays_outside(self):
        c = self.resolve("2026-11-04 18:10", "Can't do this Saturday, sorry", "Saturday", "Can't do this Saturday")
        self.assertEqual((c["date_state"], c["date_candidates"]), ("outside_week", ["2026-11-07"]))
        self.assertIn("day_modifier_from_quote", c["flags"])
        self.assertEqual(c["review"], "pending")

    def test_next_friday_stays_ambiguous(self):
        c = self.resolve("2026-11-09 08:00", "Next Friday I'm away", "Friday", "Next Friday I'm away")
        self.assertEqual((c["date_state"], c["date_candidates"]), ("ambiguous", ["2026-11-13", "2026-11-20"]))

    def test_no_modifier_or_other_weekday_is_unchanged(self):
        c = self.resolve("2026-11-05 10:00", "Friday works", "Friday", "Friday works")
        self.assertEqual((c["date_state"], c["dates"]), ("resolved", ["2026-11-13"]))
        self.assertNotIn("day_modifier_from_quote", c["flags"])
        c = self.resolve("2026-11-05 10:00", "Friday, not this Saturday", "Friday", "Friday, not this Saturday")
        self.assertEqual(c["dates"], ["2026-11-13"])
        self.assertNotIn("day_modifier_from_quote", c["flags"])


class MoreTimes(unittest.TestCase):
    def test_onwards_runs_to_day_end(self):
        for text in ("4 onwards", "from 4 on", "4pm onwards"):
            r = resolve_time(text, CAL)
            self.assertEqual((r.state, r.start, r.end), ("open", "16:00", "20:00"), text)

    def test_the_same_copies_hours_within_one_message_only(self):
        sent = datetime(2026, 11, 4, 9)
        text = "Monday 10 till 2, and Wednesday the same"
        msgs = [Message("m1", sent, "Ana", text)]
        claims = [said("m1", 1, "Monday", "Monday 10 till 2", "10 till 2"),
                  said("m1", 2, "Wednesday", "Wednesday the same", "the same")]
        wed = resolve_all(msgs, claims, ["Ana"], CAL)[1]
        self.assertEqual((wed["dates"], wed["time_state"], wed["start"], wed["end"]),
                         (["2026-11-11"], "explicit", "10:00", "14:00"))

        msgs = [Message("m1", sent, "Ana", "Monday 10 till 2"), Message("m2", sent, "Ana", "Wednesday the same")]
        claims = [said("m1", 1, "Monday", "Monday 10 till 2", "10 till 2"),
                  said("m2", 1, "Wednesday", "Wednesday the same", "the same")]
        for wed in (resolve_all(msgs, claims, ["Ana"], CAL)[1], resolve_all(msgs[1:], claims[1:], ["Ana"], CAL)[0]):
            self.assertEqual((wed["time_state"], wed["time_note"]),
                             ("unparsed", "'the same' needs a time earlier in this message"))


if __name__ == "__main__":
    unittest.main()
