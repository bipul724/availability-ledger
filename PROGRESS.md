# Progress

**Last updated:** 2026-10-20 (Asia/Kolkata). COR-01/EVAL-06 and subsequent COR-11/COR-12/EVAL-08 fixes are implemented. The latest pass aligns documentation with the owner-agreed technology direction; it changes no application code.
**Evidence provenance:** earlier implementation/source/browser checks below are historical records from this date. The latest documentation pass re-read relevant source and docs, reran all 49 offline unit tests, checked official category descriptions and verified documentation/file scope. It did not repeat browser, mutation or model-call experiments.

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

The earlier implementation audit read server, ledger/UI/tests, evaluation scripts and saved evidence, plus fixture metadata/formats without tuning behavior. The latest docs pass checked relevant current source, local Git status and all project Markdown/configuration documentation. No actual .env files, keys or private pilot data were read. Git and a comments-only .env.example exist; no application dependency manifest, licence or deployment configuration is present.

Competition research/source limits: [COMPETITION](docs/COMPETITION.md). Agreed roles, data boundaries, rollout and evidence gates: [INTEGRATIONS](docs/INTEGRATIONS.md). [AGENTS.md](AGENTS.md) is the discovery entrypoint; [CLAUDE.md](CLAUDE.md) remains the canonical detailed agent guide.

## Capabilities

