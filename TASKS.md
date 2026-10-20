# Tasks

Backlog derived from the code as inspected on 2026-10-20 and corrected after a review the same day. Every open item below is a gap that still exists in the current source.

- **Priority:** P0 (blocks submission or causes silent wrong output), P1 (important), P2 (nice to have).
- **Status:** todo, in progress, done, blocked, needs decision.
- **Type:** `impl` (code or docs work in this repo) or `external` (depends on a person, account or service outside the repo; code cannot finish it).
- Requirement IDs (FR-, PRIV-, COST-, AC-…) are in [docs/PRD.md](docs/PRD.md); decision IDs (D-…) in [docs/DECISIONS.md](docs/DECISIONS.md).

Update this file when a task changes status, and record the change in [PROGRESS.md](PROGRESS.md).

## Order of work

1. Final export and scoring: **COR-01**, **EVAL-06**.
2. Expose failures and unsupported suggestions: **COR-03**, **COR-10**.
3. Protect CSV output: **COR-02**.
4. Correct documentation and evaluation labels: **REL-03** (done 2026-10-20).
5. Run the timing study: **EVAL-02** (after 1 is done).

Owner actions can run in parallel: REL-01, REL-02, REL-04.

## Release blockers

Challenge timing (re-check before submitting). Two official sources disagree:
- The contest rules page (https://dev.to/page/hacktoberfest-week3-2026-10-19-contest-rules, read 2026-10-20) says the contest "begins on October 19, 2026 at 9:00 AM PDT and ends on October 25, 2026 at 11:59 PM PDT", which is **26 October 2026, 12:29 PM IST**.
- The DEV challenges API (via DevRelay `get_challenges`, read 2026-10-20) gives `ends_at: 2026-10-25T06:59:00.000Z`, which is **25 October 2026, 12:29 PM IST**, one day earlier, while its text says "October 25: Submissions due at 11:59 PM PDT".

Plan for the earlier time unless DEV confirms otherwise. The rules also require "A brand-new project created and completed during the Entry Period" and "a link to or embed of the project's code"; the challenge page asks for commits after the deadline to be noted in the README and for prior work to be credited.

| ID | Pri | Status | Type | Outcome | Acceptance criteria | Depends on | Links |
|---|---|---|---|---|---|---|---|
| REL-01 | P0 | needs decision | external | Owner chooses a licence | A `LICENSE` file exists and README states it; or README states "no licence granted" deliberately | — | Q5 in PRD |
| REL-02 | P0 | todo | impl | Version control | `git init`, `.gitignore` excluding `__pycache__/`, any `.env` and any pilot data folder; first commit; public repository if submitting | REL-01 for public release | — |
| REL-03 | P0 | done (2026-10-20) | impl | Evaluation notes match the artifacts | RESULTS.md: extraction vs ledger scopes labelled; effort table tied to its snapshot with frozen values shown; fresh-call vs cache-replay memory evidence separated; swap traffic vs occupied swap separated; post-hoc 2026-10-20 section added. TUNING.md: modifier row updated, new post-hoc rows. MEASUREMENT.md: protocol revised. Historical figures unchanged | — | D-10, D-14–D-16 |
| REL-04 | P0 | todo | external | Confirm challenge facts | Owner confirms the deadline to plan for, that the project was created inside the entry period, and which categories to enter; PROGRESS.md records the answers | — | — |
| REL-05 | P1 | todo | impl | DEV submission post drafted (not published) | Draft explains the open-model design, the fictional evaluation and its limits, credits prior work, uses the required tag; says time saved is unmeasured unless EVAL-02 is done; owner publishes it | REL-01–REL-04 | — |

## Core correctness

| ID | Pri | Status | Type | Outcome | Acceptance criteria | Depends on | Links |
|---|---|---|---|---|---|---|---|
| COR-01 | P0 | todo | impl | **Confirmed final-sheet export** (in addition to the record log) | (a) Built only from **accepted** and reviewer-added records, replayed with the same ledger rules as the app, including `replaces_earlier`. (b) A pending or rejected suggestion never adds or removes availability in this export. (c) A cell (person, day) is marked `needs_review` when a pending suggestion (in particular a pending cancellation over an accepted offer), a blocking issue, or an unreviewed message's claim touches it. **When an unreviewed message's scope cannot be established** (no suggestions, all dropped, unresolved person or day), the whole export stays provisional until that message is explicitly marked reviewed. Extraction finishing, or every suggestion being decided, never counts as human review. (d) Conditional segments export as `conditional` with their condition, never as `available`. (e) The file says in a header row or name whether it is complete or provisional. (f) Tests with invented messages cover a pending cancellation, an accepted correction, a conditional, and an unreviewed message. (g) With the set A reference claims accepted it reproduces `expected_sheet`. The current `ledger.sheet` includes pending suggestions and must **not** be exported as-is | — | FR-16, AC-01, D-07; spec [docs/specs/final-export.md](docs/specs/final-export.md) |
| COR-10 | P0 | todo | impl | Unsupported day/time words stay off the sheet until reviewed | A suggestion whose quote is found but whose day or time words are not in the message (flag `phrase_not_in_message`) does not count on the sheet, chart or confirmed export until accepted, and is shown as needing review. Test: message "Happy to help" with proposed "Tuesday" / "2-4" leaves the sheet empty while pending. Re-run the cached evaluation and report changes as post-hoc | — | FR-05, FR-20, D-06 |
| COR-03 | P0 | todo | impl | Extraction failures are visible | When `/api/suggest` returns `json_ok: false` or errors, the message shows a warning instead of "No availability found" (model only) or only rules-added cancellations (hybrid); the run continues with the next message and reports a failure count | — | FR-18, AC-02 |
| COR-02 | P1 | todo | impl | CSV safe to open in spreadsheets | In both exports, cells beginning with `=`, `+`, `-`, `@`, tab or carriage return are neutralised (e.g. prefixed with `'`); a unit-tested helper or a documented browser check | COR-01 | D-07 |
| COR-04 | P1 | todo | impl | Review work survives reloads and re-runs | Save/load a session file (messages, claims, reviews, week); re-running suggestions keeps decisions for unchanged messages | — | FR-17, AC-03, D-12 |
| COR-06 | P1 | todo | impl | Roster limit is visible | Pasting more than 20 names shows a warning naming the dropped people (today they are silently cut) | — | FR-02 |
| COR-07 | P1 | todo | impl | Cancellation wording coverage | Order: **freeze set C (EVAL-01) → implement COR-07 using only new invented dev phrasings, without opening set C → score once (EVAL-07)**. Never tune on set A held-out, set B or set C. Because it is motivated by the known set B "scratch" failure, any set A or set B improvement it causes is **post-hoc**; only the set C score counts as independent | EVAL-01 (frozen, unscored) | D-05, D-20 |
| COR-05 | P2 | needs decision | impl | Timezone is either used or removed | Either messages are converted from a stated source timezone, or the field is removed/relabelled as "label only" in UI and docs | Owner decision | FR-19, Q4 |
| COR-08 | P2 | todo | impl | Coordinator names configurable in the UI | The page can send `coordinators` (today only senders containing "coordinator" are recognised) | — | D-06 |
| COR-09 | P2 | todo | impl | Duplicate after an intervening change | Decide and test what a re-sent identical message means after a cancellation in between (today: "repeated", no re-apply) | — | D-14 |

Verified as working on 2026-10-20 (no task needed): duplicate collapse (FR-13), day-modifier restoration, "4 onwards" and same-message "the same", one-day corrections preserving other days, similar-name flags, unique-prefix name resolution. See [PROGRESS.md](PROGRESS.md).

## User interface

| ID | Pri | Status | Type | Outcome | Acceptance criteria | Depends on | Links |
|---|---|---|---|---|---|---|---|
| UI-01 | P1 | todo | impl | Sheet fits its panel | No horizontal overflow of the availability sheet at 1400 px and 390 px widths (overflow observed at 1400 px on 2026-10-20) | — | USE-01 |
| UI-02 | P1 | todo | impl | Accessibility pass | Keyboard focus order, labels and contrast checked in light and dark mode; findings recorded | — | USE-04 |
| UI-05 | P1 | todo | impl | Provisional sheet is obvious | The sheet and chart visibly distinguish pending from accepted availability, so a reader cannot mistake the provisional sheet for a confirmed one | COR-01 | D-13 |
| UI-03 | P2 | todo | impl | Cancel a long run | A Stop button ends the per-message loop and keeps what was read | COR-03 | — |
| UI-04 | P2 | todo | impl | Show model timing | Show per-run model time and failures from `stats` (already returned, unused) | COR-03 | — |

## Evaluation and validation

| ID | Pri | Status | Type | Outcome | Acceptance criteria | Depends on | Links |
|---|---|---|---|---|---|---|---|
| EVAL-06 | P0 | todo | impl | One scoring contract: confirmed final-sheet CSVs | New `evaluation/score_final.py` scores final-sheet CSVs from **both** timing conditions (the app's confirmed export and a manual template in the same format). It refuses provisional files unless explicitly allowed, and then labels the report provisional. `needs_review` cells count as disagreement and are reported as `unresolved_cells`/`unresolved_slots`, never silently ignored. Malformed files exit non-zero. A final file for "Tuesday 10-12" then "Tuesday 2-4 instead" scores 14:00–16:00 only. `score_csv.py` stays for record logs and is marked unfit for timing | COR-01 | AC-05; spec [docs/specs/final-export.md](docs/specs/final-export.md) |
| EVAL-01 | P0 | todo | impl | Fresh held-out set C, **frozen and not scored** | ≥ 20 new fictional messages with a hand-written reference, both frozen (and committed, once REL-02 exists) before any further behaviour change; nobody working on code opens them; no scoring in this task | — | D-10 |
| EVAL-07 | P0 | todo | impl | Score set C once | After the planned behaviour changes (at least COR-10, and COR-07 if done) land, score all readers on set C once; record the code version scored; copy results to a frozen folder; report both the 2026-10-20 changes and later ones as tested independently only here | EVAL-01, COR-10 | D-10, AC-04 |
| EVAL-02 | P1 | todo | external | Human timing study | Follows the revised [MEASUREMENT.md](evaluation/MEASUREMENT.md): matched workloads (never set A 50 vs set B 20), balanced order across participants, equivalent final outputs, corrected scorer; more than one participant; per-person results reported. Time saved stays unmeasured until done | COR-01, EVAL-06, testers | AC-05 |
| EVAL-03 | P1 | todo | external | Real-world check | 3–5 coordinator conversations, or one consented, anonymised real week processed locally under the pilot-data rule in [CLAUDE.md](CLAUDE.md#rules) | coordinators | PRD §12 |
| EVAL-04 | P2 | todo | external | Independent reference review | Someone other than the fixture author checks one reference file; disagreements recorded | a reviewer | D-10 |
| EVAL-05 | P2 | todo | impl | Re-measure speed and memory | Fresh `--refresh` Gemma runs on set A with memory sampling, kept as result JSON. Existing fresh-call evidence covers only set A Qwen, set B Gemma and Qwen, and the Gemma dev tuning runs; the Gemma first-load swap growth and "2% free" figures have no file | Ollama running | PERF-01 |

## Optional sponsor integrations

No integration other than Gemma is implemented. Each must follow D-17 (opt-in, off by default, no message content in telemetry) and D-18 (free tier or existing credits only, no auto-renew or paid fallback). Category wording was read from the challenge page on 2026-10-20 through a summarising fetch; eligibility is **unverified** until the owner re-checks it.

| ID | Pri | Status | Type | Target | Current state | Outcome / acceptance | Budget note |
|---|---|---|---|---|---|---|---|
| INT-01 | P1 | todo | impl | Gemma ("Use Gemma … in building your project") | **Implemented:** default model; evaluated | Submission post describes the Gemma role with fictional examples | Local, free |
| INT-02 | P2 | needs decision | impl + external | Render ("AI runtime, … host an agent's front end") | Nothing deployed | Render could host the app in replay mode (DEP-02) on a free plan; must not imply Gemma runs there | Free plan only; no card-backed upgrades |
| INT-03 | P2 | needs decision | impl | Sentry Agent Tracing ("show how it performs (latency, tokens, cost)", traces in the write-up) | Not implemented; the code has no telemetry | Opt-in tracing of timings and token counts only, no message text; needs a decision on breaking D-11 (SDK) or using plain HTTP | Free tier only; tracing stops when quota ends |
| INT-04 | P2 | todo | external | ElevenLabs demo narration ("generate narration for your demo") | Not done | A narrated demo video using a fictional script; no code change | Free tier/credits only |
| INT-05 | P2 | needs decision | impl | ElevenLabs voice-note transcription feeding review | Not implemented | Opt-in upload; explicit "audio leaves this device and is sent to ElevenLabs" notice; transcript goes through the normal review; local workflow unaffected when disabled | Free tier/credits only; disables itself when exhausted |
| INT-06 | P2 | needs decision | external | GitHub Copilot (coding agent, CLI, app, Actions or PR review) | No evidence in the repository that Copilot was used to develop it | Enter only with evidence of real development use (for example Copilot PR reviews or agent sessions on this repo); describe honestly | Free plan only |
| INT-07 | P2 | needs decision | external | Entire ("Share the agent sessions behind your project") | No evidence of Entire use | Enter only with real agent sessions from this project's development, with secrets and private data removed | Free |
| INT-08 | P2 | blocked | external | .tech domain ("a .tech domain you claimed through Hacktoberfest", project live on it) | `bipulchamoli.tech` is owned; whether it was claimed through the Hacktoberfest offer is **unverified**; nothing points at a hosted app | Owner confirms acquisition route; then the domain is pointed at the hosting from DEP-02 (the domain is an address, not hosting) | Page says it "renews at $29.99 a year": auto-renew must be off (COST-02) |

## Deployment and submission

| ID | Pri | Status | Type | Outcome | Acceptance criteria | Depends on | Links |
|---|---|---|---|---|---|---|---|
| DEP-01 | P1 | done | impl | Local run documented | README quickstart works: `python3 server.py`, demo, Rules only (checked 2026-10-20) | — | — |
| DEP-02 | P2 | needs decision | impl | Replay-mode hosted demo | A `replay` reader serving `evaluation/runs/` outputs for the fictional fixtures only; page banner "replaying saved model outputs; no model runs here"; hosted on a free plan (for example Render), optionally reached via `bipulchamoli.tech`; stops rather than charges | REL-02, owner chooses host | D-19 |
| DEP-03 | P1 | todo | impl | Demo recording | Short screen recording of the local app on the fictional demo (keyboard review, sheet, export) | — | — |
