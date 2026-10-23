# Progress

**Current record, 2026-10-23 (Asia/Kolkata):** release `d4b2f76` passed the post-push REL-02 check, including fresh clone, all three Actions #18 jobs and live Render replay. The owner verified the two-message Model-only review/export flow (CFG-02). Current status is in [context](context.md) and [TASKS](TASKS.md); the complete documentation audit is [DOC-12](docs/DOCUMENTATION_AUDIT.md).

**Chronology scope:** this is a dated history, not a list of current instructions. The opening inspection/capability/metric/defect sections are the original 2026-10-20 snapshot; later entries explicitly supersede old counts, holds, missing licence/replay/tracing and mistaken SDK-review conclusions. Preserve numerical evidence rather than silently rewriting historical outcomes. New verification is labelled by its actual date/task and distinguished from owner reports or earlier checks.

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

### D-33: four more categories planned (2026-10-21, about 13:00 IST)

Lead planning; no code changed. The owner asked to add Render, Sentry, ElevenLabs and GitHub Copilot.

**Checked:**
- The official routes for these four categories were re-read on the HF26 hub, and the deadline on the event API: the conflict still stands (25 Oct 12:29 IST vs 26 Oct 12:29 IST).

**Recorded:**
- D-33 in DECISIONS.
- TASKS updated: INT-02, INT-03, INT-04 and DEP-02 reactivated with gates; INT-06 superseded; new INT-11.
- Briefs in `docs/prompts/d33-integrations.md`.
- CLAUDE.md and context.md aligned with D-33.

**Not verified:** free-tier terms for Render, Sentry and ElevenLabs (owner to confirm in each dashboard), and whether the owner's Hacktoberfest ElevenLabs offer is still available.

### INT-11: GitHub Actions integrity check and cache-only re-score (2026-10-21, system clock 11:51 IST)

**Changed:**
- `evaluation/run.py`:
  - `--cache-only`: a missing saved model output raises `CacheMissError` naming the message and cache path, and the run exits 1. Ollama is never called, and the macOS-only memory sampler and `ollama_ps` are skipped.
  - `--out DIR`: writes the results file elsewhere and refuses `frozen/`, `frozen-setC/`, `tuning/` and `evaluation/runs/`.
  - `--cache-only` with `--refresh` is rejected.
  - Behaviour without these flags is unchanged.
- New `evaluation/ci_summary.py` (Markdown table plus a comparison with the committed results).
- New `evaluation/protected.sha256`: 17 files, generated from the committed copies, which matched HEAD.
- `.github/workflows/tests.yml`: new `integrity` and `rescore` jobs; the `unit` job is unchanged.
- New `tests/test_cache_only.py` (7 tests).
- The INT-10 and INT-11 rows, and TESTING.md (CI section).

**Not changed:** fixtures, saved runs, the committed and frozen results, and the prompt. Not committed.

**Checks run:**
- **Unit tests:** 91 pass on Python 3.15.0 and 3.12.6 (84 + 7).
- **Model never reached:** with the model call patched to fail, `--cache-only` raised on the missing message for both model and hybrid.
- **Checksums:** `shasum -a 256 -c` passes 17/17.
- **Local CI simulation** in a scratch copy of the working tree (ignored files excluded, as in a checkout):
  - `sha256sum --check --strict` and the folder-list check pass.
  - Both fail as intended on an edited frozen file and on an added tuning file.
  - Removing one saved set B output makes the cache-only hybrid run exit 1 with the message ID and path, writing no results.
  - Nine cache-only runs (A, B, C × rules, Gemma, Gemma + rules) took about 1.8 s on 3.12, with 0 fresh calls. All nine match the committed results on every scoring field, on 3.12 and 3.15.
