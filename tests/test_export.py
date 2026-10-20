"""Confirmed final-sheet export and its scorer. Invented messages only. Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation.fixture import load, reference_claims  # noqa: E402
from evaluation.score_final import score, score_text  # noqa: E402
from ledger.core import N_SLOTS, build_ledger, final_slots, resolve_all  # noqa: E402
from ledger.export import FinalSheetError, _cell, confirmed_export, final_csv, parse_final_csv  # noqa: E402
from ledger.messages import Message  # noqa: E402
from ledger.resolve import Calendar  # noqa: E402

CAL = Calendar(date(2026, 11, 9))
ROSTER = ["Ana Example", "Ben Example"]
META = "# availability-final v1; week=2026-11-09; status={status}; unreviewed={unrev}; pending={pending}; blocking_issues=0"
HEADER = "volunteer,date,start,end,status,condition,cell_state,sources"


def msg(mid, day, hour, text, sender="Ana Example", dup=None):
    return Message(mid, datetime(2026, 11, day, hour), sender, text, dup)


def claim(m, n, day_text, time_text, excerpt, review="accepted", status="available", replaces=False, condition=""):
    return {"id": f"{m}.{n}", "msg": m, "n": n, "source": "model", "review": review, "said": {
        "person": "SENDER", "day_text": day_text, "time_text": time_text, "status": status, "condition": condition,
        "replaces_earlier": replaces, "excerpt": excerpt}}


def export(msgs, claims, reviewed):
    return confirmed_export(msgs, resolve_all(msgs, claims, ROSTER, CAL), ROSTER, CAL, reviewed)


def rows(exp):
    return [(r["volunteer"], r["date"], r["start"], r["end"], r["status"], r["cell_state"]) for r in exp["rows"]]


def sheet(*lines, status="complete", unrev="", pending=0):
    return "\n".join([META.format(status=status, unrev=unrev, pending=pending), HEADER, *lines]) + "\n"


class ConfirmedExport(unittest.TestCase):
    def test_accepted_correction_replays_to_the_replacement_only(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12"), msg("m2", 3, 9, "Tuesday 2-4 instead")]
        exp = export(msgs, [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12"),
                            claim("m2", 1, "Tuesday", "2-4", "Tuesday 2-4 instead", replaces=True)], ["m1", "m2"])
        self.assertEqual(exp["status"], "complete")
        self.assertEqual(rows(exp), [("Ana Example", "2026-11-10", "14:00", "16:00", "available", "confirmed")])

    def test_pending_cancellation_keeps_the_offer_but_marks_the_cell(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12"), msg("m2", 3, 9, "Can't do Tuesday")]
        exp = export(msgs, [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12"),
                            claim("m2", 1, "Tuesday", "", "Can't do Tuesday", review="pending", status="unavailable")],
                     ["m1", "m2"])
        self.assertEqual((exp["status"], exp["pending"]), ("provisional", 1))
        self.assertEqual(rows(exp), [("Ana Example", "2026-11-10", "10:00", "12:00", "available", "needs_review")])

    def test_accepted_conditional_is_exported_as_conditional_and_does_not_block(self):
        msgs = [msg("m1", 2, 9, "Saturday 9-12 if my car is fixed")]
        exp = export(msgs, [claim("m1", 1, "Saturday", "9-12", "Saturday 9-12 if my car is fixed", status="conditional",
                                  condition="if my car is fixed")], ["m1"])
        self.assertEqual(exp["status"], "complete")
        self.assertEqual((exp["rows"][0]["status"], exp["rows"][0]["condition"]), ("conditional", "if my car is fixed"))

    def test_unreviewed_message_without_suggestions_keeps_the_week_provisional(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12"), msg("m2", 3, 9, "Ugh, scrap that")]
        claims = [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12")]
        exp = export(msgs, claims, ["m1"])
        self.assertEqual((exp["status"], exp["unreviewed"], exp["needs_review_cells"]), ("provisional", ["m2"], 0))
        self.assertEqual(export(msgs, claims, ["m1", "m2"])["status"], "complete")

    def test_deciding_every_suggestion_is_not_review(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12")]
        exp = export(msgs, [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12")], [])
        self.assertEqual((exp["status"], exp["unreviewed"]), ("provisional", ["m1"]))
        self.assertEqual(rows(exp)[0][-1], "needs_review")

    def test_duplicate_is_covered_by_its_original(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12"), msg("m2", 2, 10, "tuesday 10-12", dup="m1")]
        exp = export(msgs, [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12")], ["m1"])
        self.assertEqual((exp["status"], exp["unreviewed"]), ("complete", []))

    def test_accepted_ambiguous_date_blocks_and_marks_candidate_cells(self):
        msgs = [msg("m1", 9, 8, "Next Friday works")]
        exp = export(msgs, [claim("m1", 1, "Next Friday", "", "Next Friday works")], ["m1"])
        self.assertEqual((exp["status"], exp["blocking_issues"]), ("provisional", 1))
        self.assertEqual(rows(exp), [("Ana Example", "2026-11-13", "", "", "", "needs_review")])

    def test_rejected_claim_has_no_effect(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12")]
        exp = export(msgs, [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12", review="rejected")], ["m1"])
        self.assertEqual((exp["status"], exp["rows"]), ("complete", []))

    def test_csv_round_trip_gives_the_confirmed_slots(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12, Saturday mornings maybe", sender="Ben Example")]
        claims = [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12"),
                  claim("m1", 2, "Saturday", "mornings", "Saturday mornings maybe", status="conditional", condition="maybe")]
        exp = export(msgs, claims, ["m1"])
        name, text = final_csv(exp)
        self.assertEqual(name, "availability-final-2026-11-09-complete.csv")
        self.assertTrue(text.startswith("# availability-final v1; week=2026-11-09; status=complete;"))
        accepted = [c for c in resolve_all(msgs, claims, ROSTER, CAL)]
        self.assertEqual(parse_final_csv(text, ROSTER, CAL)["slots"], final_slots(build_ledger(msgs, accepted, ROSTER, CAL), CAL))

    def test_reference_claims_reproduce_the_expected_sheet(self):
        messages, roster, cal, ref = load("A")
        exp = confirmed_export(messages, reference_claims(ref), roster, cal, [m.id for m in messages])
        got = {}
        for r in exp["rows"]:
            if r["status"]:
                got.setdefault(r["volunteer"], {}).setdefault(r["date"], []).append([r["start"], r["end"], r["status"]])
        self.assertEqual(got, {p: d for p, d in ref["expected_sheet"].items() if d})


class FinalSheetScoring(unittest.TestCase):
    ref = {("Ana Example", "2026-11-10", i): "available" for i in range(32, 40)}  # 14:00-16:00

    def parse(self, text):
        return parse_final_csv(text, ROSTER, CAL)

    def test_corrected_final_file_scores_only_the_replacement(self):
        final = self.parse(sheet("Ana Example,2026-11-10,14:00,16:00,available,,confirmed,m2.1"))
        self.assertEqual(score(final, self.ref, [], [])["slot_agreement"], 1.0)

    # clarification 1: a "complete" file must not contradict itself; provisional needs an explicit flag
    def test_complete_status_contradicted_by_needs_review_rows_is_rejected(self):
        with self.assertRaisesRegex(FinalSheetError, "status=complete contradicts 1 needs_review"):
            self.parse(sheet("Ana Example,2026-11-10,,,,,needs_review,"))

    def test_complete_status_contradicted_by_metadata_is_rejected(self):
        for kw in ({"pending": 2}, {"unrev": "m03 m07"}):
            with self.subTest(**kw), self.assertRaisesRegex(FinalSheetError, "status=complete contradicts"):
                self.parse(sheet("Ana Example,2026-11-10,14:00,16:00,available,,confirmed,", **kw))

    def test_provisional_file_needs_allow_provisional(self):
        messages, roster, cal, ref = load("A")
        text = sheet(status="provisional", unrev="m03").replace("2026-11-09", ref["week_start"])
        with self.assertRaisesRegex(FinalSheetError, "allow-provisional"):
            score_text(text, "A")
        self.assertTrue(score_text(text, "A", allow_provisional=True)["provisional"])

    # clarification 2: an unresolved person/day is 68 slots of disagreement, counted once per cell
    def test_unresolved_cell_is_68_disagreeing_slots_even_when_it_matches(self):
        self.assertEqual(N_SLOTS, 68)
        final = self.parse(sheet("Ana Example,2026-11-10,14:00,16:00,available,,needs_review,m1.1",
                                 "Ana Example,2026-11-10,,,,,needs_review,", status="provisional"))
        got = score(final, self.ref, [], [])
        self.assertEqual((got["unresolved_cells"], got["unresolved_slots"], got["slots_compared"], got["slot_agreement"]),
                         (1, 68, 68, 0.0))

    # clarification 3: strict parsing straight into final slots
    def test_invalid_rows_are_rejected(self):
        bad = {
            "not on the roster": "Zed Nobody,2026-11-10,14:00,16:00,available,,confirmed,",
            "not a date in the week": "Ana Example,2026-11-17,14:00,16:00,available,,confirmed,",
            "start < end": "Ana Example,2026-11-10,16:00,14:00,available,,confirmed,",
            "06:00 <= start": "Ana Example,2026-11-10,05:45,07:00,available,,confirmed,",
            "15-minute boundary": "Ana Example,2026-11-10,14:10,16:00,available,,confirmed,",
            "not a HH:MM": "Ana Example,2026-11-10,2pm,16:00,available,,confirmed,",
            "status available or conditional": "Ana Example,2026-11-10,14:00,16:00,maybe,,confirmed,",
            "cell_state must be": "Ana Example,2026-11-10,14:00,16:00,available,,done,",
            "both available and conditional": "Ana Example,2026-11-10,10:00,12:00,available,,confirmed,\n"
                                              "Ana Example,2026-11-10,11:00,13:00,conditional,x,confirmed,",
        }
        for reason, line in bad.items():
            with self.subTest(reason), self.assertRaisesRegex(FinalSheetError, reason):
                self.parse(sheet(line))

    def test_invalid_metadata_is_rejected(self):
        cases = {
            "line 1 must be the status line": HEADER + "\n",
            "missing blocking_issues": "# availability-final v1; week=2026-11-09; status=complete; unreviewed=; pending=0\n" + HEADER,
            "does not match the week": sheet().replace("week=2026-11-09", "week=2026-11-16"),
            "complete or provisional": sheet().replace("status=complete", "status=done"),
            "whole number": sheet().replace("pending=0", "pending=two"),
            "columns must be exactly": sheet().replace(",sources", ""),
        }
        for reason, text in cases.items():
            with self.subTest(reason), self.assertRaisesRegex(FinalSheetError, reason):
                self.parse(text)

    def test_same_status_overlap_and_spreadsheet_padding_are_accepted(self):
        text = sheet("Ana Example,2026-11-10,14:00,15:00,available,,confirmed,",
                     "Ana Example,2026-11-10,14:30,16:00,available,,confirmed,").replace(
            "blocking_issues=0", "blocking_issues=0,,,,,,,")
        self.assertEqual(score(self.parse("﻿" + text), self.ref, [], [])["slot_agreement"], 1.0)

    def test_withdrawal_still_available_is_a_final_state_error(self):
        w = [{"msg": "m2", "person": "Ana Example", "date": "2026-11-10", "start": "14:00", "end": "16:00"}]
        final = self.parse(sheet("Ana Example,2026-11-10,14:00,16:00,available,,confirmed,"))
        self.assertEqual(score(final, {}, w, [])["withdrawal_final_state_errors"], 1)
        self.assertEqual(score(self.parse(sheet()), {}, w, [])["withdrawal_final_state_errors"], 0)


class UnreviewedScope(unittest.TestCase):
    """Only accepted or pending claims say which person/day an unreviewed message is about."""

    invented = claim("m1", 1, "Tuesday", "10-12", "I can do Tuesday 10-12", review="pending")  # not in the message

    def test_dropped_only_message_marks_no_cell_but_stays_unreviewed(self):
        msgs = [msg("m1", 2, 9, "Happy to help")]
        resolved = resolve_all(msgs, [self.invented], ROSTER, CAL)
        self.assertEqual(resolved[0]["review"], "dropped")
        exp = confirmed_export(msgs, resolved, ROSTER, CAL, [])
        self.assertEqual((exp["status"], exp["unreviewed"], exp["needs_review_cells"], exp["rows"]),
                         ("provisional", ["m1"], 0, []))

    def test_rejected_only_message_marks_no_cell_but_stays_unreviewed(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12")]
        exp = export(msgs, [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12", review="rejected")], [])
        self.assertEqual((exp["status"], exp["unreviewed"], exp["needs_review_cells"], exp["rows"]),
                         ("provisional", ["m1"], 0, []))

    def test_mixed_message_takes_scope_from_the_accepted_claim_only(self):
        msgs = [msg("m1", 2, 9, "Tuesday 10-12 works")]
        claims = [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12 works"),
                  claim("m1", 2, "Thursday", "2-4", "Thursday 2-4 is fine", review="pending")]  # invented, dropped
        resolved = resolve_all(msgs, claims, ROSTER, CAL)
        self.assertEqual([c["review"] for c in resolved], ["accepted", "dropped"])
        exp = confirmed_export(msgs, resolved, ROSTER, CAL, [])
        self.assertEqual((exp["status"], exp["needs_review_cells"]), ("provisional", 1))
        self.assertEqual(rows(exp), [("Ana Example", "2026-11-10", "10:00", "12:00", "available", "needs_review")])


class ConditionFinalState(unittest.TestCase):
    """Every slot of a reference condition's interval must hold the expected final status."""

    def cond(self, expected):
        return [{"person": "Ana Example", "date": "2026-11-10", "start": "14:00", "end": "16:00", "expected_final": expected}]

    def errors(self, expected, *lines):
        final = parse_final_csv(sheet(*lines), ROSTER, CAL)
        got = score(final, {}, [], self.cond(expected))
        return got["condition_final_state_errors"], got["condition_error_list"]

    def test_partial_loss_of_expected_availability_is_an_error(self):
        n, errs = self.errors("available", "Ana Example,2026-11-10,14:00,15:00,available,,confirmed,")
        self.assertEqual((n, errs), (1, ["Ana Example 2026-11-10 14:00-16:00: availability partly lost"]))

    def test_partial_loss_of_expected_conditional_is_an_error(self):
        n, errs = self.errors("conditional", "Ana Example,2026-11-10,15:00,16:00,conditional,if dry,confirmed,")
        self.assertEqual((n, errs), (1, ["Ana Example 2026-11-10 14:00-16:00: offer partly lost"]))

    def test_one_error_per_condition_and_existing_cases_unchanged(self):
        cases = [
            ("available", ["Ana Example,2026-11-10,14:00,16:00,available,,confirmed,"], 0, None),
            ("available", ["Ana Example,2026-11-10,14:00,15:00,conditional,x,confirmed,"], 1, "resolution missed"),
            ("available", [], 1, "availability lost"),
            ("conditional", ["Ana Example,2026-11-10,14:00,16:00,conditional,x,confirmed,"], 0, None),
            ("conditional", ["Ana Example,2026-11-10,14:00,15:00,available,,confirmed,"], 1, "treated as firm"),
            ("conditional", [], 1, "offer lost"),
            ("none", [], 0, None),
            ("none", ["Ana Example,2026-11-10,15:00,15:15,available,,confirmed,"], 1, "decline missed"),
        ]
        for expected, lines, n, kind in cases:
            with self.subTest(expected=expected, lines=lines):
                got_n, errs = self.errors(expected, *lines)
                self.assertEqual(got_n, n)
                if kind:
                    self.assertTrue(errs[0].endswith(kind), errs)
        final = parse_final_csv(sheet("Ana Example,2026-11-10,,,,,needs_review,", status="provisional"), ROSTER, CAL)
        self.assertEqual(score(final, {}, [], self.cond("available"))["condition_final_state_errors_unresolved"], 1)