| Capability | State | Evidence |
|---|---|---|
| Local server on 127.0.0.1, static UI, 6 JSON routes | Implemented, Verified | handler probe and headless Chrome, 2026-10-20 |
| Message parsing (pipe, WhatsApp Android/iOS, multi-line) | Implemented, Verified for pipe format (fixtures); WhatsApp formats Implemented, not exercised by a test | `ledger/messages.py` |
| Roster matching, ambiguous and similar names (a unique 3+ letter prefix resolves) | Implemented, Verified | unit tests; direct check of `match_person` |
| Readers: model, rules, model + rules | Implemented, Verified | evaluation runs (cached) |
| Day and time resolution incl. "4 onwards", "the same" in one message, day modifiers from the quote | Implemented, Verified | unit tests |
| Evidence gate and quote-supports-days | Implemented, Verified; **Partial guarantee**: a real quote with invented day/time words is flagged but applied provisionally | evaluation; mocked check 2026-10-20 ("Happy to help" + "Tuesday 2-4" reached the sheet) |
| Ledger: history, corrections per day, cancellations, conditions, conflicts, counts | Implemented, Verified | unit tests, reference-sheet test for sets A and B |
| Duplicate collapse | Implemented, Verified | unit tests; demo shows m12 "Same as m11" in headless Chrome |
| Review UI: accept/reject/edit/reset/add, bulk accept, explicit message review marks (button and `M`), "Accept all and mark reviewed" for eligible messages | Implemented, Verified | headless Chrome, 2026-10-20 (`ui_final_check`: 13 checks; keyboard check 18) |
| Keyboard review J/K/A/R/E/Esc | Implemented, Verified | headless Chrome with real key events, 2026-10-20 |
| Review-log CSV export | Implemented, Verified in headless Chrome; an audit trail that cannot be replayed into the sheet | 2026-10-20 runs |
| Confirmed final-sheet export and strict scorer (COR-01, EVAL-06), with review fixes COR-11, COR-12, EVAL-08 | Implemented, Verified | `tests/test_export.py` (28 tests, including 20 original export/scorer tests and 8 review-fix tests; earlier mutation checks); fixtures; headless Chrome; [spec](docs/specs/final-export.md) |
| Session persistence | Planned | COR-04 |
| Timezone conversion | Not implemented (field stored, unused) | COR-05 |
| Visible extraction-failure warnings | Planned | COR-03 |
| Hosted demo | Planned, not implemented/deployed; fixed fictional saved-output replay | DEP-02; [integration plan](docs/INTEGRATIONS.md) |
| Shortlisted sponsor uses | Planning direction agreed; only Gemma implemented. No completed Copilot/Actions/Entire, R-CLI, Sentry, Render/domain or ElevenLabs evidence verified | [TASKS](TASKS.md#optional-sponsor-integrations), [INTEGRATIONS](docs/INTEGRATIONS.md) |

## Earlier checks recorded on 2026-10-20

| Command | Outcome |
|---|---|
| `python3 -m unittest discover -s tests` | `Ran 49 tests … OK` (14 original, 7 for duplicates/modifiers/times, 20 for the final export and scorer, 8 for the review fixes) |
| Review fixes, red then green | the 8 new unit tests run against the unfixed code: 7 failed (unreviewed scope ×3, partial condition loss ×2, duplicate metadata ×2), 1 passed by design (guards unchanged condition outcomes); all pass after the fixes |
| `node tests/browser/session_rerun.mjs` (headless Chrome) | before the fix: 6 of 10 checks failed (a failed parse produced `availability-final-2026-11-16-complete.csv` from 9 Nov approvals; a non-Monday week and an empty input also altered the session); after: 10/10 pass, including a successful rerun that starts a fresh provisional session |
| Earlier browser checks after the fixes | final-export check 13/13, keyboard check 18/18 |
| Cached evaluation after the fixes | comparison table identical; 0 fresh model calls |
| Mutation check (scratch copy): accept contradictory `complete`; count unresolved slots as agreement; ignore unreviewed messages' claims; allow contradictory overlaps | each caught by its intended test |
| `python3 -m evaluation.score_final` on files built from the fixtures | complete file typed from `expected_sheet`: slot agreement 1.0, 0 final-state errors (sets A and B); export of the reference claims: provisional (A: 3 blocking issues, B: 1), refused without `--allow-provisional` (exit 2); blank template rejected until the week is filled |
| Cached evaluation re-run after COR-01/EVAL-06 | comparison table byte-identical to before; 0 fresh model calls |
| `python3 server.py` + headless Chrome driving the page (demo → Rules only → Suggest records → keyboard review) | all keyboard checks passed; sheet and chart updated after A and R; no console errors after adding an inline empty favicon |
| Same headless run, then the page's `buildCsv` and the Export button | CSV header and rows as documented; status line "Exported 3 rows. Review so far: … 3 accepts, 2 field edits, 3 rejects…" |
| Mocked checks for the review (fictional data, in-process) | CSV replay of "Tuesday 10-12" then "Tuesday 2-4 instead" gave both ranges (app sheet: 14:00–16:00 only); real quote + invented phrases stayed `pending` and reached the sheet; hybrid with an empty model reply added only rules cancellations; "Sam" resolved with only Samira on the roster |
| Frozen and tuning result JSONs, memory fields | fresh-call files with samples: set A Qwen (438), set B Qwen (201), set B Gemma (55), three Gemma dev tuning runs (66, 113, 79); all other frozen files are cache replays with 1 sample |
| Direct handler calls with fictional data | `/api/status` 200 (Ollama listed `gemma4:e2b-it-qat` only at that recorded probe; installed models were not rechecked in the docs pass); error shapes as documented in API.md |
| All 10 evaluation configurations from cache (`evaluation.run` loop in [CLAUDE.md](CLAUDE.md)) | 0 fresh model calls; results written to `evaluation/results/` |
| `python3 -m evaluation.compare frozen` and `python3 -m evaluation.compare` | tables below |
| `python3 -m evaluation.score_csv fixtures/manual_entry_template.csv --set A` | runs; `rows_used: 0` as expected for the empty template (record-log scorer; not for timing) |
| Cached-run statistics in `evaluation/runs/*/m*.json` | Gemma prompt 3 median 2.45 s (set A) / 2.30 s (set B), max 9.2 s, ≈ 29–33 tokens/s; Qwen median 8.71 / 11.04 s, max 17.8 s; 0 JSON failures |

Python used: 3.15.0 on macOS. Python 3.10 (the stated minimum) was not tested.

## Known defects and gaps (in current code)

1. (Fixed 2026-10-20, COR-01) The confirmed final-sheet export now exists; the review log remains an audit trail that cannot be replayed into the sheet.
1b. (Fixed for timing, EVAL-06) `evaluation/score_final.py` scores final-sheet files; `score_csv.py` still mis-scores corrections in record logs and is documented as unfit for timing.
1c. The sheet and chart include pending suggestions; a real quote with invented day/time words is applied provisionally (COR-10, UI-05).
2. Exported text is not protected against spreadsheet formula injection (COR-02).
3. A model JSON failure is not flagged: with model only it looks like "No availability found"; with model + rules only rules-added cancellations appear. A request error stops the run (COR-03).
4. Reload or a successful re-run loses review decisions; failed validation/parsing preserves the existing session (COR-04).
5. Timezone field unused (COR-05). Roster silently truncated at 20 (COR-06).
6. "Scratch Wednesday"-style cancellations are missed silently by Gemma + rules on set B (COR-07; must not be tuned on set B).
7. The availability sheet overflows its panel horizontally (UI-01).
8. No licence file (REL-01). Git exists on main tracking origin/main at 4c1f700, but intended implementation/docs include dirty/untracked files and committed HEAD does not reproduce this working tree. Public access and release reproducibility remain unverified (REL-02).
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

Not measured. The final-sheet export/scorer contract exists; the matched study has not been run. The "effort proxy" (0.37–0.54 of manual actions in the current snapshot) counts clicks and typed fields, leaves out reading, and is not a time measurement. The revised protocol in [MEASUREMENT.md](evaluation/MEASUREMENT.md) needs matched workloads (not set A 50 vs set B 20), balanced order across more than one participant, equivalent final outputs and the final-sheet scorer (in place since 2026-10-20) before any time saving can be claimed.

- `evaluation/run.py` still scores condition intervals as lost only when entirely empty (EVAL-09); the final-sheet scorer no longer does.

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

Follow [TASKS.md](TASKS.md#order-of-work):

1. Final export/scorer and review fixes are done. **Freeze unseen set C (EVAL-01) before further behavior changes**, using an independent fictional-data writer and keeping contents away from implementation agents.
2. Expose extraction failures/prevent unsupported pending suggestions affecting the sheet (COR-03/COR-10), then protect both CSV exports (COR-02).
3. Fix the separate older metric defect EVAL-09 before final C scoring; preserve historical values and label corrected metrics. Then score C once after planned behavior changes (EVAL-07).
4. Obtain coordinator feedback/authorized local pilot and independent reference review where feasible; run the matched timing protocol before claiming time saved.
5. Capture genuine development evidence during necessary work; optional diagnostics/replay/narration must pass integration, free-budget and privacy gates. Finish a truthful write-up with completed category evidence.

Owner actions in parallel: licence, release reproducibility/public access, personal/project eligibility, deadline clarification and conditional domain acquisition/renewal verification. Do not reinitialize Git.

## Documentation alignment and current plan (2026-10-20)

- All docs now point to canonical competition research and integration contracts. Full historical/category research moved from context.md to COMPETITION.md; context retains the agent handoff and strategic summary.
- Direction: Gemma/Python/human review in the local product; Copilot/Actions/Entire and optional R-CLI for genuine development; optional content-free Sentry diagnostics; Render/.tech/ElevenLabs for a fictional demonstration and narration. In-app voice remains deferred.
- Only Gemma is implemented. No application code, API, runtime configuration, service, account, credit claim, tool install, deployment or published artifact was created. Existing uncommitted implementation was preserved.
- Fresh check: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests → **49 passed** (21 ledger, 28 export/scorer). This does not remeasure accuracy, performance or human savings.
- Fresh in-process API contract probes: **14 passed** for reviewed_messages defaults, tolerated Python-falsy JSON values (including an empty object), valid marks and rejected truthy non-lists/non-string entries. No server or inference started.
- Final documentation checks: **16 Markdown files, 261 local links/anchors, 0 failures**; .env.example contains comments only; credential/email pattern scan found no matches. All 14 existing documentation/config files were updated and 3 Markdown references/entrypoints added. Before/after hashes confirm only these 17 allowed files changed. Historical numeric tables were preserved byte-for-byte. Browser checks, cached evaluation writes and inference were not rerun in this pass.
- Official HF26 hub/Week 3 full details were rechecked. The written-rules URL could not be reopened in this last pass; retain the earlier inspected written deadline/API conflict.
- ₹0, local privacy, unseen C, preserved evidence and eligibility versus award strength remain firm. See D-22 and the canonical integration plan.


## Corrections (2026-10-20 review)

Earlier versions of these documents said, wrongly:
- that replaying the CSV export reconstructs the final sheet (it cannot: no `replaces_earlier`);
- that unsupported suggestions are dropped (only when both quote and phrases are missing);
- that the frozen JSONs contain no memory samples (three fresh-call files do), and gave swap traffic as if it were occupied swap;
- that state stays "in browser memory only" (it is also processed transiently by the local server);
- that a prefix such as "Sam" is always ambiguous (it resolves when only one roster name matches);
- that a hosted demo could be "on" the domain (the domain points at hosting; it does not host);
- that no integration is implemented (Gemma is);
- that no Git repository exists (it does, with release work still outstanding);
- that the current export suite has 20 tests (it has 28, including 8 later review-fix tests);
- that there was no problem evidence (one anecdotal public post exists; still no interviews or validation).

RESULTS.md also labelled set A ledger metrics as held-out only and showed effort ratios without naming their snapshot; both are now labelled.


## Standing task-documentation rule (2026-10-20)

- **DOC-01 — done:** the owner requires every completed, attempted or newly identified project task to be recorded in documentation before the agent hands work back.
- Updated AGENTS.md, CLAUDE.md, context.md and TASKS.md with the standing rule and canonical record locations. TASKS records actual status, acceptance criteria and dependencies; PROGRESS records dated outcomes, artifacts, actual verification, blockers and remaining work; relevant detailed docs/context carry material knowledge changes.
- This task only changes those five Markdown files, including this progress entry. It introduces no application behavior or sponsor activation. Newly recorded backlog items are not implementation authorization.
- Verification: reread the affected instructions, checked their local file links/anchors and compared before/after hashes for this change. No application tests or model calls were run for this instruction-only update; the earlier 49-test/API/link results above belong to the prior all-doc audit.


## Next-work review (2026-10-20)

- **DOC-02 — done (planning only).** Rechecked TASKS/context, the fixture file inventory, current UI extraction loop, browser rerun harness and Git status against the owner's four-fix report.
- **Next execution task: EVAL-01.** No set C files are present. An independent writer must prepare at least 20 fictional messages and a handwritten reference, freeze/commit them unscored and keep their contents away from implementation agents. This review did not create, open or score C.
- **Following implementation:** COR-03/COR-10, then COR-02. Add the missing middle-of-run browser regression under COR-03: stub successful/failed/later successful requests and invalid-JSON/hybrid cases; preserve consistent new-session state and successful results, visible failure counts/warnings, explicit review and provisional-export semantics. Preserve COR-11's different old-session behavior on validation/parse failure.
- **Scoring prerequisite clarified:** fix EVAL-09 before the single final C scoring/publication. It affects the older evaluation metric, not the already-fixed final-sheet scorer. Preserve frozen figures and label corrected metric snapshots; no retrospective claim that the historical metric was fixed.
- UI-05 remains separate pending work, useful before coordinator testing/demo. Optional sponsor evidence may accompany necessary work, but core correctness and held-out discipline take priority.
- Verification for this review: read-only source/doc/inventory checks plus local documentation links/anchors and guarded write verification. No application tests/browser runs, model calls, code changes, installs, commits, deployment or publication. The last verified 49-unit-test result belongs to the earlier audit, not a rerun here.

## Claude project-lead handoff (2026-10-20)

- DOC-03 — done: prepared docs/prompts/claude-project-lead.md so Claude can take responsibility for planning, priorities, technical judgment, competition strategy and documentation.
- The prompt requires a focused source/doc/Git audit, evidence-based decisions and a separate writer brief for EVAL-01. It preserves planning as the default, independent C isolation, the current pending work and the INR 0/privacy constraints. Optional tools are not described as implemented or automatically authorized.
- Context links the handoff. Verification: reread the prompt against current TASKS/CLAUDE/context; validated local links/anchors and guarded writes. No application code, fixtures, tests or model calls were changed/run for this documentation task; no Claude session was started and no work was delegated to an external chat.

## Project-lead takeover audit (2026-10-20)

**When / who:** 2026-10-20, about 20:40–21:10 IST, Claude in the project-lead (planning) role. Documentation and planning only: no application code, fixtures, results, caches or model prompt changed; nothing installed, deployed, published or claimed; set C neither created nor opened.

**Checks actually run**

| Check | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` | **49 passed** (Python 3.15.0, macOS) |
| `git status -sb`, `git log`, `git diff --stat` | `main` = `origin/main` = `4c1f700`; 27 files modified (968+/365−) and 9 untracked paths, including `ledger/export.py`, `evaluation/score_final.py`, `tests/test_export.py` and `tests/browser/` |
| GitHub API `repos/bipul724/availability-ledger` | **Public**, default branch `main`, no licence, last pushed 2026-10-20 07:16 UTC |
| `ls fixtures` | No set C files (as expected) |
| `grep duplicate evaluation/run.py` | Extraction skips duplicates; scoring still counts duplicate reference units (→ EVAL-10) |

**Not run:** the browser harness, the server, any model inference or `evaluation.run`, link checking across all docs (only the links added here were checked by hand).

**Discrepancies found**

1. **The public repository does not reproduce the working tree.** COR-01, EVAL-06, COR-11, COR-12 and EVAL-08, their 28 export/scorer tests and the browser harness exist only locally. The repo is public with no licence. → REL-01, then new **REL-06** (P0, owner).
2. **EVAL-01 asked for set C to be committed.** In a public repository shared with implementation agents, that would expose C before scoring. → D-24: C stays outside the repo and only a SHA-256 manifest is committed.
3. **Duplicate units are still counted in extraction scoring**, so correct duplicate handling looks like misses. This was known (context §8) but had no task. → **EVAL-10**, required before EVAL-07.
4. **The silent missed-cancellation weakness** (known defect 6) was handled only by an optional vocabulary task (COR-07), which risks tuning to set B. → D-25: **COR-07a**, a warning, required before EVAL-07; COR-07b deferred.
5. **The optional integration portfolio** (≈15–35 h of estimated effort) did not fit the 4.6 days left alongside unfinished P0 work. → D-23 narrows the Week 3 entry to overall + Gemma, with Actions CI optional.
6. **Documentation volume** (over 2,500 lines across 18 files, most updated each task) is slowing the work. → D-27 limits per-task doc updates until submission.

**Outputs:** [docs/specs/eval-01-setC-brief.md](docs/specs/eval-01-setC-brief.md) (new); [DECISIONS](docs/DECISIONS.md) D-23 to D-27; [TASKS](TASKS.md) order of work and timeline rewritten, new REL-06, COR-07a/b and EVAL-10, EVAL-09 raised to P0, optional integrations deferred, DOC-04 recorded; [context.md](context.md) plan section updated.

**Next:** the owner completes REL-01 → REL-06 → EVAL-01 (brief). The lead then issues the COR-10 + COR-03 implementation assignment.

### Implementation agent blocked on the C prerequisite (2026-10-20, about 21:30 IST)

The agent made no changes. It confirmed that no set C manifest exists in any local or remote commit, and that substantial work is still uncommitted. Lead decision **D-28**: COR-03, COR-02, EVAL-09 and EVAL-10 may proceed now; COR-10 and COR-07a wait for `fixtures/setC.manifest`. The owner commits the working tree first (REL-06) so that new changes stay separable. AGENTS.md (an untracked discovery entry that points to CLAUDE.md) is consistent with CLAUDE.md; no reconciliation is needed.

### D-28 tasks implemented: COR-03, COR-02, EVAL-10, EVAL-09 (2026-10-20 21:00 IST)

**Boundary (D-28):** no change to `ledger/model.py`, `ledger/rules.py`, `ledger/hybrid.py`, `ledger/resolve.py` or claim/ledger logic in `ledger/core.py`. Changed: `ui/app.js`, `ui/style.css`, `ledger/export.py` (`_cell`/`_uncell` only), `evaluation/run.py`, `evaluation/score_final.py`, `tests/test_export.py`, new `tests/test_evaluation.py`, new `tests/browser/harness.mjs`, `extraction_failures.mjs`, `csv_safety.mjs`, `session_rerun.mjs` (moved onto the harness), plus TASKS rows, `docs/API.md` and `docs/specs/final-export.md` (CSV and failure-display contracts). Not committed.

**Checks run:**
- Cache coverage before any re-score: every non-duplicate message cached for both models and prompt 3 (A 49/49, B 19/19; duplicates m12, m13 skipped). Protected `evaluation/runs`, `results/frozen`, `results/tuning` unchanged against git before and after.
- Red then green: COR-03 browser check failed before the change (the run stopped at the first error; 8 of the 11 checks it reached failed, then it stopped at the missing failure state) and passes 14/14 after; COR-02 unit sub-checks 7 failed then pass, browser check 2 of 4 failed then 4/4; EVAL-10/EVAL-09 unit tests 4 of 5 failed then pass (the fifth guards unchanged outcomes).
- `python3 -m unittest discover -s tests`: 56 tests OK (49 earlier + 2 COR-02 + 5 EVAL-09/10). Browser: session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4; earlier scratchpad checks (final export 13/13, keyboard 18/18).
- Cached evaluation of all 10 A/B configurations before and after (0 fresh model calls): field-by-field comparison found **no change** outside the two redefined metrics; every changed split differs exactly by the duplicate message's units (same correct units, same errors minus the duplicate's).

**Metric redefined (EVAL-10), held-out split, before → after** (set A dev splits unchanged; ledger metrics unchanged):

| Configuration | Units right | Errors | Silent | Effort ratio | Duplicate units excluded |
|---|---|---|---|---|---|
| A rules | 19/30 → 19/28 | 11 → 9 | 11 → 9 | 0.50 → 0.46 | 2 (m12) |
| A Gemma only | 20/30 → 20/28 | 11 → 9 | 9 → 7 | 0.54 → 0.51 | 2 |
| A Gemma + rules | 24/30 → 24/28 | 9 → 7 | 5 → 3 | 0.49 → 0.44 | 2 |
| A Qwen only | 24/30 → 24/28 | 8 → 6 | 5 → 3 | 0.44 → 0.39 | 2 |
| A Qwen + rules | 27/30 → 27/28 | 7 → 5 | 2 → 0 | 0.40 → 0.35 | 2 |
| B rules | 16/35 → 16/34 | 19 → 18 | 19 → 18 | 0.50 → 0.48 | 1 (m13) |
| B Gemma only | 30/35 → 30/34 | 5 → 4 | 5 → 4 | 0.39 → 0.37 | 1 |
| B Gemma + rules | 31/35 → 31/34 | 4 → 3 | 4 → 3 | 0.37 → 0.35 | 1 |
| B Qwen only | 32/35 → 32/34 | 3 → 2 | 3 → 2 | 0.38 → 0.36 | 1 |
| B Qwen + rules | 32/35 → 32/34 | 3 → 2 | 2 → 1 | 0.38 → 0.36 | 1 |

All current A held-out and all set B figures remain post-hoc (D-14/D-15/D-16 history); this change is a metric definition, not a behaviour change.

**Metric redefined (EVAL-09), wrong conditions, before → after:** unchanged in all 10 configurations (A: rules 2/7, Gemma 2/7, Gemma + rules 2/7, Qwen 0/7, Qwen + rules 0/7; B: rules 1/2, others 0/2). No current output loses part of a condition interval, so the stricter definition is demonstrated only by the invented tests.

**Not run / limitations:** browser checks need Node 22+ and Chrome and are not part of `unittest`; Firefox/Safari untested. No retry for failed extraction requests. A value that genuinely starts with an apostrophe followed by `=`/`+`/`-`/`@` loses that apostrophe when a final sheet is read back. Per D-27, README.md, docs/ARCHITECTURE.md §11 (says reading stops at the first error), docs/PRD.md FR-18/S9 and context.md were **not** updated and now understate COR-03; record for the next documentation pass. COR-10 and COR-07a still wait for `fixtures/setC.manifest`.

### Lead review of the D-28 tasks (2026-10-20, about 22:15 IST)

Re-checked independently: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` gives **56 passed**. `git diff` shows no change to the five boundary files, `evaluation/runs/`, frozen/tuning results or fixtures. The agent's report for COR-03, COR-02, EVAL-09 and EVAL-10 is accepted. Browser checks were not re-run by the lead. Stale statements fixed in ARCHITECTURE §11, PRD S9/FR-18 and context.md. Still blocked: COR-10 and COR-07a wait for `fixtures/setC.manifest` (not present at 22:15 IST).

### UI-05 and UI-01 implemented (2026-10-20 21:50 IST)

**Boundary (D-28):** display only. Changed `ui/app.js`, `ui/index.html`, `ui/style.css`, `tests/browser/harness.mjs` (viewport and screenshot helpers; the viewport is emulated without mobile mode, which would widen the layout to fit overflowing content) and new `tests/browser/sheet_display.mjs`. No file in `ledger/`, `server.py`, `evaluation/` or `fixtures/` changed (checked by modification time against the previous task's final comparison script). Not committed.

**Data check before building:** `/api/resolve` already gives each sheet segment's claim ids and every claim's review state, and the per-day history gives the claim behind each change, so the pending/accepted split is derivable without an API change. Not available: which slots of a merged segment came from which claim. Adjacent accepted and pending claims with the same status are therefore shown wholly as pending (conservative); a slot-level provenance field in the ledger would be needed for an exact split.

**Checks run:**
- `tests/browser/sheet_display.mjs` before the change: every display check failed, the overflow checks failed at both widths (1400 px: table 586 px in a 394 px box, page 1544 px; 390 px: sheet ended at 619 px, page 632 px). After: 26/26 at both widths, including the chart split summing to the server's counts in every slot, all four chart layers drawn, "Complete" after full review, and no sheet cell overflowing on the invented week and the 18-volunteer demo.
- Screenshots of the chart and sheet panels at 1400 px (dark and light) and 390 px reviewed by eye: the first version split times inside numbers ("10:0/0") and "pending" mid-word although no cell overflowed, so times now wrap only before the dash and labels only between words; checked again after the fix.
- Chart palette validated with the dataviz validator: the existing `--ok`/`--maybe` pair failed (light protan ΔE 5.9; dark lightness band), so the chart uses its own validated tokens; pending is lighter and conditional is hatched, so identity never depends on hue alone.
- `python3 -m unittest discover -s tests`: 56 OK. Browser: session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, sheet_display 26/26. Scratchpad checks: final export 13/13; keyboard 18/18 after changing how it picks a card. It used to pick the first card whose rejection changed the sheet HTML; the sheet now also shows review state (a superseded pending offer, a pending cancellation), so it now requires both sheet and chart to change. The first marker version also flagged pending offers fully replaced by later messages; the marker now flags only pending removals (cancelled, condition declined, replaced).

**Not verified / limitations:** only headless Chrome on macOS; Safari and Firefox untested (CSS container queries need Safari 16+ / Firefox 110+); no screen-reader or contrast audit of the new legends (UI-02); the light-mode pending-conditional chart layer is faint (hatch at 40% opacity) though legended and in the tooltip; the chart's split is recomputed in the browser and could drift if the server's counting rule changes (the browser check compares them).


### Lead review of UI-05 and UI-01; repository synced (2026-10-20, about 22:45 IST)

Re-checked independently: **56** unit tests pass; `git diff` shows no change in `ledger/`, `server.py`, `evaluation/` or `fixtures/`; the light-mode panel screenshot was inspected. Accepted. Noted: merged segments with any pending claim show wholly as pending (UI-06, deferred, errs toward caution), and the pending-conditional chart layer is too faint in light mode (UI-07). Browser checks were not re-run by the lead. **REL-06 done:** local `HEAD` equals `origin/main` at `b8cc15a`. REL-01 (licence) is still open. Set C manifest is still absent, so COR-10 and COR-07a remain blocked. While waiting, the agent is assigned INT-10 (Actions CI) plus UI-07 and a README refresh, none of which touch extraction or the ledger.

### Licence chosen (2026-10-21, about 00:50 IST)

The owner chose **MIT**. The lead added `LICENSE` (copyright holder `bipul724`, the configured git user name; the owner may change it to their legal name) and updated the README licence section and REL-01. The model's own licence (Apache 2.0) is separate. No code changed.

CLAUDE.md, the canonical agent guide, was stale: it described the uncommitted tree at `4c1f700`, 49 tests, committing set C and the full multi-category direction. The lead aligned it with D-23, D-24, D-27 and D-28 and the current 56-test count (re-run 2026-10-21: 56 passed).

### D-29 (2026-10-21, about 01:00 IST)

The owner asked whether the coding agent could write set C. Decision: no, because it would be testing its own changes. A fresh, isolated AI session may write C if the owner cannot, provided the owner rewrites at least 5 messages and checks the answers; C is then labelled accordingly. The brief and EVAL-01 row were updated.

### INT-10, UI-07 and README refresh (2026-10-21 00:55 IST)

**Boundary:** no change to `ledger/`, `server.py`, `evaluation/` or `fixtures/`. Changed: new `.github/workflows/tests.yml`; `ui/app.js`, `ui/style.css` (chart patterns and gridline rule); `tests/browser/sheet_display.mjs` (UI-07 contrast checks); `README.md`; the INT-10 and UI-07 rows. The owner's uncommitted `LICENSE` and README licence line were kept. Not committed.

**INT-10 (in progress):** workflow added as specified (push and pull request to `main`, `ubuntu-latest`, Python 3.12 via `actions/setup-python@v6`, `actions/checkout@v5`, read-only permissions, 10-minute timeout, no secrets, no deploy, no model). Checks: YAML parsed with Ruby's YAML library; `PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest discover -s tests` → 56 OK on Python 3.12.6 locally. Not verified: an actual GitHub run (needs a push). Browser checks deliberately not in CI (reasons in the INT-10 row).

**UI-07 (done), with a pre-existing defect found:** the new check measured the conditional layers' stripe colour and found it was the gridline grey, not amber: the rule `#chart line { stroke: var(--line) }` also matched the pattern's `<line>`. So since the first prototype both conditional layers rendered grey (light: accepted 1.38:1, pending 1.13:1); earlier statements that the hatch was amber, including the UI-05 entry above, described the intended colour, not the rendered one. Fixed as recorded in the UI-07 row; now 3.92:1 (light) and 5.29:1 (dark) for both layers. The colour-blind validator still passes for the unchanged chart tokens. Light and dark screenshots reviewed by eye.

**README:** refreshed to the current state (COR-01/02/03, UI-01/05, final-sheet export, 56 unit tests, four browser checks with their Node 22+/Chrome/`CHROME` requirements), the TASKS work order, and the D-23 Week 3 scope (overall + Gemma, Actions CI; everything else deferred). Removed stale items: uncommitted-tree note, "no warning" for unreadable model replies, open EVAL-09 gap, "49 checks", the pre-D-23 integration plan. Evaluation statements limited to RESULTS.md frozen figures plus the labelled metric redefinitions.

**Checks run:** unit tests 56 OK (Python 3.15 and 3.12); browser checks session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, sheet_display 28/28 (26 before plus 2 UI-07 checks, which failed before the fix); scratchpad final-export 13/13 and keyboard 18/18; doc links 0 problems.

**Owner next step:** push, then confirm the first run as listed in the INT-10 row and the hand-back report; mark INT-10 done with the run link.


D-29 addendum (2026-10-21, ~01:15 IST): the owner will use ChatGPT (free tier) as the isolated set C writer, with a self-contained prompt from the lead; the owner saves the files outside the repo and runs the local consistency check.

### EVAL-01 done: set C frozen (2026-10-21)

Owner report: 24 messages, 12 volunteers, 21 reference claims. Coverage: 4 cancellations, 2 corrections, 6 partial-hours offers, 2 conditional offers (1 settled), 1 duplicate, 1 look-alike pair, 1 third-party message, 1 ambiguous day, 1 outside-week mention, 3 unrelated messages, 1 additional person ambiguity. Written by an isolated ChatGPT session; the owner rewrote m03, m04, m14, m15 and m21 (and aligned the duplicate m05). The owner-run consistency check printed OK and the hashes were verified.

Lead verification, without opening C: commit `688c50d` is on `origin/main`; `fixtures/setC.manifest` lists three SHA-256 hashes (setC_messages.txt, setC_roster.txt, setC_reference.json); no set C content file is tracked. Under D-29, C counts as AI-written plus owner edits, and the write-up must say so. **COR-10 and COR-07a are now unblocked.** EVAL-07 scores C once after them.

### COR-10 and COR-07a implemented; post-hoc A/B re-score (2026-10-21 03:11 IST)

**Previous assignment:** INT-10, UI-07 and the README refresh were reported in the previous hand-back; their rows stand (INT-10 stays in progress until a real GitHub run is observed).

**Changed:** `ledger/core.py` (`CHANGE_WORDS`; `held` flag in `resolve_claim`; held claims excluded and `held`/`unanswered_change` issues in `build_ledger`), `ledger/export.py` (held claims mark no cell), `ui/app.js` (flag and issue labels, issue order), new `tests/test_review_safeguards.py` and `tests/browser/review_safeguards.mjs`, `tests/test_evaluation.py` (its invented message now contains the proposed time words, so COR-10 does not hold it; expected verdicts unchanged), `docs/API.md`, `docs/ARCHITECTURE.md`, `docs/specs/final-export.md`, the two TASKS rows. Not changed: `ledger/model.py`, `ledger/rules.py`, fixtures, frozen/tuning results, cached runs. Set C not opened. Not committed.

**Checks:** unit tests 65 OK on Python 3.15 and 3.12 (56 + 9 new; the two positive tests failed before the change). Browser: session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, sheet_display 28/28, review_safeguards 7/7; scratchpad final export 13/13, keyboard 18/18. Cache coverage verified first (A 49/49, B 19/19 per model); baseline re-score matched HEAD in every scoring field; after re-score 0 fresh calls; protected folders unchanged.

**Every changed number, post-hoc (A/B)** (extraction/unit metrics unchanged everywhere; only ledger metrics moved; A rules, A Gemma only and B rules unchanged):

| Configuration | Missed cancellations | Slot agreement | Chart slots wrong | Chart abs. error | Slots compared |
|---|---|---|---|---|---|
| A Gemma + rules | 0 → 1 /12 | 0.876 → 0.871 | 28 → 30 | 34 → 36 | 646 → 650 |
| A Qwen only | 5 → 7 /12 | 0.926 → 0.880 | 24 → 36 | 24 → 36 | 650 → 666 |
| A Qwen + rules | 0 → 3 /12 | 1.0 → 0.930 | 0 → 22 (max error 0 → 1) | 0 → 22 | 602 → 630 |
| B Gemma only | 3/5 (unchanged) | 0.845 → 0.810 | 18 → 22 | 18 → 22 | 232 (unchanged) |
| B Gemma + rules | 1/5 (unchanged) | 0.925 → 0.887 | 8 → 12 | 8 → 12 | 212 (unchanged) |
| B Qwen only | 1/5 (unchanged) | 0.961 → 0.810 | 4 → 22 | 4 → 22 | 204 → 232 |
| B Qwen + rules | 0 → 1 /5 | 1.0 → 0.810 | 0 → 22 (max error 0 → 1) | 0 → 22 | 196 → 232 |

All movements come from COR-10 holds (the evaluation applies no human review, so every held suggestion stays off the sheet); COR-07a only adds issues and changes no metric.

**COR-10 hold analysis (post-hoc A/B):** held per configuration: A rules 0, A Gemma 2/2 (model/hybrid), A Qwen 5/5, B rules 0, B Gemma 2/2, B Qwen 5/5; **28 holds, all of correct suggestions (holding cost a correct unit), 0 holds of wrong suggestions.** Set A: m32, m44 (dev; Gemma and Qwen), m15, m49 (dev), m16 (held-out; Qwen). Set B (all held-out): m08, m10 (Gemma and Qwen), m02, m03, m17 (Qwen). Cause, judged on set A dev only: the model normalises wording ("Wed" → "Wednesday", "from 2 until 6" → "2-6", "the rest of this week" → "all week") and `phrase_not_in_message` checks exact words, not meaning. In the review workflow these were already excluded from bulk accept (the flag was already a warning); the new cost is that they no longer count on the provisional sheet and chart until accepted. **Lead decision needed:** (a) keep as specified; (b) revert the hold and keep the flag only (D-13 precedent); (c) hold only when the day or time words are unsupported in meaning, e.g. `resolve_day(day_text)` not within the dates the message itself names, or `resolve_time(time_text)` not matching a time the message states. Option (c) is motivated by set A dev evidence; its A/B effect would still be post-hoc, and only set C is independent.

**COR-07a warning analysis (post-hoc A/B), judged against the references:** A Gemma only 4 (m28, m31, m45, m50; all held-out), A Qwen only 4 (m45, m50 held-out; m49 ×2 dev), A Qwen + rules 2 (m49 ×2, dev), A Gemma + rules 0, A rules 0; B Gemma only 2 (m14, m19), B Gemma + rules 1 (m14, the "scratch Wednesday" case), B Qwen 0/0, B rules 0. **Set A 10 warnings, set B 3; all 13 are real misses of reference cancellations; 0 false alarms.** The warnings do not change the sheet, so the missed-cancellation metric is unchanged by them; their value is that a reviewer now sees each of these misses. "scratch"/"skip" also occur in set B, so the set B result is post-hoc; the change list was written before running and was not adjusted afterwards.

**Not verified:** behaviour on set C (EVAL-07, not run, per the assignment); false-alarm rate on real messages; the evaluation scores the provisional sheet with no human acceptance, so held correct suggestions count as misses there but would be applied after review in practice.


### Lead decision on COR-10 / COR-07a (2026-10-21, about 03:15 IST)

Re-checked independently: 65 unit tests pass; no change to `model.py`, `rules.py`, `hybrid.py`, `resolve.py`, fixtures, runs or frozen results. Reviewed the INT-10 workflow (`.github/workflows/tests.yml`: unit tests only, Python 3.12, read-only permissions, no secrets): accepted; a real GitHub run has not been observed yet. README refresh accepted, but it is stale on test count and EVAL-01 status. **D-30:** revert the COR-10 hold (28 held, all correct, 0 wrong, post-hoc), keep the flag and a non-blocking review entry; COR-07a accepted (13 warnings, all real misses, 0 false alarms, post-hoc).

### COR-10 reverted to flag only (D-30); COR-07a kept (2026-10-21 03:17 IST)

**Changed:** `ledger/core.py` (the `held` flag and its exclusion from the ledger removed; a pending `phrase_not_in_message` claim now raises a non-blocking `check_wording` issue; COR-07a code untouched), `ledger/export.py` (back to byte-identical with HEAD), `ui/app.js` (label "Check the wording" replaces the held badge and "Needs review" label), `tests/test_review_safeguards.py` (COR-10 tests rewritten to the D-30 contract), `tests/browser/review_safeguards.mjs`, README, the COR-10/COR-07a rows, and contract text in `docs/API.md`, `docs/ARCHITECTURE.md`, `docs/specs/final-export.md`. `tests/test_evaluation.py` keeps its corrected invented message (its claims' time words now appear in the message; still correct without the hold). Not changed: `ledger/model.py`, `ledger/rules.py`, fixtures, frozen/tuning results, cached runs. Set C not opened; EVAL-07 not run. Not committed.

**Checks:** the rewritten COR-10 main test failed against the hold code and passes after the revert. Unit tests 66 OK on Python 3.15 and 3.12 (56 before COR-10/COR-07a + 10 in `test_review_safeguards.py`). Browser: session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, sheet_display 28/28, review_safeguards 10/10 (flagged suggestion on the provisional sheet as pending, kept badge, "Check the wording" entry, no bulk accept, absent from the final export while pending and present once accepted; the open COR-07a warning does not block a complete file); scratchpad final export 13/13, keyboard 18/18. Cache coverage verified (A 49/49, B 19/19 per model); re-score made 0 fresh calls; **all 1,394 scoring values in the 10 result files are identical to the pre-COR-10 snapshot** (only runtime memory fields differ); COR-07a adds no result fields. Protected folders unchanged.

**Not verified:** set C behaviour (EVAL-07); the `check_wording` item's usefulness to real reviewers, since on A/B it mostly fires on harmless rewording.


### Lead review of the D-30 revert (2026-10-21, about 03:25 IST)

Re-checked: 66 unit tests pass; `ledger/export.py`, model, rules, hybrid, resolve, fixtures, runs and frozen/tuning results are unchanged against HEAD. Accepted. The agent-reported result JSON changes are memory-sample fields only, so the owner restores those files rather than committing noise. Next: owner commits and pushes, checks the first GitHub Actions run, then EVAL-07 after owner confirmation.

### INT-10 verified on GitHub (2026-10-21, about 03:30 IST)

The owner pushed; HEAD = origin/main = `56e38bd`, working tree clean. GitHub Actions 'tests #1' on `56e38bd` (main) passed in 9 s (owner screenshot). This is genuine Actions CI evidence; it is not evidence of Copilot authorship. Next: EVAL-07 once the owner starts Ollama and sends the scoring prompt.

### EVAL-07: set C scored once (2026-10-21 03:38 IST)

**Done (authorized fresh local Gemma calls on set C only; Qwen not run).** Copied the three set C files into `fixtures/` and ran `(cd fixtures && shasum -a 256 -c setC.manifest)`: `setC_messages.txt: OK`, `setC_roster.txt: OK`, `setC_reference.json: OK`. Only code change: set C registered in `evaluation/fixture.py` (`SETS`) and `evaluation/run.py` (`--set` choices). Ran once, in order: `python3 -m evaluation.run --set C --extractor rules`, `… --extractor model --model gemma4:e2b-it-qat` (23 fresh calls, 0 JSON failures, new cache `evaluation/runs/gemma4_e2b_it_qat_prompt3_setC/`), `… --extractor hybrid --model gemma4:e2b-it-qat` (0 fresh calls). All exited 0. Results copied to `evaluation/results/frozen-setC/` and made read-only; SHA-256: `setC_rules.json` 2dd5beeaf19bf4962f98c49422102fef6e3dc1bd54cdbeee6c10a871f6fa4771; `setC_model_gemma4_e2b_it_qat_prompt3.json` 75120c3e781076edf9447ba5faf4118efa8a7dea9333d45306a54c60026c8220; `setC_hybrid_gemma4_e2b_it_qat_prompt3.json` 47e4c01d38c33d3c6641175292fa1ca534dfaf7a8fa1dd5f1f5eb2345a77b0eb. No extraction, ledger, export or scoring logic changed; nothing tuned on C.

**Headline (all fictional, held-out, scored without human review):** units right rules 15/20, Gemma 17/20, Gemma + rules 17/20; silent errors 5 / 2 / 2; missed cancellations on the final sheet 4/8, 4/8, 2/8; slot agreement 0.433, 0.403, 0.527. COR-07a raised 0 warnings (0 false alarms; it could not catch C's failures by design). COR-10 flagged 4 suggestions per Gemma reader, all harmless abbreviation rewording. Full table, error record, speed and memory: [RESULTS.md, Set C](evaluation/RESULTS.md#set-c-independent-scored-once-2026-10-21-code-56e38bd--set-registration).

**Findings recorded, not fixed (per the assignment):** (1) m13 "Sat 21 Nov" resolves to Sat 28 Nov, silently, in all readers (`resolve.py` weekday + explicit date); (2) m19 an untimed "definite now" does not resolve a conditional offer (ledger confirmation rule); (3) m20/m21 corrections read with the right times but not as replacements, which unit scoring cannot see (largest source of slot disagreement); (4) m23 "T. Vekar" becomes an unknown person instead of an ambiguity between two roster names. Any fix is post-hoc with respect to set C.

**Not verified / limits:** one run only (no variance estimate); memory figures were taken with other apps open and include a cold model load; 24 messages and 8 reference cancellations make every rate coarse.


### Lead review of EVAL-07 (2026-10-21, about 03:45 IST)

Re-checked independently:
- `shasum -c setC.manifest` passes for all three files.
- The frozen set C files are read-only.
- Their values match the agent's table: Gemma + rules 17/20 units, slot agreement 0.527, 2/8 missed (both m21); Gemma only 0.403, 4/8 missed; rules 0.433, 4/8 missed.
- 66 tests pass.
- The only code change is the set registration (`evaluation/fixture.py` +1 line, `evaluation/run.py` choices).

Accepted as the **headline independent result**. The lead's reading: the main failures are deterministic reconciliation rules (explicit dates, settling conditions, replacement cues, initial + surname), not the model. **D-31** schedules COR-13 to COR-17 as post-hoc fixes and an optional set D (EVAL-11); the timeline was revised in TASKS.

### D-31 fixes COR-13 to COR-17; post-hoc re-score of A, B and C (2026-10-21 11:13 IST)

**Changed:** `ledger/resolve.py` (COR-13), `ledger/core.py` (COR-14, COR-15 `REPLACE_CUES`), `ledger/names.py` (COR-16), `ledger/rules.py` (COR-17 negation pattern), new `tests/test_d31_fixes.py` (15 tests, invented messages only), the five TASKS rows, a post-hoc subsection in the RESULTS.md set C section (frozen table untouched). Not changed: the prompt and `PROMPT_VERSION`, fixtures, `frozen/`, `frozen-setC/`, `tuning/`, `runs/`. Not committed.

**Checks:** 10 of the 15 new sub-tests failed before the fixes (one or more per fix; the rest are guards that already passed); after: 81 unit tests OK on Python 3.15 and 3.12. Cache coverage verified first (A 49/49, B 19/19 for Gemma and Qwen; C 23/23 for Gemma). Each fix was scored in turn in-process from caches with the model call disabled (0 fresh calls); the official re-score (A/B as before; C rules, Gemma, Gemma + rules) also made 0 fresh calls and matches the final stage; SHA-256 of every file in `frozen/`, `frozen-setC/` and `tuning/` unchanged; fixtures and runs unchanged. Browser checks: see the hand-back.

**What changed, by fix (all post-hoc):** COR-13: set C m13 outside-week and flagged (Gemma readers: units 17 → 18 /20, ambiguities 2/3 → 3/3). COR-14: set C m19 settled (wrong conditions 1/2 → 0/2 for all readers; slot +0.14 to +0.18). COR-15: set C m20/m21 (Gemma and Gemma + rules slot → 1.0; rules 0.582 → 0.765), A Gemma only missed cancellations 7 → 4 /12, A Qwen only 5 → 3 /12. COR-16: set C m23 ambiguous (Gemma readers 18 → 19 /20). COR-17: set C rules m15/m16 (missed cancellations 2 → 0 /8). **One regression:** COR-14 raised B rules chart slots wrong 58 → 64 (B m20 misread by the rules reader is now upgraded from conditional to available; see the COR-14 row). Frozen-to-current tables per set: in the hand-back and, for C, in RESULTS.md.

**Not verified:** generalisation (fixes were designed from set C's failures; no fresh set D, EVAL-11); the m19 unit-level time error, the rules m13 drop and the rules m23 coordinator gap remain.


### DOC-05: pre-compaction documentation pass (2026-10-21, about 11:10–11:30 IST)

Lead session, documentation only.

**Checks run:**
- `git status`, `git log`, `git rev-parse`: HEAD = origin/main = `c5a2e05`.
- Unit tests on a clean `git archive HEAD` copy: **66 passed** on Python 3.15 and 3.12, with per-file counts 21/30/5/10.
- The working tree (coding agent's uncommitted D-31 work) at 11:10: 81 tests, 7 failing in the new `tests/test_d31_fixes.py`. At 11:13: **81 passed**.
- Protected paths (fixtures, frozen, frozen-setC, tuning, runs, `model.py`): unchanged.
- Ollama 0.40.6 answering; only the `gemma4` model is installed (Qwen removed).
- App server not running.
- Repository tree and API routes inspected; `.github/workflows/tests.yml` read.

**Not run:** browser checks, `evaluation.run`, model inference, a fresh GitHub API call.

**Outputs:**
- `docs/archive/context-2026-10-20.md`: the old handoff, kept for history.
- `context.md`: rewritten in sections A–L with evidence labels.
- `TESTING.md`: new.
- README: CI run observed, set C result, work order, link to TESTING.
- AGENTS.md: stale set C line.
- TASKS: REL-02 criteria, COR-13 to COR-17 marked in progress, DOC-05.

The coding agent's D-31 report has not been received or reviewed.

### Lead review of D-31 (COR-13 to COR-17), 2026-10-21 about 12:00 IST

This supersedes the last line of the DOC-05 entry: the coding agent's D-31 report has now been received and reviewed.

**Re-run by the lead:** 81 unit tests pass on Python 3.15.0 and 3.12.6. `git diff` shows no change under `fixtures/`, `evaluation/runs/`, `evaluation/results/frozen/`, `frozen-setC/`, `tuning/` or `ledger/model.py`. The code diff (`resolve.py`, `core.py`, `names.py`, `rules.py`) matches the TASKS rows. RESULTS.md keeps the frozen set C table and labels the new numbers post-hoc.

**Not re-run by the lead:** browser checks, the evaluation re-score (the agent reports 0 fresh calls), per-fix attribution.

**Found:** COR-15's cue words are matched against the whole message. Three invented messages removed an earlier answer that should have stayed, visible only in the day's history. Recorded as **D-32**; follow-up **COR-18** (warning only). The COR-14 regression on set B rules is accepted as documented.

**Outcome:** D-31 accepted for commit.

### COR-18: cue-only replacements are visible (2026-10-21 11:29 IST)

**Changed:** `ledger/core.py` (in the replacement branch of `build_ledger`, a cue-only replacement records the removed segments and raises issue `cue_replacement`; the replacement itself is unchanged), `ui/app.js` (label "Earlier answer replaced — check", listed after possible missed changes), `tests/test_d31_fixes.py` (3 tests), `tests/browser/review_safeguards.mjs` (new final scenario), the COR-18 row. Not changed: message sets, saved runs, frozen results, the prompt. Not committed.

**Checks:** the three D-32 cases failed before the change (no warning; their sheets already matched COR-15) and pass after; a reader-set `replaces_earlier` and "Also free Sat 6-8" raise none. Unit tests 84 OK on Python 3.15 and 3.12 (81 + 3). Browser: session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, sheet_display 28/28, review_safeguards 12/12; scratchpad final export 13/13, keyboard 18/18. Cache coverage verified (A 49/49, B 19/19 for Gemma and Qwen; C 23/23 Gemma); re-score of A/B and C made 0 fresh calls; **all 1,708 scoring values in the 13 result files are identical to HEAD**; the result files differ from HEAD only in run time and memory fields; fixtures, runs, frozen folders and `model.py` unchanged.

**Frequency (informational, not a score):** cue_replacement issues per reader: set A rules 1, Gemma 8, Gemma + rules 1, Qwen 5, Qwen + rules 1; set B 0; set C rules 1, Gemma 2, Gemma + rules 1. On set C they point at m20/m21, the genuine corrections behind COR-15, so the warning also fires on correct replacements; it asks for a check rather than marking an error. Not judged per message on set A.

**Not updated (per the assignment's scope):** the issue-kind lists in `docs/API.md` and `docs/ARCHITECTURE.md` do not yet mention `cue_replacement`.


### Lead review of COR-18, 2026-10-21

**Re-run by the lead:** 84 unit tests pass on Python 3.15.0 and 3.12.6. No diff under `fixtures/`, `evaluation/runs/`, `frozen/`, `frozen-setC/`, `tuning/` or `ledger/model.py`. The `ledger/core.py` change only records the removed time and adds the issue; the replacement logic is unchanged. The 10 changed result files differ only in machine-state fields (swap, free memory, Ollama RSS, `ollama_ps`); no scoring value changed, so they are not committed.

**Set A warnings judged one by one** (cache only, model call disabled; scratch script, not in the repo). There are 16 warnings across the five readers:
- **13 are real changes:**
  - m29 for every reader: a conditional offer made firm by "shift got moved".
  - m32, m37 and m42 for the model-only readers.
  - m38 for both model-only readers (Gemma twice, Qwen once).
- **3 are the D-32 pattern:**
  - m28, Gemma and Qwen: "Change of plans … Tuesday morning still good".
  - m44, Gemma: a repeat of m32's wording.
  - In each, the reader restated the same day's time, so the removal had no effect on the final sheet. Gemma's m28 Tuesday is conditional, but that comes from Gemma's own claim, not from the removal.
- **Result:** no warning marks a removal that damaged a sheet. Set B: 0 warnings. Set C: 1–2 (agent's count, not re-checked).

**Not re-run:** browser checks (agent reports 12/12 for `review_safeguards.mjs`).

**Docs:** `cue_replacement` added to `docs/API.md`, `docs/ARCHITECTURE.md` and the `context.md` repo map.
