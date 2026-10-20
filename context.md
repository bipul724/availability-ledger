# Context hand-off

Short summary for a new session. Details live in the linked documents; this file must stay short.

**What and why.** Availability Ledger: a local tool that turns a week of dated volunteer messages into reviewed availability records (not shift assignments) for a volunteer coordinator. A local open model (Gemma 4 E2B via Ollama) copies phrases; Python resolves dates, checks evidence, keeps per-person per-day history, and counts. Goal: fewer silent missed cancellations and less retyping, with messages staying on the coordinator's computer.

**Current objective.** Make the prototype submission-ready for the DEV Hacktoberfest Week 3 challenge without spending money, and keep the evaluation honest. Deadline sources disagree: rules page 26 Oct 12:29 PM IST, DEV API 25 Oct 12:29 PM IST; plan for the earlier ([TASKS.md](TASKS.md#release-blockers)).

**Verified state (2026-10-20).** 21 unit tests pass. The local app runs (`python3 server.py`), the fictional demo works with Rules only, and keyboard review was checked in headless Chrome. Duplicate collapse, day-modifier restoration, "4 onwards" and same-message "the same" were added that day; their held-out effects are post-hoc and mixed (see [PROGRESS.md](PROGRESS.md#evaluation-status)). No licence, no git repository, no hosting, no telemetry, no environment variables.

**Key files and commands.** `ledger/core.py`, `ledger/resolve.py`, `ledger/model.py`, `server.py`, `ui/app.js`, `tests/test_ledger.py`, `evaluation/run.py`. Commands in [CLAUDE.md](CLAUDE.md#commands-verified-2026-10-20).

**Accepted decisions.** Local inference; Gemma default; model copies, code decides; model + rules cross-check; evidence gate; never guess; stdlib only; ₹0 budget. See [docs/DECISIONS.md](docs/DECISIONS.md).

**Limitations and open questions.** Export is a record log that cannot be replayed into the final sheet, and the scorer mis-scores corrections; the sheet includes pending suggestions; a real quote with invented day/time words is applied provisionally; review is lost on reload; model failures are silent; timezone unused; human time saved unmeasured (protocol revised, not run); all data fictional; problem evidence is one anecdotal post. Open: licence, eligibility of `bipulchamoli.tech` for the .tech category, whether coordinators want this.

**Budget and privacy.** ₹0 extra spending; free tiers or credits only; no auto-renew or paid fallbacks; optional features off by default and degrade gracefully. Messages stay local; any off-device feature must disclose it.

**Integrations.** Gemma: implemented (the only one). Render, Sentry, ElevenLabs: not implemented. Copilot, Entire: no evidence of development use. .tech: unverified; the domain would point at free hosting, not host anything itself ([TASKS.md](TASKS.md#optional-sponsor-integrations)).

**Next three tasks.**
1. COR-01 + EVAL-06: a confirmed final-sheet export from accepted records only (pending and unresolved items marked, corrections replayed; unreviewed messages keep the week provisional), and `score_final.py` scoring final-sheet CSVs from both timing conditions. Spec: [docs/specs/final-export.md](docs/specs/final-export.md).
2. COR-03 + COR-10: visible extraction failures; unsupported day/time words kept off the sheet until reviewed.
3. COR-02: neutralise spreadsheet formulas in exported cells.

(REL-03, documentation and evaluation labels, was done on 2026-10-20. The timing study, EVAL-02, comes after task 1.)

(Owner actions in parallel: REL-01 licence, REL-02 git, REL-04 eligibility.)

**Resume from here.** Read [CLAUDE.md](CLAUDE.md), then [PROGRESS.md](PROGRESS.md) and [TASKS.md](TASKS.md). Run `python3 -m unittest discover -s tests` to confirm 21 passing before changing anything, then start with the first open task above.
