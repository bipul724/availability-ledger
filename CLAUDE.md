# Instructions for coding agents

There is no AGENTS.md; this file is the canonical agent guide for this repository.

## Purpose

Availability Ledger turns dated volunteer chat messages into reviewed **availability** records (not shift assignments) for a volunteer coordinator. A local open model only copies phrases; ordinary Python decides dates, times, evidence, history and counts. Read [README.md](README.md) first.

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
| Quick hand-off | [context.md](context.md) |

The code wins over any document. If they disagree, fix the document in the same change.

## Commands (verified 2026-10-20)

```bash
python3 -m unittest discover -s tests           # 21 checks, offline, < 1 s
python3 server.py [port]                         # http://127.0.0.1:8765
python3 -m evaluation.compare [frozen]           # results tables
# full re-score from cached model outputs (no model calls):
for s in A B; do python3 -m evaluation.run --set $s --extractor rules; for m in gemma4:e2b-it-qat qwen3.5:4b-q4_K_M; do for ex in model hybrid; do python3 -m evaluation.run --set $s --extractor $ex --model $m; done; done; done
```

`evaluation.run --refresh` makes new model calls; do not use it unless asked.

## Code map

`ledger/model.py` (prompt, Ollama call) · `ledger/rules.py` · `ledger/hybrid.py` · `ledger/resolve.py` (dates/times) · `ledger/core.py` (evidence gate, ledger, history, counts) · `ledger/messages.py` (parsing, duplicates) · `ledger/names.py` · `server.py` · `ui/app.js` · `tests/test_ledger.py` · `evaluation/run.py`.

## Rules

- **Python standard library only.** No pip packages, no CDN or JS libraries, no network calls except to local Ollama. Changing this needs a decision in DECISIONS.md first.
- **Do not edit** `fixtures/*.txt`, `fixtures/*reference.json`, `evaluation/results/frozen/`, `evaluation/results/tuning/`, `evaluation/runs/`.
- **Do not change** `SYSTEM`, `EXAMPLES` or `PROMPT_VERSION` in `ledger/model.py` unless the task is a prompt change; any prompt change bumps `PROMPT_VERSION` and gets a row in TUNING.md.
- **Never tune on held-out messages** (set A held-out ids in `fixtures/reference.json` `split.heldout`; all of set B). Write new test cases with your own invented messages. Label any change made after seeing held-out errors as post-hoc.
- **Keep the model/code boundary.** The model copies words; dates, times, history and counts are code.
- **Preserve history and review behaviour:** later answers change only the times they mention; ambiguous people/dates are never guessed; conditionals stay conditional until a later message settles them; a reviewer's decision (`review`, `override`) controls **that same claim** and is never overwritten by automatic checks, but other claims, including later pending ones, still change the provisional sheet; rejected suggestions never reach the sheet or export.
- **Tests:** any change to parsing, resolution, ledger or review semantics needs a unit test with invented messages, and all existing tests must pass. Re-run the cached evaluation and report held-out regressions plainly; never hide one by editing fixtures or scoring.
- **Budget: ₹0.** Do not install software, download models, create accounts, claim credits, purchase, deploy or publish without the owner's explicit request. No paid fallbacks or auto-renewals. Optional services must be opt-in and fail safe.
- **Secrets and data:** never read, print or commit `.env` files or keys. The app reads no environment variables today ([.env.example](.env.example)). Fixtures are fictional; keep it that way.
- **Real messages:** do not read real messages, with one exception: data for an approved pilot (TASKS EVAL-03). Allowed only when the owner has confirmed in writing that the people involved consented, the data was anonymised before it reached you, it is kept outside version control (never committed, never added to `fixtures/`), and it is processed locally only. Never copy pilot text into docs, tests, logs, issues, telemetry or any external service; report only aggregate results.
- **Telemetry:** none exists. If added, it must be opt-in and must not include message text, names, quotes or model replies.
- **Honesty:** never describe a planned or partial integration as completed. Today no integration other than Gemma exists, and there is no evidence of Copilot or Entire development use. Use the status words in [PROGRESS.md](PROGRESS.md#status-vocabulary). Do not turn click counts or fictional results into claims of real-world time saved.

## Work order

Follow [TASKS.md § Order of work](TASKS.md#order-of-work): final export and scorer (COR-01, EVAL-06) → visible failures and unsupported suggestions (COR-03, COR-10) → CSV protection (COR-02) → documentation and labels → timing study (EVAL-02).

## After a change

1. Update the task's status in [TASKS.md](TASKS.md).
2. Add what was checked, with commands and outcomes, to [PROGRESS.md](PROGRESS.md) and bump its date.
3. Update [context.md](context.md) if the objective, next tasks or verified state changed.
4. Update the affected doc in `docs/` if behaviour or interfaces changed.
