# Interfaces

Everything here was read from `server.py`, `ui/app.js`, `ledger/*.py` and `evaluation/*.py` on 2026-10-20. Status and error examples were produced by calling the running handlers locally with fictional data. Nothing in the "Proposed" section can be called today.

Related: [ARCHITECTURE.md](ARCHITECTURE.md) for data structures and flow.

## Contents

- [HTTP server basics](#http-server-basics)
- [GET / and static files](#get--and-static-files)
- [GET /api/status](#get-apistatus)
- [GET /api/demo](#get-apidemo)
- [POST /api/parse](#post-apiparse)
- [POST /api/suggest](#post-apisuggest)
- [POST /api/resolve](#post-apiresolve)
- [Flags](#flags)
- [Message import format](#message-import-format)
- [CSV export](#csv-export)
- [Model-adapter boundary](#model-adapter-boundary)
- [Command-line interface](#command-line-interface)
- [Proposed interfaces (not implemented)](#proposed-interfaces-not-implemented)

## HTTP server basics

- Base URL: `http://127.0.0.1:<port>` (default 8765). The host is fixed to `127.0.0.1`; it is not reachable from other machines.
- **Authentication: none.** Anyone who can open a connection to that port on the same machine can call every route.
- Request bodies are JSON (the `Content-Type` header is not checked; `Content-Length` is used to read the body). An empty body is treated as `{}`.
- Responses: JSON (`application/json`, UTF-8, non-ASCII kept), or the static files. Every response carries `Cache-Control: no-store`.
- **Errors.** Any exception raised while handling a POST returns **400** with `{"error": "<ExceptionType>: <message>"}`. This includes malformed JSON, missing fields, a `week_start` that is not a Monday, and Ollama being unreachable. There is no 500 response. Unknown POST path: **404** `{"error": "unknown endpoint"}`. Unknown GET path: **404** `text/plain` body `not found`.
- No request logging, rate limiting, CORS headers or streaming.

Observed error responses (fictional calls):

| Call | Status | Body |
|---|---|---|
| `POST /api/suggest` with `{}` | 400 | `{"error": "KeyError: 'message'"}` |
| `POST /api/parse` with body `not json` | 400 | `{"error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"}` |
| `POST /api/resolve` with `"week_start": "2026-11-10"` | 400 | `{"error": "ValueError: week_start must be a Monday"}` |
| `POST /api/nope` | 404 | `{"error": "unknown endpoint"}` |
| `GET /nope` | 404 | `not found` |

## GET / and static files

- `GET /` → `ui/index.html`.
- `GET /<name>` → a file inside `ui/` if it exists and ends in `.html`, `.js` or `.css`. Paths that resolve outside `ui/` return 404. A query string on `/` (for example `/?x=1`) returns 404.
- Side effects: none.

## GET /api/status

Purpose: tell the page which local models are installed.

Response 200:

```json
{"models": ["gemma4:e2b-it-qat"], "default_model": "gemma4:e2b-it-qat"}
```

- `models` comes from Ollama `GET http://127.0.0.1:11434/api/tags` with a 2 s timeout. If Ollama cannot be reached, `models` is `[]` (still 200) and the page shows "Ollama is not reachable: only 'Rules only' will work."
- Side effects: one local request to Ollama.

## GET /api/demo

Purpose: load the fictional set A fixture into the form.

Response 200:

```json
{"text": "# FICTIONAL TEST FIXTURE. Riverside Community Pantry does not exist; ...\n2026-11-02 09:41 | ... ",
 "roster": "# FICTIONAL roster (18 volunteers). One name per line.\nMaria Lopez\n...",
 "week_start": "2026-11-09", "timezone": "America/New_York"}
```

Reads `fixtures/riverside_week.txt`, `fixtures/roster.txt` and `week_start`/`timezone` from `fixtures/reference.json`. Side effects: none.

## POST /api/parse

Purpose: turn pasted text into dated messages and a roster.

Request:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string | no (default `""`) | messages, see [import format](#message-import-format) |
| `roster` | string | no | one name per line; `#` lines ignored |
| `day_first` | bool | no | WhatsApp dates are DD/MM rather than MM/DD |

Response 200:

```json
{"messages": [
   {"id": "m01", "sent": "2026-11-03 09:00", "sender": "Ana Example", "text": "Tuesday 2-5 works", "duplicate_of": null},
   {"id": "m02", "sent": "2026-11-03 09:30", "sender": "Ana Example", "text": "tuesday 2–5 works", "duplicate_of": "m01"}],
 "roster": ["Ana Example"]}
```

Validation and behaviour:
- Lines that do not start a message are appended to the previous message; text before the first message is dropped; blank lines and lines starting with `#` are skipped.
- Messages are sorted by timestamp (stable for equal times) and numbered `m01`… (more digits when there are 100 or more).
- `duplicate_of` is set when the same sender sent the same text (ignoring case, whitespace, curly quotes and dash style) within 24 hours of the earliest copy.
- The roster is de-duplicated case-insensitively and **silently truncated to 20 names**.
- An input with no recognisable lines returns `"messages": []` (200); the page then shows an error itself.
- Side effects: none.

## POST /api/suggest

Purpose: propose claims for **one** message.

Request:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `message` | object | yes | a message as returned by `/api/parse` |
| `roster` | list of strings | yes | truncated to 20 |
| `week_start` | `YYYY-MM-DD` | yes | must be a Monday |
| `timezone` | string | no | stored only; not used in any calculation |
| `extractor` | `hybrid` \| `model` \| `rules` | no (default `hybrid`) | which reader |
| `model` | string | no | Ollama model name; default `gemma4:e2b-it-qat` |
| `coordinators` | list of strings | no | extra coordinator sender names (only used by `hybrid`; the UI never sends it) |

Response 200 (rules reader, fictional):

```json
{"claims": [{"id": "m01.1", "msg": "m01", "n": 1, "source": "rules", "review": "pending",
  "said": {"person": "SENDER", "day_text": "Tuesday", "time_text": "2-5", "status": "available",
           "condition": "", "replaces_earlier": false, "excerpt": "Tuesday 2-5 works"}}],
 "stats": {}}
```

- With `model` or `hybrid`, `stats` holds `wall_s`, `prompt_tokens`, `output_tokens`, `prompt_s`, `output_s`, `load_s`, `json_ok`. The page ignores `stats`.
- With `hybrid`, claims may carry `hints` (`replace_cue`, `readers_disagree`, `one_reader`, `added_by_rules`); rules-only cancellations are appended as extra claims with `source: "rules"`.
- If `message.duplicate_of` is set the server returns `{"claims": [], "stats": {}, "duplicate_of": "m01"}` **without** calling the model.
- If the model's reply is not valid JSON, the model contributes no claims and `stats.json_ok` is `false` (still 200). With `model` the response has no claims at all. With `hybrid` the rules' cancellations (days the rules read as unavailable) are still added and flagged `added_by_rules`, but no availability is. The page shows neither case as an error (COR-03).
- Errors: Ollama unreachable or a timeout (300 s) → 400 with the exception text. No retries.
- Side effects: one Ollama `/api/chat` call for `model`/`hybrid`; nothing stored.

## POST /api/resolve

Purpose: recompute everything derived from what was said plus the reviewer's decisions. The page calls it every five messages during reading and 250 ms after each edit or click.

Request:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `messages` | list | yes | all messages from `/api/parse` (including `duplicate_of`) |
| `claims` | list | yes | all raw claims, with `review` and optional `override` |
| `roster` | list | yes | truncated to 20 |
| `week_start` | `YYYY-MM-DD` | yes | Monday |
| `timezone` | string | no | stored only |
| `coordinators` | list | no | extra coordinator names |

`override` fields a reviewer can set: `person`, `dates` (list of ISO dates; days outside the week are discarded), `start`/`end` (`HH:MM`; both empty means "no time"; start must be before end, otherwise the time is unparsed), `status`, `condition`.

Response 200 (fictional: Ana offers Tuesday 2–5 on 3 Nov, then cancels on 5 Nov; "Ana Exampel" is a second, similar roster name):

```json
{"claims": [{"id": "m01.1", "msg": "m01", "source": "rules", "review": "pending", "said": {"…": "…"}, "n": 1,
   "person": "Ana Example", "person_state": "resolved", "person_candidates": [], "similar": ["Ana Exampel"],
   "dates": ["2026-11-10"], "date_state": "resolved", "date_candidates": [], "date_note": "",
   "start": "14:00", "end": "17:00", "time_state": "explicit", "time_note": "",
   "status": "available", "condition": "", "replaces_earlier": false,
   "excerpt_state": "exact", "excerpt_span": [0, 17], "flags": ["similar_name"]}, "…"],
 "ledger": {
   "sheet": {"Ana Example": {}, "Ana Exampel": {}},
   "review_notes": {},
   "history": {"Ana Example|2026-11-10": [
      {"msg": "m01", "sent": "Tue 03 Nov 09:00", "claim": "m01.1", "status": "available", "what": "added", "span": "14:00-17:00"},
      {"msg": "m02", "sent": "Thu 05 Nov 18:00", "claim": "m02.1", "status": "unavailable", "what": "marked unavailable, cancelled", "span": "06:00-23:00"}]},
   "issues": [],
   "counts": {"start": "08:00", "end": "22:00", "step": 30,
              "days": [{"date": "2026-11-09", "available": [0, 0, "…28 values"], "conditional": [0, 0, "…"]}, "…"]}}}
```

- Claims whose `msg` is not among `messages` are ignored.
- `review` becomes `dropped` (with `drop_reason`) only when **both** the quote and the day/time phrases are missing from the message, when the quote names none of the claimed days, or for a coordinator's own self-claim when the coordinator does not resolve to a roster name (a coordinator who is also on the roster is kept). A `rejected` or `accepted` review is never overwritten.
- **Limitation:** a suggestion whose quote is found but whose day or time words are invented is **not** dropped. Example (mocked, fictional): message "Happy to help", proposed day "Tuesday", time "2-4". It gets `phrase_not_in_message`, stays `pending`, and Tuesday 14:00–16:00 appears on the provisional sheet (COR-10).
- `history` entries for duplicate messages have `"what": "repeated"` and an extra `duplicate_of` field.
- Side effects: none.

## Flags

Shown as badges on cards. "Info" flags do not block "Accept all suggestions without warnings".

| Flag | Meaning | Info? |
|---|---|---|
| `who_ambiguous` | name matches several roster entries | |
| `who_unknown` | person not on the roster | |
| `similar_name` | a similar name is on the roster | info |
| `date_ambiguous` | the message does not settle the day | |
| `outside_week` | day is outside the selected week | |
| `date_unreadable` | no day could be read | |
| `time_unreadable` | time could not be read; not applied | |
| `time_unstated` | no time given | info |
| `conditional` | status is conditional | info |
| `excerpt_missing` / `excerpt_approx` | quote not found / only roughly found in the message | |
| `phrase_not_in_message` | day or time words not in the message (still applied provisionally if the quote was found) | |
| `days_narrowed_to_quote` / `days_not_in_quote` | quote supports only some / none of the days | |
| `day_modifier_from_quote` | "this/next/last/coming" restored from the quote | |
| `time_from_same_message` | hours copied for "the same" from earlier in the message | info |
| `edited` | the reviewer changed something | info |
| `replace_cue` | hybrid: replacement word, replaces the earlier answer for the day | info |
| `readers_disagree` / `one_reader` | hybrid: model and rules differ / only one found it | |
| `added_by_rules` | hybrid: cancellation only the rules saw | |

## Message import format

Pasted text or an uploaded `.txt`/`.csv` file (read as text in the browser). Three line formats are recognised:

```
2026-11-02 09:41 | Ana Example | I can do Tuesday mornings            # pipe format (YYYY-MM-DD HH:MM or YYYY-MM-DDTHH:MM)
02/11/2026, 09:41 - Ana Example: I can do Tuesday mornings           # WhatsApp Android export
[02/11/2026, 09:41:03] Ana Example: I can do Tuesday mornings        # WhatsApp iOS export
```

- WhatsApp dates are month-first unless **WhatsApp dates are day-first** is ticked; 2-digit years and am/pm are accepted.
- Times are taken as written. They are **not** converted between timezones.
- Roster: one name per line, `#` comments allowed, up to 20 names.

## CSV export

Built entirely in the browser by **Export reviewed records (CSV)**; the file is named `availability-<week_start>.csv`. Every value is quoted and inner quotes are doubled.

| Column | Meaning |
|---|---|
| `record_id` | claim id, e.g. `m04.1` (or `m04.u1` for one added by the reviewer) |
| `review` | `accepted`, or `pending` when "include records not yet reviewed" is ticked |
| `volunteer` | roster name, or empty if unresolved |
| `date` | ISO date; one row per date; empty when the date is unresolved |
| `start`, `end` | `HH:MM`, empty when no time |
| `status` | `available`, `conditional` or `unavailable` |
| `condition` | condition text for conditional offers |
| `message_id`, `message_time`, `sender` | source message |
| `excerpt` | the supporting quote as proposed |
| `warnings` | readable text of non-info flags, `; `-separated |

Rejected and dropped suggestions are never exported. **The file is a log of reviewed records in message order, not the final sheet**: an offer and its later cancellation are both rows.

**It cannot reliably reconstruct the final sheet.** There is no `replaces_earlier` column, and `evaluation/score_csv.py` replays every row with `replaces_earlier` set to false. "Tuesday 10-12" followed by "Tuesday 2-4 instead" therefore replays as both ranges, while the app's sheet shows 14:00–16:00 only (checked 2026-10-20 with fictional data). Treat the in-app sheet as the reconciled view until a confirmed final export exists (COR-01, EVAL-06).

After export the status line reports review minutes and counts of accepts, edits, rejects, added records and bulk accepts.

Fictional example:

```csv
"record_id","review","volunteer","date","start","end","status","condition","message_id","message_time","sender","excerpt","warnings"
"m01.1","accepted","Ana Example","2026-11-10","14:00","17:00","available","","m01","2026-11-03 09:00","Ana Example","Tuesday 2-5 works",""
"m02.1","accepted","Ana Example","2026-11-10","","","unavailable","","m02","2026-11-05 18:00","Ana Example","Sorry, can't do Tuesday after all",""
```

## Model-adapter boundary

Internal Python interface, not an HTTP route (`ledger/model.py`):

```python
extract(msg: Message, week: str, model: str = "gemma4:e2b-it-qat",
        num_ctx: int = 4096, timeout: float = 300) -> tuple[list[dict], dict]
available_models() -> list[str]
```

- Returns claim dicts in the `said` shape and a stats dict (including the raw reply under `raw`, which the server removes before responding).
- The only outbound calls are `POST /api/chat` and `GET /api/tags` on `http://127.0.0.1:11434` (hard-coded).
- Any other reader must return the same `said` shape: `person, day_text, time_text, status, condition, replaces_earlier, excerpt`. `ledger/rules.py` (`extract(msg, roster)`) is the second implementation.
- Changing `SYSTEM` or `EXAMPLES` requires bumping `PROMPT_VERSION`, which changes the cache folder in `evaluation/runs/` (see [TUNING.md](../evaluation/TUNING.md)).

## Command-line interface

All commands run from the project folder. None read environment variables.

| Command | Purpose | Notes |
|---|---|---|
| `python3 server.py [port]` | start the app | default 8765; host 127.0.0.1 |
| `python3 -m unittest discover -s tests` | 21 offline checks | no Ollama needed |
| `python3 -m evaluation.run --set A\|B --extractor rules\|model\|hybrid [--model NAME] [--only m02,m05] [--refresh] [--label X]` | score a reader against the fictional reference | model outputs cached per message in `evaluation/runs/<model>_prompt<v>[_setB]/`; `--refresh` makes new model calls; writes `evaluation/results/set<S>_<extractor>[_<model>_prompt<v>][_<label>].json` |
| `python3 -m evaluation.compare [frozen]` | print the results table | `frozen` reads `evaluation/results/frozen/` |
| `python3 -m evaluation.score_csv FILE.csv --set A\|B` | score a hand-typed or exported CSV against the reference | **does not replay replacements** (`replaces_earlier` is always false), so it is not yet valid for the timing study in [MEASUREMENT.md](../evaluation/MEASUREMENT.md) (EVAL-06) |

Never point `--label` or any script at `evaluation/results/frozen/`; that folder is the first-scored record.

## Proposed interfaces (not implemented)

These **cannot be called today**. They are listed so nobody mistakes them for existing routes.

| Proposal | Purpose | Task |
|---|---|---|
| A `replay` reader for `/api/suggest` that returns saved outputs from `evaluation/runs/` for the fictional fixtures | free hosted demo without a model | [DEP-02](../TASKS.md#deployment-and-submission) |
| Session save/load (download and re-open a JSON file of messages, claims and reviews) | survive reloads | [COR-04](../TASKS.md#core-correctness) |
| `POST /api/export` and a confirmed final-sheet CSV | final sheet from accepted records only, with pending and unresolved items marked; specified in [specs/final-export.md](specs/final-export.md) | [COR-01](../TASKS.md#core-correctness) |
| Optional voice-note transcription feeding `/api/parse` (ElevenLabs) | audio input; **audio would leave the device** | [INT-05](../TASKS.md#optional-sponsor-integrations) |