class DuplicateMetadata(unittest.TestCase):
    """A repeated status-line key must never silently overwrite an earlier value."""

    def with_extra(self, extra, status="provisional", unrev="m03", pending=0):
        return sheet(status=status, unrev=unrev, pending=pending).replace("blocking_issues=0", "blocking_issues=0; " + extra, 1)

    def test_duplicate_keys_are_rejected_by_the_parser(self):
        cases = [self.with_extra("status=complete"), self.with_extra("pending=0", pending=2),
                 self.with_extra("unreviewed=", unrev="m03"), self.with_extra("status=provisional")]  # last: same value
        for text in cases:
            with self.subTest(text=text.split(chr(10))[0]), self.assertRaisesRegex(FinalSheetError, "repeats"):
                parse_final_csv(text, ROSTER, CAL)

    def test_scorer_and_cli_refuse_duplicate_keys_even_with_allow_provisional(self):
        import os
        import subprocess
        import tempfile
        text = self.with_extra("status=complete")
        with self.assertRaisesRegex(FinalSheetError, "repeats"):
            score_text(text, "A", allow_provisional=True)
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write(text)
        try:
            root = Path(__file__).resolve().parent.parent
            for extra in ([], ["--allow-provisional"]):
                r = subprocess.run([sys.executable, "-m", "evaluation.score_final", f.name, "--set", "A", *extra],
                                   cwd=root, capture_output=True, text=True)
                self.assertEqual(r.returncode, 2, r.stderr)
                self.assertIn("repeats", r.stderr)
        finally:
            os.unlink(f.name)


