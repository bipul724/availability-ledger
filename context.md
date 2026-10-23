# Availazy: current project context

Updated 2026-10-23 during DOC-12. Start with [AGENTS.md](AGENTS.md), then [CLAUDE.md](CLAUDE.md). This file is the current handoff; dated snapshots and prompts preserve history and must not override current source or superseding decisions.

**DEP-03 script v2 (2026-10-23):** `docs/demo/script.md` is now an 11-shot, roughly 4–5 minute script. Its moments were re-verified on current code from saved outputs (no model calls), with a fact-source table and a do-not-say list. The owner records next.

## Current assignment and release state

- **DOC-12 complete locally:** comprehensive implementation/history review and all 28 existing project docs inspected; 25 updated, 3 retained, current handoff archived and audit report created. Fresh unit/browser/optional-SDK/cache-only/link/diagram/scope checks are in [DOCUMENTATION_AUDIT](docs/DOCUMENTATION_AUDIT.md). Application/configuration/protected evidence is unchanged. The three existing local post-push record changes were preserved. These documentation updates remain uncommitted.
- **DOC-13 independent follow-up complete locally:** actual hashes/Git, original raw browser logs, saved scoring/render/layout artifacts and fresh unit/tracing/checksum/link checks substantiate the mechanical totals. Four residual wording corrections applied; earlier exact timings/read depth and the listed manual gaps remain unverified. Scope is still 25 existing docs changed, 3 unchanged, 2 new; all 313 non-doc baseline files also match HEAD. Details and retained-log limitations are in the audit report's DOC-13 section; no model, account, commit, push or deployment action.
- **Published code:** owner-pushed `d4b2f76c6b1e5da1da7b00b0dcecf586284a86aa`, branch `main`. REL-02 verified public main, a fresh clone, [Actions tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754), and the live Render front end/replay on 2026-10-23. A documentation edit after that observation is not itself committed or deployed.
- **Remaining owner work:** record/upload the demo (DEP-03), finish the unpublished post (REL-05), confirm personal eligibility and final entries (REL-04), then publish. A draft/script exists; no video URL or publication is established. Read the current [TASKS](TASKS.md#order-of-work), not the old calendar plan.
- **No new model run, installation, account change, commit, push, deploy or publication is authorized by a documentation task.** The owner commits and pushes manually. Additional spend stays ₹0.

## What the application does

Availazy is a local, single-user availability-review prototype for volunteer coordinators. The repository/service name remains `availability-ledger`. It records when people can help, not shift assignments.

- Paste pipe-format dated messages or a WhatsApp text export, or upload a text file; enter up to 20 roster names. There is no input-CSV requirement, WhatsApp connection, archive/media import or automatic message ingestion. Extra roster entries are silently truncated.
- Three readers: Rules only, Model only, Model + rules (default). Model readers use local Ollama at the fixed `http://127.0.0.1:11434`; default `gemma4:e2b-it-qat`, prompt v3. The model copies phrases and proposes status/replacement hints. Code resolves people/dates/times, checks evidence, reconciles history and counts; a person accepts/rejects/edits.
- Suggestions stay beside highlighted source quotes. Per-message failures remain visible and reading continues without automatic retries. Duplicate messages are collapsed. Wording/missed-change warnings do not silently edit accepted decisions.
- Review state lives in browser memory. Reload loses it; a successful parsed rerun replaces it. Bad-week, failed-parse or empty-input rejection preserves the prior session. Later failures are recorded in the new session, not a rollback to the old session.
- The light Forest & Parchment appearance is always used, including under dark OS preference (D-36). The app/landing/guide/404 use vanilla HTML/CSS/JS with no CDN/runtime frontend libraries.

## Review and exports

- The in-app ledger/chart include pending and accepted claims, with pending labels/dashes. Rejected/dropped claims do not contribute unless restored by the reviewer.
- Final-sheet CSV replays **accepted records only**, including later accepted corrections/cancellations. Accepting a suggestion does not mark its message reviewed.
- **Complete:** every non-duplicate message explicitly reviewed, zero pending claims and zero blocking who/date/time/conflict issues. Otherwise the CSV still downloads as provisional. Unreviewed/pending scope can mark cells `needs_review`; other populated cells can be `confirmed` even in a provisional file. Accepted conditions do not by themselves prevent completeness.
- Review-log CSV is a separate audit trail, not an importable saved session. Its optional pending inclusion is independent of message-review marks.
- Both CSV writers neutralize formula-starting text. The final CSV reader/scorer applies a stricter format contract than general API payload handling. See [final-export specification](docs/specs/final-export.md).

## Architecture, configuration and boundaries

Python standard-library core, vanilla front end, no database/schema/migrations, auth, accounts, durable sessions or cloud sync. The server processes requests transiently and reads shipped fictional fixtures and saved outputs for demos. Optional tracing retains temporary in-process run metadata; this is not saved review work.

| Item | Actual contract |
|---|---|
| Pages | `/` landing, `/app` review app, `/docs` guide; styled 404 for unknown static paths |
| JSON routes | GET `/api/status`, `/api/demo`; POST `/api/parse`, `/api/suggest`, `/api/resolve`, `/api/export` |
| Local start | `python3 server.py [port]`, loopback 127.0.0.1, default 8765 |
| Replay start | Only exact `LEDGER_DEMO=1`; bind 0.0.0.0, port from `PORT` or default 8765; saved set-A outputs, no Ollama call |
| Tracing | `SENTRY_DSN` empty/unset disables it; nonempty plus optional pinned SDK permits initialization; replay bypasses tracing |
| Env files | `.env` ignored/local; `.env.example` safe assignments; server never loads dotenv automatically. Owner manually sources/exports as in README; agents never open actual `.env` or keys |
| Dependencies | Core needs no pip install; `requirements-tracing.txt` pins optional sentry-sdk 2.72.0. No Node package manifest/application frontend build |
| Tests | Unit suite and browser scripts use invented inputs, saved outputs/stubs; loopback HTTP is used, no external model calls required. Exact commands/results in [TESTING](TESTING.md) |

API bodies/reviewer overrides are trusted local-client inputs, not a fully schema-validated security boundary. Replay source-message/settings checks do not detect arbitrary private text in every supplied claim/override field. Do not treat the local server or public replay as an authenticated data service. See [API](docs/API.md) and [ARCHITECTURE](docs/ARCHITECTURE.md) for precise validation, grid, calendar and failure behavior.

## Implemented integrations and evidence

| Integration | State and limits |
|---|---|
| Gemma/Ollama | Local runtime phrase proposals; fictional A/B/C evaluations and historical full-week live/trace runs exist. CFG-02 explicitly verified two Model-only Ana/Ben suggestions and the manual provisional→complete export path on 2026-10-23; not proof of general model accuracy |
| GitHub Actions | Main push/PR: offline unit tests (Python 3.12), protected SHA/inventory and cache-only A/B/C re-score. All three #18 jobs green on d4b2f76; no browser/model/deploy job |
| Render | [Fictional replay](https://availability-ledger-replay.onrender.com/app) live. Nine front-end responses matched d4b2f76; 50 messages → 67 saved-output suggestions, review and both exports worked. Server source/dashboard/logging were not directly inspected |
| Sentry | Optional, off by default, application-side transaction/envelope allowlists. Historical owner traces verify delivery, four client timeouts, a later successful run and targeted filtering of four inspected geo values. Attribute origin, full received-payload audit, export-span delivery and post-trial entitlement remain unverified; account observations are dated, not fresh account inspection |
| Other proposed tools | ElevenLabs dropped by D-37. No evidenced Copilot coding-agent, Entire, Backboard or .tech routing use. Actions is the planned Copilot-category route, not proof of Copilot-agent development |

Use [SENTRY_HANDOFF](docs/SENTRY_HANDOFF.md), [INTEGRATIONS](docs/INTEGRATIONS.md) and [COMPETITION](docs/COMPETITION.md) for dated evidence. Eligibility/category entry is not inferred from an implementation or a public pricing page.

## Evaluation and unresolved limits

- A/B fixtures, references and baseline share an assistant author. C was written in an isolated ChatGPT session, with five owner-rewritten messages, frozen by manifest and scored once on 2026-10-21. Independent first scores remain frozen; every later A/B/C change is post-hoc. No real-coordinator pilot or measured human time saving exists.
- Extraction units, all-pending provisional-ledger metrics and human-reviewed final-CSV scoring have different scopes. Canonical numbers/provenance are in [RESULTS](evaluation/RESULTS.md); the unperformed timing-study protocol is in [MEASUREMENT](evaluation/MEASUREMENT.md).
- COR-13 to COR-18 are implemented post-hoc fixes; do not resurrect the old C isolation task or describe those fixes as pending. Fresh independent validation would need separately authorized new data (optional EVAL-11).
- Current limitations include no persistence/Stop button/timezone conversion; silent roster truncation; unsupported point times; exact-word evidence false positives; pending/accepted merged segments shown wholly pending; COR-19 negation-inside-condition error in Rules only; UI-22 screen-reader follow-ups unverified. See TASKS and ARCHITECTURE for scope.
- Bounded Chrome layout/focus/contrast checks exist. No Safari, Firefox or VoiceOver pass is established. Python 3.10/3.11 and local Linux are not verified; CI covers Ubuntu/Python 3.12.
- Current external-rule research retains a deadline discrepancy; personal eligibility, actual development start, final categories, video, redacted evidence and actual AI-assistance disclosure remain owner decisions. No date or eligibility resolution should be invented.

## Preservation and history

Never edit fixtures, setC.manifest, frozen/tuning results, cached model outputs or model prompt/version in a documentation task. Use `--cache-only` plus temporary `--out` for verification; no `--refresh`. Preserve existing work and make new checks distinguishable from historical/owner evidence.

The former mixed-date handoff is preserved in [pre-audit context](docs/archive/context-2026-10-23-before-doc-audit.md); the [2026-10-20 archive](docs/archive/context-2026-10-20.md) is older. Neither is a current work order. PROGRESS preserves dated chronology; DECISIONS preserves decisions and supersessions. Do not duplicate those records in the current handoff.
