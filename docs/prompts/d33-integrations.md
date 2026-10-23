# D-33 integration briefs for the coding agent

> **Historical implementation briefs; do not execute again (status reviewed 2026-10-23).** INT-11 Actions, DEP-02 replay and INT-03 tracing code are implemented. Release `d4b2f76` passed [tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754), a fresh-clone check and the live replay verification (REL-02). INT-03 retains only the named evidence/account/privacy gaps in [SENTRY_HANDOFF.md](../SENTRY_HANDOFF.md). The instructions below preserve the original D-33 assignment, not new authorization for installs, inference, account actions or deployment. Use current [context](../../context.md), [TASKS](../../TASKS.md) and [integration status](../INTEGRATIONS.md) before any new assignment. D-37 dropped ElevenLabs; recording uses owner voice or captions.

Give these one at a time, in order; wait for the lead's review before the next. Each brief is complete on its own. Decision: [D-33](../DECISIONS.md). Standing rules for all three:

- Read `CLAUDE.md`, `AGENTS.md` and the task's row in `TASKS.md` first.
- Never touch `fixtures/`, `evaluation/runs/`, `evaluation/results/frozen/`, `frozen-setC/`, `tuning/`, or the prompt in `ledger/model.py`. Never call the model for set C.
- No accounts, installs outside a local virtualenv, deploys or key handling: those are the owner's. Never read or write `.env` contents into files, logs or reports.
- Fictional data only. Don't commit. Update the TASKS row and add one PROGRESS entry. Report test counts, files changed and anything not verified.

---

## 1. INT-11: GitHub Actions automation (Copilot category) — Wed 21 Oct

Implement INT-11 as defined in `TASKS.md` (D-33).

1. Add `--cache-only` to `evaluation.run`. With it, a missing cached model output raises an error naming the message and cache path, instead of calling Ollama. Add a unit test that patches the model call and proves it is never reached.
2. Add `evaluation/protected.sha256`: SHA-256 for every file under `evaluation/results/frozen/`, `evaluation/results/frozen-setC/`, `evaluation/results/tuning/` and for `fixtures/setC.manifest`, in `sha256sum` format. Generate it from the committed files and confirm `shasum -a 256 -c` passes locally.
3. Extend `.github/workflows/tests.yml` (or add `integrity.yml`), keeping read-only permissions, no secrets and no Ollama:
   - an **integrity** job: `sha256sum -c evaluation/protected.sha256`;
   - a **re-score** job: for sets A, B and C, run rules, model and hybrid with `--model gemma4:e2b-it-qat --cache-only` into a temporary results directory. Don't overwrite committed `evaluation/results/*.json` in the checkout, or if the runner must, never commit back. Then write a Markdown table of units right, missed cancellations and slot agreement per set and reader to `$GITHUB_STEP_SUMMARY`.
   - If writing results to a temp directory needs a small `--out` option, add it with a test.
4. Document the jobs in `TESTING.md` (CI section) and the INT-10/INT-11 rows. Mention in the workflow header comment that these are the GitHub Actions automation used for the Copilot category.
5. Verify locally: unit tests on Python 3.15 and 3.12; the checksum check; the cache-only re-score for all nine set/reader runs with 0 fresh calls; and the table matches the committed results. YAML parses.

Report the counts, the generated summary table and the diff stat. The owner pushes and sends the lead a screenshot of the green run and its job summary.

---

## 2. DEP-02 / INT-02: Render-hosted read-only replay — Thu 22 Oct

Implement DEP-02 as defined in `TASKS.md` and `docs/INTEGRATIONS.md` §6 (D-33).

