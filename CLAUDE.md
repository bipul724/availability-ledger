# Instructions for coding agents

[AGENTS.md](AGENTS.md) is the discovery entrypoint; this file is the canonical agent guide. Both lead to [context.md](context.md) and the same project contracts. Do not create a second, conflicting set of instructions.

## Purpose

Availazy (formerly Availability Ledger; the repository keeps `availability-ledger`) turns dated volunteer chat messages into reviewed **availability** records (not shift assignments) for a volunteer coordinator. A local open model only copies phrases; ordinary Python decides dates, times, evidence, history and counts. After the handoff and this guide, read [README.md](README.md) for setup and user flow.

## Source of truth

| Topic | Canonical file |
|---|---|
| What exists and its evidence | [PROGRESS.md](PROGRESS.md) |
| What to do next | [TASKS.md](TASKS.md) |
| How it works | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Interfaces | [docs/API.md](docs/API.md) |
| Why | [docs/DECISIONS.md](docs/DECISIONS.md) |
| Intended behaviour | [docs/PRD.md](docs/PRD.md) |
| Evaluation numbers and provenance | [evaluation/RESULTS.md](evaluation/RESULTS.md), [evaluation/TUNING.md](evaluation/TUNING.md) |
| Competition rules, historical evidence and strategy | [docs/COMPETITION.md](docs/COMPETITION.md) |
| Intended sponsor roles, evidence gates and data boundaries | [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) |
| Quick hand-off | [context.md](context.md) |

For implemented behavior, source and reproducible checks take precedence over stale prose. Official rules establish competition requirements; the owner's current assignment establishes scope. Planned requirements describe future behavior, so do not rewrite them to claim current implementation. If documents disagree, investigate and correct the affected status/contract rather than changing code merely to match a stale claim.

## Owner-approved direction (planning, 2026-10-20)

Keep the coordinator's local availability-review workflow at the center. Gemma is the current runtime model integration. Copilot and Entire support genuine future development; GitHub Actions supplies CI separately. A proposed Sentry adapter would send structural metadata only. A proposed Render demo would use fictional saved model outputs and identify replay clearly. The existing .tech domain would point to that host only if acquisition eligibility and renewal settings are verified. ElevenLabs is for fictional demo narration; in-app voice is deferred. Backboard R-CLI is an optional bounded development tool if a real task, compatible local model and free route are verified. See D-22 and [INTEGRATIONS](docs/INTEGRATIONS.md). **For the Week 3 submission, D-33 (owner override of D-23, 2026-10-21) adds GitHub Actions automation (Copilot category), a Render read-only replay, opt-in Sentry tracing and ElevenLabs demo narration, each with a dated gate; a category that misses its gate is dropped. Briefs: [docs/prompts/d33-integrations.md](docs/prompts/d33-integrations.md).**

This direction authorizes documentation and planning, not installation, account changes, credit claims, external data transfer, runtime changes, deployment or publication. Select only useful, evidenced categories; one entry may seek multiple qualifying awards but can win only one. Recheck official rules before submission; no category is known to offer easier odds.

## Commands (re-verified 2026-10-21)

```bash
python3 -m unittest discover -s tests           # 91 checks (2026-10-21), offline, < 1 s
node tests/browser/session_rerun.mjs            # optional browser check (Node 22+, local Chrome)
python3 -m evaluation.score_final FILE.csv --set A   # final-sheet scorer (timing study)
python3 server.py [port]                         # http://127.0.0.1:8765/app (landing page at /, UI-09)
python3 -m evaluation.compare [frozen]           # results tables
# CI-style re-score, never calls the model (fails on a missing saved output), results to a temp folder:
python3 -m evaluation.run --set A --extractor hybrid --model gemma4:e2b-it-qat --cache-only --out /tmp/rescore
# re-score using existing complete caches; verify coverage first (see warning below):
for s in A B; do python3 -m evaluation.run --set $s --extractor rules; for m in gemma4:e2b-it-qat qwen3.5:4b-q4_K_M; do for ex in model hybrid; do python3 -m evaluation.run --set $s --extractor $ex --model $m; done; done; done
```

