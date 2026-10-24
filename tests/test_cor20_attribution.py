"""COR-20: warn when a suggestion may be about someone other than the sender. Invented messages only; none copy or
paraphrase set A, B or C.
Run: python3 -m unittest discover -s tests"""
import re
import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ledger.core import resolve_all  # noqa: E402
from ledger.messages import Message  # noqa: E402
from ledger.resolve import Calendar  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CAL = Calendar(date(2026, 11, 9))  # Mon 9 Nov 2026 to Sun 15 Nov 2026
ROSTER = ["Ana Example", "Ben Example", "Cleo Sample", "Tomás Demo"]
NEW = {"not_sender", "names_other_person"}


def flags_for(sender, text, person="SENDER", override=None, roster=ROSTER):
    m = Message("m01", datetime(2026, 11, 9, 9, 0), sender, text)
    c = {"id": "m01.1", "msg": "m01", "n": 1, "source": "model", "review": "pending", "said": {
        "person": person, "day_text": "Friday", "time_text": "morning", "status": "available", "condition": "",
        "replaces_earlier": False, "excerpt": text}}
    if override:
        c["override"] = override
    r = resolve_all([m], [c], roster, CAL)[0]
    return r["person"], set(r["flags"]) & NEW


class NotSender(unittest.TestCase):
    def test_offer_filed_under_the_person_asked_about(self):
        # The sender offers to cover for someone else; the model files it under that person.
        person, new = flags_for("Ben Example", "Is Ana still on for Friday morning? Happy to cover it if not.", person="Ana")
        self.assertEqual(person, "Ana Example")
        self.assertEqual(new, {"not_sender"})

    def test_coordinator_relaying_for_a_volunteer(self):
        person, new = flags_for("Pat (coordinator)", "Cleo says Friday morning works for her.", person="Cleo")
        self.assertEqual(person, "Cleo Sample")
        self.assertIn("not_sender", new)

    def test_own_answer_is_not_flagged(self):
        self.assertEqual(flags_for("Ana Example", "Friday morning works for me.")[1], set())

    def test_accents_in_the_sender_name_still_count_as_the_sender(self):
        person, new = flags_for("Tomas Demo", "Friday morning is fine.")
        self.assertEqual((person, new), ("Tomás Demo", set()))

    def test_model_naming_the_sender_explicitly_is_not_flagged(self):
        self.assertEqual(flags_for("Ana Example", "Friday morning works.", person="Ana")[1], set())

    def test_a_reviewer_choosing_the_person_clears_it(self):
        _, new = flags_for("Ben Example", "Is Ana still on for Friday morning?", person="Ana",
                           override={"person": "Ana Example"})
        self.assertNotIn("not_sender", new)


class NamesOtherPerson(unittest.TestCase):
    def test_a_second_volunteer_mentioned_alongside_the_sender(self):
        # Both readers would credit only the sender here; the message also speaks for Ben.
        person, new = flags_for("Cleo Sample", "Ben and I can both do Friday morning.")
        self.assertEqual(person, "Cleo Sample")
        self.assertEqual(new, {"names_other_person"})

    def test_names_are_matched_as_whole_words_after_normalising_case(self):
        self.assertEqual(flags_for("Cleo Sample", "Friday morning, bringing the bench and a benefit form.")[1], set())
        self.assertEqual(flags_for("Cleo Sample", "friday morning, ana might join too")[1], {"names_other_person"})

    def test_the_senders_own_first_name_is_not_another_person(self):
        self.assertEqual(flags_for("Ana Example", "Hi, it's Ana. Friday morning works.")[1], set())

    def test_the_person_already_flagged_by_not_sender_is_not_counted_twice(self):
        self.assertEqual(flags_for("Ben Example", "Is Ana still on for Friday morning?", person="Ana")[1], {"not_sender"})


class BlocksBulkAccept(unittest.TestCase):
    """Both flags are warnings: they block "Accept all suggestions without warnings" and count as visible in scoring."""

    def test_flags_are_labelled_and_not_informational_in_the_ui(self):
        js = (ROOT / "ui" / "app.js").read_text()
        info = re.search(r"const INFO_FLAGS = new Set\(\[(.*?)\]\)", js).group(1)
        for f in NEW:
            self.assertIn(f"{f}:", js, f"{f} has a label")
            self.assertNotIn(f'"{f}"', info, f"{f} must not be informational")

    def test_scoring_treats_them_as_visible_warnings(self):
        from evaluation.run import WARNING_FLAGS
        self.assertTrue(NEW <= WARNING_FLAGS)


if __name__ == "__main__":
    unittest.main()
