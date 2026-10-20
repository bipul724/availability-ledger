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
