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

**Working tree, 2026-10-21 (INT-11, uncommitted):** **91 tests pass** on Python 3.15.0 and 3.12.6. Since `c5a2e05`: `tests/test_d31_fixes.py` (COR-13 to COR-18, 18 tests) and `tests/test_cache_only.py` (INT-11, 7 tests: `--cache-only` never reaches the patched model call, `--out` refuses protected folders, the CI summary fails on any score difference or fresh call).

**Working tree (uncommitted, 2026-10-21):** a new `tests/test_d31_fixes.py` for COR-13 to COR-17 brings the total to **81**. At 11:13 IST all 81 passed. That work is in progress and unreviewed (see [context.md §G](context.md#g-current-state-at-handover-2026-10-21-about-1115-ist)).

**CI:** see [CI (GitHub Actions)](#ci-github-actions).

## CI (GitHub Actions)

`.github/workflows/tests.yml` runs on every push and pull request to `main` (ubuntu-latest, Python 3.12). It has read-only token permissions, no secrets, no deployment and no Ollama. Its jobs are the GitHub Actions automation entered under the Copilot category (D-33).

| Job | What it does | Fails when |
|---|---|---|
| `unit` (INT-10) | The unit-test command above | Any test fails |
| `integrity` (INT-11) | `sha256sum --check --strict evaluation/protected.sha256` (every file in `evaluation/results/frozen/`, `frozen-setC/`, `tuning/` and `fixtures/setC.manifest`); then compares the folders' file list with the checksum list | A protected file changed, went missing or was added |
| `rescore` (INT-11) | For sets A, B and C: rules, then Gemma and Gemma + rules with `--model gemma4:e2b-it-qat --cache-only --out "$RUNNER_TEMP/rescore"`. Then `python3 -m evaluation.ci_summary` writes a table (units right on held-out messages, missed cancellations and slot agreement on the final sheet, fresh calls, "matches committed") to `$GITHUB_STEP_SUMMARY`. Last step: the checkout has no changes, so nothing is committed back | A saved model output is missing; any scoring field differs from the committed `evaluation/results/*.json` of the same name (run time, speed and memory are not compared); any fresh model call |

- **Consequence:** a commit that changes scores must also commit the re-scored `evaluation/results/*.json`, or `rescore` fails.
- **Changing a protected file:** `evaluation/protected.sha256` may only be regenerated after a recorded decision, never to make the check pass.
- **Run the same checks locally:**

```bash
shasum -a 256 -c evaluation/protected.sha256      # sha256sum -c on Linux
out=$(mktemp -d); for s in A B C; do python3 -m evaluation.run --set $s --extractor rules --out $out >/dev/null; for ex in model hybrid; do python3 -m evaluation.run --set $s --extractor $ex --model gemma4:e2b-it-qat --cache-only --out $out >/dev/null; done; done; python3 -m evaluation.ci_summary $out
```

**Runs observed:** "tests #1" on `56e38bd` (unit job only) passed (owner screenshot). The `integrity` and `rescore` jobs have **not yet run on GitHub**; locally (2026-10-21, macOS, Python 3.12.6 and 3.15.0, a copy of the working tree with ignored files left out) both pass, `rescore` takes under 2 s, and the checksum checks fail as intended on a modified frozen file and on an added file.

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

- **Fresh model calls on cache misses:** `evaluation.run` with `--extractor model` or `hybrid` calls Ollama whenever a cached output is missing, even without `--refresh`. Add `--cache-only` to make a miss an error instead (no model call, no memory sampling), and `--out DIR` to write results somewhere other than `evaluation/results/`. Confirm `evaluation/runs/<model>_prompt3[_setB|_setC]/` covers every non-duplicate message first.
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
