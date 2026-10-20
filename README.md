# Availability Ledger

A local review tool for volunteer coordinators who collect availability through ordinary messages. You paste a week of dated chat messages and your volunteer roster; the tool suggests availability records, shows each one beside the message it came from, and keeps a per-person, per-day history of offers, corrections, cancellations and conditions. You review the suggestions, explicitly mark each message reviewed, and export a reconciled final sheet built from accepted records. A separate review log preserves the record trail.

It records **availability** (when people say they can or cannot help), not shift assignments.

**A local open model proposes and ordinary code decides.** The model (Gemma 4 E2B through Ollama) only copies phrases such as "next Tuesday", "after 3" or "if needed". Python code turns them into dates and times, checks each suggestion's words against the message and flags or drops unsupported ones (with one documented gap: a real quote with invented day or time words is only flagged and counts on the provisional sheet), keeps each person's history per day, keeps conditional offers conditional, and does every count. In the core workflow nothing leaves your computer.

Status: validation prototype. Every message, name and organisation in `fixtures/` is **fictional**. No real-coordinator pilot or measured human time saving is recorded. Read [context.md](context.md) and [CLAUDE.md](CLAUDE.md) before changing the project; this working tree includes uncommitted implementation and documentation that committed HEAD does not yet reproduce.

## Example (fictional)

```
2026-11-02 09:41 | Ana Example | I can do Tuesday 2-5. Thursday mornings too
2026-11-04 18:10 | Ana Example | Can't do Thursday after all, sorry
```

With the week of Monday 2026-11-09 selected and the **Rules only** reader (checked on 2026-10-20), the tool suggests Tuesday 10 Nov 14:00–17:00 and Thursday 12 Nov 09:00–12:00 from the first message and Thursday unavailable from the second. The sheet ends with Tuesday 14:00–17:00 only, and **Changes over time** lists "m02 Wed 04 Nov 18:10: Ana Example, Thu 12 06:00-23:00 marked unavailable, cancelled", linked to the message.

## Current capabilities

