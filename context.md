# Availability Ledger: project context (main handoff)

**Final local release review (REL-07, 2026-10-23; read first):** the release working tree on top of `a4bebb7` was reviewed and verified locally: unit 116 OK (8 skipped), all seven browser suites (28, 23, 12, 10, 14, 4, 20), protected checksums 17/17 and inventory OK, cache-only re-score 9/9 matching with 0 fresh calls, `.env.example` syntax and `git diff --check` clean. One material issue fixed: `.env.example` had a real-looking Sentry DSN as its value (never committed); restored to empty. The demo script's live opening now uses the verified two-message Ana/Ben Model-only flow, with saved-output replay for everything else. Still uncommitted: owner commits and pushes with the commands from this review, optionally rotates the Sentry key, then the post-push REL-02 check (pushed commit, fresh clone, CI, Render). Details: PROGRESS REL-07, TASKS REL-07.

**Local live-model check passed (CFG-02, 2026-10-23):** the owner completed the two-message Model-only Chrome workflow at 127.0.0.1:8780/app with gemma4:e2b-it-qat. Screenshots showed correct suggestions and source quotes. Agent directly checked both supplied CSVs: accepted/unreviewed export provisional with m01 m02 unreviewed, zero pending/blocking issues and needs_review cells; explicit message review produced complete, no unreviewed/pending/blocking issues, Ana on 10 Nov 2026 09:00–12:00 and Ben on 12 Nov 13:00–15:00, both confirmed. The earlier terminal attempt stopped at acceptance and is not a completed checker pass. No additional model calls or .env read by agent. This supersedes older live-inference-pending notes below and clears DEP-03's short dry-run prerequisite; full-week/hybrid inference was not tested. Next: owner review/commit/push release changes, verify the new CI/Render revision (REL-02), then record the demo and finish the post. Details and external evidence paths are in PROGRESS.

**Local configuration files (CFG-01, 2026-10-22):** ignored owner-only .env created, with a matching usable .env.example template: local mode and tracing off by default. server.py does not auto-load .env; README Configuration documents the explicit subshell export/start command. PORT remains hosted-replay-only; local port is the server argument. No credentials added, runtime code changed or services started.

**Release state (2026-10-22, release-preparation session; read first):** `main` = `origin/main` = `a4bebb7`, and the work labelled below as BRAND-01, UI-09 to UI-21 and DOC-09 to DOC-11 is **committed** in it. GitHub Actions "tests #17" on `a4bebb7` passed all three jobs; a fresh clone passed 116 unit tests (8 skipped) and every protected checksum; the public Render site served UI files byte-identical to `a4bebb7` (`/`, `/app`, `/docs`, the 404 page, CSS and JS). **In the working tree only (not committed, not deployed):** UI-11 accurate privacy wording, UI-12 hosted replay link to `/app`, UI-18 landing fix at 320 px, the UI-02 accessibility pass with an app skip link, the updated demo script (DEP-03), the submission-post draft [docs/demo/post-draft.md](docs/demo/post-draft.md) (REL-05) and these docs. New proposals, not implemented: COR-19 (Rules only reads "if it isn't raining" as unavailable) and UI-22 (screen-reader follow-ups). Live model inference was not re-checked that day (Ollama not running); superseded by the 2026-10-23 CFG-02 owner check above. Deadline sources still conflict (Oct 25 12:29 IST by the event API vs Oct 26 12:29 IST by the written rules); plan for the earlier. Owner steps: review and commit, push, confirm CI and Render, record the demo, finish and publish the post (REL-04/REL-05/DEP-03). See PROGRESS for the full record.

**Release review follow-up (2026-10-22):** independent review found no material issue in UI-11/UI-12/UI-18 or the app skip link; the changed landing/guide suite passed 20/20, including element bounds at 320px. Before recording/publishing, REL-05/DEP-03 copy still needs the no-blocking-issues completeness gate, and the post’s specific Sentry geo-origin/filtering claim must be bounded to observed evidence. COR-19 was reproduced offline with invented phrases; it remains a separate proposed fix. Live-model inference was then unverified; the short two-message check passed on 2026-10-23 (CFG-02, above). See PROGRESS.

