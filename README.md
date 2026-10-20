# Availability Ledger

A local review tool for volunteer coordinators who collect availability through ordinary messages. You paste a week of dated chat messages and your volunteer roster; the tool suggests availability records, shows each one beside the message it came from, and keeps a per-person, per-day history of offers, corrections, cancellations and conditions. You review the suggestions and export the ones you accept.

It records **availability** (when people say they can or cannot help), not shift assignments.

**A local open model proposes and ordinary code decides.** The model (Gemma 4 E2B through Ollama) only copies phrases such as "next Tuesday", "after 3" or "if needed". Python code turns them into dates and times, checks each suggestion's words against the message and flags or drops unsupported ones (with one documented gap: a real quote with invented day or time words is only flagged and counts on the provisional sheet), keeps each person's history per day, keeps conditional offers conditional, and does every count. In the core workflow nothing leaves your computer.

Status: validation prototype. Every message, name and organisation in `fixtures/` is **fictional**. It has not been used by a real coordinator.

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
- CSV export of reviewed records.

## Limitations

- Review work lives only in the browser tab; reloading or re-running loses it.
- The CSV is a **log of reviewed records** in message order, not the final sheet: an offer and its later cancellation are both rows, and the file cannot reliably be replayed into the sheet because it does not record which records replace earlier ones. See [docs/API.md](docs/API.md#csv-export).
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
3. Review the cards, then **Export reviewed records (CSV)**.

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

**Export reviewed records (CSV)** downloads accepted suggestions (tick "include records not yet reviewed" to add pending ones), one row per date, with the source message, quote and warnings. Column meanings: [docs/API.md](docs/API.md#csv-export). The status line then shows review time and counts of accepts, edits, rejects and additions.

## Local and online behaviour

| | Today |
|---|---|
| Messages, roster, review decisions | retained in browser memory and processed transiently by the local Python server on 127.0.0.1; no application persistence |
| Model calls | only to Ollama on 127.0.0.1 |
| Telemetry, analytics, crash reports | none |
| Hosted version | none; there is no public URL |

## Optional integrations and costs

The project runs with **₹0 additional spending**: free plans, existing local resources or sponsor credits only, with no automatic upgrades, top-ups, paid fallbacks or renewals. Any optional feature must stop or degrade when a free allowance ends, and the local workflow must keep working without it ([docs/DECISIONS.md](docs/DECISIONS.md) D-17, D-18).

| Integration | Status |
|---|---|
| Gemma 4 E2B via Ollama | Implemented (default model) |
| Hosted demo | Not implemented. Proposed: a labelled replay of saved outputs on free hosting (for example Render), optionally reached via the existing `bipulchamoli.tech` domain pointed at it (DEP-02) |
| Sentry Agent Tracing | Not implemented |
| ElevenLabs narration or voice-note transcription | Not implemented; transcription would send audio off the device and must say so |
| GitHub Copilot, Entire | No evidence in this repository that either was used to develop it; entering those categories would need such evidence |
| .tech domain category | Unverified: depends on how `bipulchamoli.tech` was acquired; renewal must not be paid |

No integration other than Gemma is implemented. Details and challenge wording: [TASKS.md](TASKS.md#optional-sponsor-integrations).

## Evaluation summary

On fictional held-out messages (set A: 20 messages, 30 units; set B: 20 messages, 35 units), at first (frozen) scoring:

- Rules alone: 20/30 and 17/35 units right, with many silent errors.
- Gemma alone: 20/30 and 28/35; it left 7 of 12 set A cancellations on the final sheet (a ledger figure computed over all 50 set A messages, dev included).
- Gemma + rules: 26/30 and 30/35; no cancellations left on either final sheet (the set B result was partly luck).

Changes made after reading held-out errors (most recently on 2026-10-20) moved these numbers, some up and some down; they are labelled post-hoc and are not independent evidence. The same author wrote the fixtures, references and rules. Human time saved has not been measured, and cannot be until the export and scorer are fixed ([evaluation/MEASUREMENT.md](evaluation/MEASUREMENT.md)). Full tables and provenance: [PROGRESS.md](PROGRESS.md#evaluation-status) and [evaluation/RESULTS.md](evaluation/RESULTS.md).

```bash
python3 -m unittest discover -s tests                        # 21 offline checks
python3 -m evaluation.run --set A --extractor rules          # no model needed
python3 -m evaluation.run --set A --extractor hybrid         # uses cached model outputs in evaluation/runs/
python3 -m evaluation.compare                                # current results; add "frozen" for first scoring
```

## Documentation

| Document | For |
|---|---|
| [docs/PRD.md](docs/PRD.md) | problem, users, scenarios, requirements, metrics |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | how it works, data, boundaries, deployment |
| [docs/API.md](docs/API.md) | HTTP routes, import and CSV formats, CLI |
| [docs/DECISIONS.md](docs/DECISIONS.md) | why it is built this way |
| [TASKS.md](TASKS.md) | backlog |
| [PROGRESS.md](PROGRESS.md) | current status and evidence |
| [context.md](context.md) | short hand-off for a new session |
| [CLAUDE.md](CLAUDE.md) | rules for coding agents |
| [evaluation/TUNING.md](evaluation/TUNING.md), [evaluation/MEASUREMENT.md](evaluation/MEASUREMENT.md) | prompt tuning log; human timing protocol |

## Layout

```
server.py, ui/       local review page (no external libraries)
ledger/messages.py   parse dated text and WhatsApp exports; mark duplicates
ledger/names.py      roster matching; similar names are flagged, never guessed
ledger/resolve.py    day and time phrases -> dates and times (no model)
ledger/core.py       evidence checks, per-person history, conflicts, counts
ledger/model.py      Ollama call: copy phrases into JSON (schema-constrained)
ledger/rules.py      keyword baseline
ledger/hybrid.py     model + rules cross-check
tests/               offline unit tests
evaluation/          scoring, cached model outputs, results, tuning and measurement notes
fixtures/            fictional message sets, rosters, references
```

## Licence

No licence file is included, so no licence has been granted yet. The model's licence (Apache 2.0, as recorded in [evaluation/RESULTS.md](evaluation/RESULTS.md)) applies to the model, not to this code.