Implemented (which items are verified, and how, is in [PROGRESS.md](PROGRESS.md#capabilities)):

- Paste text or upload a `.txt`, in `YYYY-MM-DD HH:MM | Sender | text` lines or a WhatsApp export (Android or iOS, month-first or day-first).
- Roster of up to 20 volunteers; similar names are flagged and short names that match several people are left unresolved, never guessed (a short name matching only one person resolves).
- Three readers: **Model + rules cross-check** (default), **Model only**, **Rules only** (no model needed).
- Day and time phrases resolved in code: relative days, "next/this" weekdays, numeric dates, ranges, "after 3", "4 onwards", morning/afternoon/evening, "the same" (within one message). Ambiguous days are shown with their candidates, not guessed.
- Suggestions beside their source message with the quote highlighted; warnings in plain English. Suggestions with neither their quote nor their day/time words in the message are not applied unless you choose "Use it anyway" (a real quote with invented day/time words is only flagged; see Limitations).
- Accept, reject, edit (volunteer, days, times, status, condition), reset or add records; "Accept all suggestions without warnings"; keyboard review (J/K move, A accept, R reject, E edit, Esc leave field).
- Repeated messages (same sender, same text within 24 h) are collapsed and shown as "Same as mXX".
- **Needs a decision** list, half-hourly **People available** chart, **Availability sheet**, **Changes over time**.
- Explicit message review marks and the `M` shortcut; **Accept all and mark reviewed** appears only for eligible pending suggestions with resolved person/day and readable time.
- A confirmed final-sheet CSV (complete or clearly provisional) and a review-log CSV.

## Limitations

- Review work lives only in the browser tab; reloading or a successful re-run replaces it. A re-run that fails (bad week, parse error, no dated messages) keeps the current review unchanged.
- The review-log CSV is an audit trail, not the final sheet, and cannot be replayed into it; use **Export final sheet** for the reconciled result. A message with no suggestions can be marked reviewed only with its button (J/K move between suggestion cards).
- A suggestion whose quote is real but whose day or time words were invented is flagged ("Some words are not in this message") but still counts on the provisional sheet until you reject it.
- The timezone field is stored but not used; timestamps are read as written.
- If the model returns invalid JSON there is no warning: with **Model only** the message shows "No availability found"; with **Model + rules** only the rules' cancellations appear.
- Point times ("at 9") are not read. Names not on the roster are never applied.
- Pending (unreviewed) suggestions already count on the sheet and chart.
- Accuracy figures come from fictional messages only; human time saved has **not** been measured.

Full list: [docs/ARCHITECTURE.md §14](docs/ARCHITECTURE.md#14-known-technical-limitations) and [TASKS.md](TASKS.md).

## Prerequisites

- macOS or Linux with Python 3.10+ (stated requirement; checked on Python 3.15.0 on macOS). Standard library only: nothing to `pip install`.
- A modern browser (checked with Chrome).
- For the model readers only: [Ollama](https://ollama.com) and the `gemma4:e2b-it-qat` model (about 4.3 GB download; about 1.6 GB of memory once loaded, recorded on an 8 GB Mac). **Rules only** needs neither.

## Quickstart

```bash
cd availability-ledger
python3 server.py                 # open http://127.0.0.1:8765 (or: python3 server.py 8780)
```

1. Click **Load fictional demo**.
2. Choose **Reader → Rules only** (works without Ollama) and click **Suggest records**.
3. Review the cards and mark each message reviewed (or use **Accept all and mark reviewed** where offered), then **Export final sheet (CSV)**.

To use the model readers, in another terminal first:

```bash
ollama serve
ollama pull gemma4:e2b-it-qat     # one-time download; only if not already installed
```

The page's **Model** list shows whatever Ollama has installed. If Ollama is not reachable, the page says so and only **Rules only** works.

## Configuration

There are no environment variables and no `.env` loading; [.env.example](.env.example) explains this. Configuration is:

| Setting | Where |
|---|---|
| Port | first argument to `server.py` (default 8765); the host is always 127.0.0.1 |
| Week (a Monday), timezone label, reader, model, day-first WhatsApp dates | the page |
| Ollama address | fixed in `ledger/model.py` (`http://127.0.0.1:11434`) |
| Default model | `DEFAULT_MODEL` in `ledger/model.py` |
| Day start/end (09:00–20:00) and period hours | `Calendar` in `ledger/resolve.py` (not exposed in the UI) |

## Reviewing and exporting

Each message appears on the left with its suggestions on the right. Warnings (yellow) mean "check this"; grey badges are informational. Editing any field marks the suggestion accepted. Work through **Needs a decision** for unresolved people, ambiguous days, unreadable times, same-message conflicts and open conditions.

Each message also has **Mark message reviewed** (keyboard `M`). Marking is always explicit: deciding every suggestion does not mark a message. **Accept all and mark reviewed** appears only for eligible pending suggestions with a resolved person/day, readable time and no blocking warning; approved informational flags are allowed. The line above the list shows how many messages are marked and whether the final sheet would be complete.

Two exports:

- **Export final sheet (CSV)** (`availability-final-<week>-complete|provisional.csv`) contains accepted records only, replayed with corrections. It is **complete** only when every non-duplicate message is marked reviewed (the original covers its duplicates), nothing is pending and no blocking issue (unresolved person, unclear day, unreadable time, same-message conflict) is open; otherwise it is labelled **provisional**, and affected person/days are marked `needs_review`. An unreviewed message with unknown scope keeps the whole file provisional even if no cell can be marked. Accepted conditional offers remain conditional and do not by themselves prevent completeness. Format: [docs/specs/final-export.md](docs/specs/final-export.md).
- **Export review log (CSV)** lists reviewed records in message order with their source and warnings. It is an audit trail, not the final sheet. Columns: [docs/API.md](docs/API.md#csv-export).

The status line then shows review time and counts of accepts, edits, rejects, additions, bulk actions and messages marked.

## Local and online behaviour

| | Today |
|---|---|
| Messages, roster, review decisions | retained in browser memory and processed transiently by the local Python server on 127.0.0.1; no application persistence |
| Model calls | only to Ollama on 127.0.0.1 |
| Telemetry, analytics, crash reports | none |
| Hosted version | none; there is no public URL |

## Agreed direction, optional integrations and costs

The core remains a **local review-and-export tool**: Gemma proposes phrases, Python reconciles them, and the coordinator decides. Sponsor tools support that workflow through development evidence, diagnostics or demonstration. They are not reasons to add accounts, a cloud database, in-app voice or a different model provider.

The additional-spending budget is **₹0**: existing resources, verified free plans or confirmed sponsor credits only. No automatic upgrades, top-ups, paid fallbacks or renewals. Optional services must be off by default where they affect runtime, stop or degrade when allowances end, and leave the local workflow usable. This documentation direction does not install, claim, deploy or activate anything.

| Technology | Agreed role | Status and gate |
|---|---|---|
| Gemma 4 E2B via local Ollama | Core phrase extraction, with rules cross-check and human review | **Implemented.** Preserve local processing and the model/code boundary. |
| GitHub Copilot + GitHub Actions | Genuine needed development/review tasks; automated regression checks in CI | **Planned use; no qualifying evidence verified.** Agent/PR work and Actions are distinct evidence routes; CI alone must not be presented as Copilot-authored work. |
| Entire | Capture real future coding sessions, decisions and checkpoints | **Planned use; no qualifying evidence verified.** Confirm current agent compatibility and inspect/redact anything shared; never fabricate retrospective provenance. |
| Sentry Agent Tracing | Optional failure/latency diagnostics with a documented useful finding | **Conditional proposal.** Requires an explicit dependency/network/privacy decision, metadata allow-list, opt-in/off-by-default behavior and verified free allowance. Private messages, names, quotes, model content and raw sensitive exceptions must not leave the device. |
| Render | Interactive demonstration using saved Gemma outputs for fixed fictional fixtures | **Planned demonstration; not built or deployed.** Label replay clearly, disable arbitrary input for hosted model replay, and verify free limits. It is not hosted live inference. |
| `bipulchamoli.tech` | DNS address for the eventual hosted project | **Owned per owner; connection unverified.** It need not match the project name. The .tech prize additionally depends on evidence it was claimed through Hacktoberfest; prevent paid renewal. |
| ElevenLabs | Narrate the fictional demonstration video | **Planned demonstration asset; not generated.** Use a fictional script with verified free credits, publication rights and required attribution/disclosure. In-app voice/transcription is not selected. |
| Backboard R-CLI | Optional bounded development task if genuinely useful | **Conditional proposal.** Verify local-model compatibility and data routing first; do not replace local Gemma inference or upload private messages. |

**Work order:** freeze unseen fictional set C before further behavior changes → visible extraction failures and unsupported-phrase safeguards (COR-03/COR-10) → protect both CSV exports (COR-02) → score C once after planned behavior changes → coordinator validation and the matched timing study. Capture genuine development evidence while doing necessary work. Add diagnostics and demo assets only after their gates are met; they do not replace core correctness work.

The strategy retains **Overall + Gemma**, then considers additional categories supported by completed, meaningful use. Week 3 permits multiple genuinely used categories but a maximum of one prize; no reliable evidence establishes an easier category. No published entry or qualifying use beyond Gemma is verified. Canonical details: [integration roles, boundaries and gates](docs/INTEGRATIONS.md), [official rules and historical competition research](docs/COMPETITION.md), and [TASKS.md](TASKS.md).

## Evaluation summary

On fictional held-out messages (set A: 20 messages, 30 units; set B: 20 messages, 35 units), at first (frozen) scoring:

- Rules alone: 20/30 and 17/35 units right, with many silent errors.
- Gemma alone: 20/30 and 28/35; it left 7 of 12 set A cancellations on the final sheet (a ledger figure computed over all 50 set A messages, dev included).
- Gemma + rules: 26/30 and 30/35; no cancellations left on either final sheet (the set B result was partly luck).

Changes made after reading held-out errors (most recently on 2026-10-20) moved these numbers, some up and some down; they are labelled post-hoc and are not independent evidence. The same author wrote the fixtures, references and rules. Human time saved has not been measured. The final-sheet export and strict scorer exist, including partial-condition-loss checks. The older `evaluation/run.py` condition metric still has a partial-loss gap (EVAL-09). The study itself (matched workloads, several participants) has not been run ([evaluation/MEASUREMENT.md](evaluation/MEASUREMENT.md)). Full tables and provenance: [PROGRESS.md](PROGRESS.md#evaluation-status) and [evaluation/RESULTS.md](evaluation/RESULTS.md).

```bash
python3 -m unittest discover -s tests                        # 49 offline checks
node tests/browser/session_rerun.mjs                        # optional: needs Node 22+ and Chrome
python3 -m evaluation.run --set A --extractor rules          # no model needed
python3 -m evaluation.run --set A --extractor hybrid         # uses cached model outputs in evaluation/runs/
python3 -m evaluation.compare                                # current results; add "frozen" for first scoring
python3 -m evaluation.score_final my_final.csv --set A        # score a final-sheet CSV (timing study)
```

Model/hybrid evaluation uses existing per-message caches, but a missing cache triggers a fresh model call even without --refresh. Evaluation also writes current results and may create caches. Verify complete cache coverage before a cache-only run; use evaluation.compare to read saved results without rescoring. No model calls or evaluation writes were made in this docs pass.

## Documentation

| Document | For |
|---|---|
| [docs/PRD.md](docs/PRD.md) | problem, users, scenarios, requirements, metrics |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | how it works, data, boundaries, deployment |
| [docs/API.md](docs/API.md) | HTTP routes, import and CSV formats, CLI |
| [docs/DECISIONS.md](docs/DECISIONS.md) | why it is built this way |
| [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) | agreed technology roles, current status, privacy/budget gates and evidence |
| [docs/COMPETITION.md](docs/COMPETITION.md) | verified challenge rules, category eligibility, Week 1/2 research and strategy |
| [TASKS.md](TASKS.md) | backlog |
| [PROGRESS.md](PROGRESS.md) | current status and evidence |
| [context.md](context.md) | persistent starting point and verified hand-off for agents |
| [AGENTS.md](AGENTS.md), [CLAUDE.md](CLAUDE.md) | discovery entrypoint and canonical detailed rules for coding agents |
| [evaluation/TUNING.md](evaluation/TUNING.md), [evaluation/MEASUREMENT.md](evaluation/MEASUREMENT.md) | prompt tuning log; human timing protocol |

## Layout

```
server.py, ui/       local review page (no external libraries)
ledger/messages.py   parse dated text and WhatsApp exports; mark duplicates
ledger/names.py      roster matching; similar names are flagged, never guessed
ledger/resolve.py    day and time phrases -> dates and times (no model)
ledger/core.py       evidence checks, per-person history, conflicts, counts
ledger/export.py     confirmed final sheet: export and strict reader
ledger/model.py      Ollama call: copy phrases into JSON (schema-constrained)
ledger/rules.py      keyword baseline
ledger/hybrid.py     model + rules cross-check
tests/               offline unit tests
evaluation/          scoring, cached model outputs, results, tuning and measurement notes
fixtures/            fictional message sets, rosters, references
```

## Licence

No licence file is included, so no licence has been granted yet. The [Ollama listing for gemma4:e2b-it-qat](https://ollama.com/library/gemma4:e2b-it-qat) identifies Apache 2.0 (checked 2026-10-20); the model licence does not grant a licence to this application code.