**Owner-selected public identity (2026-10-22):** **Availazy — Local AI for Coordinators Who Have Better Things to Do**. **Applied 2026-10-22 (BRAND-01, committed by `a4bebb7`):** the landing page, app, guide, 404 page, startup lines, README and demo script say Availazy; the landing hero and README carry the exact headline. Repository, Render, Sentry and code identifiers keep `availability-ledger`, and historical records keep the old name. Brief: [docs/prompts/availazy-branding.md](docs/prompts/availazy-branding.md).

**Current Sentry handoff (2026-10-22; owner evidence through 00:37 IST):** read [docs/SENTRY_HANDOFF.md](docs/SENTRY_HANDOFF.md) for the complete setup, run chronology, SDK review correction, timeout/log findings, privacy verification, billing evidence, cleanup and open checks. Real delivery and a useful finding are verified: four 300 s timeouts in c26d2afd, followed by successful trace 969d7ee9 (1.42 min, 49 calls, 0 errors). A separate one-message trace bc88af7a shows filtered geo values on inspected chat/parent attributes and no content in the chat Input/Output tabs; this is not a complete payload audit. Public Developer Free / 1 user / 5M spans is verified; actual account remains Business Trial with no payment method, and post-trial Agents entitlement is unknown. Cleanup is owner-confirmed, not process-inspected. **INT-03 remains in progress** with scoped open checks; no further inference or billing clicks needed for completed findings. PROGRESS preserves the dated chronology. The morning handoff below is historical and must not override this current summary.

