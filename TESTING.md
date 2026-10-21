# Testing

How to check this project, and what has actually been checked. Written 2026-10-21. Counts are snapshots: re-run before you rely on them.

## Unit tests (offline: no model, no network)

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

**At committed HEAD `c5a2e05`:** **66 tests pass** on Python 3.15.0 and 3.12 (macOS), verified 2026-10-21 in a clean `git archive` copy.

| File | Tests at HEAD | Covers |
|---|---|---|
| `tests/test_ledger.py` | 21 | Date/time resolution, names, ledger history; references A and B reproduce their `expected_sheet` (set C's was checked by the owner's script before freezing, not in this test) |
| `tests/test_export.py` | 30 | Accepted-only final sheet, explicit review, strict CSV reader/scorer, formula neutralising |
| `tests/test_evaluation.py` | 5 | Duplicate-aware unit scoring (EVAL-10), partial condition loss (EVAL-09) |
| `tests/test_review_safeguards.py` | 10 | COR-10 "check the wording" flag (no hold), COR-07a warning |

**Working tree (uncommitted, 2026-10-21):** a new `tests/test_d31_fixes.py` for COR-13 to COR-17 brings the total to **81**. At 11:13 IST all 81 passed. That work is in progress and unreviewed (see [context.md §G](context.md#g-current-state-at-handover-2026-10-21-about-1115-ist)).

**CI:** `.github/workflows/tests.yml` runs this command on push and PR to `main` (Python 3.12, ubuntu-latest). First run "tests #1" on `56e38bd` passed (owner screenshot); later runs have not been observed by the lead.

## Browser checks (optional, not in CI)

Need Node 22+ and a local Google Chrome (`CHROME=/path` to override). They start `server.py` and headless Chrome, install nothing, and use invented messages:

```bash
PYTHONDONTWRITEBYTECODE=1 node tests/browser/session_rerun.mjs
```

| Script | Checks | Last reported result (coding agent, 2026-10-20/21; not re-run by the lead) |
|---|---|---|
| `session_rerun.mjs` | A failed rerun keeps the reviewed session and export; a successful one starts fresh (COR-11) | 10/10 |
| `extraction_failures.mjs` | Per-message failure warnings and continued reading (COR-03) | 14/14 |
| `csv_safety.mjs` | Formula neutralising in both exports (COR-02) | 4/4 |
| `sheet_display.mjs` | Pending vs accepted display at 1400 px and 390 px (UI-05/UI-01/UI-07) | 28/28 |
| `review_safeguards.mjs` | "Check the wording" flag and the missed-change warning in the UI | 10/10 |
| `harness.mjs` | Shared helper, not a test | — |

The agent also ran two checks kept in its own scratchpad, not in the repo: final export 13/13 and keyboard 18/18. They are not reproducible from the repo.

## Evaluation (accuracy on fictional data)

```bash
python3 -m evaluation.compare            # saved current tables (read-only)
python3 -m evaluation.compare frozen     # A/B first scores
python3 -m evaluation.run --set A --extractor rules
```

- **Fresh model calls on cache misses:** `evaluation.run` with `--extractor model` or `hybrid` calls Ollama whenever a cached output is missing, even without `--refresh`. Confirm `evaluation/runs/<model>_prompt3[_setB|_setC]/` covers every non-duplicate message first.
- **Results get overwritten:** it overwrites `evaluation/results/*.json`. Never write into `frozen/`, `frozen-setC/` or `tuning/`.
- **Qwen is no longer installed** (2026-10-21). Its cached A/B outputs still allow cache-only re-scoring.
- **Set C** was scored once (EVAL-07, frozen in `evaluation/results/frozen-setC/`). Every later set C number is **post-hoc**.
- **Results and provenance:** [evaluation/RESULTS.md](evaluation/RESULTS.md).

## Final-sheet scoring (timing study)

```bash
python3 -m evaluation.score_final FILE.csv --set A
```

This scores a confirmed final-sheet CSV, from the app's **Export final sheet** or a manual sheet filled in from `evaluation/final_sheet_template.csv`. The study protocol is in [evaluation/MEASUREMENT.md](evaluation/MEASUREMENT.md). **No human timing has been run.**

## Not tested

- Safari and Firefox.
- Screen readers, colour contrast (UI-02).
- Python 3.10 and 3.11.
- Linux locally (CI covers Ubuntu with 3.12).
- Real messages.
- Run-to-run model variation.
- Any hosted deployment (none exists).