Model/hybrid evaluation makes fresh calls when a cache file is missing, even without --refresh; --refresh forces fresh calls. It also writes current results and may write new cache entries. Before a cache-only check verify complete coverage for the selected messages/model/prompt/set; do not run if a fresh call or protected-cache write would be required without authorization. Use evaluation.compare for a read-only saved-results check. Existing session authorization remains valid; do not ask again when it covers the exact action.

## Code map

`ledger/model.py` (prompt, Ollama call) · `ledger/rules.py` · `ledger/hybrid.py` · `ledger/resolve.py` (dates/times) · `ledger/core.py` (evidence gate, ledger, history, counts) · `ledger/export.py` (confirmed final sheet, strict reader) · `ledger/messages.py` (parsing, duplicates) · `ledger/names.py` · `server.py` · `ui/app.js` · `tests/` · `evaluation/run.py` · `evaluation/score_final.py`.

## Rules

- **Python standard library only.** No pip packages, no CDN or JS libraries, no network calls except to local Ollama. Changing this needs a decision in DECISIONS.md first. **The one exception (D-33):** the optional `sentry-sdk` for opt-in tracing (INT-03), listed in `requirements-tracing.txt`, imported only when `SENTRY_DSN` is set; the core must still run with nothing installed.
- **Do not edit** `fixtures/*.txt`, `fixtures/*reference.json`, `fixtures/setC.manifest`, `evaluation/results/frozen/`, `evaluation/results/frozen-setC/`, `evaluation/results/tuning/`, `evaluation/runs/`.
- **Do not change** `SYSTEM`, `EXAMPLES` or `PROMPT_VERSION` in `ledger/model.py` unless the task is a prompt change; any prompt change bumps `PROMPT_VERSION` and gets a row in TUNING.md.
- **Never tune on held-out messages** (set A held-out ids in `fixtures/reference.json` `split.heldout`; all of sets B and C). Write new test cases with your own invented messages. Label any change made after seeing held-out errors as post-hoc.
- **Keep the model/code boundary.** The model copies words; dates, times, history and counts are code.
- **Preserve history and review behaviour:** later answers change only the times they mention; ambiguous people/dates are never guessed; conditionals stay conditional until a later message settles them; a reviewer's decision (`review`, `override`) controls **that same claim** and is never overwritten by automatic checks, but other claims, including later pending ones, still change the provisional sheet; rejected suggestions never reach the sheet or export; only accepted records reach the final-sheet export, and a message counts as reviewed only when the reviewer marks it (never inferred).
- **Tests:** any change to parsing, resolution, ledger or review semantics needs a unit test with invented messages, and all existing tests must pass. Re-run the cached evaluation and report held-out regressions plainly; never hide one by editing fixtures or scoring.
- **Scope:** read the current assignment before acting. Backlog items and proposed sponsor uses are not automatic implementation permission. Check `git status` first and preserve unrelated uncommitted work. The owner commits and pushes; agents do not commit or push unless asked.
- **Evaluation status (D-24, D-31):** set C was frozen by hash, then **scored once on 2026-10-21 at `56e38bd` (EVAL-07)**. It is now in `fixtures/` and its first score is frozen in `evaluation/results/frozen-setC/`, which is the headline independent result. Every later change is **post-hoc** for A, B and C alike: report it beside the frozen numbers, never instead of them. Fix behaviour with invented development messages, not by fitting C's wording. An optional fresh set D (EVAL-11) would follow the same isolation rules as C.
- **Budget: ₹0.** Do not install software, download models, create accounts, claim credits, purchase, deploy or publish without the owner's explicit request. No paid fallbacks or auto-renewals. Optional services must be opt-in and fail safe.
- **Secrets and data:** never read, print or commit `.env` files or keys. The local app reads only `SENTRY_DSN` (opt-in tracing, INT-03); the hosted replay reads `LEDGER_DEMO` and `PORT` (DEP-02, [.env.example](.env.example)). Never ask for, read or print the DSN. Fixtures are fictional; keep it that way.
- **Real messages:** do not read real messages, with one exception: data for an approved pilot (TASKS EVAL-03). Allowed only when the owner has confirmed in writing that the people involved consented, the data was anonymised before it reached you, it is kept outside version control (never committed, never added to `fixtures/`), and it is processed locally only. Never copy pilot text into docs, tests, logs, issues, telemetry or any external service; report only aggregate results.
- **Telemetry:** only the opt-in Sentry tracing in `ledger/tracing.py` (INT-03, 2026-10-21), off unless `SENTRY_DSN` is set and `sentry-sdk` is installed; any change to it keeps `tests/test_tracing.py` passing. It must stay opt-in, off by default and free-budget bounded, with no message text, names, quotes, model replies, audio, person/message identifiers or exception content that can contain those values. Review default instrumentation and redact before transmission. D-33 is the D-11 exception for INT-03 only, with the attribute allowlist it defines; any other SDK or outbound call still needs its own decision. Do not send pilot data to any external service.
- **Honesty:** never describe a planned or partial integration as completed. As of 2026-10-22 the integrations that exist are Gemma (runtime), GitHub Actions (unit tests, integrity check, cache-only re-score), the Render replay (deployed) and opt-in Sentry tracing (real failed/successful traces received; targeted geo redaction verified on an inspected fictional trace, with wider privacy and account checks open; see [Sentry handoff](docs/SENTRY_HANDOFF.md)); ElevenLabs is planned under D-33, and there is no evidence of Copilot coding-agent or Entire use. Use the status words in [PROGRESS.md](PROGRESS.md#status-vocabulary). Do not turn click counts or fictional results into claims of real-world time saved.

## Work order

Follow [TASKS.md § Order of work](TASKS.md#order-of-work), which is canonical. As of 2026-10-21 13:00 IST: everything through EVAL-07, the D-31 fixes (COR-13 to COR-17) and COR-18 are done. D-33 sequence: INT-11 (Actions) and DEP-02 replay completed; INT-03 real delivery/finding and targeted privacy check verified by owner evidence on 2026-10-21/22, with explicit remaining checks in [SENTRY_HANDOFF](docs/SENTRY_HANDOFF.md). Do not repeat the full demo or paid checkout for setup confirmation. Demo with ElevenLabs narration (DEP-03, INT-04) and post (REL-05) remain separate work. Per D-27, each task updates its TASKS row and one dated PROGRESS entry.

## Mandatory documentation for every task

**Standing owner instruction (2026-10-20):** record project work done and work that needs doing in the docs. This applies to implementation, research, reviews, experiments and documentation tasks, including partial/blocked outcomes. Do not leave material project knowledge only in chat or agent memory.

1. Keep [TASKS.md](TASKS.md) current: record the active task and its actual status; add newly identified necessary work with a stable ID, priority, acceptance criteria and dependencies/required decisions. Label optional ideas as proposed/deferred rather than silently approving scope. Before marking a task done, confirm its required outcome and record its verification.
2. Update [PROGRESS.md](PROGRESS.md) before handing work back: date, task ID, what changed or was learned, relevant files/artifacts, checks actually run and their results, checks not run, limitations/blockers and next steps. Separate attempts from successful outcomes. Preserve useful historical evidence; never describe old checks as fresh.
3. Refresh [context.md](context.md) when the verified state, objective, current/next work, decision, constraint or material knowledge changes. Make the next agent's starting point accurate.
4. Update affected detailed docs when applicable: PRD/architecture/API/export specification for contracts, DECISIONS for choices, INTEGRATIONS for sponsor status/gates, COMPETITION for dated sourced rules/research, and evaluation notes for provenance/results. Do not duplicate every detail everywhere; link canonical records.
5. Re-read the affected docs for consistency and validate changed links. Preserve secrets, private pilot data and frozen evidence. Record uncertainty explicitly and avoid invented dates, outcomes, test results or completion claims.

A task is not ready to hand back until its documentation is current. This bookkeeping rule does not authorize executing newly discovered backlog work, changing protected artifacts, publishing or activating external services.