**Landing page (UI-09, 2026-10-22, committed):** `/` now serves a landing page (`ui/home.html`, `home.css`, `home.js`) and the review app, including the hosted replay, moved to `/app` ([D-34](docs/DECISIONS.md#d-34-landing-page-at--review-app-at-app-ui-09)). The live Render site changes only after the owner pushes and Render redeploys. Link the replay as `/app` in the demo recording and the post. Every figure on the page is traced in [PROGRESS](PROGRESS.md#ui-09-landing-page-at--review-app-at-app-2026-10-22).

**Colour theme (UI-13, 2026-10-22, committed):** the owner-approved Forest & Parchment palette ([D-35](docs/DECISIONS.md#d-35-forest--parchment-colour-palette-ui-13)) is applied to the landing page, app, guide and 404 (CSS custom properties in `home.css`, `style.css`, `docs.css`; favicons and theme-colour metadata). Colour only: copy, layout, behaviour and contracts are unchanged. Forest green is the action/brand colour; red is reserved for cancellations, rejects and errors. **Light only (UI-14, [D-36](docs/DECISIONS.md#d-36-light-appearance-only-ui-14)):** the dark-preference overrides were removed, so every page shows the light palette whatever the OS or browser prefers; there is no theme switcher.

**Navbar divider (UI-15, 2026-10-22, committed):** the shared landing/guide/404 navbar has a persistent 1px sage (`--rule-2`) bottom border before and after scrolling. Chrome desktop/mobile visual checks passed; see PROGRESS.

**Desktop inset (UI-16, 2026-10-22, committed):** the landing page now uses a 1340px frame (including its header/footer), placing the ledger line 149.5px from the left edge at 1455px available width and 100% zoom. Font sizes and phone spacing are unchanged; guide/404 frames remain 1240px. Eight viewport checks and the existing 18 landing browser checks passed; see PROGRESS.

**Section rhythm (UI-17, 2026-10-22, committed):** the landing page now has sage horizontal rules between sections and reduced whitespace (48px per side desktop, 32px phone; hero initial top spacing retained). Hero-to-Problem gap is 97px / 65px including the divider. Existing 18 landing checks passed; the pre-existing 320px overflow was later fixed under UI-18 (working tree, 2026-10-22). See PROGRESS.

**Review app polish (UI-19, 2026-10-22, committed):** `/app` has a compact header with guide navigation, clearer setup/review headings, a wider messages field, organised actions/status, and refined cards/summary panels in the same light Forest & Parchment palette. Review rows adapt to their column width; failed reads remain explicit and use amber summaries. No JavaScript, API, model or export changes. Seven browser suites passed (109 checks), unit suite 116 OK (8 skipped), and 11 app widths from 320–1455px fit without overflow. The screenshot's model connection refusal remains a separate runtime issue; verification used Rules only/saved replay/simulated failures. See PROGRESS.

**Setup card (UI-20, 2026-10-22, committed):** CSS-only refinements to Prepare your week: tagline under the title, settings in one recessed strip, one label style, format hints beside field titles, a solid file-picker button without the gap, and no empty action row in the replay. Behaviour unchanged; seven browser suites and unit tests pass. See PROGRESS.

**Availability sheet card (UI-21, 2026-10-22, committed):** CSS-only: tidier two-column legend, lighter table with zebra rows and row hover, solid edge on accepted times while pending stays dashed. Name column stays 17% because wider names overflow pending times (UI-01). See PROGRESS.

**Read this first, then [CLAUDE.md](CLAUDE.md).** Written 2026-10-21, about 11:10–11:30 IST (Asia/Kolkata), by the Claude **project-lead (planning) session** before a context compaction. The previous version is preserved in [docs/archive/context-2026-10-20.md](docs/archive/context-2026-10-20.md): it is outdated in places but holds extra detail.

**Evidence labels used below:**
- **[V]** verified in this pass (command output or file inspection).
- **[R]** read from repository files or docs, not re-run in this pass.
- **[C]** from the owner conversation only, not verifiable in the repo.
- **[H]** historical: true when recorded, not re-checked.

If source code or a fresh check contradicts this file, trust the source and fix this file.

---

## A. Project identity and purpose

- **Name:** Availazy (formerly Availability Ledger; BRAND-01). Repository: public [github.com/bipul724/availability-ledger](https://github.com/bipul724/availability-ledger) (GitHub API, 2026-10-20: public, default branch `main`) [H]. Licence: MIT ([LICENSE](LICENSE), owner decision 2026-10-21) [V].
- **Purpose [R]:** a local, single-user review tool for a volunteer coordinator. The coordinator pastes a week of dated chat messages and a roster (≤ 20 volunteers). The tool suggests **availability** records, each beside its source quote. It keeps per-person, per-day history (offers, corrections, cancellations, conditions) and exports a reconciled **final sheet built from accepted records only**. It records availability, **not shift assignments**.
- **Core design [R]:** a local open model (Gemma 4 E2B through Ollama) only **copies phrases**. Ordinary Python decides people, dates, times, evidence, history and counts. A person reviews, and explicitly marks each message reviewed.
- **Why it exists [C]:** built for the DEV **Hacktoberfest Open-Source AI Challenge, Week 3, "Slow and Steady"**: open-source AI at the core, a project that "rewards laziness". The owner chose this problem after an idea search in this session. Owner-supplied problem evidence: two Reddit threads, [r/nonprofit](https://www.reddit.com/r/nonprofit/comments/1apjpbc/volunteer_scheduling_help/) and [r/volunteer](https://www.reddit.com/r/volunteer/comments/1b2wrkl/way_of_scheduling_volunteers_where_they_can_pick/). **Neither could be read by any tool in this session** (Reddit is blocked for WebFetch and the browser pane), so problem demand is **unverified**.
- **Non-goals [R]:** shift assignment, contacting volunteers, automated chat ingestion, accounts, collaboration, cloud sync, in-app voice.
- **Hard constraints [C/R]:**
  - ₹0 additional spending.
  - Private messages stay local (only to Ollama on 127.0.0.1).
  - Python standard library only, with vanilla JS/CSS and no external libraries (D-11).
  - Human overrides win.
  - Ambiguities are never guessed.
  - Conditions stay conditional until settled.
- **Who does what [C]:**
  - **Owner** (GitHub `bipul724`) decides scope and commits and pushes **manually**. The owner prefers copy-paste commands in the form `git add <files> && git commit -m "<message>"`.
  - **This Claude session** is the project lead and decision-maker. It plans, makes decisions (DECISIONS.md, D-23 onward) and writes docs. It implements only when the current request explicitly asks.
  - **A separate coding agent session** implements assignments; the owner relays its reports here.
  - **ChatGPT** (a separate service) wrote set C under D-29.

## B. Technology stack and environment

| Item | Value | Evidence |
|---|---|---|
| Language/runtime | Python, standard library only; no `requirements.txt`, `pyproject` or `package.json` | [V] repo tree |
| Python on this Mac | `/opt/homebrew/bin/python3` = **3.15.0**; also `python3.12` (`/Library/Frameworks/Python.framework/Versions/3.12`) | [V] |
| Stated minimum | Python 3.10+ (README); only 3.15 and 3.12 have been run | [R] |
| Server | `http.server.ThreadingHTTPServer`, always `127.0.0.1`, port = first CLI arg (default 8765) | [V] `server.py` |
| Front end | `ui/index.html`, `ui/app.js`, `ui/style.css` (review app at `/app`); landing page `ui/home.*` at `/` (UI-09, D-34); vanilla, no CDN | [R] |
| Model runtime | Ollama **0.40.6** (Homebrew; installed 2026-10-20 with owner approval); URL fixed in `ledger/model.py` as `OLLAMA = "http://127.0.0.1:11434"` | [V] |
| Default model | `DEFAULT_MODEL = "gemma4:e2b-it-qat"` (Apache 2.0; 4.3 GB download; about 1.56–1.59 GB reported by Ollama when loaded); `PROMPT_VERSION = 3` | [V] constants; [H] sizes |
| Installed models (11:10 IST) | Only the `gemma4` manifest is in `~/.ollama/models`. `qwen3.5:4b-q4_K_M` (used for A/B comparisons) **is no longer installed**; its cached outputs remain in `evaluation/runs/` | [V] |
| Ollama server | Answering on 127.0.0.1:11434 at about 11:10 IST | [V] |
| Browser checks | `tests/browser/*.mjs` (optional): need **Node 22+** (this Mac: v22.11.0) and local Chrome (`CHROME=` overrides); install nothing | [V] node; [R] harness |
| CI | `.github/workflows/tests.yml`: unit tests on push/PR to `main`, ubuntu-latest, Python 3.12, `permissions: contents: read`, no secrets. First run **"tests #1" on `56e38bd` passed in 9 s** (owner screenshot). Later runs not observed | [V] file; [C] run |
| Hardware | Apple M2, **8 GB RAM**, macOS 26.6.2; memory pressure is a real constraint | [H] 2026-10-20 |
| Environment variables | **None for local use.** The local app reads no env vars and loads no `.env` ([.env.example](.env.example) says so). The hosted replay reads `LEDGER_DEMO=1` and `PORT` (DEP-02). The browser harness reads `CHROME` | [R] |
| Hosting | Render free web service: read-only fictional replay at https://availability-ledger-replay.onrender.com (landing `/`, app `/app`, guide `/docs`); UI files matched `a4bebb7` on 2026-10-22 | [V] |

Preview tooling, outside the repo [V]: `week 3/.claude/launch.json` attaches the desktop app's browser pane to an **already running** server at `http://127.0.0.1:8765`. History [H]: when the preview tool launched `server.py` itself, the process hung in `getcwd()` (macOS Desktop-folder permission). The fix was to start the server from a shell and attach by URL.

## C. Repository structure (verified tree, 2026-10-21)

| Path | Responsibility |
|---|---|
| `server.py` | Static files plus JSON API; `MAX_VOLUNTEERS = 20` |
| `ledger/messages.py` | Parse pipe-format and WhatsApp exports; message IDs `m01…`; duplicates (same sender + normalised text within 24 h) |
| `ledger/names.py` | Roster matching; similar-name flags; ambiguity, never guessed |
| `ledger/resolve.py` | Day and time phrases → dates and times, using the message timestamp and the selected week (no model) |
| `ledger/core.py` | Claim resolution, evidence gate, quote-day narrowing, ledger history, conflicts, issues (incl. `unanswered_change`, `cue_replacement`, "check the wording"), counts |
| `ledger/model.py` | Ollama call with JSON schema; SYSTEM/EXAMPLES prompt v3 |
| `ledger/rules.py` | Regex baseline reader |
| `ledger/hybrid.py` | Model + rules cross-check (default reader) |
| `ledger/export.py` | Accepted-only final sheet, CSV writer/strict reader, formula neutralising (`_cell`) |
| `ui/` | Browser session, review UI, keyboard, chart and sheet, both exports |
| `tests/test_*.py` | Offline unit tests. `tests/browser/` holds optional headless-Chrome checks and `harness.mjs`. Details: [TESTING.md](TESTING.md) |
| `evaluation/` | `run.py` (score readers), `compare.py`, `fixture.py` (sets A/B/C), `score_final.py` (final-sheet scorer), `score_csv.py` (review-log scorer, **not** for timing), `final_sheet_template.csv` |
| `evaluation/results/` | Current tables; `frozen/` (A/B first scores), `frozen-setC/` (set C single score, read-only), `tuning/` (prompt v1–v3 dev runs) |
| `evaluation/runs/` | Cached model outputs per model/prompt/set, so tables can be re-scored without model calls |
| `fixtures/` | Fictional set A (`riverside_week.txt`, `roster.txt`, `reference.json`), set B (`setB_*`), set C (`setC_*` plus `setC.manifest`), manual template |
| Docs | [README](README.md), [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md), [TASKS](TASKS.md), [PROGRESS](PROGRESS.md), [TESTING](TESTING.md), [docs/](docs/) (PRD, ARCHITECTURE, API, DECISIONS, INTEGRATIONS, COMPETITION, specs, prompts, archive), [evaluation/RESULTS](evaluation/RESULTS.md), [TUNING](evaluation/TUNING.md), [MEASUREMENT](evaluation/MEASUREMENT.md) |

## D. Architecture and data flow (implemented) [R; routes V]

1. The browser loads the page. `GET /api/status` lists installed Ollama models; `GET /api/demo` returns fictional set A.
2. `POST /api/parse`: text, roster and day-first flag → sorted messages with IDs and `duplicate_of`.
3. For each **non-duplicate** message, the browser calls `POST /api/suggest` (reader `hybrid`, `model` or `rules`). The model sees only the planning week, sent time, sender and text. A failure marks only that message with a warning and reading continues (COR-03).
4. Every 5 messages, at the end and after edits: `POST /api/resolve` (whole session plus `reviewed_messages`) returns resolved claims, the provisional ledger and a `confirmed` summary.
5. `POST /api/export` returns the **accepted-only** final-sheet CSV (complete or provisional). The review-log CSV is built in the browser.
6. All state is in browser memory. No database, no persistence; a reload loses work.

Contracts: [docs/API.md](docs/API.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/specs/final-export.md](docs/specs/final-export.md). No auth, database or migrations. Telemetry only as opt-in Sentry tracing (`SENTRY_DSN`, INT-03).

## E. Feature inventory

| Feature | Status | Evidence / limits |
|---|---|---|
| Parsing (pipe + WhatsApp), duplicates collapsed | COMPLETED AND VERIFIED | Unit tests at HEAD (66/66 [V]) |
| Roster matching; similar names flagged; ambiguous names unresolved | IMPLEMENTED, NOT FULLY VERIFIED | Set C m23 "T. Vekar" → unknown; COR-16 change in the working tree, unreviewed (§G) |
| Day/time resolution (relative days, next/this, numeric dates, ranges, periods, "4 onwards", same-message "the same", modifier restoration) | IMPLEMENTED, NOT FULLY VERIFIED | Set C m13 "Sat 21 Nov" → the planning week's Saturday (silent wrong day); COR-13 change in the working tree, unreviewed |
| Readers: rules, model, hybrid (default) | COMPLETED AND VERIFIED (functionally) | Evaluated on A/B/C; accuracy limits in §G and RESULTS |
| Evidence gate (quote/phrase checks, quote-day narrowing, coordinator self-claims dropped) | COMPLETED AND VERIFIED | Tests; D-06 |
| COR-10 "check the wording" flag (no hold) | COMPLETED AND VERIFIED | D-30: a hold was built then reverted (28 held, all correct). Set C: 4 flags, all harmless rewording |
| COR-07a "possible change not applied" warning | COMPLETED AND VERIFIED (behaviour); usefulness unproven | A/B: 13 warnings, all real (post-hoc). Set C: **0** warnings, so it missed C's failures by design |
| Ledger: per-day history, partial corrections, replacements, conflicts, conditions | IMPLEMENTED, NOT FULLY VERIFIED | Set C: replacement cues missing (m20/m21); "definite now" doesn't settle a condition (m19). COR-14/COR-15 changes in the working tree, unreviewed |
| COR-03 visible extraction failures | COMPLETED AND VERIFIED | Browser check 14/14 [H, agent report] |
| COR-02 CSV formula neutralising (both exports) | COMPLETED AND VERIFIED | Unit + browser checks [H] |
| UI-05 / UI-01 / UI-07 provisional display, layout, chart contrast | COMPLETED AND VERIFIED (headless Chrome only) | Safari, Firefox, screen readers and contrast untested (UI-02) |
| COR-01 accepted-only final export, explicit message review; strict scorer (EVAL-06/08) | COMPLETED AND VERIFIED | `tests/test_export.py` |
| COR-11 / COR-12 safe reruns, review scope | COMPLETED AND VERIFIED | Browser rerun check [H] |
| GitHub Actions CI (INT-10) | COMPLETED AND VERIFIED | First run green [C screenshot] |
| Session save/load (COR-04), roster-limit warning (COR-06), coordinator names in UI (COR-08), timezone use (COR-05), stop button (UI-03) | PLANNED, NOT IMPLEMENTED | Deferred (D-23) or P2 |
| Human time saved | UNKNOWN: EVIDENCE INSUFFICIENT | Never measured; see [evaluation/MEASUREMENT.md](evaluation/MEASUREMENT.md) |
| Real-world usefulness / demand | UNKNOWN: EVIDENCE INSUFFICIENT | No coordinator interviews or pilot |
| Sponsor integrations for this submission: Actions automation (INT-11), Render replay (DEP-02), Sentry tracing (INT-03) | INT-11 and DEP-02 done and verified; INT-03 real delivery verified; timeout and privacy follow-up open; ElevenLabs (INT-04) dropped by the owner (D-37, 2026-10-22) | [briefs](docs/prompts/d33-integrations.md) |
| Other sponsor integrations (.tech, Entire, Copilot coding agent, R-CLI) | PLANNED, NOT IMPLEMENTED; deferred (D-23) | — |

## F. Decisions (canonical: [docs/DECISIONS.md](docs/DECISIONS.md))

Key recent decisions:
- **D-23:** the Week 3 entry targeted **overall + Gemma**, with Actions CI as the only addition. **Overridden in part by D-33** (owner, 2026-10-21): also Copilot (via Actions), Render, Sentry and ElevenLabs, each dropped if it misses its gate. **D-37** (owner, 2026-10-22): ElevenLabs dropped.
- **D-32:** COR-15 accepted; cue-only replacements raise a warning (COR-18, done). **D-33:** see above; deadline planning unchanged (25 Oct 12:29 IST).
- **D-24:** set C was frozen outside the repo by hash.
- **D-25:** missed cancellations get a warning first; no vocabulary tuning.
- **D-26:** duplicate-aware scoring.
- **D-27:** documentation economy (TASKS row + one PROGRESS entry per task).
- **D-28:** work that can't bias C may proceed before the freeze.
- **D-29:** C may be written by an isolated AI (ChatGPT was used), with the owner editing at least 5 messages.
- **D-30:** COR-10 is a flag only, not a hold.
- **D-31:** fix C-revealed defects post-hoc (COR-13 to COR-17), and keep set C's first score as the headline.

Earlier, D-01 to D-22 covered local model, Gemma default, Qwen comparison only, model copies and code decides, hybrid default, evidence gate, and so on. **D-13** (holding flagged suggestions) was superseded.

Conversation-only history **[C]**:
- The idea search first recommended "Let It Rot", then "Background Check" (camera-roll home inventory). The owner instead chose to test Availability Ledger.
- A competitor check (2026-10-20) found:
  - **Proximatic:** emailed replies → draft roster, on a Pro plan ($16/mo per organisation), web app.
  - **SignUpGenius:** free with ads.
  - **Google Forms:** free, edit-after-submit.
  - **An n8n template:** form-based.

  Conclusion: the remaining gap is any-channel message history, local processing, quote-linked review and per-day history. **Not unprecedented.**
- The rules baseline was strong on set A, which it was written against, but brittle on unseen wording (set B: 17/35 units).
- Qwen 4B read better but caused heavy swapping on 8 GB, so Gemma E2B stays the default.

## G. Current state at handover (2026-10-21, about 11:15 IST)

- **Git [V]:** branch `main`. `HEAD = origin/main = c5a2e05` ("docs: record set C results, lead review and D-31 fix plan"). A clean copy of HEAD passes **66/66** unit tests on Python 3.15 and 3.12 [V].
- **Working tree [V]: uncommitted coding-agent work on D-31, not yet reported or reviewed.**
  - **Changed during this pass:** `ledger/resolve.py` (COR-13), `ledger/names.py` (COR-16), `ledger/rules.py` (COR-17), `ledger/core.py`, the new `tests/test_d31_fixes.py`, and 12 files in `evaluation/results/` (a re-score in progress).
  - **Tests:** at 11:10 IST, 81 tests ran with 7 failing in the new D-31 tests; **at 11:13 IST all 81 passed** [V].
  - **Protected paths:** fixtures, `frozen/`, `frozen-setC/`, `tuning/`, `runs/` and `ledger/model.py` were unchanged at 11:13 [V].
  - **Treat this as unreviewed until the lead checks the agent's report.**
- **This documentation pass** archived the old context, rewrote this file, added [TESTING.md](TESTING.md), and updated README, TASKS (REL-02, DOC-05) and PROGRESS. It did not touch code.
- **Evaluation headline [V], set C:** independent, scored once at `56e38bd`, frozen in `evaluation/results/frozen-setC/`.

  | Reader | Units right | Final-sheet slot agreement | Missed cancellations |
  |---|---|---|---|
  | Rules | 15/20 | 0.433 | 4/8 |
  | Gemma 4 E2B | 17/20 | 0.403 | 4/8 |
  | Gemma + rules | 17/20 | 0.527 | 2/8 |

  Main lesson: **the model mostly read correctly; the deterministic reconciliation rules caused the bad sheets.** A/B results are post-hoc; their frozen first scores are in [evaluation/RESULTS.md](evaluation/RESULTS.md). Fictional data only; A/B fixtures, rules and references share one author.
- **Set C provenance [V/C]:** written by ChatGPT; the owner rewrote m03, m04, m14, m15 and m21 and aligned duplicate m05. Manifest commit `688c50d`; hashes verified at scoring. A private copy also exists at `~/Documents/availability-setC/` (including `setC_notes.md`, **not** in the repo) [V, file listing only].
- **Deployment:** none. **Runtime:** the app server was not running at 11:10 IST; Ollama was.
- **Latest confirmed milestone:** EVAL-07 (set C scored once), committed and pushed (`deaefed`, `9327e30`, `c5a2e05`).

## H. Outstanding work (canonical: [TASKS.md](TASKS.md))

**Deadline [R]:** the written rules say 25 Oct 11:59 PM PDT (**26 Oct 12:29 IST**), but the DEV event API end_time is **25 Oct 12:29 IST**. Plan for the earlier one. **Internal target: publish by Sat 24 Oct, 21:00 IST.**

Mandatory, in order:
1. **COR-13 to COR-17** (D-31; coding agent, in progress). Acceptance criteria are in the TASKS rows. Verify with the full unit suite, including `tests/test_d31_fixes.py`, then a cache-only re-score of A/B/C labelled **post-hoc**, never written into `frozen*/`. The lead reviews the agent's report before the owner commits.
2. **DEP-03 demo recording.** The lead writes the script; the owner records a local video of a fictional workflow. It must show corrections/cancellations, review uncertainty, explicit review and the final CSV, and must not claim time savings.
3. **REL-05 DEV post draft.** The lead drafts; the owner publishes. Required: tags `devchallenge` and `hf26challenge`, the template sections, an honest set C story, and "time saved unmeasured" unless EVAL-02 is done.
4. **REL-04.** The owner confirms eligibility, that the project started inside the entry window, and the categories (overall + Gemma).
5. **REL-02.** A final release check: a clean clone reproduces, the README matches, CI is green.

Optional: **EVAL-11** set D (about 45 min of owner time) to test the fixes independently; **EVAL-03** coordinator conversations; **EVAL-02** timing pilot (≥ 2 participants). Deferred items are listed in TASKS.

## I. Known bugs and limitations

- **From set C, fixes in the working tree but unreviewed:**
  - m13: an explicit date was mapped into the wrong week.
  - m19: "definite now" leaves a condition conditional.
  - m20/m21: replacements ("change … to", "only … now") not applied.
  - m23: initial + surname → unknown person.
  - The rules reader misses "cancelling" and "I'm out".
- **Design limitations:**
  - COR-07a fires only when no suggestion touched the day.
  - The COR-10 flag compares exact words, so it also fires on harmless rewording.
  - A merged accepted + pending segment shows wholly as pending (UI-06).
  - Point times ("at 9") are unreadable.
  - Failed extraction requests are not retried.
  - The timezone field is unused.
  - A reload loses review work.
- **Performance [H]:** on the 8 GB Mac with other apps open, Gemma runs show memory pressure "warn" or "critical", up to about 4 GB of swap growth on a cold load, a median of about 1.8–3.4 s per message, and about 48 s for a cold load.
- **Security:** local only, with no auth (single user on 127.0.0.1); CSV formulas are neutralised; no secrets or keys in the repo (grep in this pass found none [V]).

## J. Configuration, integrations, deployment

There are no secrets in the repo. Environment variables: the replay's `LEDGER_DEMO` and `PORT` (DEP-02), and `SENTRY_DSN` for opt-in tracing (INT-03; the owner keeps it in their own shell). The only external runtime dependency is local Ollama; GitHub Actions runs on GitHub's free hosted runners. No deployment, nothing to migrate.

Local run: `python3 server.py` → http://127.0.0.1:8765/app (the root is the UI-09 landing page). Use "Rules only" without Ollama; the model readers need `ollama serve` and `gemma4:e2b-it-qat`.

## K. Rules for future sessions

Follow [CLAUDE.md](CLAUDE.md). In particular:
- **Python standard library only.**
- **Never edit** the fixtures, `setC.manifest`, `frozen/`, `frozen-setC/`, `tuning/` or `runs/`.
- **Never change the prompt or `PROMPT_VERSION`** without a prompt task.
- **Never tune on held-out data** (A held-out, B, C). Label post-hoc changes.
- **Report regressions plainly.**
- **The owner commits and pushes**; agents don't.
- **₹0 budget.** No installs, accounts, deploys or publishing without an explicit owner request.
- **Never claim time saved, or integrations that don't exist.**

Lessons learned:
- **Holding flagged suggestions** back from the sheet failed twice (D-13: 15 correct vs 3 wrong; D-30: 28 vs 0). Don't retry it without new evidence.
- **Agent guide drift:** the guide went stale twice and once told agents to commit set C. Update CLAUDE.md whenever the workflow changes.
- **Evaluation runs:** model/hybrid runs make **fresh model calls on cache misses**, even without `--refresh`. Verify cache coverage first.
- **Documentation volume:** keep docs lean (D-27).

**DOC-09 (2026-10-22, uncommitted):** the `/docs` guide now has source-checked diagrams for all eight sections, and Mermaid diagrams were added to README, ARCHITECTURE, API, the final-export spec and TESTING. `docs/DIAGRAMS.md` maps every diagram to its source and tests; keep it in step when code changes. ARCHITECTURE's stale statements (failure warnings, CSV formula protection, 404 page, hosted replay, ElevenLabs) were corrected.

**DOC-10 (2026-10-22, uncommitted):** the six review findings (export inclusion vs completeness, restoring dropped cards, the pending-count source, startup readiness, API payload labels, architecture action and inference arrows) are corrected and checked in source. All 10 Mermaid blocks rendered with an existing local Mermaid 11.16.1; GitHub rendering not checked. Details in PROGRESS and `docs/DIAGRAMS.md`.

**DOC-11 (2026-10-22, uncommitted):** the two residual guide wordings are corrected: Gemma is the default but not the only evaluated model (Qwen results exist), and message-review marks help determine complete/provisional status and which cells need review, never blocking the download.

## L. Immediate next action (updated 2026-10-21, about 13:00 IST)

D-31 and COR-18 are reviewed, accepted and committed (`13e5527`). The owner chose to add four categories (D-33).

1. The owner gives the coding agent brief 1 (INT-11) from [docs/prompts/d33-integrations.md](docs/prompts/d33-integrations.md). The lead reviews the report the same way as D-31: tests, protected paths, then the diff. Then briefs 2 and 3, one at a time, each by its D-33 gate.
2. Meanwhile, the lead writes the DEP-03 demo script (narrated live by the owner or captioned; ElevenLabs dropped, D-37), then the REL-05 post draft.
3. The owner does the account steps (Render, Sentry) and never pastes keys into chat.

If the agent hasn't reported, ask the owner for its status rather than inspecting half-finished files as if they were final.
