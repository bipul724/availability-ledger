# Progress

**Last updated:** 2026-10-20 11:25 IST (Asia/Kolkata, the machine's local time). Corrected after a same-day review; see "Corrections" below.
**Inspected by:** a coding agent reading the source, running the offline checks below, and probing the local server with fictional data. No model calls were made for this report.

## Status vocabulary

| Word | Meaning |
|---|---|
| Implemented | present in source |
| Verified | supported by a check that was run, or recorded evidence in the repo |
| Partial | some behaviour exists; specific pieces are missing |
| Planned | intended, not implemented |
| Unverified | not enough evidence either way |
| Deferred | deliberately outside the current release |

Implemented does not imply Verified.

## What was inspected

`server.py`, every file in `ledger/`, `ui/`, `tests/`, `evaluation/` (scripts, `RESULTS.md`, `TUNING.md`, `MEASUREMENT.md`, result JSONs including `frozen/`, cached run statistics), fixture metadata and formats (not used to change behaviour), and the project folder for manifests, licence, deployment files and environment files (none exist). The challenge page was read once for category wording.

## Capabilities

| Capability | State | Evidence |
|---|---|---|
| Local server on 127.0.0.1, static UI, 5 JSON routes | Implemented, Verified | handler probe and headless Chrome, 2026-10-20 |
| Message parsing (pipe, WhatsApp Android/iOS, multi-line) | Implemented, Verified for pipe format (fixtures); WhatsApp formats Implemented, not exercised by a test | `ledger/messages.py` |
| Roster matching, ambiguous and similar names (a unique 3+ letter prefix resolves) | Implemented, Verified | unit tests; direct check of `match_person` |
| Readers: model, rules, model + rules | Implemented, Verified | evaluation runs (cached) |
| Day and time resolution incl. "4 onwards", "the same" in one message, day modifiers from the quote | Implemented, Verified | unit tests |
| Evidence gate and quote-supports-days | Implemented, Verified; **Partial guarantee**: a real quote with invented day/time words is flagged but applied provisionally | evaluation; mocked check 2026-10-20 ("Happy to help" + "Tuesday 2-4" reached the sheet) |
| Ledger: history, corrections per day, cancellations, conditions, conflicts, counts | Implemented, Verified | unit tests, reference-sheet test for sets A and B |
| Duplicate collapse | Implemented, Verified | unit tests; demo shows m12 "Same as m11" in headless Chrome |
| Review UI: accept/reject/edit/reset/add, bulk accept | Implemented; button flows Verified indirectly | headless Chrome keyboard run exercised the same code paths |
| Keyboard review J/K/A/R/E/Esc | Implemented, Verified | headless Chrome with real key events, 2026-10-20 |
| CSV export (record log) | Implemented, Verified in headless Chrome (CSV content and export status line); the saved download itself was not inspected. **Cannot reliably be replayed into the final sheet** (no `replaces_earlier`) | 2026-10-20 run: 3 accepted rows with the documented columns; a superseded offer was still exported as `available`, confirming COR-01 |
| Confirmed final-sheet export | Planned | COR-01 (pending items must not be exported as confirmed) |
| Session persistence | Planned | COR-04 |
| Timezone conversion | Not implemented (field stored, unused) | COR-05 |
| Visible extraction-failure warnings | Planned | COR-03 |
| Hosted demo | Planned (replay only) | DEP-02 |
| Sponsor integrations other than Gemma | Planned or needs decision; none other than Gemma implemented; no evidence of Copilot or Entire development use | [TASKS.md](TASKS.md#optional-sponsor-integrations) |

## Checks performed on 2026-10-20

| Command | Outcome |
|---|---|
| `python3 -m unittest discover -s tests` | `Ran 21 tests … OK` (14 original + 7 added that day) |
| `python3 server.py` + headless Chrome driving the page (demo → Rules only → Suggest records → keyboard review) | all keyboard checks passed; sheet and chart updated after A and R; no console errors after adding an inline empty favicon |
| Same headless run, then the page's `buildCsv` and the Export button | CSV header and rows as documented; status line "Exported 3 rows. Review so far: … 3 accepts, 2 field edits, 3 rejects…" |
| Mocked checks for the review (fictional data, in-process) | CSV replay of "Tuesday 10-12" then "Tuesday 2-4 instead" gave both ranges (app sheet: 14:00–16:00 only); real quote + invented phrases stayed `pending` and reached the sheet; hybrid with an empty model reply added only rules cancellations; "Sam" resolved with only Samira on the roster |
| Frozen and tuning result JSONs, memory fields | fresh-call files with samples: set A Qwen (438), set B Qwen (201), set B Gemma (55), three Gemma dev tuning runs (66, 113, 79); all other frozen files are cache replays with 1 sample |
| Direct handler calls with fictional data | `/api/status` 200 (Ollama listed `gemma4:e2b-it-qat` only, so Qwen is not installed on this machine now); error shapes as documented in API.md |
| All 10 evaluation configurations from cache (`evaluation.run` loop in [CLAUDE.md](CLAUDE.md)) | 0 fresh model calls; results written to `evaluation/results/` |
| `python3 -m evaluation.compare frozen` and `python3 -m evaluation.compare` | tables below |
| `python3 -m evaluation.score_csv fixtures/manual_entry_template.csv --set A` | runs; `rows_used: 0` as expected for the empty template |
| Cached-run statistics in `evaluation/runs/*/m*.json` | Gemma prompt 3 median 2.45 s (set A) / 2.30 s (set B), max 9.2 s, ≈ 29–33 tokens/s; Qwen median 8.71 / 11.04 s, max 17.8 s; 0 JSON failures |

Python used: 3.15.0 on macOS. Python 3.10 (the stated minimum) was not tested.

## Known defects and gaps (in current code)

1. Export is a record log, not the final sheet; superseded offers appear as rows, and the log cannot reliably be replayed into the sheet because it lacks `replaces_earlier` (COR-01, EVAL-06).
1b. `evaluation/score_csv.py` replays every row as not replacing anything, so it mis-scores corrections. EVAL-06 replaces it for timing with a final-sheet scorer ([docs/specs/final-export.md](docs/specs/final-export.md)).
1c. The sheet and chart include pending suggestions; a real quote with invented day/time words is applied provisionally (COR-10, UI-05).
2. Exported text is not protected against spreadsheet formula injection (COR-02).
3. A model JSON failure is not flagged: with model only it looks like "No availability found"; with model + rules only rules-added cancellations appear. A request error stops the run (COR-03).
4. Reload or re-run loses review decisions (COR-04).
5. Timezone field unused (COR-05). Roster silently truncated at 20 (COR-06).
6. "Scratch Wednesday"-style cancellations are missed silently by Gemma + rules on set B (COR-07; must not be tuned on set B).
7. The availability sheet overflows its panel horizontally (UI-01).
8. No licence file; not a git repository (REL-01, REL-02).
9. (Fixed 2026-10-20, REL-03) RESULTS.md, TUNING.md and MEASUREMENT.md now carry scope labels, snapshot labels, the swap distinction, the post-hoc section and a revised timing protocol.

## Evaluation status

All data is **fictional**, written by the same author who wrote the references and the rules; nobody independent checked it. These numbers describe technical behaviour on synthetic messages. They are **not** evidence of demand, accuracy on real chats, or time saved.

### Provenance

| Snapshot | What it is | Where |
|---|---|---|
| Frozen | first scoring of prompt v3 on each set; set B frozen before any scoring | `evaluation/results/frozen/` (never overwrite) |
| Post-hoc 1 | after the quote-supports-days rule (designed after seeing set B); changed only Qwen on set B | described in [RESULTS.md](evaluation/RESULTS.md) |
| Post-hoc 2 (current) | after the 2026-10-20 changes: duplicate collapse, day-modifier restoration, "onwards" and "the same". Day modifiers and "the same" were motivated by held-out messages (set A m26, set B m18, set B "the same") | `evaluation/results/*.json` |

Dev data: 30 set A messages (prompt tuning only). Held-out: 20 set A messages and all 20 set B messages.

### Held-out results

Format: units right · silent errors · cancellations still on the **final sheet** (ledger level) · message-level missed cancellations (unit level) · slot agreement.

| Reader | Set A frozen | Set A current (post-hoc) | Set B frozen | Set B current (post-hoc) |
|---|---|---|---|---|
| Rules only | 20/30 · 10 · 0/12 · 0 · 0.787 | 19/30 · 11 · 0/12 · 0 · 0.787 | 17/35 · 18 · 3/5 · 1 · 0.570 | 16/35 · 19 · 3/5 · 1 · 0.570 |
| Gemma 4 E2B only | 20/30 · 9 · 7/12 · 4 · 0.775 | 20/30 · 9 · 7/12 · 4 · 0.797 | 28/35 · 5 · 1/5 · 2 · 0.731 | 30/35 · 5 · 3/5 · 2 · 0.845 |
| Gemma 4 E2B + rules | 26/30 · 3 · 0/12 · 0 · 0.851 | 24/30 · 5 · 0/12 · 0 · 0.876 | 30/35 · 3 · 0/5 · 1 · 0.776 | 31/35 · 4 · 1/5 · 1 · 0.925 |
| Qwen3.5 4B only | 24/30 · 5 · 5/12 · 3 · 0.902 | 24/30 · 5 · 5/12 · 3 · 0.926 | 31/35 · 3 · 0/5 · 0 · 0.409 | 32/35 · 3 · 1/5 · 0 · 0.961 |
| Qwen3.5 4B + rules | 29/30 · 0 · 0/12 · 0 · 0.973 | 27/30 · 2 · 0/12 · 0 · 1.0 | 32/35 · 1 · 0/5 · 0 · 0.409 | 32/35 · 2 · 0/5 · 0 · 1.0 |

Every "current" set B number is **post-hoc (code changed after set B was seen)**.

**Scope:** units right, silent errors and message-level missed cancellations are computed on held-out messages only. Final-sheet cancellations and slot agreement are ledger metrics over every message in the set: all 50 set A messages (30 of them dev), and all 20 set B messages.

What moved, from switching each 2026-10-20 change off in turn:
- **Duplicate collapse** lowers "units right" by 1–2 and raises silent errors, because the references count a duplicate's units separately and a duplicate now produces none. Final sheets are unchanged.
- **Day-modifier restoration** raises slot agreement (set B: 0.776 → ≈ 0.93–1.0 for model readers).
- **"Onwards" and "the same"** make previously unreadable claims apply, which exposes cancellations the readers miss: more final-sheet misses for Gemma only (1/5 → 3/5), Gemma + rules (0/5 → 1/5) and Qwen only (0/5 → 1/5).

Message-level and final-sheet misses differ: a cancellation missed in its message can still be absent from the sheet if the offer it cancels was never applied, and the reverse when a newly readable offer is applied. RESULTS.md's ‡ note already warned that set B's 0/5 for Gemma + rules was partly luck.

### Speed and memory

Measures that must not be mixed:
- **Model-reported memory:** Ollama `/api/ps` says Gemma 4 E2B occupies 1.59 GB and Qwen3.5 4B 2.95 GB. That is the model's own allocation, not total system use.
- **System-wide memory:** lowest free memory during fresh runs was 14–15% for Gemma (dev tuning runs, set B) and 7% for Qwen (set A); macOS pressure was "warn" in nearly every sample.
- **Occupied swap vs swap traffic:** for Qwen on set A, occupied swap grew by 1,242 MB (6,653 → 7,896 MB, ≈ 1.2 GB) while swap-out *traffic* was ≈ 14.8 GiB (968,208 pages × 16 KB). The "about 15 GB" in RESULTS.md is traffic.

Provenance: only runs with fresh model calls measured memory. These are `results/frozen/setA_model_qwen…` (50 calls, 438 samples), `results/frozen/setB_model_qwen…` (20, 201), `results/frozen/setB_model_gemma…` (20, 55) and the three Gemma dev runs in `results/tuning/`. Every other frozen file replayed cached outputs and holds one sample describing the machine at replay time. RESULTS.md's Gemma "swap grew about 4 GB on first load" and "2% during the first load" have no backing file and are treated as unverified.

### Human effort

Not measured, and not measurable yet. The "effort proxy" (0.37–0.54 of manual actions in the current snapshot) counts clicks and typed fields, leaves out reading, and is not a time measurement. The revised protocol in [MEASUREMENT.md](evaluation/MEASUREMENT.md) needs matched workloads (not set A 50 vs set B 20), balanced order across more than one participant, equivalent final outputs and one scoring contract for confirmed final-sheet CSVs (COR-01, EVAL-06) before any time saving can be claimed.

## Remaining uncertainties

- Whether coordinators want this rather than a signup form (no user research).
- Whether review is faster than typing (no timing study).
- Behaviour on real chat exports, other languages and longer weeks.
- Challenge eligibility for every category, including whether `bipulchamoli.tech` was claimed through the Hacktoberfest offer, and whether the project was created inside the entry period.
- The deadline: the contest rules page says 25 Oct 11:59 PM PDT (26 Oct 12:29 PM IST); the DEV challenges API says `2026-10-25T06:59Z` (25 Oct 12:29 PM IST). See [TASKS.md](TASKS.md#release-blockers).
- The r/nonprofit post cited as anecdotal problem evidence could not be re-opened by the agent (fetch blocked).
- Licence the owner wants.
- Python versions below 3.15 and browsers other than headless Chrome.

## Next milestones

Order of work (from [TASKS.md](TASKS.md#order-of-work)):
1. Confirmed final export and one scoring contract for confirmed final-sheet CSVs (COR-01, EVAL-06).
2. Expose extraction failures and keep unsupported suggestions off the sheet (COR-03, COR-10).
3. Protect CSV output (COR-02).
4. Documentation and evaluation labels (REL-03, done 2026-10-20).
5. Timing study under the revised protocol (EVAL-02).

In parallel, owner actions: licence, git, eligibility and deadline confirmation (REL-01, REL-02, REL-04).

## Corrections (2026-10-20 review)

Earlier versions of these documents said, wrongly:
- that replaying the CSV export reconstructs the final sheet (it cannot: no `replaces_earlier`);
- that unsupported suggestions are dropped (only when both quote and phrases are missing);
- that the frozen JSONs contain no memory samples (three fresh-call files do), and gave swap traffic as if it were occupied swap;
- that state stays "in browser memory only" (it is also processed transiently by the local server);
- that a prefix such as "Sam" is always ambiguous (it resolves when only one roster name matches);
- that a hosted demo could be "on" the domain (the domain points at hosting; it does not host);
- that no integration is implemented (Gemma is);
- that there was no problem evidence (one anecdotal public post exists; still no interviews or validation).

RESULTS.md also labelled set A ledger metrics as held-out only and showed effort ratios without naming their snapshot; both are now labelled.