class CsvFormulaSafety(unittest.TestCase):
    """Cells a spreadsheet would run as formulas are written with a leading apostrophe (COR-02)."""

    def test_cells_starting_with_formula_characters_are_neutralised(self):
        for raw in ("=1+1", "+44 7700", "-if dry", "@SUM(A1)", "\tTab", "\rReturn"):
            with self.subTest(raw=raw):
                self.assertEqual(_cell(raw), "'" + raw)
        for raw in ("Ana Example", "2026-11-10", "14:00", "", "a=b", "'quoted"):
            with self.subTest(raw=raw):
                self.assertEqual(_cell(raw), raw)
        self.assertEqual(_cell(None), "")

    def test_round_trip_keeps_formula_like_names_and_conditions(self):
        roster = ["=Eve Example", "Ben Example"]
        msgs = [msg("m1", 2, 9, "Tuesday 10-12 if =SUM(A1) is dry", sender="=Eve Example")]
        claims = [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12 if =SUM(A1) is dry", status="conditional",
                        condition="=SUM(A1) is dry")]
        resolved = resolve_all(msgs, claims, roster, CAL)
        exp = confirmed_export(msgs, resolved, roster, CAL, ["m1"])
        _, text = final_csv(exp)
        self.assertIn("'=Eve Example,2026-11-10,10:00,12:00,conditional,'=SUM(A1) is dry,confirmed,m1.1", text)
        parsed = parse_final_csv(text, roster, CAL)
        self.assertEqual(parsed["slots"], final_slots(build_ledger(msgs, resolved, roster, CAL), CAL))
        typed = text.replace("'=Eve Example", "=Eve Example")  # a typist who does not add the apostrophe
        self.assertEqual(parse_final_csv(typed, roster, CAL)["slots"], parsed["slots"])


class ServerRoutes(unittest.TestCase):
    def test_resolve_summary_and_export_route(self):
        import server
        msgs = [msg("m1", 2, 9, "Tuesday 10-12").to_dict()]
        body = {"messages": msgs, "claims": [claim("m1", 1, "Tuesday", "10-12", "Tuesday 10-12")], "roster": ROSTER,
                "week_start": "2026-11-09"}
        self.assertEqual(server.resolve(body)["confirmed"]["status"], "provisional")
        out = server.export({**body, "reviewed_messages": ["m1", "m99"]})
        self.assertEqual((out["status"], out["unknown_reviewed"], out["rows"]), ("complete", ["m99"], 1))
        self.assertEqual(out["filename"], "availability-final-2026-11-09-complete.csv")
        with self.assertRaisesRegex(ValueError, "reviewed_messages"):
            server.export({**body, "reviewed_messages": "m1"})


if __name__ == "__main__":
    unittest.main()