- **YAML:** parses (Ruby's YAML): three jobs, `contents: read`.

**Generated table (local):**

| Set | Reader | Units right (held-out) | Missed cancellations | Slot agreement | Fresh calls | Matches committed |
|---|---|---|---|---|---|---|
| A | Rules only | 19/28 | 0/12 | 0.787 | 0 | yes |
| A | Gemma 4 E2B only | 20/28 | 4/12 | 0.811 | 0 | yes |
| A | Gemma 4 E2B + rules | 24/28 | 0/12 | 0.876 | 0 | yes |
| B | Rules only | 16/34 | 3/5 | 0.57 | 0 | yes |
| B | Gemma 4 E2B only | 30/34 | 3/5 | 0.845 | 0 | yes |
| B | Gemma 4 E2B + rules | 31/34 | 1/5 | 0.925 | 0 | yes |
| C | Rules only | 17/20 | 0/8 | 1.0 | 0 | yes |
| C | Gemma 4 E2B only | 19/20 | 0/8 | 1.0 | 0 | yes |
| C | Gemma 4 E2B + rules | 19/20 | 0/8 | 1.0 | 0 | yes |

These are the current, post-hoc numbers; the frozen first scores are unchanged.

**Not verified:**
- No run on GitHub yet, so Ubuntu's `sha256sum`, `$RUNNER_TEMP` and `$GITHUB_STEP_SUMMARY` are untested there. Locally `/sbin/sha256sum` on macOS was used.
- The browser checks were not re-run; no UI or server code changed.

**Design note:** `rescore` fails whenever scores differ from the committed `evaluation/results/*.json`. A scoring change must therefore commit its re-scored results in the same push.

**Next:** the owner pushes and sends the lead a screenshot of the green run and its job summary. Then DEP-02 (brief 2), after the lead's review.

### Lead review of INT-11 (2026-10-21)

**Re-run by the lead:**
- 91 unit tests pass on Python 3.15 and 3.12.
- `shasum -a 256 -c evaluation/protected.sha256`: 17/17 OK.
- No diff under `fixtures/`, `evaluation/runs/`, `evaluation/results/` or `ledger/`.
- The CI re-score loop run locally with **`TZ=UTC`** on Python 3.12, as on GitHub's runners: 9/9 files match the committed results, 0 fresh calls, exit 0.
- Code read: `--cache-only` raises before any model call; `--out` refuses the protected folders; normal (non-cache-only) runs are unchanged.

**Decision on the agent's extra gate:** kept. The re-score fails if any score differs from the committed results, so committed results always match the code. Consequence for every future scoring change: re-score locally (cache-only) and commit the result files in the same push. CI checks only the Gemma and rules files, so Qwen result files must be re-scored by hand when scoring changes.

**Not verified:** a run on GitHub itself (owner to push and send a screenshot of the run and its job summary).

### INT-11 verified on GitHub (2026-10-21, about 12:00 IST)

Run "tests #5" on `8c5f975`, checked by the lead through the public GitHub API: conclusion success, 06:27:39–06:27:53 UTC. Unit tests, "Protected evidence unchanged" and "Cache-only re-score" all passed, every step green. The owner will keep screenshots of the run and its job summary for the post.

### DEP-03 / INT-04: demo script and narration written (2026-10-21)

The lead wrote `docs/demo/script.md`: 8 shots, about 2 min 30 s, with narration text for ElevenLabs.

**Checked:** the script's moments were checked in-process against the saved Gemma 4 E2B outputs with Model + rules on set A (0 model calls). They are:
- Maria's Thursday cancellation (m28);
- Kofi's condition settled (m13 → m29), which raises the COR-18 warning;
- "this Saturday" outside the week (m26);
- "next Tuesday" ambiguous (m41);
- a real model error caught by review: m48 files Marta's offer under Maria. Rejecting it turns Maria's Tuesday 09:00–12:00 from conditional back to available.

**Not done:** the recording and narration (owner, Sat 24 Oct). The replay (DEP-02) isn't built yet. A live local run may differ from the saved outputs, so do a dry run first.

### DEP-02 / INT-02: read-only replay built, not deployed (2026-10-21, system clock 12:42 IST)

**Changed:**
- **`server.py`:** demo mode, on only when `LEDGER_DEMO=1`.
  - It binds `0.0.0.0:$PORT`. Without `LEDGER_DEMO`, `PORT` is ignored and the host stays 127.0.0.1.
  - Suggestions for `model`/`hybrid` come from `evaluation/runs/gemma4_e2b_it_qat_prompt3/<id>.json`, with `stats.saved = true`. The rules reader runs as normal.
  - It returns 403 for:
    - pasted text, or a roster that isn't the served one, on `/api/parse`;
    - any message that is not a served set A message, unchanged, on `/api/suggest`, `/api/resolve` and `/api/export`;
    - another roster, week, timezone or `coordinators`;
    - any model other than `gemma4:e2b-it-qat`.
  - `/api/status` answers without contacting Ollama and adds `"demo": true`.
- **UI** (`ui/index.html`, `ui/app.js`, `ui/style.css`):
  - A sticky banner with the exact wording from the brief, linking the repo.
  - The paste box, roster box, file upload, demo button and day-first option are hidden; week and timezone are disabled.
  - Set A loads on arrival, and the progress line says "Replayed N messages … from saved outputs".
- **New files:** `render.yaml` and `tests/test_demo_mode.py` (7 tests).
- **Browser checks:** a new `tests/browser/demo_mode.mjs` (23 checks). `tests/browser/harness.mjs` gains an optional `env` argument for `openApp`, so existing checks are unchanged.
- **`render.yaml`:**
  - Free plan, no region pinned.
  - `buildCommand` is a no-op `echo`, because Render requires one for Python.
  - `PYTHON_VERSION` is 3.12.6, because Render's default is 3.14.8, which isn't tested here.
  - Health check `/api/status`; no secrets.
- **Docs:**
  - README: configuration, online behaviour, status row, and a "Hosted replay (Render)" deploy section with the free-tier facts read from render.com/docs/free.
  - `docs/API.md`: a demo-mode section, the 403 error and the CLI row.
  - The "reads no environment variables" statements corrected in ARCHITECTURE, `.env.example`, context.md and CLAUDE.md.
  - The DEP-02 and INT-02 rows, and TESTING.md.

**Not changed:** `ledger/`, fixtures, saved runs, results and the prompt. Not committed.

**Checks run:**
- **Unit tests:** 98 pass on Python 3.15.0 and 3.12.6, and with `TZ=UTC` on 3.12.
- **`test_demo_mode.py`**, through real HTTP with `model.extract` and `available_models` patched to fail:
  - Each of the 50 messages, for all three readers, gives the same claims as a non-demo run whose model call returns the same saved output.
  - Model-only claims equal `evaluation.run`'s cache-only reader output.
  - The refusals listed above return 403.
  - A subprocess with `LEDGER_DEMO=1 PORT=n` prints `0.0.0.0:n` and serves; without it, `PORT` is not bound.
- **Browser:** `demo_mode.mjs` 23/23 (load, pasted text refused, Model only 62 and Model + rules 67 suggestions, both with no failures, accept/mark/reject, sheet/chart/history/warnings, both exports, no horizontal scroll and a pinned banner at 1400 and 390 px, no console errors).
- **Existing browser checks with demo mode off:** session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, sheet_display 28/28, review_safeguards 12/12.
- **`render.yaml`:** parses (Ruby YAML).
- **Screenshots** (viewport, 1400 and 390 px, top and scrolled) are in the agent's scratchpad, not the repo. `node tests/browser/demo_mode.mjs <dir>` writes them again.

**Not verified:**
- Any Render deploy, its free plan in the owner's dashboard, Python 3.12.6 availability there, and cold-start time. The README facts on sleep, hours and overage billing come from Render's docs page, not from a deploy.
- The demo has no rate limiting. Each request is cheap and stateless, and nothing is stored.

**Next:** the owner deploys (New → Blueprint, check Free and no payment method) and sends the URL; the lead checks it. Gate: Thu 22 Oct 22:00 IST.

### Lead review of DEP-02 (2026-10-21)

**Re-run by the lead:** 98 unit tests pass on Python 3.15 and 3.12. Checksums 17/17. No diff under `fixtures/`, `evaluation/` or `ledger/`.

**Live probe** of `LEDGER_DEMO=1 PORT=18766` on Python 3.12:
- `/api/status` reports demo and never contacts Ollama.
- Requests refused with 403: pasted text; altered message text; another model; a path-like message id; another roster.
- Served set A parses to 50 messages, and a hybrid suggest answers from saved outputs.

**Code read:** every demo request is checked against the served set A data before any work; saved outputs are looked up only by ids that passed that check; the local default is unchanged. Screenshots at 1400 px and 390 px show the banner, repo link and Needs a decision list, matching the demo script's moments.

**Accepted.** Known and acceptable for a fictional replay: no request-size cap or rate limit. Without a card on file, Render suspends rather than bills.

**Not verified:** a Render deploy, Python 3.12.6 availability there, wake-up time.


### DEP-02 owner deployment walkthrough (2026-10-21)

Provided dashboard guidance for the owner: New → Blueprint, connect bipul724/availability-ledger on main using root render.yaml, review one availability-ledger-replay web service on Free, then deploy and verify Live plus the exact public URL. Verified the local Blueprint specifies Python, a no-op build, python3 server.py, LEDGER_DEMO=1, PYTHON_VERSION=3.12.6 and /api/status health check. Its local commit is 96fdfa7; the GitHub branch contents were not checked remotely in this guidance task.

Rechecked official Render Blueprint/free-service docs: https://render.com/docs/infrastructure-as-code and https://render.com/docs/free. Keep the workspace without a payment method; stop on a card requirement. Free compute does not by itself prevent bandwidth/build overage charges when a payment method exists. Initial build duration is variable; require Live and a working replay banner rather than promising 1–3 minutes.

No account was operated, deployment triggered, URL verified, code changed, model called or application test rerun. DEP-02 remains pending its actual dashboard deployment and public verification. The owner can provide the URL or a screenshot of the step/error, excluding sensitive information.

### DEP-02 deployed and checked live (2026-10-21)

The owner deployed the Blueprint to https://availability-ledger-replay.onrender.com on Render's free plan. The lead checked it:
- **API (curl):** home page 200 in 0.34 s (already awake); `/api/status` reports demo mode with `gemma4:e2b-it-qat`; pasted text to `/api/parse` refused with 403; replay banner present.
- **Browser pane:** Suggest records filled all 50 message cards with no errors in about 25 s; suggestions are fetched one message at a time from India.
  - Needs a decision showed the same 10 items as the local cache-only replay.
  - Rejecting m48's suggestion removed its warning and returned Maria's Tuesday 09:00–12:00 to available (pending acceptance), matching demo shot 5.

**Not checked live:** the CSV downloads (covered locally by `demo_mode.mjs`, 23/23) and cold-start wake time.

**Docs:** README scope moved from D-23 to D-33, with the replay URL and an integration status table; demo script count corrected to 10 decision items.

### INT-03: opt-in Sentry tracing implemented; real traces pending (2026-10-21, system clock 18:59 IST)

**Docs used for span names:** Sentry "Set Up" for agent monitoring (docs.sentry.io/product/agents/getting-started/), which points to the Python manual-instrumentation page (docs.sentry.io/platforms/python/agent-tracing/manual-instrumentation). Span names and ops follow that page:
- agent run: op `gen_ai.invoke_agent`, name `invoke_agent availability-reader`;
- model call: op `gen_ai.chat`, name `chat <model>`;
- attributes: `gen_ai.operation.name`, `gen_ai.agent.name`, `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.response.model` and `gen_ai.usage.{input,output,total}_tokens`;
- on failure: `error.type`.

The `gen_ai.input/output.messages` and `gen_ai.system_instructions` attributes are deliberately never set. That page notes that `send_default_pii`/`data_collection` do not filter manually set attributes, so our own allowlist does it.

**Installed (owner-approved):** `python3 -m venv .venv`, then `.venv/bin/pip install -r requirements-tracing.txt`, giving `sentry-sdk==2.72.0` (the newest on PyPI on 2026-10-21), plus its dependencies `certifi` 2026.10.19 and `urllib3` 2.8.0. `.venv/` was already in `.gitignore`. Nothing was installed globally.

**Changed:**
- **New `ledger/tracing.py`:**
  - It is a no-op without `SENTRY_DSN` or without an importable `sentry_sdk`, and then never imports it.
  - Init settings:
    - `traces_sample_rate=1.0`, `send_default_pii=False`, `data_collection` all off;
    - default and auto-enabled integrations off;
    - `max_breadcrumbs=0`, and `before_breadcrumb` drops all;
    - `before_send` drops every error event;
    - no local variables, stack traces or source context;
    - no sessions, client reports or logs; no trace propagation;
    - fixed release, environment and server name.
  - `before_send_transaction` rebuilds each transaction from an allowlist:
    - fields, trace context and sampling context;
    - span keys;
    - span-data keys with value types;
    - strings only as identifiers (`^[A-Za-z0-9_.:/-]{1,100}$`);
    - span and transaction names only of our own forms.

    The SDK (2.64+) sends `gen_ai` spans as separate v2 items, copied from the already-scrubbed transaction, so they are covered (checked in the SDK source).
  - Handles with a no-op `OFF`, and a `Runs` registry: one agent span across a browser run's requests.
- **`server.py`:**
  - `/api/suggest` joins the page's run and wraps the model call (`gen_ai.chat`) and the hybrid merge.
  - `/api/resolve` and `/api/export` add `ledger.resolve`, `ledger.confirmed_export`, `ledger.build_ledger` and `ledger.export` to the open run, or else to a `ledger request` transaction.
  - `tracing.init()` runs only after the demo branch, so the Render replay is never traced. Spans are flushed on shutdown.
  - `ledger/model.py` is not changed.
- **`evaluation/run.py`:** one agent transaction per run, a chat span per fresh model call (cached reads make none), and `ledger.hybrid_merge`, `ledger.score` and `ledger.build_ledger`.
- **`ui/app.js`:** each suggest request carries `run: {id: random, index, total}`, which the server ignores when tracing is off.
- **New files:** `requirements-tracing.txt`, `tests/test_tracing.py`.
- **Docs:**
  - README: a new "Opt-in tracing (Sentry)" section, the configuration and online-behaviour rows, and the status rows.
  - ARCHITECTURE §1, §12 and §13, and the integrations table.
  - API: `run` in `/api/suggest`, and the environment-variable lines.
  - INTEGRATIONS: the Sentry row and §5 status.
  - `.env.example`, context.md and CLAUDE.md: secrets line, telemetry rule, honesty line.
  - TESTING.md: test counts, "Opt-in tracing" and "Record real traces"; this row.

**Not changed:** fixtures, saved runs, results, the prompt, and `ledger/` apart from the new `tracing.py`. Not committed.

**Checks run:**
- **Unit tests:** 105 in all.
  - Plain `python3` 3.15.0, and 3.12.6 (also with `TZ=UTC`): 103 pass, 2 skipped (no SDK).
  - `.venv` (3.15.0, `sentry-sdk` 2.72.0): 105 pass.
- **Leak test:** the real server over HTTP and `evaluation.run`, traced into a capturing test transport with no DSN and no network. With invented name, phone, address, prompt, reply, error and log strings, plus simulated careless instrumentation, none appear in any envelope. Neither do message IDs or the run token.
- **Mutation check:** with the scrubber made a pass-through, the leak test fails (the strings appear). So the test catches a leak, and the call sites alone already send no content.
- **Cache-only re-score** after the instrumentation: 9/9 match the committed results.
- **Browser checks** with tracing off: session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, sheet_display 28/28, review_safeguards 12/12, demo_mode 23/23 (`LEDGER_DEMO=1`, no DSN, unchanged behaviour).
- **Links:** 0 problems.

**Not done or not verified:**
- **No real traces.** The DSN is the owner's, and the agent never saw it. The owner's steps are in TESTING.md "Record real traces".
- No finding yet; it will be whatever the traces show.
- The Sentry free-plan quota and settings were not checked (owner).
- The SDK prints a `DeprecationWarning` for `send_default_pii` (kept because the brief requires it; `data_collection` is its successor and is also set). It is visible only where warnings are shown, such as unittest.
- CI skips the 2 SDK tests because it installs nothing.

**Not updated (outside this task):** the INTEGRATIONS table rows for GitHub Actions and Render still describe the pre-D-33 state.

### Lead review of INT-03 (2026-10-21)

**Historical review; gap conclusion superseded:** the streamed-span bypass/SDK-filtering claim below was explicitly corrected in the later “Correction and acceptance: INT-03 privacy layers” entry. See [Sentry handoff §3](docs/SENTRY_HANDOFF.md#3-source-contract-and-earlier-review-correction) for the current explanation. The original review is retained as history.

**Re-run by the lead:** 105 tests in total, with no protected file changed (checksums 17/17, no diff to fixtures, saved runs, results or `ledger/model.py`).

| Interpreter | Result |
|---|---|
| Python 3.15 and 3.12, no SDK | pass, 2 skipped (they need `sentry-sdk`) |
| `.venv` with `sentry-sdk` 2.72.0 | all 105 pass |

**Independent leak probe** (capturing transport, no DSN): an invented name, phone number, address and prompt/reply markers went through a failing and a succeeding suggest. None of them, and no message ID, appeared in any envelope. Token counts, load time and message position arrive on the `chat` spans.

**Gap found, blocking commit:**
- `sentry-sdk` 2.72 sends `gen_ai.*` spans as separate streamed span items (`stream_gen_ai_spans` is on by default). They never pass through `before_send_transaction`, so `tracing.scrub` doesn't apply to the model-call spans.
- Nothing leaks today: the call sites set only approved keys, and the SDK dropped the unapproved string keys the lead injected. That protection comes from the SDK, not from this code.
- An approved string field still accepts any identifier-like value (a single name passed the check on both paths). Those values are code-controlled (model names, stage names), so this is accepted.
- Fix requested: apply the same allowlist to streamed spans through `before_send_span`, test it with an unapproved key on a `chat` span, and correct the docs wording.

**Also:** `docs/INTEGRATIONS.md` status rows for Copilot, Actions, Render and ElevenLabs brought up to date.

### INT-03 lead-review fix: streamed chat spans under our own allowlist (2026-10-21, system clock 19:12 IST)

**The lead's concern:** `gen_ai.*` spans (our `chat` spans) are sent as separate streamed span items (`stream_gen_ai_spans`, default on). The concern was that our allowlist might not cover them, leaving the protection to SDK behaviour.

**Checked in sentry-sdk 2.72.0** (source and experiments, capturing transport, no DSN):
1. With `stream_gen_ai_spans` on, `Transaction.finish` still puts the `gen_ai` spans in the transaction's span list. `client.capture_event` runs `_prepare_event` (including `before_send_transaction`) and only afterwards splits the `gen_ai` spans into a v2 span item. So `scrub()` did already apply to the chat spans.
   - An unapproved key plus message text on a chat span: absent with scrub on, **present with scrub off**. The SDK does not drop them.
2. `before_send_span` is called 0 times on this path. The SDK warns: "The `before_send_span` parameter only works when `trace_lifecycle` is set to `stream`." It would be dead code here.

**Option chosen:** neither the `before_send_span` hook nor `stream_gen_ai_spans=False`.
- `stream_gen_ai_spans` stays at its default (on) for the Agents view.
- `trace_lifecycle` is pinned to `"static"`.
- A second allowlist runs where it demonstrably sees every streamed item: `clean_envelope()`, in a `CleaningTransport` that wraps the SDK's transport at init. All sends go through `client.transport.capture_envelope`, which is looked up at call time, including the batchers' `_capture_envelope`.
  - It runs `scrub()` on transactions again.
  - It rebuilds each v2 span with the same `_value` rules and `NAME`, replacing a foreign name with `sentry.op`, or dropping the span if it can't be cleaned.
  - It drops every other item type and filters the envelope headers (event_id, sent_at, and the sampling context via `_dsc`).
- `before_send_transaction` now calls `transaction_hook()`, which runs `scrub()`. Being separate, each layer can be switched off in tests on its own.

**Kept on streamed spans:**
- **Fields:** `trace_id` (32 hex), `span_id`, `parent_span_id` (16 hex), `name` (ours, or `sentry.op`), `status` (`ok`/`error`), `is_segment`, `start_timestamp`, `end_timestamp`.
- **Attributes:** allowlisted `gen_ai.*`/`ledger.*`/`error.type` keys with `_value` rules, plus these structural keys with fixed checks:
  - `sentry.op`, `sentry.origin`;
  - `sentry.release` (ours only), `sentry.environment` (`local` only);
  - `sentry.segment.name` (our names), `sentry.segment.id` (16 hex);
  - `sentry.sdk.name`, `sentry.sdk.version`;
  - `process.runtime.name`, `process.runtime.version`.
- **Dropped,** among others: `server.address`, `user.*`, `thread.*`.

**Tests** (`tests/test_tracing.py`, 7 → 13):
- **`NoContentLeaves`** now also sets, on the streamed chat span, an unapproved key through `Handle.set` and through raw `span.set_data`, and message text under an approved key. None appear, and the existing assertions are kept: 3 chat spans with token counts, load time, position, and `error.type` on the failed call.
- **New `EachAllowlistAlone` (6):**
  - no leak with both layers on, with the cleaner alone, and with the hook alone (a canary for the SDK's ordering);
  - with both off, the strings appear, so the SDK itself does not drop them;
  - `clean_envelope()` output tested directly on a crafted envelope;
  - the pinned options (`trace_lifecycle="static"`, no `before_send_span`, `stream_gen_ai_spans` on, cleaning transport installed).

**Checks run:**
- **Unit tests:** 111.
  - Plain `python3` 3.15.0, and 3.12.6 (also with `TZ=UTC`): 103 pass, 8 skipped.
  - `.venv`: 111 pass.
- **Layers switched off, on `NoContentLeaves`:** `clean_envelope` alone off passes; `transaction_hook` alone off passes; both off fails (the fake name appears).
  - A first version shared `scrub()` between both layers, so switching off "the hook" also switched off the cleaner's transaction path, and that run failed. Separating `transaction_hook` fixed the coupling.
- **Cache-only re-score:** 9/9 match the committed results.
- **Protected checksums:** 17/17. **Links:** 0 problems.
- **Browser checks:** not re-run. `server.py`, the UI and the tracing-off path are unchanged since the last run, when all passed.

**Docs:** the module docstring, README (opt-in tracing), ARCHITECTURE §12–13, API, INTEGRATIONS and TESTING now name both layers. The INT-03 row is updated. Not committed.

### Correction and acceptance: INT-03 privacy layers (2026-10-21)

**Correction to the lead's INT-03 review above:** its "gap" was wrong. In `sentry-sdk` 2.72.0 the `gen_ai` spans are still inside the transaction when `before_send_transaction` runs, and are split into streamed items only afterwards. The lead's own probe had shown the `chat` span in the pre-scrub transaction. The unapproved key the lead injected was removed by our scrub, not by the SDK.

**Accepted fix (coding agent):**
- `trace_lifecycle="static"` pinned.
- A second allowlist, `clean_envelope()`, runs in a wrapper around the SDK transport. It re-scrubs transactions, rebuilds streamed spans and drops every other item type.
- `before_send_span` not used: it never runs in this mode.

**Re-checked by the lead:** 111 tests in total, and no protected file changed (checksums 17/17).

| Interpreter | Result |
|---|---|
| Python 3.15 and 3.12, no SDK | pass, 8 skipped (they need `sentry-sdk`) |
| `.venv` | all 111 pass |

Independent toggle probe, with an unapproved string key and raw `set_data` on a `chat` span:

| Hook | Cleaner | Result |
|---|---|---|
| on | on | clean |
| on | off | clean |
| off | on | clean |
| off | off | leaks |

Token counts survive in every case.

**Not verified until the owner's real run:** that the transport wrapper delivers to Sentry with a real DSN, and how the traces appear in Sentry's Agents view.


### INT-03: owner Sentry setup guidance (2026-10-21)

Checked current agent instructions, tracing source, README and TESTING record-real-traces steps. The existing project .venv reports sentry-sdk 2.72.0 via package metadata; nothing was installed. The remaining owner steps are account/project/free-plan verification, private DSN entry in their own terminal, live fictional cold/warm runs and verification of received traces. Startup saying tracing is on proves initialization only, not event delivery.

Begin with Sentry signup and a plain Python project named availability-ledger. No payment method, paid upgrade or pay-as-you-go enrollment; do not promise automatic trial downgrade or Agents dashboard entitlement before checking the actual account. Do not paste DSNs into chat/screenshots. Use the local app for live tracing; the Render replay does not make model calls. Source references checked: docs.sentry.io/platforms/python and sentry.io/pricing returned unsupported Markdown to the web fetcher; official help/search results support the Developer plan and Client Keys (DSN) location, but actual account access/allowances remain unverified.

No DSN was read, local app/server or inference started, account created, event uploaded, application test rerun or application code changed by this guidance task. INT-03 remains in progress until real traces and an honest finding are verified.

### INT-03: owner live traces received; four timeouts and log review (2026-10-21, owner UI 20:19–20:21 IST)

**Evidence:** owner-operated local server printed tracing enabled. Owner screenshots show a fictional-demo run completed in 1,616 s with 4 extraction warnings, Sentry Explore/Traces with 130 spans, and Agents with one availability-reader trace (122 spans), 49 model calls, about 65K tokens and 26.93 min duration. These different counts describe different views, not missing-event proof. Agents is usable during the current trial; post-trial entitlement remains unverified. The onboarding UI stated no card required and a post-trial 5M spans/mo allowance.

**Finding:** owner inspected all four failed chat spans. Positions 37, 38, 39 and 40 have status error / TimeoutError with durations 300.010, 300.047, 300.047 and 300.038 seconds, about 20 minutes combined. The first inspected successful call took 72.086 s (1,416 input, 177 output tokens). Input tab showed no input for that span; this is limited visible evidence, not a complete payload audit. No warm-run improvement or cold-load cause has been established.

**Log review:** read the owner's pasted Ollama terminal log. Ordinary calls near the interruption and after recovery take about 1–3 s. At one runner task, detailed output stops mid-processing; HTTP log lines then appear at roughly five-minute intervals from 19:51 to 20:11 while reporting status 200 and only 2–3 s handler durations. Detailed runner output later resumes and normal calls continue around 20:15. This discrepancy does not explain the client timeouts by itself. Sleep, terminal/output blocking, runner stalls, queuing or response-delivery problems are hypotheses only, not findings. Ask about sleep/lid closure or paused terminal output before choosing a bounded reproduction; do not ask the owner to repeat the entire 27-minute run.

**Privacy follow-up:** owner-pasted attributes contain user.geo fields. Their origin (SDK payload versus ingestion enrichment) is unverified; do not claim the received trace contains only timings/tokens. Audit origin and removal before more traced runs or public privacy claims. Do not retain the personal field values in project docs.

**Limits / next:** initialization and real delivery are now proven by owner evidence; INT-03 remains in progress for privacy, bounded performance diagnosis, quota/retention/export checks and any justified comparison run. Only the provided log and project docs were read; no DSN accessed or retained, no application code changed, no inference, upload, tests or browser checks run by this agent. Frozen evaluation evidence is untouched.

### INT-03: retry after owner-reported memory warning (2026-10-21, owner screenshots 20:54–20:57 IST)

The owner recalled a macOS application-memory warning listing Claude and ChatGPT in red, with Resume/Force Quit choices. This is conversation evidence of memory pressure, not measured RAM/swap or proof of the timeout mechanism. Guided saving/quitting other apps, keeping Terminal services/browser available, restarting Ollama and the local server with private DSN entry, and avoiding another full run until a small check passed. No DSN was read or retained. Tracing activation after this restart was not independently observed.

**Owner-operated checks:** two newly invented simple messages (separate from protected fixtures) completed in 24 s, with two pending suggestions and no extraction warning visible. The subsequent unchanged fictional-demo input completed in **85 s**, compared with **1,616 s** in the earlier interrupted run. Its screenshot has no extraction-failure summary; ordinary ambiguity/review warnings remain, with 49 unreviewed messages and 62 pending suggestions. This establishes successful extraction completion, not correct or accepted final availability.

**Log read:** the supplied retry excerpt has 41 /api/chat records, all HTTP 200, from 20:55:26 to 20:56:31, with handler durations about 0.257–2.541 s. No timeout/error/panic/fatal/cancellation text appears in that excerpt. It begins mid-run, so do not claim it contains all 49 model calls. No agent-run tests, inference, code changes or frozen-result updates occurred; checks are owner screenshots plus read-only log inspection.

**Interpretation / next:** improvement after closing apps is consistent with memory pressure contributing, but services were restarted and the two-message check had already loaded the model before the full retry. This is neither a controlled memory experiment nor a cold/warm benchmark, accuracy score or human-time-saved claim. Confirm the new run in Sentry Agents (duration, errors, calls) before declaring retry delivery verified. Privacy follow-up for received user.geo fields and quota/retention/export checks remain open under INT-03. Docs updated: its TASKS row and this entry.

### INT-03: tracing restored and 86-second demo completed (2026-10-21, owner screenshot 21:11 IST)

The owner's server-startup transcript after the 85 s retry lacked the tracing-enabled line, and the Sentry dashboard still showed only the earlier 26.93 min trace. Treat the 85 s retry as local completion evidence, not a received Sentry trace. Repeated hidden-input attempts did not enable tracing. Guided stopping only the owner's app server and copying the complete DSN privately into their shell via clipboard; copying the shell command itself replaces clipboard content, so the owner recopied the DSN before recalling/executing the export command. No DSN value was retained in docs or used by the agent.

The next owner transcript explicitly printed Sentry tracing on. The owner then reran the fictional demo: the 21:11 screenshot reports **50 messages in 86 s**, no extraction-failure summary, 49 unreviewed messages and 62 pending suggestions; normal ambiguity/review warnings remain. Read the new supplied Ollama log excerpt: 41 /api/chat lines from 21:09:03 to 21:10:07, all HTTP 200, no timeout/error/panic/fatal/cancellation text. The excerpt is partial and does not establish every call's status.

Next: confirm the new trace and its duration/error/call counts in Sentry Agents before declaring delivery verified. No further inference is needed for that check. The privacy/geo and quota/export follow-ups remain open. No application code, prompt, fixtures, saved model outputs or frozen results changed; no automated tests or inference run by the agent. TASKS INT-03 updated; documentation diff whitespace check follows.

### INT-03: successful retry received in Agents (2026-10-21, owner screenshot 21:11:39 IST)

The owner screenshot confirms the new availability-reader trace **969d7ee9** in the same Python project: **1.42 min, 49 LLM calls, 0 errors, about 71K total tokens**. The earlier trace **c26d2afd** remains visible beside it: **26.93 min, 49 calls, 4 errors, about 65K tokens**. Thus both the failed-run finding and a subsequent successful traced run are verified by owner evidence. The latest local UI reported 86 s; the rounded agent-root duration measures a different scope and is consistent with that observation, not an exact equality claim. Token totals differ in a run containing four failures; do not present this as controlled token-cost comparison. The displayed $0 estimate is not a Sentry billing/allowance audit or measured hardware cost.

No more model runs are needed to establish setup/delivery. Remaining workflow evidence: owner accepts/reviews fictional suggestions and exports the final sheet, retaining a provisional label if warnings/messages remain unresolved. Privacy origin/removal of received user.geo fields, post-trial Agents entitlement, retention/exhaustion and export-route checks remain open under INT-03. Closing apps plus restarting services preceded recovery, but memory pressure is still a plausible contributor, not proven causation. This is not a cold/warm benchmark or human-time-saved result.

Updated TASKS, this entry, context summary and INTEGRATIONS status. Screenshot inspection only; no agent-run inference, SDK transmission, code change or automated test. Documentation whitespace check follows. Frozen evidence and model outputs unchanged; no DSN retained.

### INT-03: owner review actions and provisional CSV checked (2026-10-21, after owner screenshot 21:24 IST)

Owner screenshots show 39 warning-free suggestions accepted, leaving 23 pending; Maria's m02 was explicitly marked reviewed. The supplied final-sheet CSV confirms only m02/m03 marked reviewed: **47 messages unreviewed, 23 pending, 0 blocking issues**. The owner downloaded and attached availability-final-2026-11-09-provisional.csv. No completion or accepted-final-accuracy claim is warranted; the ordinary unresolved review warnings remain.

Read the attached fictional export without editing it. Used the project's strict parse_final_csv reader with the existing fictional roster and Calendar for 2026-11-09: **PASS**, **45 rows**, **44 needs_review rows/cells**, **1 confirmed row**. These are output rows including review markers, not 45 accepted availability records. Checked SHA-256 before/after: attached file unchanged. No scorer/reference accuracy comparison, new inference, automated test-suite run or external transmission by the agent. The read-only check used bundled Python and standard-library CSV; the Spreadsheets skill was consulted. Protected fixture and result files unchanged.

Basic setup, actual failed/successful trace delivery and local accepted-only provisional-export workflow have now been exercised. Export-specific span delivery has not been inspected in Sentry. Remaining INT-03 privacy/geo-origin/removal and free-account retention/exhaustion/export-route checks are still open; no additional run is needed for setup confirmation. Next owner cleanup: stop their Python server with Ctrl+C to flush spans, unset SENTRY_DSN in that shell, and stop the Ollama server if finished. Do not describe cleanup as completed until the owner confirms it. TASKS updated; documentation whitespace check follows.

### INT-03: owner cleanup confirmation and geo-setting research (2026-10-21)

Owner confirmed completion after guidance to stop the Python server, unset SENTRY_DSN in its shell, then stop the Ollama server. This is owner-reported cleanup; no process or environment inspection was performed.

Official Sentry Help article, read 2026-10-21: https://www.sentry.help/en/articles/13964201-can-i-disable-ip-geolocation-for-gdpr-compliance (dated 2026-07-29), says Sentry derives geographic context from event-associated IP addresses by default and recommends Project Security & Privacy / Data Scrubbing / Additional Sensitive Fields, one per line: city, subdivision, region, country_code, ip_address; changes may take 5–15 minutes. Official project/organization API docs also describe scrubIPAddresses and sensitiveFields: https://docs.sentry.io/api/projects/update-a-project/ and https://docs.sentry.io/api/organizations/update-an-organization/ . This supports an ingestion-enrichment hypothesis for the observed geo metadata; it does not establish the origin of the specific streamed spans or that these controls scrub every span attribute. No legal/GDPR compliance conclusion is being made.

Next owner step: open Settings and inspect actual project Security & Privacy controls before choosing settings. No account setting changed, no new upload/inference run, no code or protected evaluation data modified. Actual removal on newly received spans remains unverified; prior stored traces must not be assumed retroactively scrubbed. INT-03 stays in progress for privacy and account checks.

### INT-03: project IP-storage prevention enabled in owner UI (2026-10-21, screenshot 22:09:52 IST)

Owner navigated to Settings / Projects / python / Processing / Security & Privacy. Earlier screenshot showed Data Scrubber and Use Default Scrubbers ON, Prevent Storing of IP Addresses OFF. Latest screenshot shows **Prevent Storing of IP Addresses ON** (purple checked toggle and green save check). This verifies visible project configuration; persistence after refresh and effect on newly received streamed spans have not yet been tested. No claim is made that prior traces were changed or all geo fields removed.

Additional Sensitive Fields displays email (may be placeholder rather than a saved entry); Safe Fields displays business-email (also may be placeholder). Do not overwrite actual existing entries based on these placeholders. Next guidance: retain existing sensitive entries, add city, subdivision, region, country_code and ip_address from the official Sentry help article; add subregion as well because that attribute was observed in the owner trace. Confirm saving/persistence before any bounded verification event. No fields added by the agent, no account API call, SDK upload, inference or application-code change. TASKS INT-03 updated; remaining geo-removal verification remains open.

### INT-03: geo fields saved and visible after refresh (2026-10-21, owner screenshot 22:14:43 IST)

Owner entered six newline-separated Additional Sensitive Fields: city, subdivision, region, country_code, subregion, ip_address. After guidance to blur/save and refresh, the next screenshot shows all six entries still present and Prevent Storing of IP Addresses ON; Data Scrubber and Use Default Scrubbers remain ON. This is visible persistence evidence following the requested refresh, not inspection of a backend API or a post-change span. Safe Fields was not intentionally changed; the UI still displays business-email (actual value versus placeholder unverified).

Privacy configuration is now saved. Official help allows 5–15 minutes for propagation. The remaining privacy check is a single bounded fictional-message traced run after propagation, inspecting new chat/transaction attributes for the observed geo/IP fields. Do not repeat the 50-message benchmark for this check or assume earlier traces are retroactively scrubbed. Span scrubbing efficacy remains unverified; keep INT-03 open for it and account/retention/exhaustion checks. Basic setup and successful 49-call trace delivery already passed. No application code, SDK data transfer, inference or automated tests by the agent in this step. TASKS updated; documentation whitespace check follows.


### INT-03: bounded post-setting privacy test completed locally (2026-10-22, owner screenshot 00:06:01 IST)

After the propagation wait, the owner restarted Ollama; the 00:01:53 screenshot shows it listening on local port 11434. Guided private clipboard-based DSN export and starting the existing Python server; the owner answered yes to seeing the tracing-on startup line (owner report, no startup screenshot independently inspected). No DSN read or used by the agent.

The owner submitted one newly invented fictional message with a matching one-person roster and planning week 2026-10-26, using Model + rules cross-check and gemma4:e2b-it-qat. The result screenshot reports **1 message in 17 s**, with one pending suggestion for **Monday 26 Oct, 10:00–12:00, available**, matching the supplied message. No extraction warning is visible; the message remains unreviewed and its suggestion pending. This is a bounded local completion check, not an accuracy benchmark or proof of telemetry privacy.

Next: inspect the newly received Sentry trace and its chat/transaction attributes for geo/IP fields and content absence. Delivery of this specific run and the effect of the saved privacy controls remain unverified. No further model run is needed to inspect it. INT-03 remains in progress for these checks and the existing account/retention/exhaustion/export follow-ups. Only documentation was edited by the agent; no code, prompt, protected fixtures/results, inference, SDK transmission or automated tests were run by the agent. TASKS and context summary updated; git diff --check follows.


**Delivery follow-up (2026-10-22, owner screenshot 00:09:12 IST):** new trace bc88af7a is visible in Sentry Agent Activity, with 3 spans, root duration 16.39 s and 0 displayed Issues. Selected gen_ai.chat span is 16.36 s and shows about 1.3K input tokens plus 82 output tokens (about 1.4K total). Input tab explicitly says No input for this span. This verifies delivery of the bounded run and input absence in that selected UI tab only; Issues is not being relabelled as an error count. Output and Attributes have not yet been inspected, so geo/IP removal remains open. Next owner action: open Attributes on this selected chat span. TASKS/context updated; documentation-only edit, no model run or tests by the agent; git diff --check follows.


**Chat-attribute privacy follow-up (2026-10-22, owner-pasted UI attributes):** the supplied attribute list for chat span 99ded4d22add4a92 in trace bc88af7a shows span.status ok, provider ollama, model gemma4:e2b-it-qat and 1,386 input / 82 output / 1,468 total tokens. user.geo.city, country_code, region and subdivision keys remain present but each value is **[Filtered]**. No ip_address or subregion key appears in the supplied list. The owner pasted the same list twice; this is one span observation, not two checks.

This verifies redaction of the four visible geo values on this newly received selected chat span after the settings change. It does not prove key removal, the specific enrichment origin, whole-event/parent privacy, absence from every stored payload or retroactive changes to older traces. No source message/name/quote or model reply is visible in the supplied attribute list. Input absence was shown previously; Output and parent attributes still need inspection. Next: owner opens Output on the same chat span. TASKS, context and INTEGRATIONS updated; no application code, protected evidence, SDK transmission or model run by the agent. Documentation whitespace check follows.


**Output follow-up (2026-10-22, owner screenshot 00:12:07 IST):** Output tab on the same selected gen_ai.chat span explicitly says No output for this span. Alongside the previously inspected Input and Attributes, this establishes no content displayed in either chat content tab and filtered values for the four visible geo attributes on that span. Parent transaction attributes and wider payload/account checks remain open. Next owner action: select the upper availability-reader row and open its Attributes. Documentation updated only; no further inference, SDK transmission, code changes or automated tests by the agent. git diff --check follows.


**Parent-attribute follow-up (2026-10-22, owner-pasted UI attributes after 00:12 screenshot):** parent gen_ai.invoke_agent span a2aa299db9e14fa3 in the same bounded trace shows is_transaction true, hybrid reader, message_count 1, prompt_version 3 and root duration about 16.39 s. Its city/country_code/region/subdivision values are each **[Filtered]**. No ip_address/subregion key or fictional source text/name/quote/model reply appears in the supplied attribute list. span.status and trace.status are unknown; these are not being interpreted as failure or success. The UI's 97% faster than average compares a mixed history and is not a controlled performance result.

**Outcome:** targeted geo-value filtering verified on the supplied chat and parent attributes; chat Input and Output tabs both display no content. Keys remain present with redacted values. This is not a full raw-payload audit, observation of every span/content tab, proof of enrichment origin, legal compliance or retroactive scrubbing of prior traces. Account entitlement, retention/exhaustion and export-route checks remain open, so INT-03 stays in progress. No new model run is needed for this finding. Next owner cleanup: Ctrl+C in Python server tab, unset SENTRY_DSN, then stop Ollama if finished; cleanup remains pending until owner confirmation. TASKS, context and INTEGRATIONS updated. Documentation-only work by agent, no application code/protected evidence changed, no inference/SDK transmission/tests run by agent; git diff --check follows.


**Cleanup confirmation (2026-10-22, owner conversation after parent-attribute check):** the owner replied done after instructions to stop the Python server with Ctrl+C and unset SENTRY_DSN, then replied done after instructions to stop Ollama with Ctrl+C. Recorded as owner-reported cleanup; no process, environment or clipboard inspection by the agent. The bounded privacy verification workflow is finished: inspected chat and parent geo values are [Filtered], and chat Input/Output tabs show no content. INT-03 overall remains in progress for the documented wider privacy/account/retention/exhaustion/export checks; no further inference needed for this finding. TASKS, context and INTEGRATIONS updated; documentation-only work, no code/protected evidence changes or agent-run tests, inference or external transmission. git diff --check follows.


### INT-03: owner span usage inspected; plan quota still pending (2026-10-22, screenshot 00:23:37 IST)

Owner opened Stats & Usage, selected python and Category Spans, retaining 14D. Screenshot shows **291 Total Spans, 291 Accepted Spans, 0 Filtered Spans, 0 Rate Limited Spans, 0 Invalid Spans**; client-discarded data is hidden and labelled 0. These counters apply to the selected view, not an individual trace or a monthly quota. Filtered Spans is an ingestion outcome count, distinct from the [Filtered] geo attribute values observed in the prior privacy check. Earlier Errors view had all zero counters, which does not contradict model timeouts captured in spans.

No current plan, trial-end date, quota, retention, post-trial Agents entitlement or exhaustion behavior is established by this page; the Upgrade to Business banner is not proof of the exact existing plan. Official Sentry help consulted 2026-10-22: https://www.sentry.help/en/articles/15901850-how-can-i-manage-my-sentry-subscription-billing-and-pay-as-you-go-payg-usage says Subscription Settings shows current plan, quota and reserved volume; https://www.sentry.help/en/articles/13964886-if-i-downgrade-my-reserved-capacity-when-does-it-apply gives navigation Settings / Usage & Billing / Subscription. Next owner step is to inspect that overview only. No upgrade, checkout, plan change, payment or PAYG activation authorized or performed. TASKS updated; documentation-only changes, no tests/inference/SDK transmission/account mutation by the agent. git diff --check follows.


### INT-03: trial subscription confirmed; general retention/exhaustion policy researched (2026-10-22, screenshot 00:25:11 IST)

Owner Subscription Overview shows **Trial plan / Business Plan Trial / 14 Days Left**, **No billing details on file**, **No payment method on file**, usage period Oct 21–Nov 3, 2026, and **Spans 280 / 100M with $0.00 additional spend**. The 100M denominator belongs to this trial and is not proof of the post-trial Developer quota. The difference from 291 accepted spans on the prior project Stats view is not reconciled; do not infer data loss, billing error or total monthly ingestion from either counter alone. A +5K/month Replay credit ending Feb 21, 2027 is visible, but is unrelated to tracing allowance and was not claimed or changed by the agent. No exact trial-end timestamp inferred from a rounded days-left badge.

Official sources read 2026-10-22:
- https://www.sentry.help/en/articles/17619175-how-does-trace-sampling-and-data-retention-affect-visibility-in-sentry-io-and-how-can-i-troubleshoot-related-issues says Developer and Team plans keep spans for 30 days without a sampled tier; Business/Enterprise have full-fidelity spans up to 30 days and a sampled tier thereafter. This documents general policy, not this account's eventual entitlement or actual retention observation.
- https://www.sentry.help/en/articles/13964891-i-ve-exhausted-my-quota-what-now?code=firesideswiftFireside says quota-exhausted new events are not accepted until reset unless additional capacity is enabled, and are dropped rather than queued/recoverable. https://www.sentry.help/en/articles/13965037-can-i-set-up-an-on-demand-pay-as-you-go-budget-for-my-free-developer-plan confirms PAYG is unavailable on Developer. These are policy checks, not an intentional exhaustion test.

Pricing, quotas and Agents documentation pages could not be read by the web tool (unsupported text/markdown); searches did not establish an authoritative current numeric Developer allowance, exact trial-expiry transition or post-trial Agents feature entitlement. Third-party pricing claims were not used. Prior 5M/month evidence remains onboarding UI evidence only. Next: inspect Manage plan options read-only, without selecting/submitting a paid subscription, adding payment or enabling PAYG. No need for more model calls. TASKS, context and INTEGRATIONS updated; documentation-only work, no code/protected evidence/test/inference/SDK transmission or account mutation by the agent. git diff --check follows.


**Manage Subscription follow-up (2026-10-22, owner-pasted page):** the view offers Team $29/month and Business $89/month, shows trial expiry in 13 days, a paid-plan comparison including 5M spans, a proposed PAYG limit of $300/month, Business $89/month in Plan Summary, Due today $0, and Save Changes/Confirm controls with recurring-charge authorization text. This is checkout/draft information, not proof of a submitted change, active PAYG budget or paid subscription. The 5M allowance here belongs to the displayed paid plans, not verified Developer quota. Due today $0 does not establish zero future charges. No payment details were supplied/read, and no agent account action occurred.

Guided owner to use browser Back, leaving the paid checkout without Save Changes/Confirm or payment submission. Do not direct a plan cancellation based on draft values. Exit is not yet owner-confirmed. The earlier overview remains the actual observed account evidence: trial and no payment method on file. Numeric post-trial Developer allowance and Agents entitlement remain unresolved; no further inference needed. TASKS/context updated; documentation-only work, no tests/code/protected evidence/inference/external account mutation. git diff --check follows.


**Checkout-exit follow-up (2026-10-22, owner screenshot 00:32:27 IST):** owner is back on Subscription Overview. It still shows Trial plan / Business Plan Trial / 14 Days Left, no billing details or payment method on file, and Spans 280 / 100M with $0.00 additional spend. This confirms the visible return to trial overview; no checkout submission is evidenced. Rounded trial-day displays differ from the checkout's 13-day text, so do not infer an exact expiry timestamp. Post-trial free allowance and Agents entitlement remain unverified. Next owner navigation: Learn more in the Business Plan Trial card, to inspect the linked trial information read-only. TASKS updated; no tests, inference, code changes or external account mutation by the agent. git diff --check follows.


### INT-03: public Developer free allowance confirmed from owner pricing screenshot (2026-10-22, 00:37:09 IST)

Owner followed the trial-information modal's Learn more and compare plans link and supplied the official Sentry pricing page screenshot (https://sentry.io/pricing/). The Developer card states **Free**, **one user**, and **Error Monitoring and Tracing**. The comparison table independently lists Developer **Tracing 5M spans**, **5K errors**, **5GB logs**, **5GB application metrics**, **50 replays** and **1GB attachments**. This now confirms the public free-tier numeric allowance from an official-page screenshot, overcoming the earlier web tool's content-type limitation. Do not describe the screenshot itself as showing an observed monthly reset or this trial account already migrated.

The trial modal at 00:35 showed current Business Trial, trial feature marketing, Upgrade now / Maybe Later and the compare-plans link; it did not establish free Agents entitlement. Current account evidence remains Trial / no payment method / $0.00 additional span spend. Post-trial availability of the specialized Agents screen, complete raw-payload privacy and export-route span delivery remain unverified; keep INT-03 in progress with these explicit limits. Official retention/exhaustion policy is documented in the preceding entry and has not been tested by waiting/exhausting quota. No further billing navigation or inference is needed for the public quota check. Do not start a second trial, submit checkout, add payment or enable PAYG.

TASKS, context and INTEGRATIONS updated. Documentation-only work; no account mutation, SDK transmission, code/protected evidence changes, model calls or automated tests by the agent. git diff --check follows.


### DOC-06: comprehensive Sentry session handoff and stale-guidance audit (2026-10-22)

Owner explicitly requested documenting all Sentry work/learning with no false data. Added docs/SENTRY_HANDOFF.md as the consolidated entrypoint: evidence labels and account identity; private DSN/clipboard instructions; actual source safeguards and correction of the earlier streamed-span review; every distinct run, four timeout durations and partial-log limitations; memory hypothesis; geo settings, propagation and bounded chat/parent checks; review/provisional CSV findings; usage/trial/paid-checkout/public-free-plan distinctions; cleanup, official sources, attachment provenance, unsupported claims and scoped open checks. Historical PROGRESS entries were retained.

Corrected current Sentry guidance in README, TESTING, CLAUDE, context and ARCHITECTURE; linked the handoff from INTEGRATIONS and TASKS. Removed current claims that no real traces exist and the default instruction to repeat two full cold/warm demos. Shortened the oversized INT-03 row by linking the complete evidence instead of deleting history; INT-03 remains in progress. New DOC-06 tracks this documentation audit. No unrelated project backlog was implemented.

Verification in this pass: source/document reads only so far; application tests, model inference, SDK transmission, billing mutations and new external research were not run. Earlier test/log/CSV/source-research observations remain explicitly historical. No DSN or actual geo values copied into documentation. Verification completed: all 7 local link targets in the new handoff exist; all 7 current entrypoints link to it; 32 evidence-coverage markers are present; fences/whitespace and a no-ingestion-DSN-URL check pass for the new file. Git path inspection shows only 8 tracked Markdown documents plus the new handoff changed; no application or protected-evaluation path is changed. git diff --check passed. These are documentation checks, not fresh application or provider tests. DOC-06 complete; INT-03 remains in progress for its explicit open checks.


### DOC-07: current competing-category evidence audit (2026-10-22)

Owner asked how many categories the project is competing in now. Read D-33/integration/task/research records and checked current model default, Render free deployment config and GitHub Actions unit/integrity/rescore job definitions. Existing deployment/CI/live-trace results are recorded evidence, not re-run in this audit. ElevenLabs has a script but no generated/used narration evidence recorded.

Reopened official Week 3 and HF26 hub HTML on 2026-10-22: https://dev.to/challenges/hacktoberfest-week3-2026-10-19 and https://dev.to/challenges/hf26 . Actions is explicitly a permitted route in Best Use of GitHub Copilot; demo narration is a permitted ElevenLabs route; Sentry requires trace/screenshots and performance/debugging findings in the write-up. Hub says valid submissions receive Overall and qualifying partner consideration, maximum one win per challenge. Event 81 / Slow and Steady is listed Oct 19–25 and Live in the hub. Exact prior deadline conflict remains unresolved; raw API fetch failed and DevRelay gateway tools were unavailable, so no fresh full_details/API timestamp check is claimed. Consulted devrelay-challenges skill, using official web fallback.

**Assessment:** 5 evidence-backed target categories including Overall: Overall, Gemma, Render, GitHub Copilot via Actions, Sentry Agent Tracing. ElevenLabs would be sixth after actual narration used in the demo with verified rights/allowance. This is not organizer-confirmed eligibility or proof of a published entry. Do not count Actions twice, use of Codex/Claude as Copilot/Entire, or domain ownership as the .tech route. Sentry's unresolved checks remain explicit. No numerical win odds inferred. Updated COMPETITION current portfolio/stale status wording, INTEGRATIONS scope header and TASKS DOC-07. No code, model call, account mutation, publication or test run. Documentation link/whitespace check follows.


### UI-08: visual polish of the review page, no behaviour change (2026-10-22)

Owner asked to improve the page's UI and not to change any functionality. Changed `ui/style.css` only; `ui/index.html`, `ui/app.js`, all wording, IDs, classes the script or tests use, the API, ledger and export are untouched. Chart colours, hatch patterns and sheet layout rules are unchanged, so the UI-05/UI-07 contrast and colour-blind validation still applies.

- **Bug fixed (display only):** before a run the empty review workspace was visible because `main { display: grid }` overrode the `hidden` attribute that `app.js` sets. A `[hidden] { display: none !important }` rule restores what the script intends; `tests/browser/demo_mode.mjs` already asserts `workspace.hidden` after a refused paste.
- **Layout:** above 900 px the summary (Needs a decision, chart, sheet, changes, export) stays visible beside the messages while scrolling, with its own scroll. The summary column grew from 420 to 432 px to give back the scrollbar width; without that, `sheet_display.mjs` failed (demo, 1400 px: 14 cells overflowing at 383 px sheet width).
- **Review controls:** Accept is green, Reject red and Reset a quiet text button; the decided state fills its button; "✓ Reviewed" is green; accepted cards are lightly tinted; checked day chips are highlighted; the add-record button is dashed; warning badges have a border.
- **Theming and focus:** `color-scheme` set per theme so native time pickers, checkboxes and scrollbars follow dark mode; dark-mode primary button text is dark (white on `#8aa8ff` was low contrast); a visible `:focus-visible` ring.

Checks run (2026-10-22): `node tests/browser/{sheet_display,demo_mode,review_safeguards,session_rerun,extraction_failures,csv_safety}.mjs`: 28/28, 23/23, 12/12, 10/10, 14/14, 4/4; `python3 -m unittest discover -s tests`: OK (8 skipped). The original stylesheet was also run through `sheet_display.mjs` for comparison (demo 1400 px: 394 px sheet, 0 overflowing). Light and dark screenshots at 1400 and 390 px inspected (kept outside the repo). Not run: no UI-02 accessibility audit (screen reader, full contrast survey); no Firefox/Safari check. Minor: at 1400 px a card's seven day chips can wrap to two rows.

**UI-08 second pass (2026-10-22):** owner asked to make the UI look attractive without changing any functionality. Again `ui/style.css` only (`git diff` shows no change to `ui/index.html` or `ui/app.js`); `--panel` and the chart tokens are unchanged, so the UI-07 contrast check is measured against the same panel colours. Added: a header band with a gradient brand mark (decorative `content` with empty alt text), a gradient top edge on the setup panel, custom-drawn checkboxes and select arrows (still native `<input>`/`<select>`, so keyboard and form behaviour are unchanged), chat-style message bubbles with an underline on highlighted quotes, a filled green Accept when accepted, warning badges with a dot, issue items as tinted callouts ("Nothing open." shown in green), the changes list as a timeline, coloured dots on summary headings and `prefers-reduced-motion` support. Card spacing was measured in the browser so all fields and all seven day chips stay on one row at 1400 px (fields 475 px and chips 488 px of 491 px). Checks run: the same six browser checks 28/28, 23/23, 12/12, 10/10, 14/14, 4/4; unit tests OK (8 skipped); light/dark screenshots at 1400 and 390 px inspected. Not run: UI-02 audit, Firefox/Safari. `:has()` (summary dots, checked chips, "Nothing open." colour) needs Firefox 121+; older browsers simply skip those touches.


### UI-09: landing page at `/`, review app at `/app` (2026-10-22)

Owner asked for an attractive landing page for the website, with only correct data, no purple or AI-looking gradients, and no commits (the owner commits). Decision [D-34](docs/DECISIONS.md#d-34-landing-page-at--review-app-at-app-ui-09).

- **Added:** `ui/home.html`, `ui/home.css`, `ui/home.js`. A ledger-paper design: warm paper, ink, a red double margin rule down the page with section numbers in the margin, ledger green for available, amber with hatching for conditional, red strike-through for cancellations, highlighter yellow for quotes; serif headings (Iowan Old Style, then Charter, Palatino, Georgia), system sans and mono. Light and dark themes. No web fonts, CDN, images or libraries (D-11).
- **Sections:** hero with an animated, step-through ledger card; the problem with six annotated demo-week messages; how it works (model copies, Python decides, you approve) with the saved Gemma JSON for m03; review (keyboard, four Needs-a-decision items, final-sheet CSV); evidence (frozen A/B/C tables, silent errors as one dot each, set C's 0.527, time saved not measured); privacy and the built-with list (Gemma, Render, Actions, Sentry; ElevenLabs omitted as planned); run it; fine print.
- **Where the data comes from:** frozen tables, speed and memory from `evaluation/RESULTS.md`; product facts, limits and hosting from README and PRD; Sentry facts from `docs/SENTRY_HANDOFF.md`. The hero, the six cases, the Needs-a-decision texts and both CSV exhibits were produced by replaying set A through `server.py`'s demo path (`suggest`/`resolve`/`export` with `DEMO` on and the model call patched to fail): 50 messages, 67 suggestions, 10 issues (matching the demo script); m28's Thursday cancellation was added by the rules reader ("Added by the rules: possible cancellation the model missed"); the four hero messages alone give Maria Tue 09:00–12:00 and Fri 14:00–17:00 with Thursday unavailable, and Kofi Thu 13:00–17:00 conditional, then available; accepting them and marking them reviewed exports a complete sheet with three confirmed rows. The scripts were kept in the session scratchpad, not the repo. Set C files were not opened.
- **Routes (`server.py`):** `/` → `ui/home.html`, `/app` → `ui/index.html` (`/index.html` unchanged); a query string no longer makes the root a 404; the local startup line prints the `/app` address. API, README, ARCHITECTURE, TESTING, CLAUDE command hint, context, INTEGRATIONS (landing page is an entry point, not a substitute for the replay) and the demo script updated.
- **App:** `ui/index.html` title now links to `/`, and the app uses the landing page's ledger logo (replacing the blue-green gradient ✓ mark) and the same SVG favicon (was none); `ui/style.css` styles both. Nothing else in the app changed. After that change: `demo_mode` 23/23, `sheet_display` 28/28, `landing` 15/15, unit tests OK; app header checked in light and dark.
- **Spacing (owner feedback):** the margin column narrowed from 88 to 60 px and the gap after the red rule from 56 to 40 px (52/32 below 1180 px); the sticky header is now opaque, so page text no longer shows through it.
- **Tests:** `tests/test_pages.py` (4 tests: landing page at `/` and with a query string, app at `/app` and `/index.html`, other paths unchanged, no external loads). `tests/browser/landing.mjs` (15 checks with `LEDGER_DEMO=1`, including following the button to the replay, and local labels via a simulated status). `tests/browser/harness.mjs` opens `/app` by default and takes an optional page.

Checks run (2026-10-22, macOS, Chrome headless, Node 22.11): `python3 -m unittest discover -s tests` 115 tests OK (8 skipped without `sentry-sdk`, Python 3.15); browser checks `landing` 15/15, `sheet_display` 28/28, `demo_mode` 23/23, `review_safeguards` 12/12, `session_rerun` 10/10, `extraction_failures` 14/14, `csv_safety` 4/4. Screenshots inspected at 1440, 1100, 960 and 390 px in light mode and 1440 px in dark mode (kept outside the repo): no horizontal page scroll; the first pass found a review-panel overflow at 1440 px, split log lines, wrapped sheet times and a styled terminal, all fixed. WCAG contrast of every text colour pair computed at 4.5:1 or more in both themes; the chart colours (green/amber) are the UI-05 pair, validated again on the new surfaces (protan ΔE 6.2 light / 6.6 dark, so conditional keeps its hatching and labels); red is used only with a strike-through or a label.

Not run: Firefox and Safari; a screen-reader pass (UI-02 still open); the deployed site (unchanged until the owner pushes). Not done: a social preview image. Next: the owner reviews and commits; after deploy, check `/` and `/app` on Render and use `/app` in the demo recording and post (DEP-03, REL-05).


### DOC-08: hackathon-aligned app-name brainstorm (2026-10-22)

Owner requested an eye-catching, distinctive name aligned with the app philosophy and Slow and Steady hackathon theme. Brainstormed availability/chat/evidence names with one naming subagent, then checked exact-name web queries for Availazy, SlothSignal, SlothSlot, SlothScribe and QuoteSloth. Recommendation: **Availazy** (availability + lazy), proposed tagline **Let AI read. You decide.** It connects less coordinator busywork with retaining human review; no measured time-saving claim is implied. QuoteSloth was another evidence-themed idea; no name was selected by the owner.

Collision observations: SlothScribe already names another Week 3 submission, https://dev.to/ankit_sharma_f0b6003cb4b1/slothscribe-59nj . SlothSignal appears as a feature in the publisher's SlothMograph listing, https://superhivemarket.com/products/slothmograph . Do not recommend either as unique. No obvious Availazy app match surfaced in this limited search; that is not proof of name/domain/trademark availability. Search results are a naming screen, not a legal clearance or a challenge eligibility check.

TASKS DOC-08 records proposal status. Availability Ledger remains the actual app/repository name; no source, branding, public listing, domain, account, deployment or submission renamed. No tests/inference or frozen-evidence changes. Documentation whitespace check follows.

### UI-10: user guide at `/docs` with diagrams, styled 404 page (2026-10-22)

Owner asked for a docs page that uses diagrams rather than more text. Added `ui/docs.html` and `ui/docs.css` (extends `home.css`, same ledger design, contents column with the section in view marked) and `ui/404.html`. Diagrams are HTML/CSS, so they reflow on phones and follow the theme: architecture (browser, server.py routes, the eight ledger modules, Ollama, opt-in Sentry), the seven-step run, a 09:00–20:00 ruler for time phrases, a day-resolution table, review states, export gates, final sheet vs review log. Facts come from README, `docs/API.md`, `ledger/resolve.py` (periods, day 09:00–20:00, 1–7 read as pm) and `tests/test_ledger.py` (every ruler/day example is a unit-test case except "until 2", which follows the `until` rule in `resolve_time`); badge texts are `FLAG_TEXT` in `ui/app.js`. Developer docs are linked on GitHub, not copied. `server.py`: `/docs` route; unknown GET paths return the 404 page as HTML instead of plain `not found`. Landing page: Guide in the nav and footer; footer links open in a new tab.

Checks run: `python3 -m unittest discover -s tests` 116 OK (8 skipped; `test_pages.py` now also covers `/docs`, the 404 page and no external loads in all three pages); `landing.mjs` 18/18; `sheet_display` 28/28, `demo_mode` 23/23, `review_safeguards` 12/12, `session_rerun` 10/10, `extraction_failures` 14/14, `csv_safety` 4/4; screenshots of the guide at 1440 and 390 px light and 1440 px dark, and the 404 page. Not run: Firefox/Safari, screen reader.


### BRAND-01: owner selected Availazy; coding-agent rebranding brief prepared (2026-10-22)

Owner selected **Availazy — Local AI for Coordinators Who Have Better Things to Do** and asked for a prompt for the coding agent. Created docs/prompts/availazy-branding.md, recording exact name/headline, current landing/app/guide/404 surfaces, minimal design scope, behavior/privacy/replay constraints, present-tense documentation, and appropriate existing verification. An independent naming-prompt review subagent identified the same identifier/provenance/layout boundaries; it did not edit files.

Read-only inspection found existing uncommitted UI-09/UI-10 work and current routes `/`, `/app`, `/docs`, styled 404; the brief requires preserving that work. It explicitly preserves repository and Render identities, Sentry org/project/agent/release, API/CSV/DOM/internal interfaces, fixtures/prompt/frozen evidence and historical records. No new logo, installs, model runs, traces, external changes or commits/deployment authorized by this handoff. Updated TASKS DOC-08 selection status, added BRAND-01 todo and a current context identity note. Implementation is not claimed complete: actual pages still read Availability Ledger. No application tests/browser/model runs in this prompt-writing pass; documentation links/fences and git diff --check follow.

### BRAND-01: public name Availazy applied locally (2026-10-22)

Implemented the owner-selected identity from [docs/prompts/availazy-branding.md](docs/prompts/availazy-branding.md): **Availazy — Local AI for Coordinators Who Have Better Things to Do**. Formerly Availability Ledger; earlier entries in this file keep the old name.

- **Pages:** wordmark, ARIA labels and titles say Availazy on `/` (title `Availazy — Local AI for Coordinators Who Have Better Things to Do`, also Open Graph), `/app` (title and header `Availazy`), `/docs` (`Guide · Availazy`, heading "How Availazy works") and the 404 page (`Not found · Availazy`). Landing hero: the exact headline is the H1, with "Let AI read. You decide." below it and Availazy in the line above; the H1 size went from up to 86 px to up to 64 px (`ui/home.css`) so the longer headline wraps in four lines on desktop and five on a 390 px phone. The replay preview card shows the app's new title. No other design, link, route or behaviour change; replay banner, warnings, provisional states and exports unchanged.
- **Elsewhere:** `server.py` startup lines; README title and intro (headline plus a former-name note); the first comment in `.env.example`; demo script narration ("a sheet you can check" instead of "a sheet you can trust", "your messages never leave your machine"); CLAUDE, context, PRD and ARCHITECTURE opening lines.
- **Kept on purpose (searched with `grep -rn "Availability Ledger"` and `availability-ledger`):** GitHub repo and clone URL, checkout folder, Render service and hostname, Sentry organization/release identifiers, `ledger/` modules (including the `ledger/__init__.py` docstring, an internal name), CSV names and headers, fixtures and frozen evidence, and every historical PROGRESS/DECISIONS/COMPETITION/SENTRY_HANDOFF/archive record. Remaining "Availability Ledger" in current docs is either one of these or a deliberate "formerly" note.
- **Tests:** only presentation expectations changed: `tests/test_demo_mode.py` checks the root page for "Availazy"; `tests/browser/landing.mjs` checks the new landing and 404 titles and the headline text.

Checks run: `python3 -m unittest discover -s tests` 116 OK (8 skipped without `sentry-sdk`); browser checks `landing` 18/18, `demo_mode` 23/23, `sheet_display` 28/28, `review_safeguards` 12/12, `session_rerun` 10/10, `extraction_failures` 14/14, `csv_safety` 4/4; `shasum -a 256 -c evaluation/protected.sha256` all OK and no diff under `fixtures/`, `evaluation/` or `ledger/`; screenshots of `/` at 1440 and 390 px in light and dark, the `/app` header in light and dark, `/docs` at 1440 and 390 px dark and the 404 page: no horizontal page scroll, headline readable, buttons visible. Not done: deployment (owner), Firefox/Safari.


### BRAND-01: independent review of coding-agent report (2026-10-22)

Read current instructions/context, source/diffs, branding across all four pages, startup strings, metadata, README and script; one independent read-only review subagent checked the same scope. No confirmed branding regression or weakened tracked behavioral assertion found. The existing test_demo_mode.py diff changes only the expected display name. Kept identifiers match the brief. This is a review of local files, not deployment or original screenshot reproduction.

**Fresh verification:** first offline unit attempt in the restricted sandbox ran 107 tests, 8 skipped, with 7 errors: socket bind PermissionErrors prevented demo/page setup and left subsequent replay-state errors; this was not counted as an application pass or silently omitted. Retried with local test-server sockets allowed and SENTRY_DSN/LEDGER_DEMO removed from the child environment: **116 tests run, OK, 8 skipped**, Python 3.12. A ResourceWarning about an unclosed test subprocess output stream was visible; suite exit 0. `shasum -a 256 -c evaluation/protected.sha256`: all 17 entries OK. No tracked diff in fixtures/, evaluation/, ledger/ or render.yaml; git diff --check clean before this doc update. No model inference, SDK transfer, external lookup/account action, commit/push/deploy or owner-server restart. The coding agent's seven browser-suite results and screenshots were not re-run or independently re-viewed by this review.

**Current pre-existing UI findings, not attributed to the rename:** (UI-11) landing privacy heading says Nothing leaves your laptop despite its explicit outbound Sentry node; the illustrated/app replay banner has similar blanket wording. Qualify to messages/core workflow while preserving opt-in disclosure. (UI-12) ui/home.js REPLAY_URL and the local-mode browser expectation use the hosted root, now the landing page, instead of the replay at /app. Source establishes the wrong direct target; this was not tested against the live deployment. Added separate scoped follow-up rows; no UI/code fix applied in this review.

**Documentation correction:** README's new formerly note incorrectly called the Sentry project availability-ledger. Corrected to organization availability-ledger / actual project python, preserving account identifiers. BRAND-01 remains implemented locally; live branding was not fetched in this pass, and the owner report says it is not deployed. The accumulated working tree includes earlier UI-09/UI-10 work, so do not attribute all HEAD differences to BRAND-01. TASKS and PROGRESS updated; whitespace recheck follows.


### UI-13: Forest & Parchment colour theme, colour only (2026-10-22)

Owner request: implement the approved Forest & Parchment palette across the landing page, review app, guide and 404 without changing the Availazy name, copy, typography, layout, spacing, responsiveness or behaviour; the reference screenshots (pre-rebrand) were used for colour only. Decision recorded as [D-35](docs/DECISIONS.md#d-35-forest--parchment-colour-palette-ui-13). Existing uncommitted BRAND-01/UI-09/UI-10 work was preserved and built on.

**Files changed:** `ui/home.css` (shared by the landing page, guide and 404: palette tokens; new `--brand`/`--on-brand` and `--glyph-*` tokens; forest-green hero heading, links, focus, primary and outline buttons, active nav/step controls and skip link; soft wash on the demo header; sage margins and pull-quote rule; brand-green decorative numbering; amber wash for the replicas of the app's banner; sage highlighter), `ui/docs.css` (contents counters and active item, steps markers, active pipeline step, warning badge replica, secondary ink on green-wash labels), `ui/style.css` (palette tokens with `--accent` as the action colour separate from `--text`; status text vs border/accent tokens `--ok`/`--ok-accent`, `--maybe`/`--maybe-accent`; `--warn-bg` folded into `--maybe-bg`; `--control` border for form controls; solid header and primary buttons instead of gradients; white message bubbles; sage quote marks; themed glyph; checkbox-tick and select-arrow SVGs recoloured per theme; file input focus ring), and the favicon in `ui/index.html`, `home.html`, `docs.html`, `404.html` (forest square, sage margin, parchment rules) with theme-colour metadata updated (added to `/app`, which had none). No change to HTML structure, copy, JS, server, API, exports, fixtures or evaluation.

**Kept on purpose:** chart hatching, pending dashed outlines, cancellation strikethroughs, animations, and the guide's time-ruler fades (they show open-ended ranges). Semantic red stays on cancellations (`CANCELLED`, struck segments, 404 strikethrough), rejects, silent-error dots and "not exported" labels. The dark chart pair is unchanged.

**Checks run (2026-10-22, fictional set A, Rules only or saved replay outputs; no model inference):** `node tests/browser/{sheet_display,demo_mode,review_safeguards,session_rerun,extraction_failures,csv_safety,landing}.mjs`: 28/28, 23/23, 12/12, 10/10, 14/14, 4/4, 18/18 (UI-07 hatch contrast 4.07:1 light, 5.33:1 dark); `python3 -m unittest discover -s tests`: 116 OK, 8 skipped. A scratch audit script (outside the repo) loaded `/`, `/docs`, a missing path (404) and a populated `/app` (accepted, rejected and reviewed states) at 1440 and 390 px in light and dark: every visible text element (about 10 to 1,520 per page) met 4.5:1, or 3:1 for large text, against its composited background colour; no horizontal overflow; no console errors; keyboard focus visible at every tab stop checked (10 on the landing page, 14 in the app; the date field's built-in picker button draws Chrome's own ring). The first audit pass found five items, all fixed: kicker separator dots in sage (2.4:1), the demo week line and three guide labels in muted text on a wash (4.50:1), and no focus ring on the file input (a UI-08 regression). Screenshots of all four pages in both themes and widths were inspected, including a zoom of the ledger mark in both themes.

**Limits:** the audit uses background colours, not gradients or images (the hero highlighter band and hatched cells were checked visually); text inside rejected/duplicate items is intentionally faded and not counted; Firefox and Safari not checked; not a UI-02 audit (no screen reader pass). The live Render site changes only after the owner commits, pushes and Render redeploys.


### UI-14: light Forest & Parchment on every page, whatever the OS/browser theme (2026-10-22)

Owner request: make the approved light appearance the default on all four pages regardless of the dark-mode preference, disable the automatic dark overrides, align theme-colour metadata, keep the light palette, branding, layout and behaviour, and add no theme switcher ([D-36](docs/DECISIONS.md#d-36-light-appearance-only-ui-14)).

**Changed:** removed the `@media (prefers-color-scheme: dark)` palette blocks from `ui/home.css` (shared by the landing page, guide and 404) and `ui/style.css` (review app); `color-scheme: light` kept with a comment; "same in both themes" comments corrected; in `ui/index.html`, `home.html`, `docs.html` and `404.html` the light/dark `theme-color` pair became one `<meta name="theme-color" content="#f4f2e8">`. No other selector, value, markup, script or test changed. ARCHITECTURE, TASKS (UI-14 row; UI-02's criterion now says light only), DECISIONS (D-36; D-35's dark sentence marked superseded) and context updated.

**Checks run (2026-10-22, fictional set A, Rules only, no model inference):** a scratch script (outside the repo) loaded `/`, `/docs`, a missing path and a populated `/app` (accepted, rejected and reviewed states) at 1440 and 390 px, once with Chrome emulating a light preference and once a dark one (`matchMedia('(prefers-color-scheme: dark)')` true). All eight dark-preference renders showed body `#F4F2E8`, ink `#1B2B23`, computed `color-scheme: light` and a single theme-colour `#f4f2e8`. Seven were pixel-identical to the light render; the 1440 px app differed by one antialiased pixel at a box edge, and a fresh-session recheck of that view gave 0 differing pixels for light vs light again and for light vs dark preference. `node tests/browser/{sheet_display,demo_mode,review_safeguards,session_rerun,extraction_failures,csv_safety,landing}.mjs`: 28/28, 23/23, 12/12, 10/10, 14/14, 4/4, 18/18 (`sheet_display`'s run labelled "dark" now emulates a dark preference and measures the light hatch contrast, 4.07:1); `python3 -m unittest discover -s tests`: 116 OK, 8 skipped; no console errors. The UI-13 light contrast audit still applies, since no light value changed; it was not re-run. Not checked: Firefox and Safari.


### UI-15: persistent navbar divider (2026-10-22)

Owner requested a line separating the navbar and hero. Changed only the two header-border declarations in `ui/home.css`: `.top` now has a 1px solid `--rule-2` (#B9C9B2) bottom border from initial load, and `.top.is-stuck` keeps the same colour after scrolling. The existing transparent border already reserved the space, so header geometry is unchanged. The shared navbar on the guide and 404 inherits the divider. No JavaScript, application logic, model, API, export, fixture or evaluation changes; previous uncommitted work preserved. TASKS and context updated.

**Verification:** installed Google Chrome driven with the existing bundled Playwright, temporary local server with Sentry disabled and Python bytecode writes disabled. At 1440 and 390 px, with a dark OS preference emulated, the landing page, guide and 404 passed 12 checks (page top and after scrolling): 1px solid rgb(185, 201, 178) border, parchment background, no horizontal page overflow and no page exceptions. Desktop landing screenshot visually inspected. Screenshots and JSON report are outside the repository in `/Users/bipulchamoli/.codex/visualizations/2026/10/22/01a16160-ed4b-7e12-a603-78f5643745cf/` (`navbar-divider-1440.png`, `navbar-divider-390.png`, `navbar-divider-verification.json`). No new tests added; full behavioural suites and unit tests were not rerun for this border-only change. Not committed, pushed or deployed.


### UI-16: reduce the desktop left inset (2026-10-22)

Owner approved reducing the left-edge-to-ledger-line distance from approximately 200px to 150px at the current desktop size and normal 100% zoom. `ui/home.css`: increased `.entry` max-width from 1240px to 1340px and added `.landing .wrap { max-width: 1340px; }` so the landing header/footer remain aligned with its wider content. `ui/home.html`: added `class="landing"` to the body to scope that wrapper change; guide and 404 retain their original 1240px frames. At 1455px of available width, `(1455 - 1340) / 2 + 32 + 60 = 149.5px`, down from 199.5px. Wider/narrower desktop windows continue to use the existing centred responsive layout rather than a fixed 150px margin. Font sizes, colours, inner padding, navbar divider and all mobile breakpoints are unchanged. No JavaScript, review-app, backend, model, API, export, fixture or evaluation changes; existing uncommitted work preserved. TASKS and context updated.

**Verification:** installed Chrome with the existing bundled Playwright, temporary local server with tracing disabled and Python bytecode writes disabled. Checked landing layouts at 1455, 1440, 1280, 1180, 1060, 900, 720 and 390px; measured the requested 199.5px to 149.5px change, identical heading font/colour and inner padding, no horizontal overflow, retained sage navbar border, and identical measured layouts before/after below 1240px. Guide and 404 still have 1240px desktop wrappers; no page exceptions. Inspected desktop and phone screenshots. Re-ran the existing `tests/browser/landing.mjs`: all 18 checks passed (demo replay/steps, links, local vs hosted labels, desktop/phone landing and guide layouts, styled 404, no external loads or console errors). No fresh model calls. Full unit/other browser suites were not rerun for this scoped layout change. Browser evidence and before/after screenshots are outside the repo under `/Users/bipulchamoli/.codex/visualizations/2026/10/22/01a16160-ed4b-7e12-a603-78f5643745cf/landing-spacing/`. Not committed, pushed or deployed.


### UI-17: tighter landing sections and sage separators (2026-10-22)

Owner requested less blank space between sections and a line at each boundary. Changed `ui/home.css` only: standard landing `.entry > .body` padding is now 48px top/bottom on desktop and 32px on phones; hero initial top padding stays 64px desktop / 40px phone, with bottom padding reduced to 48px / 32px; fineprint uses 48px top/bottom desktop and 32px top/40px bottom phone. A 1px `--rule-2` top border on `.entry + .entry > .body` separates all seven boundaries, joining the existing vertical ledger line and stopping at the content right edge. Normal and fineprint margin-number offsets are 50px to align with the labels. Existing UI-15 navbar divider, UI-16 frame/inset, font sizes, palette, copy, JS, app/guide/404 behaviour, server, exports and protected evidence preserved. TASKS and context updated.

**Verification:** installed Google Chrome driven by the existing bundled Playwright, temporary local server with Sentry and bytecode writes disabled. Compared the pre-change stylesheet with current CSS at 1455, 1100, 900, 720, 390 and 320px. All seven section gaps shrink at each width; desktop hero-to-Problem gap is 224px → 97px, phone 148px → 65px (including the 1px divider). All seven rules have the intended sage colour, numbering stays aligned and nav targets remain below the sticky navbar. Existing font values and 149.5px desktop line position retained; no external resource loads or page exceptions. Desktop hero/Problem, review/evidence and phone transition screenshots visually reviewed, including an independent review. Re-ran the existing `tests/browser/landing.mjs`: 18/18 passed. No unit/other browser suites rerun for this CSS-only spacing change; no new test file or inference. `git diff --check` clean.

**Existing limit found, not hidden or fixed:** first scratch pass passed five widths then stopped on horizontal overflow at 320px. A fresh before/after comparison confirmed overflow at that width with both the old and new CSS; there is no overflow at the other five widths. Recorded separately as proposed UI-18, without expanding this task. Scratch comparisons, before/after screenshots and report are outside the repo under `/Users/bipulchamoli/.codex/visualizations/2026/10/22/01a16160-ed4b-7e12-a603-78f5643745cf/section-spacing/`. Not committed, pushed or deployed.


### UI-19: clearer setup and review page (2026-10-22)

Owner requested UI improvements to `/app`, showing a populated page with model connection-refused warnings. Changed `ui/index.html` and `ui/style.css`: compact header aligned with the page frame, serif Availazy wordmark and About/User guide navigation; numbered “Prepare your week” and review headings; settings grid; messages/roster inputs in a 2:1 desktop split with short labels and separate format hints; upload/demo actions grouped apart from the primary Suggest records action; run status on its own line. Refined source/suggestion cards, summary headings and export-button layout. The review column uses a container query to stack source/suggestion rows when its own available width is small, retaining the existing 432px desktop summary column and sheet width. Phone controls and fields stack. Existing semantic states, hatching, dashed pending outlines, review actions, focus styling and explicit failure alerts remain; failure summaries now use amber when failed-message elements are present.

Approved light Forest & Parchment colour tokens retained, including under a dark browser preference. Existing form IDs and action hooks retained; added explicit textarea names/descriptions and an upload label. No dependencies, JavaScript, server, API, ledger, export, model, fixture or evaluation changes. Previous uncommitted landing work preserved. TASKS and context updated. No commit, push or deployment.

Independent final markup audit confirmed all 31 original IDs retained, five new IDs, no duplicates, and all label/ARIA targets resolving. Existing status roles, hidden workspace, hosted `.local-only` restrictions, replay banner and JavaScript action hooks remain intact. This was a source audit, not a screen-reader test.

**Verification:** installed Chrome, existing bundled Node/Playwright/Python, temporary local servers with Sentry and Python bytecode writes disabled. The six existing app browser scripts passed: `sheet_display` 28/28, `demo_mode` 23/23, `review_safeguards` 12/12, `session_rerun` 10/10, `extraction_failures` 14/14, `csv_safety` 4/4. After the final replay-grid, label and amber-summary refinements, `demo_mode` 23/23 and `extraction_failures` 14/14 were re-run and passed. The existing landing suite passed 18/18. Unit discovery ran 116 tests: OK, 8 skipped (optional tracing SDK); Python also emitted a ResourceWarning about an unclosed subprocess stream, without a test failure. No browser console exceptions reported. `git diff --check` clean.

A scratch browser check on the final source loaded fictional set A using Rules only, exercised accepted/rejected/reviewed states, and checked 1455, 1400, 1200, 1100, 1024, 901, 900, 720, 600, 390 and 320px: no horizontal page/control/sheet overflow, no external resource loads, parchment body even with dark preference. A simulated `/api/suggest` failure retained all 49 per-message `role="alert"` warnings and the overall failure count. Desktop setup/workspace, phone setup/workspace and failure-state screenshots visually inspected, with an independent review of desktop layout and regression results. Scratch scripts, before/after captures and reports are outside the repo under `/Users/bipulchamoli/.codex/visualizations/2026/10/22/01a16160-ed4b-7e12-a603-78f5643745cf/app-ui/`.

**Limits:** no fresh model inference, runtime installation/start, Firefox, Safari, screen-reader pass or full new contrast audit. The model connection refusal visible in the owner's screenshot is separate from presentation and is not resolved or hidden by this change. Rules-only, saved replay outputs and simulated failures were used for browser verification. UI-18's pre-existing narrow landing overflow remains separately proposed; the app checks here do not claim to fix it.


### UI-20: setup card refinements (2026-10-22)

Owner request: "improve the ui of this card", with a screenshot of the Prepare your week card (uncommitted UI-19 state, preserved and built on). Standing owner instruction from UI-08: do not change functionality. Changed `ui/style.css` only.

- **Heading:** the tagline now sits under "Prepare your week", aligned with the title text, instead of floating at the far right; the 01 step number is a filled chip.
- **Settings:** week, timezone, reader, model and the day-first option sit in one recessed strip (`--bg`), separating how to read from what to read; the day-first checkbox is boxed to the input height so the row lines up.
- **Labels:** settings labels now use the same ink, size and weight as Messages and Volunteers (they were smaller and muted).
- **Source fields:** each format hint sits on the title line, right-aligned (under the box on phones), which shortens the card.
- **Actions:** the file picker's button is solid like Load fictional demo (it was dashed) and the input is 210px wide, removing the gap after "No file chosen"; a probe with a real fixture file showed Chrome shortening a long filename in the middle ("rivers…ek.txt"). In the hosted replay, where the source actions are hidden, the empty divided row is removed.

Checks run (2026-10-22, fictional set A, Rules only or saved replay outputs, no model inference): `node tests/browser/{sheet_display,demo_mode,review_safeguards,session_rerun,extraction_failures,csv_safety,landing}.mjs`: 28/28, 23/23, 12/12, 10/10, 14/14, 4/4, 18/18; `python3 -m unittest discover -s tests`: 116 OK, 8 skipped. Scratch screenshots of the card (outside the repo) at 1455, 1100, 720 and 390px locally and 1455/390px in replay mode: no page overflow, no element outside the card, no console errors. Not run: new contrast audit (no colour value changed; label text moved from `--muted` to `--text`, which only raises contrast), Firefox/Safari.


### UI-21: availability sheet card refinements (2026-10-22)

Owner request: "improve the ui of this card", with a screenshot of the Availability sheet after a run whose model reads failed (empty 18-row grid). Changed `ui/style.css` only; the sheet's markup, legend wording, JavaScript, ledger and export are unchanged.

- **Legend:** a two-column key in a recessed box; samples never wrap ("pending change" stays on one line) and its long explanation spans the full width.
- **Table:** row rules and faint day-column lines instead of a full cell grid, a quieter header with a stronger underline, zebra rows and a row hover to follow one volunteer across the week, volunteer names in ink.
- **Status:** accepted segments get a solid 2px edge in the status colour; pending segments keep the dashed outline and "pending" label, so accepted and pending differ by line style as well as colour (UI-05 unchanged). Phone cards keep plain backgrounds.

**Tried and reverted (UI-01):** a 20% name column and tabular numerals each made pending times overflow the day columns at 1400px (`sheet_display`: 5 overflowing cells in the test week and 28 in the demo, then 12 from the column width alone); the name column stays at 17% (day columns 47px) and digits stay proportional, with comments in the CSS. Long names still wrap to two lines.

Checks run (2026-10-22, fictional set A, Rules only; Model only with Ollama unreachable for the empty state; no model inference): `node tests/browser/{sheet_display,demo_mode,review_safeguards,session_rerun,extraction_failures,csv_safety,landing}.mjs`: 28/28, 23/23, 12/12, 10/10, 14/14, 4/4, 18/18; `python3 -m unittest discover -s tests`: 116 OK, 8 skipped; scratch screenshots of the filled and empty card at 1455 and 390px, no page overflow, no console errors. Not run: contrast audit (no new colour values; names moved from muted-on-sunken to ink), Firefox/Safari.

### D-37: ElevenLabs dropped (2026-10-22)

The owner decided to drop ElevenLabs, after the rival scan rated demo narration the weakest of our routes and syncing generated audio was judged not worth the time.

**Updated:**
- DECISIONS (D-37, index row);
- the TASKS INT-04 row (dropped);
- README, INTEGRATIONS and context.md status lines;
- the demo script: narrate live with the Mac microphone while recording each shot, or add on-screen captions.

No ElevenLabs account, offer or audio was used.

### DOC-09: diagrams for the guide and the developer docs (2026-10-22)

Documentation only: no change to `server.py`, `ui/app.js`, `ledger/`, fixtures, saved runs or results (`git diff` on those paths is empty).

**Read first:** AGENTS, context, CLAUDE. Then `ui/docs.html`/`docs.css`, README, ARCHITECTURE, API, `specs/final-export.md`, TESTING and the SENTRY_HANDOFF opening. Then the source: `server.py`, `ui/app.js`, `ui/index.html`, `ledger/messages.py`, `names.py`, `resolve.py`, `core.py`, `hybrid.py`, `model.py`, `export.py`, and the test names in `tests/`.

**Added or improved on `/docs`:**
- **01:** architecture with the optional Sentry path drawn separately (it had sat in the Ollama column), and the run pipeline with its re-resolve loop.
- **02:** page-start check and the three readers' actual code paths.
- **03:** the parsing decision flow and roster limits.
- **04:** copied words → person, day and time outcomes, plus the evidence check. The time ruler and day table were kept.
- **05:** a card's states, where each state counts, message marks and the one combined action, and failures.
- **06:** status gates (provisional still downloads) and how each file is made.
- **07:** where data goes (local, hosted replay, optional tracing) and how long a review lasts.
- **08:** a developer map from code to route, tests and docs.

Each figure has a caption and a "Sources" toggle.

**Mermaid diagrams:**
- README: workflow.
- ARCHITECTURE: §4 corrected (marks are not claims; status call added), §10 card states and message marks, §13 data boundaries.
- API: request sequence and demo-mode checks.
- final-export spec: status and cell states.
- TESTING: check layers.

**Map:** new `docs/DIAGRAMS.md`.

**Inaccuracies corrected:**
- **/docs review log:** it said "every reviewed record". It is accepted cards, plus pending ones only with the checkbox, and never rejected or not-applied cards.
- **/docs Model + rules card:** it implied both readers' suggestions are shown. Gemma's are shown; the rules flag disagreements and add only missed cancellations.
- **/docs Sentry box:** it sat inside the Ollama column; it is now a separate outbound path, and its privacy claim is bounded by the handoff evidence.
- **/docs prerequisites:** "macOS or Linux, 3.10+" is now "3.10+ stated, tested on 3.12 and 3.15".
- **ARCHITECTURE:**
  - §5 and §14 said JSON failures show no warning; they do since COR-03.
  - §14 said there was no formula protection; COR-02 added it to both CSV writers.
  - §11 said unknown GET paths return plain-text 404; they return the 404 page, and demo refusals are 403.
  - §15 said "hosted demo: none"; it is deployed.
  - §16 still listed ElevenLabs; it was dropped (D-37).
  - The sheet-overflow note is now marked historical.

**Checks run:**
- Unit tests: 116 run, OK, 8 skipped (Python 3.15, no sentry-sdk).
- `tests/browser/landing.mjs`: 18/18 PASS.
- In the browser pane on the owner's running local server, `/docs` at 1400, 390 and 320 px:
  - no horizontal page scroll after two fixes (a class clash with `home.css` `.flow`, renamed `.dflow`; the review matrix at 320 px now stacks);
  - no clipped diagram text;
  - phone branches redrawn as a left rail so options don't read as a chain.
- Contrast of the new text/background pairs is at least 4.76:1.
- The first "Sources" toggle opens with Enter and shows a focus outline.
- All 18 figures have a caption or label.
- Relative links and anchors in the edited Markdown: 0 problems.

**Not run:**
- GitHub rendering of the Mermaid blocks: no renderer is installed locally, so the syntax was reviewed by hand (semicolons and a `--` edge label removed).
- Other browser scripts: `app.js` and the server are unchanged.
- Safari, Firefox and screen readers.

**Note:** `/docs` links to `docs/DIAGRAMS.md` on GitHub, which resolves only after the owner pushes.

### DOC-10: independent review of DOC-09's completion report (2026-10-22)

Owner pasted Claude's DOC-09 completion report after requesting source-accurate diagrams. Inspected the actual working-tree diff, diagram-source map, guide markup, Markdown diagrams and relevant `ui/app.js`, `server.py`, `ledger/model.py`, `ledger/export.py` and CI source. Two independent review subtasks checked review/export semantics and Mermaid/API/CI diagrams. Product source was not changed. This entry, TASKS and context record the review and proposed corrections; no commit, push, inference, installation or deployment.

**Corrections proposed, not applied:**
- `ui/docs.html` Reviewing introduction/card/matrix (lines 332, 339, 359 at review time) overstates accepted-card inclusion and the need for explicit message marks. Accepted claims enter reconciliation, so later accepted changes may remove/replace their ranges. Unreviewed accepted availability can still be exported with `needs_review`; explicit marks determine complete status. Source: `ledger/export.py` `confirmed_export`, especially accepted/pending split, row generation and `complete` predicate.
- The `cap-card` caption says only “Use it anyway” restores a not-applied card, contradicting its preceding note and `ui/app.js` `onFieldChange`, which sets any edited card accepted. Retain the narrower A-key limitation.
- The final-export spec status diagram filters to accepted claims, then checks for pending claims along that sole path. Show a separate original-session pending branch or otherwise label the independent inputs; `confirmed_export` counts pending from the original live claims, not the accepted ledger.
- The startup figure asks only whether Ollama answers, then declares all readers ready. `available_models` also returns an empty list for a reachable Ollama with no installed models; `init` checks list length. Show the actual non-empty model-list condition. The reader caption should distinguish the default Gemma model from the selectable local installed model.
- API sequence request objects omit required data: `/api/suggest` uses `week_start`, not `week`, and sends `timezone`; `/api/export` also needs roster/week context. Correct the labels or explicitly identify abbreviated summaries; compare `payload()`, `run()` and `server.calendar`.
- Architecture arrows include J/K/E as if they mutate claims/recompute, while they navigate/focus only. Its Ollama node says model readers only even though `/api/tags` is queried at startup regardless of the selected reader; separate catalogue lookup from model inference. The card-state figure also omits valid Accept/Reject/edit transitions; either show them or label it as a selected-transition illustration.

**Verification and limits:** `git diff --check` passed. No obvious Mermaid syntax blocker found by static inspection, but no bundled parser was found, so Mermaid rendering remains unverified. The pasted report's 116 unit-test run, 18 browser checks, contrast measurements and screenshots were not independently rerun; do not relabel them as fresh results from this review. The new GitHub DIAGRAMS link cannot establish published availability before the owner pushes. These are proposed documentation corrections, not application defects or permission to change runtime behaviour.

### DOC-10: corrections to DOC-09's diagrams (2026-10-22)

Documentation only. `git diff` on `server.py`, `ui/app.js`, `ui/index.html`, `ledger/`, fixtures and `evaluation/` is empty.

**Each fix checked against source:**

1. **Export inclusion vs completeness** (`ledger/export.py` `confirmed_export`):
   - Accepted claims go into `build_ledger`, so a later accepted correction or cancellation replaces or removes their time.
   - Rows include accepted availability from unreviewed messages; those cells are `needs_review`.
   - Marks affect only complete vs provisional; `/api/export` always returns the file.
   - Fixed in the `/docs` prose, the "where each card counts" matrix, the marks caption, the files figure and the Accepted node.
2. **Not-applied cards** (`ui/app.js`):
   - `onFieldChange` sets `accepted` on any card.
   - `onKey` blocks only `a` for a dropped card; `r` rejects it.
   - The `/docs` caption and node now say this; the claim that "only Use it anyway" restores a card is gone.
3. **Pending-status diagram** (`docs/specs/final-export.md`): redrawn as one request feeding three separate inputs to the status decision: accepted claims → ledger → blocking issues; pending claims counted from the same session; unreviewed messages from `reviewed_messages`.
4. **Startup** (`ledger/model.py` `available_models`, `ui/app.js` `init`):
   - An empty list covers Ollama being down, too slow, or having no models; it shows the same message.
   - With models, the menu lists all of them and preselects `gemma4:e2b-it-qat` when present.
   - With none, the menu falls back to the default name.
   - Gemma is described as the default model, not the only one.
5. **API labels:**
   - suggest: `{message, roster, week_start, timezone, extractor, model, run}`;
   - resolve and export: `{messages, claims, roster, week_start, timezone, reviewed_messages}`.
6. **ARCHITECTURE:**
   - J/K/E/Esc are a separate dashed "no claim change, no request" node.
   - `/api/tags` is shown on every page load for any reader; `/api/chat` is labelled as the only call that needs a model reader (in §4 and §13).
   - The card state diagram now has every transition the code allows: accepted ⇄ rejected, dropped → rejected by R, dropped → accepted by edit, Reset from every state.

**Also aligned:** the startup prose in ARCHITECTURE §3 and API `/api/status`.

**Checks:**
- **Mermaid rendering:** all 10 blocks render without errors in headless Chrome with Mermaid 11.16.1, copied from the owner's existing local `kestra/ui/node_modules` (nothing installed). Screenshots inspected, and three readability problems fixed: a J/K self-loop label overlapping the review-log label, two state labels overlapping, and a sequence note spilling outside its box.
- **`/docs` in the browser pane** at 1400, 390 and 320 px: no horizontal page scroll and no clipped diagram text, after fixing a non-wrapping phone label (420 px at 390) and a long tag (347 px at 320).
- **Unit tests:** 116 run, OK, 8 skipped.
- **`landing.mjs`:** 18 PASS, 0 FAIL.

**Not verified:** GitHub's own Mermaid version and rendering.


### DOC-11: bounded verification of DOC-10 corrections (2026-10-22)

Owner pasted Claude’s DOC-10 follow-up report. Source inspection confirmed the original fixes in the guide, export-spec flow, API payload labels and architecture arrows; an independent review confirmed the R-key rejection of dropped cards against `ui/app.js`. No product source edits, tests, browser/rendering checks, inference, installation, commit or deployment were performed in this verification. `git diff --check` passed. The working-tree diff for `server.py`, `ui/app.js`, `ui/index.html`, `ledger/`, fixtures and evaluation was empty. The report’s Mermaid 11.16.1 renders, unit and browser checks remain Claude-reported results, not fresh runs by this review.

Two newly introduced guide statements still need correction (proposed, not applied): `ui/docs.html` line 181 says Gemma is the only model evaluated, contradicting Qwen model/hybrid A/B results in `evaluation/RESULTS.md` lines 24–25 and fresh-call provenance at 42–44; line 388 says marks only decide file status, while `ledger/export.py` lines 74–92 also changes `needs_review` cell flags and empty placeholder rows according to unreviewed messages. Suggested wording: Gemma is the default; marks help determine file status and cells needing review, and never block download. TASKS records proposed DOC-11, its DOC-10 summary no longer repeats the overly narrow marks claim, and context records this bounded follow-up. Other original DOC-10 findings were not reopened.

### DOC-11: two guide wording corrections applied (2026-10-22)

Wording only, in `ui/docs.html`:
1. **Reader caption:** removed "and the only one evaluated". `evaluation/RESULTS.md` records Qwen3.5 4B model-only and Qwen + rules results on sets A and B.
2. **Message-marks caption:** now reads "Message-review marks help determine complete/provisional status and which cells need review. They never block downloading the export."

**Checked in source:**
- `ledger/export.py` `confirmed_export`: unreviewed non-duplicate messages keep the status provisional, and their accepted or pending claims mark cells `needs_review`.
- `ui/app.js` `exportFinal`: the CSV is downloaded whatever the status.

**Also changed:** the matching `docs/DIAGRAMS.md` row. The DOC-10 records keep their earlier wording as history; DOC-11 supersedes the "marks decide only status" phrasing.

**Checks:** see the hand-back. No layout or behaviour change.


### Release preparation: UI-11, UI-12, UI-18, UI-02, release verification, DEP-03, REL-05 (2026-10-22)

Owner assignment: prepare Availazy for final release and submission; implement and verify the scoped fixes; prepare the release materials; do not commit, push, deploy or publish.

**Baseline.** `git status` clean; `HEAD` = `origin/main` = `a4bebb7` (`git ls-remote`). The "uncommitted" labels on BRAND-01, UI-09 to UI-21 and DOC-09 to DOC-11 were stale: that work is committed (TASKS and context corrected). Outstanding before this pass: UI-11, UI-12 (todo), UI-18 (proposed), UI-02 (todo), REL-02 (todo), REL-05 (todo), DEP-03 (in progress), REL-04 (owner).

**UI-11 privacy wording.** Replaced the blanket "Nothing leaves your laptop/machine" claims (landing hero note, facts row, privacy heading and paragraph, Sentry node and its screen-reader caption, illustrated replay banner, app replay banner; README's core-workflow sentence) with message-local wording that separates the local app from the hosted fictional replay, keeps the saved-output disclosure, says reading your own messages happens in the local app, keeps the opt-in Sentry disclosure and adds the bounded caveat that Sentry can add data of its own on receipt (approximate location observed, see SENTRY_HANDOFF §5). Source checked: `ledger/tracing.py` allowlists. No tracing or account change. `demo_mode.mjs`'s exact banner string updated; its behaviour checks unchanged.

**UI-12 replay link.** `ui/home.js` `REPLAY_URL` → `https://availability-ledger-replay.onrender.com/app`; `landing.mjs` expectation updated. Local "Open the app" buttons still open the local `/app`.

**UI-18 landing overflow at 320 px.** Reproduced with element bounds, not page width (the body's `overflow-x:hidden` masked it): the first "How it works" card was 299 px in a 254 px column, cutting off its text and JSON exhibit (screenshot). A first attempt (`min-width: 0`) changed nothing; tracing the ancestor chain showed the card is itself a grid whose implicit column was sized by the JSON's `white-space: pre`. Fix in `ui/home.css`: `.hand { grid-template-columns: minmax(0, 1fr) }`, and on phones the JSON exhibit wraps instead of scrolling. Afterwards no visible element is past the viewport at 320/360/390 px except the terminal block's code inside its own horizontal scroller (unchanged, with its Copy button). `landing.mjs` extended to 320 px with an element-bounds check on the landing page and the guide; it fails on the old CSS and passes now.

**UI-02 accessibility (bounded, automated; Chrome 155).** Landing, guide, 404 and the review app (setup, populated, 49 failed reads): one `h1` and no skipped heading levels; lang/title set; labelled landmarks; 0 unnamed controls in the accessibility tree; logical tab order with a visible focus indicator at every stop checked; 0 text elements under 4.5:1 (3:1 large) on all four pages, including the new privacy copy and the amber failure state; `role="status"` on progress and review state, `role="alert"` per failed read; app and landing fit at 320 and 640 px (≈400%/200% zoom). Fixed: the app had no keyboard bypass past the suggestion cards (≈20 tab stops each, ≈1,200 to reach the exports); added a skip link to the week overview and exports, hidden until the workspace exists (verified: first stop after a run, visible on focus, Enter then Tab lands on the first Needs-a-decision link). Not done: VoiceOver/screen readers; Safari (safaridriver gave no session response; automation settings not changed); Firefox (not installed). Follow-ups proposed as UI-22 (identical Accept/Reject/Reset names; possible re-announcement of 49 alerts on each re-render, unverified).

**Import → review → export (invented messages, Rules only, Sentry unset).** Scratch script: non-Monday week refused with no session; a WhatsApp-style `.txt` upload fills the box; the day-first switch reads 03/11/2026 as 3 Nov (11 Mar without it); roster entry; suggestions beside their highlighted quotes; pending suggestions shape the provisional sheet (Ben's pending cancellation shows "pending change"); review log 0 rows without and 5 with the pending option; accept, edit (auto-accepts, end time 11:30 exported), reject, reset; with everything accepted but no message marked reviewed the final sheet downloads as provisional (unreviewed IDs in its first line, `needs_review` cells); after marking every message reviewed it is complete; Ben's later cancellation removes his Wednesday; Cleo's "if it's dry" stays conditional (the Rules reader records only the cue word "if" as the condition). Existing suites cover the replay with served inputs and saved outputs and its refusals (`demo_mode`), visible extraction failures with continued reading (`extraction_failures`) and a failed rerun preserving the previous review (`session_rerun`). **Finding (COR-19, proposed):** Rules only read "Saturday 9-12 if it isn't raining" as unavailable instead of conditional. **Live model smoke check: not run**: Ollama was not running (no process, no answer on 127.0.0.1:11434) and was not started.

**Regression checks (working tree).** `sheet_display` 28/28, `demo_mode` 23/23, `review_safeguards` 12/12, `session_rerun` 10/10, `extraction_failures` 14/14, `csv_safety` 4/4, `landing` 20/20; `python3 -m unittest discover -s tests` 116 OK (8 skipped); no console errors; `git diff --check` clean. Desktop/phone screenshots of all four pages inspected; the guide's diagrams reflow at 390 px.

**Release verification.**
- **A. This working tree:** everything above; not committed or deployed.
- **B. `origin/main` = `a4bebb7`:** fresh clone: 116 tests OK (8 skipped), `shasum -c evaluation/protected.sha256` all OK, no `.env`/secret files tracked. GitHub Actions "tests #17" on `a4bebb7`: success (unit tests, protected evidence, cache-only re-score).
- **C. Render (observed 2026-10-22):** woke in 23 s; `/`, `/app`, `/docs` returned 200, an unknown path 404; `home.html`, `index.html`, `docs.html`, `404.html`, `style.css`, `home.css`, `docs.css`, `app.js`, `home.js` byte-identical to `a4bebb7` (which changed `docs.html`/`home.html` from its parent, so the deployed front end is `a4bebb7`'s); `/api/status` reports `demo: true`. Server code was not compared. The public site still shows the old privacy wording until the owner pushes and Render redeploys.
- **GitHub Markdown diagrams:** ARCHITECTURE (4), README (1), TESTING (1) and API (2) each show one rendered Mermaid frame per block; ARCHITECTURE checked visually.

**DEP-03 demo script** updated in place: the m28 wording matches the app ("replaced earlier answer for this day"); the inaccurate "never leave your machine" line replaced; explicit captions for local live vs hosted replay; message marks shown as separate from accepting, with the provisional CSV's first line; the stale "if the replay isn't deployed" contingency replaced; Sentry line bounded to recorded evidence; captions option (D-37). Its moments were re-checked on the replay path: 67 suggestions, 10 Needs-a-decision items (m26, m41, m29 among them), m28 and m29 in Changes over time, rejecting m48 turns Maria's Tuesday from conditional to available.

**REL-05 post draft:** [docs/demo/post-draft.md](docs/demo/post-draft.md), not published. Uses the official template headings and tags (rechecked today), frozen set C as the headline (Gemma + rules 0.527) with the 1.0 labelled post-hoc, limitations including COR-19, repo/replay/guide links and `[VIDEO LINK — not recorded yet]`. Owner items listed at its top.

**Official rules rechecked:** deadline conflict unchanged (see COMPETITION). Eligibility, final categories, recording and publication remain the owner's (REL-04).

**Not done / limits:** no commit, push, deploy or publication; no live inference; no screen reader, Safari or Firefox; the Render server code and Render logs were not inspected; Sentry was not enabled and no account was opened.


### Release-preparation review: UI-11/UI-12/UI-18/UI-02, REL-05 and DEP-03 (2026-10-22)

Owner supplied the completion report. Inspected the actual working-tree UI/test diff, task records, post draft, script and Sentry handoff. Independent read-only UI review found no material issue in the scoped privacy/replay/320px fixes or keyboard skip link; scratch evidence checked Enter then Tab reaches the summary. Independently reran the changed `tests/browser/landing.mjs` using existing Node/Chrome, Sentry unset and bytecode writes disabled: 20/20 passed, no console errors, landing/guide element bounds passed at 1400, 390 and 320px. `git diff --check` passed. No app, backend, extraction or export source was changed by this review; unit and other browser suites were not rerun and their results remain those in the supplied report. No inference, installation, account action, commit, push, deployment or publication.

Independent pure-Python reproduction confirmed COR-19 with invented Cleo Example messages: “Saturday 9-12 if it isn't raining” and “if it is not raining” resolve to unavailable with an empty condition, while “if it's dry” is conditional and plain “I cannot do Saturday 9-12” is unavailable as expected. Cause: Rules NEG wins before COND. This is an existing extraction limitation, not introduced by the UI release diff; no fix or held-out tuning was attempted. A future fix requires a scoped task and invented regression cases; model behaviour was not established.

Before recording/publishing, two release-copy corrections are still needed (not applied here): `docs/demo/post-draft.md` line 29 and `docs/demo/script.md` line 49 should include no blocking who/date/time/conflict issues as the third complete-status gate (`ledger/export.py` BLOCKING and complete predicate). Post draft line 59 claims the origin of geo values and broad filtering more strongly than the evidence: SENTRY_HANDOFF states enrichment origin is not established and filtering was verified only for four visible geo values on an inspected chat and its parent. Describe the received attributes and targeted filtered observation, retaining the full-audit/origin limits. TASKS REL-05/DEP-03 and context record these outstanding copy items and the still-unverified live-model dry run. Other release checks, public CI/deployment observations and deadline research were not independently repeated.


### REL-05 / DEP-03: release-copy corrections (2026-10-22)

Owner request: two corrections to the submission-post draft and the demo script; application behaviour unchanged.

- **Completeness:** both now state all three conditions for a *complete* final sheet (every non-duplicate message marked reviewed, no pending claims, no blocking issues) and that a provisional export still downloads. Checked in source: `ledger/export.py` `confirmed_export` lists unreviewed messages excluding duplicates (`not m.duplicate_of`), counts pending claims and blocking issues (kinds `who`, `date`, `time`, `conflict`), and sets `complete = not unreviewed and not pending and not blocking`; `ui/app.js` `exportFinal` downloads either status. Files: `docs/demo/post-draft.md` (What I Built), `docs/demo/script.md` (shot 6 narration). This also closes the DEP-03 row's request to add the no-blocking-issues requirement; its live-model dry run remains open.
- **Sentry claim:** the post's caveat now says only what docs/SENTRY_HANDOFF.md §5 records: received traces displayed geo attributes (not sent by our code); after the settings change, the four visible geo values on one inspected chat span and its parent appeared filtered; the enrichment origin and a complete received-data audit remain unverified. The prize-category line no longer says "content-free", only that our code sends no message content. The script's optional Sentry line gives the same bounded statement for use if location comes up.

Checks: relative `.md` links in the changed files resolve; `git diff --check` clean. No application file changed in this step.

**Flagged, not changed (outside this request):** `ui/index.html:85`, the sheet panel hint, still says "Provisional until every message is marked reviewed and nothing is pending" (two conditions; the export panel's hint has all three). `ui/home.html:426`, the landing Sentry node (UI-11 wording), says "Sentry can add data of its own on receipt, such as an approximate location", which asserts the enrichment origin that the handoff leaves unverified. Both await an owner decision.


### UI-11 follow-up: final copy corrections (2026-10-22)

Owner request: two copy-only corrections, resolving the two items flagged in the REL-05/DEP-03 entry above. Layout, styling and behaviour unchanged.

- `ui/index.html` availability-sheet hint: "Provisional until every non-duplicate message is marked reviewed, nothing is pending and no blocking issue is open. The final-sheet export uses accepted records only." It now matches `ledger/export.py` `confirmed_export` and the export panel's hint.
- `ui/home.html` landing Sentry box: the location-origin claim is replaced with "Received traces have shown location attributes that our code does not send; their origin remains unverified." The figure's screen-reader caption is aligned with the same sentence. "Sentry, only if you opt in", the metadata list and "Our code never sends message text, names, quotes, prompts or replies" are kept.

No test asserts these strings. Checks run (Chrome 155, Sentry unset): `landing` 20/20 (layout and element bounds at 1400/390/320 px), `demo_mode` 23/23, `sheet_display` 28/28, `review_safeguards` 12/12, `session_rerun` 10/10, `extraction_failures` 14/14, `csv_safety` 4/4; `python3 -m unittest discover -s tests` 116 OK (8 skipped); `git diff --check` clean. Privacy-figure screenshots at 1440 and 390 px inspected: the box grows by a line or two and nothing else moves. Not committed, pushed or deployed.


### CFG-01: local environment file and example (2026-10-22)

Owner requested .env and .env.example. Verified current supported variables from server.py and ledger/tracing.py: only exact LEDGER_DEMO=1 enables the hosted replay; local mode otherwise binds 127.0.0.1, with the port from argv (default 8765); PORT is read only in replay; empty SENTRY_DSN keeps optional tracing off. An independent read-only review confirmed the file-only approach and identified the obsolete comments-only claim in API docs.

Created a new local .env using exclusive creation with mode 600 (no pre-existing file, no local .env contents read or printed). Updated .env.example from an old explanatory comments-only file to a shell-compatible template with LEDGER_DEMO=0, empty SENTRY_DSN and commented PORT=10000 for hosted replay only. Neither file contains credentials or speculative settings; model/reader are still chosen in the app and Ollama’s URL remains fixed in source. No automatic loader or dependency added. Existing .gitignore patterns already ignore .env/.env.* and allow .env.example; only the explanatory comment changed. README Configuration now documents optional copy-without-overwrite and a subshell that sources/exports .env before starting server.py on port 8780. Updated docs/API.md’s comments-only assertion and TASKS/context. Previous release work preserved.

Verification: bash -n and zsh -n on .env.example both passed; metadata/Git checks verified .env exists, is not a symlink, has mode 600, is ignored and untracked, while .env.example is not ignored. git diff --check passed. The local .env was not read during verification; the manual source/start command was documented, not executed. Unit/browser suites were not rerun because application source/behaviour is unchanged. No secret supplied or tracing enabled; no server/model process, inference, installation, account change, commit, push or deployment.


### CFG-02: terminal-only live-model check guide and checker (2026-10-23)

Owner asked how to perform the remaining test from Terminal after creating the environment files. Source review confirmed there is no app review CLI; the stateless HTTP API requires full messages, raw claims, roster list, week_start, timezone and reviewed_messages on resolve/export. An independent review confirmed the request fields and the need to distinguish model-source claims from rules/replay output. Actual .env contents were not read.

Prepared `/Users/bipulchamoli/.codex/visualizations/2026/10/22/01a16160-ed4b-7e12-a603-78f5643745cf/terminal-testing/check_model.py` outside the repository. It uses Python standard library and a loopback-only URL (port 8780 by default; --port can select another), no proxy, a 330-second client timeout for the backend’s 300-second model timeout, at most two sequential model-only requests and no retries. Invented Ana/Ben messages have known expected dates/times for the week of 9 Nov 2026. It requires readable non-saved model claims, correct resolved values and exact source quotes, prints flags/messages/quotes for inspection, then asks separately for ACCEPT and REVIEWED. Exports verify pending claims contribute no time ranges, accepted/unreviewed messages stay provisional with needs_review, and explicit review yields the two expected confirmed ranges. It saves fictional requests/responses, failure details and CSVs in a private tempfile directory and never imports app code, reads .env, writes fixtures/caches, starts services, installs software or commits changes. This API checker does not exercise browser UI/file upload/shortcuts or hybrid-reader behaviour, and its terminal session is not loaded into browser state.

Validation (offline only): five scenarios using simulated model replies plus the actual server.parse/resolve/export functions passed: correct output, wrong model time rejected before acceptance, unreadable reply rejected, declined acceptance stops without a complete pass, replay mode rejected before any suggestion request. No HTTP server, model calls or protected-repository writes were used for validation. An independent static review found no material contract/false-PASS issue. Application unit/browser suites were not rerun because application code is unchanged. Live inference remains pending the owner running the checker against their own untraced local server; no live success is claimed. Updated TASKS and context. No commit, push, deploy, publication or account action.


### CFG-02 / DEP-03: owner manual live-model smoke check passed (2026-10-23)

The owner first ran the terminal checker: Ana and Ben suggestions and quotes matched the invented input, and pending-export exclusion passed. That attempt stopped without an ACCEPT confirmation and correctly reported CHECK NOT PASSED; it is not recorded as a complete checker success. The owner then requested manual steps and completed a separate Chrome workflow at `http://127.0.0.1:8780/app`, using Model only, `gemma4:e2b-it-qat`, the week starting 9 Nov 2026 and the invented Ana/Ben roster/messages. Screenshots showed both messages read in 4 s, matching source quotes, Ana selected on Tue 10 09:00–12:00, Ben on Thu 12 13:00–15:00, and no open issues. The owner accepted both suggestions separately from marking the messages reviewed.

Agent directly parsed the two owner-supplied files with Python's standard-library CSV reader; files were read only and remain outside the repository:

- `/Users/bipulchamoli/Downloads/availability-final-2026-11-09-provisional (1).csv`: metadata `week=2026-11-09; status=provisional; unreviewed=m01 m02; pending=0; blocking_issues=0`. Exactly two available rows: Ana Example, 2026-11-10, 09:00–12:00, source m01.1; Ben Example, 2026-11-12, 13:00–15:00, source m02.1. Both have empty conditions and `cell_state=needs_review`.
- `/Users/bipulchamoli/Downloads/availability-final-2026-11-09-complete.csv`: same week and exact two availability/source rows, `status=complete; unreviewed=; pending=0; blocking_issues=0`, both `cell_state=confirmed` after the owner's explicit review actions.

Checks asserted the exact rows, metadata, empty conditions and expected cell states in both files; all passed. This establishes the tested local model → human acceptance → explicit message review → provisional/complete CSV flow. It clears DEP-03's short live-model dry-run prerequisite, not the whole recording task. It is not a full-week, hybrid-reader, privacy-payload or general model-accuracy test; unit/browser suites were not rerun in this follow-up, and the agent made no new model calls, started no services and read no .env.

Updated TASKS CFG-02/DEP-03 and the current context summary. Read-only release review confirmed release changes remain local and uncommitted: next are owner review/commit/push, then fresh-clone/unit/protected-evidence and latest CI/Render verification for that new revision (REL-02), recording, final post and owner eligibility/publication steps. The existing script opens with a full-week live Model + rules run, which this short check does not validate; the proven two-message live flow can be used for the opening, with clearly labelled saved-output replay for history/cancellation scenes. No script or application change was made in this follow-up, and no commit, push, deployment, publication or account action occurred.


### REL-07: final local release review before the owner's push (2026-10-23)

Owner assignment: complete the release review and verification, adjust the demo script to the verified live workflow, update the records and hand back exact commit/push commands. No commit, push, deployment, publication, installation, account change or model request. The owner's two-message Model-only Chrome check (CFG-02, recorded above) was taken as completed evidence and not repeated; the earlier terminal checker attempt remains recorded as not passed.

**Baseline.** `main` tracking `origin/main` at `a4bebb7`; 18 modified tracked files plus untracked `docs/demo/post-draft.md`; `.env` ignored, untracked, mode 600 and not opened. A `server.py 8766` process (started by someone else about 18 h earlier) was listening and was left alone; nothing was on 8780 or 11434 at check time.

**Review of the release diff.** Checked against source and evidence:
- Privacy wording (landing hero, facts row, privacy section, Sentry node and caption, both replay banners, README) separates the local app (messages go only to 127.0.0.1 and local Ollama), the hosted fictional replay (saved outputs, no pasted text) and opt-in tracing (structural metadata, no content from our code). The geo sentence ("origin remains unverified") stays within SENTRY_HANDOFF §5; so do the post draft and the script's optional Sentry line.
- Completeness: `ledger/export.py` `confirmed_export` gives complete only with no unreviewed non-duplicate message, no pending claim and no blocking (`who`, `date`, `time`, `conflict`) issue, and builds rows from accepted claims only; `ui/app.js` `exportFinal` downloads either status. App hint, README, post and script all state the three conditions.
- Replay links: `ui/home.js` `REPLAY_URL` and the post/script point to `/app`; the remaining bare-root URLs are the landing page or `og:url`, which is correct.
- UI-18 (`.hand` `minmax(0, 1fr)`, phone `pre-wrap`) and the app skip link are intact; `landing.mjs` covers 320 px element bounds.
- Configuration: README, API.md and `.env.example` say `server.py` does not load `.env` and give the subshell start command.

**Material issue found and fixed.** The working-tree `.env.example` held a real-looking Sentry DSN as the `SENTRY_DSN` value, contradicting its own comment ("Empty means OFF … Never put a real DSN in .env.example"), README and the CFG-01 record. It was restored to `SENTRY_DSN=`. Checks by file name/commit only (the value was not printed): no other repository file outside `.env` contains it, and `git log --all -S` finds it in no commit. It is unknown whether the owner meant it for `.env`; the agent did not read `.env`. Owner decision recorded in TASKS REL-07: optionally rotate the key.

**Other changes (docs only).**
- `docs/demo/script.md` (DEP-03): shot 1 now records the verified Ana/Ben flow (start commands, Model only, `gemma4:e2b-it-qat`, week 2026-11-09, exact roster and messages, expected Tue 10 Nov 09:00–12:00 and Thu 12 Nov 13:00–15:00, optional accept/mark-reviewed). Its narration no longer implies the live shot is the fifty-message week; shot 2 introduces the replay as the fifty-message week with answers saved earlier. The Render-down fallback is now the local replay (`LEDGER_DEMO=1 PORT=8781`, saved outputs, binds 0.0.0.0, captioned) instead of an unvalidated live Model + rules run. New honesty rule: shot 1 is not accuracy evidence. No time-saving claim.
- `README.md`: replay `/app` line no longer says "after its next deploy"; scope sentence and work order say ElevenLabs was dropped; Actions row cites the latest observed run ("tests #17" on `a4bebb7`).
- `docs/demo/post-draft.md`: Sentry allowlist sentence says "structural metadata such as …" (the allowlist also keeps reader, prompt version and counts); owner checklist adds a post-push CI check before keeping "The latest run on `main` passed".
- `CLAUDE.md` work order: ElevenLabs narration replaced by the D-37 wording and the CFG-02 status.
- `TESTING.md`, `TASKS.md` (REL-07 added; REL-02, REL-05, DEP-03 updated), `context.md`.

**Verification (fresh, 2026-10-23; `SENTRY_DSN`/`LEDGER_DEMO` unset, `PYTHONDONTWRITEBYTECODE=1`, `.env` not sourced).**
- `python3 -m unittest discover -s tests` (Python 3.15.0): 116 run, OK, 8 skipped (no `sentry-sdk`).
- Browser suites (Node 22.11.0, Chrome; their own ports 8767–8774 and 9335–9342 were confirmed free first): `sheet_display` 28/28, `demo_mode` 23/23, `review_safeguards` 12/12, `session_rerun` 10/10, `extraction_failures` 14/14, `csv_safety` 4/4, `landing` 20/20; each exited 0 with no console errors; no server left listening afterwards.
- `shasum -a 256 -c evaluation/protected.sha256`: 17/17 OK. CI inventory diff of `frozen/`, `frozen-setC/`, `tuning/` against the checksum list: no difference.
- CI-equivalent re-score, A/B/C × rules, Gemma (`--cache-only`), Gemma + rules (`--cache-only`), `--out` a scratch temp folder, then `evaluation.ci_summary`: all 9 files match the committed results; fresh model calls 0 in every row.
- `bash -n` / `zsh -n` on `.env.example`: OK (after the DSN fix). `git diff --check`: clean.
- `git status --porcelain` identical before and after the checks (the doc edits came afterwards; none touch code, tests or protected files).

**Not done / limits.** No live inference, fresh clone, GitHub Actions or Render check of the release revision (it does not exist until the owner commits and pushes). Not re-run: Safari, Firefox, screen readers, the tracing suite with `sentry-sdk`. The owner's live evidence covers the two-message Model-only flow only, not full-week or Model + rules accuracy. COR-19 and UI-22 stay proposed and out of scope.

**Next (owner).** Optionally rotate the Sentry key; commit the listed files and push; then the post-push REL-02 task: verify the pushed commit, a fresh clone, its CI run and Render's pages/assets and replay. Then record the demo and finish/publish the post (DEP-03, REL-05, REL-04).

**Independent hand-back check (2026-10-23).** Confirmed the current `.env.example` has exactly one empty SENTRY_DSN assignment, `.env` is ignored and untracked (contents not opened), the index is empty, and HEAD remains `a4bebb7`. The proposed 19-file staging list matches the 18 modified tracked files plus `docs/demo/post-draft.md`; `git diff --check` passed. Only this verification note was added by the hand-back review. The full test suites, historical DSN search and remote CI/Render were not independently repeated here; their results above remain the coding agent's reported evidence. TASKS REL-07 and the current context already accurately describe the local-ready, pre-push state. No staging, commit, push, deployment or account action.

### REL-02: pushed release, fresh clone, CI and live Render verified (2026-10-23)

Owner reported the push and asked what remained. Initial owner checkout was clean at `d4b2f76c6b1e5da1da7b00b0dcecf586284a86aa`. The public GitHub main branch and an independent fresh clone both matched that exact SHA. The following checks were split between independent release/CI reviews and the live-site check; no commit, push, account change or deployment trigger was performed by agents.

**Fresh public clone:** `/private/tmp/availazy-rel02-clone.QBsX6Y`, created from `https://github.com/bipul724/availability-ledger.git` (main, single branch). Existing bundled Python 3.12.14, SENTRY_DSN/LEDGER_DEMO unset, PYTHONDONTWRITEBYTECODE=1: `python3 -m unittest discover -s tests` ran 116 tests, OK, 8 optional Sentry SDK skips, in 1.930 s. A non-failing ResourceWarning about a test file handle was observed. `shasum -a 256 -c evaluation/protected.sha256`: 17/17 pass; protected-folder inventory 16 actual files = 16 recorded, no additions/removals. Tracked-filename check found no actual `.env` or private `.env.*` (only `.env.example`). Clone final Git status clean. No install, fresh inference, re-score or evaluation-cache write.

**Public CI:** [GitHub Actions tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754), push event on that SHA, completed success. Timing 2026-10-22 20:50:18–20:50:30 UTC (23 Oct 02:20:18–02:20:30 IST). All three jobs succeeded: Protected evidence unchanged (SHA-256); Cache-only re-score of sets A, B, C (saved Gemma outputs); Unit tests (Python 3.12, offline). Every returned step succeeded. Main branch/run/job metadata read through unauthenticated public GitHub APIs; no auth or secret read.

**Live Render:** `https://availability-ledger-replay.onrender.com`, observed starting 2026-10-22T20:55:38Z (23 Oct IST). `/api/status` returned HTTP 200 with `demo: true` and saved model `gemma4:e2b-it-qat`. Landing `/`, app `/app`, guide `/docs` returned 200; `/__release_check_d4b2f76` returned the styled 404. Nine response bodies match `git show d4b2f76:ui/<file>` byte for byte: home.html, index.html, docs.html, 404.html, home.css, style.css, docs.css, home.js, app.js. An invented suggestion message not served by the replay was refused with HTTP 403.

**Live Chrome replay:** separate headless Chrome session using existing bundled Playwright, no installation or local server. Disclosure visible; own-message text/file inputs hidden. Model + rules replay read 50 fictional fixture messages in 20 s from saved outputs, produced 67 suggestions (model/rules sources) and no failures. Four eligible messages were explicitly accepted/marked reviewed; rejection worked (6 claims accepted, 1 rejected at check time). Sheet and history rendered (31 segments, 18 history items). Final CSV capture had `availability-final-2026-11-09-provisional.csv`, provisional metadata and confirmed accepted records; review-log capture had `availability-log-2026-11-09.csv` and 7 lines. The partial replay review is correctly provisional; the separate two-message complete export remains the CFG-02 evidence. Page width fits at 1400 and 390 px; no browser console errors or exceptions. All 22 bounded live checks passed. Script/report outside repo: `/private/tmp/availazy-release-d4b2f76-o2sfxgn4/verify_render.mjs`, `render-report.json`. No real messages, new local model calls or downloaded CSV files were used by this live check; exports captured in the disposable browser session.

**Limits:** web-reader access to Render was unavailable and sandbox DNS was restricted; authorized network/browser execution succeeded. Render dashboard, server source and logs were not directly inspected, so byte matching establishes the served front-end files, with server replay behavior checked through its public endpoints/UI. Full local seven-suite results remain the pre-push REL-07 evidence; not rerun here. No additional account/privacy audit, Safari/Firefox or screen-reader check.

Marked REL-02 done and updated committed/deployed statuses for REL-07, UI-11/UI-12/UI-18, CFG-01 and the DEP-02 verification link; added the current handoff summary. Only TASKS.md, PROGRESS.md and context.md changed locally in this follow-up. Next: owner records the demo (DEP-03), adds its URL/screenshots and actual disclosures/credits to the drafted post (REL-05), confirms personal eligibility/current entry requirements/categories (REL-04), and publishes. Optional/proposed product follow-ups remain outside this release. These tracking-doc changes can be included with the final demo/post update; no application change or new release deployment is required by this verification.

### DOC-12: complete project documentation audit (2026-10-23)

Owner requested every project document be inspected and reconciled with the complete implementation before any documentation changes, without application/configuration/dependency/data/deployment changes or fabricated evidence. The source/history review covered server/routes, all ledger modules, front-end files, tests/browser harness, evaluation/cache/scoring, fixture/reference formats, environment references, CI and Render configuration. Inventoried 28 existing project-owned docs, five reference configs and 49 generated dependency documents. The starting tree had three local post-push record edits; those were preserved.

**Coverage/outcome:** 25 existing docs updated; LICENSE, the dated Sentry handoff and the 2026-10-20 archive retained unchanged. Added the complete file-by-file [audit report](docs/DOCUMENTATION_AUDIT.md) and an [archive of the prior mixed-date context](docs/archive/context-2026-10-23-before-doc-audit.md). No useful history deleted; frozen numeric tables and decisions retained. Current context is now a concise handoff rather than contradictory successive work orders. Historical prompts/plans explicitly defer to current source/status and superseding decisions.

**Corrections:** actual text/WhatsApp inputs and transient state; model phrase/status/replacement proposals versus deterministic resolution; trusted API overrides and bounded public-replay checks; accepted-only export, all non-duplicate review marks/no pending/no blocking completeness, provisional downloads; optional tracing and bounded observed geo/delivery evidence; A/B shared authorship, isolated C with owner rewrites, frozen/post-hoc/provisional-ledger/reviewed-CSV/timing-study distinctions; implemented versus dropped/deferred integrations, current CI #18/release and Render overage behavior. Existing product/account/submission gaps remain open. Guide edits change text only; tags/attributes, CSS, JS and behavior are unchanged.

**Fresh verification (no actual .env read/sourced, SENTRY_DSN and inherited LEDGER_DEMO unset, bytecode writes disabled):**
- Bundled Python 3.12.14 unit suite: 116 run, OK, 8 optional-SDK skips, 2.521 s; non-failing ResourceWarning for a test file handle.
- Existing .venv Python 3.15.0 / sentry-sdk 2.72.0 tracing module: 13 tests, all pass in 0.901 s, capturing transport/invented data with no provider request. SDK send_default_pii deprecation warnings observed; dependency/configuration unchanged.
- All seven browser scripts: sheet_display 28/28, demo_mode 23/23, review_safeguards 12/12, session_rerun 10/10, extraction_failures 14/14, csv_safety 4/4, landing 20/20 (111 assertions), each exit 0, no reported console errors. Existing Node 24.19.0, harness Python 3.15.0, Chrome 155.0.8059.85. Initial sandbox Chrome-start failures ran zero assertions; authorized local-browser retries passed. Fixed test ports free afterward; no user process stopped.
- Guide checked at 320/390/1440 px: no page overflow, visible elements outside viewport, console errors or page exceptions. Reader/export/privacy/review-lifetime visuals inspected with no clipping or overlap. Final parser found 2,381 identical tag/attribute events versus HEAD. All 10 current Mermaid blocks parsed/rendered locally with existing Mermaid 11.16.1; no error diagrams/browser errors/external page requests. GitHub rendering not freshly checked.
- A/B/C × rules/model/hybrid with cache-only model readers and temporary output: 9/9 match committed results, 0 fresh model calls. SHA checks 17/17; protected folder inventory 16/16 with no additions/removals. Historical Markdown numeric tables remain byte-identical to HEAD (RESULTS 44 rows, TUNING 22, MEASUREMENT 5).
- Safe .env.example bash/zsh syntax and four evaluation CLI help commands: exit 0. Bounded local-target/anchor/HTML audit found no issues; all 28 Markdown files' 52 fences close. External URLs were classified, not all fetched. Selected current contest/hosting/model claims were separately checked against official sources; the deadline disagreement remains unresolved.
- Baseline hash comparison: all 313 non-documentation files unchanged, no missing files; exactly the 25 documented existing doc changes plus two new Markdown files. Five reference configs unchanged. git diff --check clean, index empty, HEAD still d4b2f76.

**Evidence and limits:** local artifacts in /private/tmp/availazy-docs-audit-rppxdor3 (baseline, suite logs/results, evaluation/check summaries, guide captures, Mermaid SVG/PNGs, link/fence/scope reports). Fresh checks above are distinct from REL-02's earlier fresh-clone/CI/live-Render evidence and CFG-02's owner model/CSV smoke. No new inference, model download, install, account/billing/settings action, commit, push, deploy or publication. No Safari/Firefox/VoiceOver, real-user/time-saving study, full received Sentry payload or post-trial entitlement audit. COR-19, UI-22, API/session/roster/time limitations and owner eligibility/video/disclosure/publication work remain explicit in the audit and current tasks. DOC-12 is complete locally; the owner decides when to commit these docs.

### DOC-13: independent evidence check of the completed documentation audit (2026-10-23)

Owner requested verification of DOC-12 using repository evidence and artifacts, with documentation-only corrections, no staging/commit/push/deploy and no expensive or destructive reruns without checking impact. Read the audit, source contracts and changed documentation; checked actual baseline hashes/Git HEAD, original test logs, evaluation JSONs, render extraction/SVG/PNG artifacts and guide captures/layout report. Earlier read depth and exact original unit/tracing durations cannot be established from retained raw artifacts; the original directory has no raw unit/tracing logs.

**Independently confirmed:** 28 original docs accounted for, 25 changed, three unchanged, two new. All 313 non-doc baseline files byte-identical to both starting hashes and HEAD; no missing baseline files. LICENSE, SENTRY_HANDOFF and the older context archive match baseline and HEAD. Reversing the new archive's link relocation/header, including directory-slash normalization, reconstructs the original context SHA exactly. Numeric table rows in RESULTS/TUNING/MEASUREMENT still equal HEAD (44/22/5). Index empty, HEAD d4b2f76; .env ignored/untracked and unopened. Value-free credential pattern scan of all project docs/new files found no recognizable keys, private-key blocks, credential URLs or real-looking DSNs; this cannot rule out every possible secret encoding.

**Actual checks:** new verbose unit run with existing bundled Python 3.12.14: 116 run, OK, 8 skipped, 2.498 s. Existing .venv SDK tracing module: 13 run, OK, 0.807 s, capturing transport/invented content only. Initial restricted attempts failed on loopback socket permissions (including cascading test-setup failures); authorized retries passed. Non-failing ResourceWarning and SDK deprecation warnings observed. No dependency install or external Sentry/model call. Raw browser logs independently count 111 PASS / 0 FAIL (28/23/12/10/14/4/20), with saved exit-0 records; no fresh browser suite claimed. All nine saved evaluation JSONs match HEAD scoring fields and report zero fresh calls; read-only summary validator exit 0. Fresh protected hash check 17/17, inventory 16/16. Fresh bounded local-reference audit reproduces 590 local references / 0 issues; 151 external links not fetched. Safe example bash/zsh syntax and four evaluation CLI help commands exit 0. All ten current Mermaid sources match saved extraction; nonempty SVG/browser PNGs and passing render report present. Layout report and full-PNG widths substantiate 320/390/1440; phone reader and desktop privacy/lifetime captures inspected. No fresh Mermaid/GitHub or responsive browser run claimed.

**Four documentation corrections:** CLAUDE purpose now states model status/replacement proposals; TESTING says 13 tracing tests discovered with five pass/eight skip without SDK; ARCHITECTURE scopes outside-roster exclusion to automatic matching because overrides are trusted; README combined acceptance explicitly permits unstated time and lists actual eligibility. Changed no guide HTML/diagrams or application behavior. Added DOC-13 verification detail to the existing audit, TASKS and current context; original audit evidence remains dated.

**Artifacts:** /private/tmp/availazy-docs-independent.RxgFw6/ contains new verbose unit/tracing logs and exit records, initial restricted-failure logs, verify_evidence.py, independent-evidence.json, additional-checks.json, fresh checksum/summary/syntax/help logs and fresh link report. Original /private/tmp/availazy-docs-audit-rppxdor3/ artifacts preserved. No new project file; scope remains 25 existing docs updated, three unchanged and two created by DOC-12.

**Still unverified/manual:** complete Sentry received-payload/geo-origin/account/post-trial/export-span audit; VoiceOver/Safari/Firefox and UI-22; independent real-user/timing study; competition eligibility/deadline clarification; recording/upload, disclosures/credits and final publication. Existing task records keep these open. No fresh external rules/pricing, CI or Render requests; prior evidence is not upgraded to a new check. No real messages, .env read, fresh inference, install, account/config/data/deployment change, staging, commit or push. Final whitespace/link/scope checks follow the text corrections.

### DEP-03: demo script v2, about 4–5 minutes (2026-10-23)

The owner asked for a 3–5 minute script, with every fact verified. `docs/demo/script.md` was rewritten:
- 11 shots, about 640 narration words: a landing-page open, the verified two-message live local read, then the hosted replay;
- the m28 cancellation the model missed and the rules caught, Kofi's settled condition, Olu's "rest of this week", three Needs-a-decision items, the m48 model error rejected, the review/export split, the frozen set C score with its causes, CI, and optional Sentry.

It also has a pre-recording checklist, a do-not-say list, fallbacks and a fact-source table.

**Verified on 2026-10-23:**
- **Current code, saved Gemma outputs, Model + rules, no model calls:**
  - 50 messages (m12 a repeat), 67 suggestions, 10 Needs-a-decision items.
  - m03 resolves to Mon 15:00–20:00 and Wed 13:00–17:00.
  - m28's Thursday cancellation is `added_by_rules`; a Model-only replay leaves Maria's Thu 09:00–12:00 on the sheet.
  - Kofi m13 → m29 conditional → available, with m29 `cue_replacement`.
  - m49 marks Olu Wed 11 – Sun 15 unavailable, removing Thu 17:00–20:00 and Sat 09:00–12:00.
  - m26 is outside the week; m41 is ambiguous.
  - m48 is filed under Maria; rejecting it restores Tue 09:00–12:00 available.
  - With m02/m28 accepted and reviewed and m48 rejected, the export is provisional and Maria's Tue and Fri rows are `confirmed`, with no Thursday.
  - "Accept all suggestions without warnings" would accept 39 of 67 on a fresh run.
- **UI labels** from `ui/index.html` and `ui/home.html`.
- **Replay:** live `/app` returned 200 and `/api/status` reported demo mode.
- **CI:** run #19 on `d322342` succeeded (GitHub API).
- **Set C and Sentry facts:** from `evaluation/RESULTS.md` and the frozen-setC JSON (0.527, 2 of 8 cancellations missed, 17/20), and from `docs/SENTRY_HANDOFF.md` (traces `c26d2afd` with four timeouts, `969d7ee9` with zero errors).

**Corrected while fact-checking:**
- Olu's line: he had no Monday or Tuesday availability.
- The set C explanation: for Gemma + rules the misses were m21 (a correction not replacing) and m13 (wrong-Saturday cancellation), not "two corrections".
- The accept-cancellation line: the provisional sheet already drops Thursday while the cancellation is pending.

**Not done:** no recording, no live full-week model run, no browser walk-through of the replay this time (the UI code behind these moments was last changed before the 2026-10-22 replay checks).

### DEP-03: click-by-click run sheet (2026-10-23)

Added `docs/demo/run-sheet.md`: the setup commands, six tabs with exact links, the Ana/Ben input, and three takes (A: shots 1–2, B: 3–9, C: 10–11). Each take is a table with video time, click/type and narration, followed by the iMovie steps.

**Labels and links checked against source:**
- `ui/index.html`: the page layout (messages on the left; Needs a decision, chart, sheet, Changes over time and export in the right panel) and button names.
- `ui/app.js`:
  - the progress texts ("Replayed … from saved outputs", "Accepted … suggestions that had no warnings");
  - the review-state line;
  - issue links to message rows;
  - the "Changes over time" filter, `cancelled|condition|replaced|now`.
- `evaluation/RESULTS.md` headings; GitHub run #20 on `2ada0d9` succeeded.

**Corrected in `script.md` shot 6:** Kofi's first conditional answer (m13) is not listed under Changes over time; that list shows only changes. The shot now finds m13 and m29 on their message cards.

No recording made; no browser walk-through in this step.

### DEP-03: YouTube upload kit (2026-10-23)
The owner has recorded the demo video (owner's report; the video itself was not reviewed here). Added:
- [docs/demo/youtube.md](docs/demo/youtube.md): three title options, a ready-to-paste description (3,645 characters, no `<` or `>`), chapters that follow the run sheet's times, upload settings and a fact-source table.
- [docs/demo/thumbnail.png](docs/demo/thumbnail.png) (1280 × 720, about 128 KB), rendered with local headless Chrome from [docs/demo/thumbnail.html](docs/demo/thumbnail.html). Its text is the fictional m02/m28 messages exactly as written in `fixtures/riverside_week.txt` and `ui/home.html`, plus Maria's post-review rows from the run sheet.

**Checks:**
- Every quoted phrase was found in `fixtures/riverside_week.txt`.
- Set C figures match `evaluation/RESULTS.md`.
- The CI triggers match `.github/workflows/tests.yml`.
- The replay wake time matches the `ui/home.html` fine print.

**Not checked:**
- The chapter times against the actual edited video; the owner must adjust them.
- Whether YouTube accepts the upload.

Nothing was uploaded or published.

### DEP-03: demo video uploaded (2026-10-23)
- **Video:** https://www.youtube.com/watch?v=Qlq_kEsDr4g (the owner uploaded it).
- **Checked in the built-in browser:**
  - The title matches option 1 in `docs/demo/youtube.md`.
  - The duration is 348 s (5:48), longer than the run sheet's plan of about 4:15.
  - The custom thumbnail is served (`maxresdefault.jpg`, 1280×720).
  - The description is the prepared text, minus the CHAPTERS and "What you'll see" blocks, so it has no timestamps that could be wrong.
- **Not checked:** the video's content (not watched) and its visibility setting.
- `docs/demo/post-draft.md` now embeds the video; owner note 1 was updated. DEP-03 is marked done in TASKS.
- **Remaining:** REL-05 (credits/disclosure, then publish) and REL-04 (eligibility).
