# Availability Ledger: project context (main handoff)

**Read this first, then [CLAUDE.md](CLAUDE.md).** Written 2026-10-21, about 11:10–11:30 IST (Asia/Kolkata), by the Claude **project-lead (planning) session** before a context compaction. The previous version is preserved in [docs/archive/context-2026-10-20.md](docs/archive/context-2026-10-20.md): it is outdated in places but holds extra detail.

**Evidence labels used below:**
- **[V]** verified in this pass (command output or file inspection).
- **[R]** read from repository files or docs, not re-run in this pass.
- **[C]** from the owner conversation only, not verifiable in the repo.
- **[H]** historical: true when recorded, not re-checked.

If source code or a fresh check contradicts this file, trust the source and fix this file.

---

## A. Project identity and purpose

- **Name:** Availability Ledger. Repository: public [github.com/bipul724/availability-ledger](https://github.com/bipul724/availability-ledger) (GitHub API, 2026-10-20: public, default branch `main`) [H]. Licence: MIT ([LICENSE](LICENSE), owner decision 2026-10-21) [V].
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
| Front end | `ui/index.html`, `ui/app.js`, `ui/style.css`; vanilla, no CDN | [R] |
| Model runtime | Ollama **0.40.6** (Homebrew; installed 2026-10-20 with owner approval); URL fixed in `ledger/model.py` as `OLLAMA = "http://127.0.0.1:11434"` | [V] |
| Default model | `DEFAULT_MODEL = "gemma4:e2b-it-qat"` (Apache 2.0; 4.3 GB download; about 1.56–1.59 GB reported by Ollama when loaded); `PROMPT_VERSION = 3` | [V] constants; [H] sizes |
| Installed models (11:10 IST) | Only the `gemma4` manifest is in `~/.ollama/models`. `qwen3.5:4b-q4_K_M` (used for A/B comparisons) **is no longer installed**; its cached outputs remain in `evaluation/runs/` | [V] |
| Ollama server | Answering on 127.0.0.1:11434 at about 11:10 IST | [V] |
| Browser checks | `tests/browser/*.mjs` (optional): need **Node 22+** (this Mac: v22.11.0) and local Chrome (`CHROME=` overrides); install nothing | [V] node; [R] harness |
| CI | `.github/workflows/tests.yml`: unit tests on push/PR to `main`, ubuntu-latest, Python 3.12, `permissions: contents: read`, no secrets. First run **"tests #1" on `56e38bd` passed in 9 s** (owner screenshot). Later runs not observed | [V] file; [C] run |
| Hardware | Apple M2, **8 GB RAM**, macOS 26.6.2; memory pressure is a real constraint | [H] 2026-10-20 |
| Environment variables | **None for local use.** The local app reads no env vars and loads no `.env` ([.env.example](.env.example) says so). The hosted replay reads `LEDGER_DEMO=1` and `PORT` (DEP-02). The browser harness reads `CHROME` | [R] |
| Hosting | **None.** No deployment, no public URL | [R] |

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

Contracts: [docs/API.md](docs/API.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/specs/final-export.md](docs/specs/final-export.md). No auth, database, migrations or telemetry.

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
| Sponsor integrations for this submission: Actions automation (INT-11), Render replay (DEP-02), Sentry tracing (INT-03), ElevenLabs narration (INT-04) | PLANNED, NOT IMPLEMENTED (D-33, 2026-10-21; each has a dated gate) | [briefs](docs/prompts/d33-integrations.md) |
| Other sponsor integrations (.tech, Entire, Copilot coding agent, R-CLI) | PLANNED, NOT IMPLEMENTED; deferred (D-23) | — |

## F. Decisions (canonical: [docs/DECISIONS.md](docs/DECISIONS.md))

Key recent decisions:
- **D-23:** the Week 3 entry targeted **overall + Gemma**, with Actions CI as the only addition. **Overridden in part by D-33** (owner, 2026-10-21): also Copilot (via Actions), Render, Sentry and ElevenLabs, each dropped if it misses its gate.
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

There are no secrets; the only environment variables are the replay's `LEDGER_DEMO` and `PORT` (DEP-02). The only external runtime dependency is local Ollama; GitHub Actions runs on GitHub's free hosted runners. No deployment, nothing to migrate.

Local run: `python3 server.py` → http://127.0.0.1:8765. Use "Rules only" without Ollama; the model readers need `ollama serve` and `gemma4:e2b-it-qat`.

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

## L. Immediate next action (updated 2026-10-21, about 13:00 IST)

D-31 and COR-18 are reviewed, accepted and committed (`13e5527`). The owner chose to add four categories (D-33).

1. The owner gives the coding agent brief 1 (INT-11) from [docs/prompts/d33-integrations.md](docs/prompts/d33-integrations.md). The lead reviews the report the same way as D-31: tests, protected paths, then the diff. Then briefs 2 and 3, one at a time, each by its D-33 gate.
2. Meanwhile, the lead writes the DEP-03 demo script with ElevenLabs narration text, then the REL-05 post draft.
3. The owner does the account steps (Render, Sentry, ElevenLabs offer) and never pastes keys into chat.

If the agent hasn't reported, ask the owner for its status rather than inspecting half-finished files as if they were final.