1. **Demo mode, off by default.** Enable it with `LEDGER_DEMO=1`. In demo mode, `server.py` binds `0.0.0.0` on `$PORT`. Without it, behaviour stays exactly as today (127.0.0.1:8765, live model, paste box).
2. **In demo mode:**
   - Only fictional set A loads (the existing `/api/demo` data).
   - The paste box and custom message input are hidden, and the server rejects them (`/api/parse` with arbitrary text returns 403).
   - `/api/suggest` answers only from saved Gemma outputs in `evaluation/runs/gemma4_e2b_it_qat_prompt3/`, by message ID. It never calls Ollama and never accepts message text it didn't serve.
   - The rules and hybrid readers work as normal. Review, accept and reject, history, warnings, the chart and both CSV exports all work.
   - A persistent banner says: "Replay: fictional messages and saved Gemma 4 outputs. To use your own messages, run it locally — nothing leaves your machine." It links the repo.
     **Superseded disclosure wording (UI-11):** that quoted original brief is historical. The implemented banner distinguishes local message processing from optional Sentry metadata and does not promise that nothing leaves the machine. Preserve the current source wording rather than restoring this old sentence.
3. Add `render.yaml`: a free web service, Python, start command `python3 server.py` with `LEDGER_DEMO=1`, no build step (standard library only), and a health check on `/api/status`. Add no secrets.
4. **Tests:**
   - Unit tests for the demo-mode routes: arbitrary text rejected, unknown IDs rejected, no model call (patched), outputs identical to a local cached run.
   - A browser check `tests/browser/demo_mode.mjs` that starts the server with `LEDGER_DEMO=1` and walks load → suggest → accept → export.
   - All existing checks still pass with demo mode off.
5. Write a short deploy section in `README.md`: the owner's steps in the Render dashboard (New → Blueprint → this repo) and what the free tier does (sleeps when idle, so the first load takes time).

Report counts, files and screenshots at 1400 px and 390 px. The owner creates the Render account, deploys and sends the URL. The lead then checks it.

---

## 3. INT-03: Sentry Agent Tracing, opt-in — Fri 23 Oct

Implement INT-03 as defined in `TASKS.md`, `docs/INTEGRATIONS.md` §5 and D-33. First read the current [Sentry agent monitoring docs](https://docs.sentry.io/product/agents/getting-started/) and the Python SDK's manual AI-span instrumentation. Use the attribute names those docs give, and say in the report which page you used.

1. **New `ledger/tracing.py`:**
   - If `SENTRY_DSN` is unset or `sentry_sdk` isn't importable, every function is a no-op and nothing is imported.
   - Otherwise it initialises with `send_default_pii=False`, default integrations off, `traces_sample_rate=1.0`, and a `before_send_transaction` / span hook that keeps only allowlisted attributes. The allowlist: op/name, model name, prompt version, duration, load time, input/output token counts, JSON-ok flag, claim count, reader kind, stage name, error category, instrumentation version.
2. **Spans at the call sites, not inside `ledger/model.py`:**
   - In `server.py` and `evaluation/run.py`: one agent span per suggest run, and one gen_ai span per model call (model, tokens from the returned stats, load time). Also spans for hybrid merge, resolve, `build_ledger` and export.
   - Message IDs and names must not appear: use the message's position number only.
3. **Optional dependency:** `requirements-tracing.txt` pins `sentry-sdk`. Update README (opt-in section, what is sent, what is never sent) and `docs/ARCHITECTURE.md`. The core still runs with no packages installed: a test runs with `sentry_sdk` hidden.
4. **Scrubber test:** fictional messages containing invented sensitive strings (a fake name, phone number and address). Capture events with a test transport and assert none of the strings appear anywhere in the payload.
5. **Real traces:**
   - The owner sets `SENTRY_DSN` locally. Run the local app on the fictional demo messages with Gemma, live: a fresh, cold-start session through the app, not the evaluation caches. Never write into `evaluation/runs/`.
   - Then look at the traces in Sentry and report what they actually show: for example, where time goes (cold load vs per-message inference vs ledger), token counts per message, and any slow or failed call.
   - If you find a real problem, debug it, fix it under its own small task if it's in scope, and show before and after traces. Don't invent a finding. "No problem found" is a valid result.
   - Cost is $0 per token (local inference); say so, without inventing an energy or hardware cost.

Report counts, files, the trace findings, and which screenshots the owner should take for the post.
