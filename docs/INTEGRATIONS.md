# Technology integration plan

> **Current Week 3 scope (2026-10-23, D-33 supersedes D-23):** five evidence-backed target categories including Overall: Overall, Gemma, Render, GitHub Copilot through GitHub Actions, and Sentry Agent Tracing. ElevenLabs was dropped on 2026-10-22 (D-37). This is not a verified published entry or organizer acceptance. Release `d4b2f76` is pushed: [tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754), a fresh clone and the live replay were verified on 2026-10-23 (REL-02). See [current category audit](COMPETITION.md#current-category-portfolio--2026-10-22) and the dated integration rows; historical planning below does not override current status.

**Planning direction agreed: 2026-10-20 (IST). Current implementation snapshot: 2026-10-23.** Availazy (formerly Availability Ledger) remains a local review tool for a volunteer coordinator. The owner wants multiple genuine prize opportunities while preserving a useful, coherent product and an additional ₹0 budget.

This document distinguishes implemented integrations from proposals, with their boundaries and acceptance evidence. It does not establish prize eligibility or authorize new installation, integration, deployment or publication. Follow the owner's actual implementation request and existing session authorization. Read [COMPETITION.md](COMPETITION.md) for verified rules, historical examples and unresolved eligibility; [../TASKS.md](../TASKS.md) for execution status and dependencies.

## 1. Product and architecture boundary

The coordinator supplies dated volunteer messages, a roster and a planning week. Gemma through local Ollama copies phrases; Python resolves people, dates, times, evidence and chronological changes. The coordinator reviews suggestions and explicitly marks messages. The confirmed final CSV uses accepted claims only. Availability is not a shift assignment.

The browser sheet/chart include pending claims; the accepted-only export is separate. Per-message extraction-failure warnings, day/quote evidence checks and formula protection on both CSV exports are implemented. Unsupported-phrase warnings remain flags rather than automatic holds (D-30). A file is complete only with every non-duplicate message explicitly reviewed, no pending suggestions and no blocking person/date/time/conflict issue; a provisional file still downloads. The final-sheet scorer is implemented; human time saved and real-world usefulness remain unmeasured.

Keep the local workflow usable without the optional services. Private messages must stay local. Development provenance, diagnostics and demonstration artifacts have different data boundaries; they are not interchangeable evidence.

## 2. Roles and present state

| Technology | Distinct role in the agreed direction | Current verified state | Evidence required before claiming use |
|---|---|---|---|
| Gemma / Ollama | Local availability phrase extraction; deterministic Python and human review handle reconciliation. | Implemented; saved fictional benchmarks and owner live runs exist. The 2026-10-23 Ana/Ben Model-only check verified suggestions, explicit review and provisional/complete CSVs (CFG-02); it is not a full-week accuracy test. No fresh inference in this documentation audit. | Preserve model/prompt/code/data versions and frozen/post-hoc limitations. |
| GitHub Copilot | The targeted category uses its separately permitted GitHub Actions route (D-33, INT-11). | No Copilot coding-agent, CLI or review use. Other agents' work must not be attributed to Copilot. | For the selected route, the workflow and successful Actions runs below. A future Copilot-tool claim would require its own actual contribution/review evidence and access check. |
| GitHub Actions | Automated regression checks and reproducibility. This is a permitted route in the Copilot category. | **Running (INT-10, INT-11):** unit tests, SHA-256 integrity of frozen evidence, cache-only re-score of A/B/C with a job-summary table. [tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754) on `d4b2f76` passed all three jobs (2026-10-23 IST). | Committed workflow, genuine successful run, useful checks and actual failures when they occur. Do not manufacture a failure or claim Copilot authored the code. |
| Entire | Capture and explain genuine future agent work, checkpoints and decisions. | No qualifying capture/share verified. | Supported agent, authentic checkpoint/session provenance and a useful decision/bug explained. Inspect and redact before sharing. |
| Sentry Agent Tracing | Optional diagnostics for real extraction latency, schema/error behavior and useful debugging. | **Code added 2026-10-21 (INT-03, D-33):** opt-in via `SENTRY_DSN` and the optional `sentry-sdk`; two allowlists (transaction hook and transport) and leak tests. Owner screenshots now verify real delivery/Agents, four 300 s timeouts (positions 37–40), and a later successful trace (1.42 min, 49 calls, 0 errors, about 71K tokens); post-setting bounded trace bc88af7a (2026-10-22) shows city/country_code/region/subdivision values [Filtered] on its selected chat span and supplied parent transaction attributes. Selected chat Input/Output tabs both show no content; wider payload/privacy/account checks remain open. See PROGRESS live-trace entries. | Actual traces/screenshots and a genuine finding; fictional data initially, metadata allowlist, opt-in behavior, privacy validation and a documented dependency/network exception. |
| Render | A public, useful interactive demonstration of review and export using fictional saved outputs. | **Deployed (DEP-02):** [landing page](https://availability-ledger-replay.onrender.com), [replay at `/app`](https://availability-ledger-replay.onrender.com/app), guide at `/docs`. REL-02 on 2026-10-23 matched nine served UI files to `d4b2f76` and passed 22 bounded live replay checks, including review and both exports. Free plan is specified in `render.yaml`; the dashboard/server source was not inspected in that check. | Keep the saved-output disclosure and existing account budget controls. Served-file matching is not a direct audit of deployed server source or billing settings. |
| bipulchamoli.tech | An address pointing to the hosted project. DNS/domain ownership is separate from hosting. | Owner reports ownership; routing, Hacktoberfest acquisition and renewal settings unverified. | Live project, domain acquisition evidence satisfying the official offer condition and no paid renewal. Name need not match the project. |
| ElevenLabs | Narration for the finished fictional-data demonstration video. | **Dropped** (D-37, 2026-10-22): not used; the category is not claimed. | Actual ElevenLabs-generated narration used in the demo, valid generation/publication rights, attribution where required and verified free credit/plan. |
| Backboard R-CLI | Optional bounded development assistance using a compatible local model. | Proposed/untried. No Backboard runtime API or memory layer exists. | A real useful task, local compatibility, reviewable contribution and validation. Stop the trial if it adds little value or needs paid access. |

Rows explicitly separate existing, proposed and dropped uses. Sentry is the approved optional runtime-dependency/network exception; development tooling does not become an application dependency. Eligibility does not establish award strength: inspected historical Copilot/ElevenLabs winners used deeper capabilities than CI or narration alone. Retain Gemma and overall consideration while claiming only completed meaningful uses.

## 3. Local core contract

- Preserve phrase-copying/model versus deterministic-code responsibilities, ambiguity handling, conditional availability, correction history and reviewer overrides.
- Preserve accepted-only final export and explicit message-review marks. Pending/rejected claims never add or cancel confirmed final availability.
- Keep the Python standard-library core and vanilla frontend. D-33 permits the optional pinned Sentry SDK only for opt-in tracing; the core runs without it. Any further runtime dependency needs its own scoped decision.
- No cloud model routing, external search, cloud database, authentication or agent orchestration is selected for the local core. All 20 sponsor categories were screened; the full screening and reasons for deferral live in [COMPETITION.md](COMPETITION.md).
- Do not turn the project into a rota assignment system, group-chat integration or multi-user cloud service to accommodate a sponsor.

## 4. Development evidence: Copilot, Actions, Entire and optional R-CLI

Use a genuine necessary task, such as an agreed correctness fix or regression check. Capture before/after behavior, the actual tool's contribution, review decisions and verification. A session transcript or installed tool alone is not proof of useful development. Evaluation commands are not automatically cache-only: a missing cache triggers fresh calls even without --refresh. Verify coverage and scope before running; evaluation.compare only reads saved tables. Published transcripts rebuilt from authentic records are acceptable evidence to assess; fabricated past sessions are not.

Entire must be configured before the task whose history it records. Verify its currently supported agent and integration path; existing use of Claude/Codex does not prove Entire captured it. Copilot IDE, CLI, agent and review routes have different access requirements. Check actual free access rather than assuming they are interchangeable.

Actions runs the existing offline regression/scorer checks from a committed checkout. REL-02 verified a clean public clone of `d4b2f76`: 116 unit tests, 8 optional SDK skips, protected checksums/inventory and clean final Git status. Set C was already frozen and scored once on 2026-10-21; preserve its first score and label later changes/re-scores post-hoc. Do not recreate an independent-evaluation claim by reusing the seen set.

Use public-repository standard hosted runners only if that setup and billing behavior are confirmed. Avoid paid/larger runners and unbounded artifacts/caches. R-CLI is an optional trial, not a second required coding stack or a reason to add a Backboard API/memory service.

## 5. Optional diagnostics contract: Sentry

**Owner evidence through 2026-10-22; source reviewed again 2026-10-23:** implemented under D-33 (INT-03), with real owner-operated fictional trace delivery and a useful finding verified. Four 300 s client timeouts at positions 37–40 account for about 20 of the initial 26.93 minutes; a later trace took 1.42 min, 49 calls, 0 errors. Cause remains unproven. A separate post-setting one-message trace showed four geo values `[Filtered]` on inspected chat/parent attributes, and no content in the chat Input/Output tabs. This is a bounded privacy observation, not complete received-payload validation. The account was last observed on Business Trial / no payment method; public Developer Free / 1 user / 5M spans was verified from the dated owner pricing screenshot. Post-trial Agents-screen entitlement and export-span delivery remain open. General retention/exhaustion policy is documented, not experimentally tested. Earlier cleanup is owner-reported; this audit did not inspect processes, environment or account settings.

**Read [SENTRY_HANDOFF.md](SENTRY_HANDOFF.md)** for the complete source contract, corrected SDK review, private setup and clipboard lesson, distinct runs/logs, privacy configuration/results, provisional CSV check, trial/paid-checkout/free-plan distinctions, official sources, evidence provenance and open-check criteria. [PROGRESS](../PROGRESS.md) retains chronology. INT-03 remains in progress; no further full demo or paid-checkout navigation is needed for the completed findings.

The items below were the pre-implementation checklist:

1. Record the exact dependency/network/privacy exception in DECISIONS.md and update architecture/configuration docs when code actually changes. The general direction in this file is not that exception.
2. Verify the account's usable free tracing allowance, retention and behavior when exhausted. No paid fallback or top-up.
3. Begin with fictional sessions. Keep real pilot data and its derivatives out of telemetry and public evidence.
4. Define a small attribute allowlist: model/prompt version, duration, token counts when actually reported, aggregate schema/error outcomes and instrumentation version. Avoid names, message IDs linked to private records, text, excerpts, prompts, replies, paths containing private names and unrestricted exception/request bodies. No content hashes as a substitute for this boundary.
5. Audit automatic SDK integrations and transport payloads before any upload. Exclude personal fields before leaving the process; downstream redaction alone is insufficient. Test using invented sensitive strings.
6. Keep tracing opt-in/off by default. Exporter failure or allowance exhaustion must not block local review/export. Show the difference between healthy traffic, disabled tracing and lost/dropped events; a quiet dashboard is not proof of no failures.
7. Produce actual traces and a real debugging/performance finding. Do not invent findings, describe replay timings as inference latency, or turn successful HTTP/schema responses into quality measurements.

Local inference has no per-token API bill. Do not invent a dollar saving or pretend hardware/energy costs were measured. Token counts describe work; they are not accuracy or human time saved.

## 6. Demonstration and domain contract: Render + .tech

The selected hosting direction is an **interactive fictional saved-output replay**, not free live hosted Gemma. A hosted process cannot use the Mac's localhost Ollama. The current app needs Python APIs, so uploading ui/ alone is not a working deployment plan.

The replay is implemented in `server.py`: it accepts only the served fictional set A messages, roster, week and timezone; model/hybrid requests use saved Gemma outputs and never Ollama. Own-message paste/file inputs are hidden and unserved input is refused. Review, correction history, the chart and both CSV exports work; REL-02 exercised the live hosted workflow. The local app is the route for users' own messages. All public examples, captures, exports and narration use fictional data.

The deployment already exists; do not repeat account setup. Preserve the owner's budget controls and distinguish the observed service from account-specific billing settings. [Render's free-service policy](https://render.com/docs/free), rechecked 2026-10-23, says idle services spin down after 15 minutes and wake in about one minute; without a payment method, bandwidth exhaustion suspends free services and build-minute exhaustion disables new builds. This policy is not a fresh account-settings observation. If the replay is unavailable when recording, the script provides a clearly labelled local saved-output fallback.

After a real host exists, route the chosen domain/subdomain and verify public resolution/TLS and project links. A project/domain name mismatch is acceptable; ownership alone does not satisfy the .tech category. The official description requires a domain claimed through Hacktoberfest, and advertises $29.99 renewal after the first year. Verify acquisition and disabled paid renewal before claiming eligibility.

## 7. Narration contract: ElevenLabs

**Historical option, dropped 2026-10-22 (D-37).** The owner will narrate or use captions. The former contract and dated offer research below are retained as history, not a request to install, redeem, generate audio or claim the category.

Use narration to explain the actual problem, a fictional correction/cancellation/condition example, explicit review, the resulting final CSV and honest limitations. Demonstrate the product as implemented at recording time. Use a permitted voice; do not clone a real person's voice without proper permission.

Narration is explicitly an eligible route in the official category description. In-app voice entry, volunteer voice messages, transcription routes and cloud audio processing are **deferred**, not part of the selected product scope. If a later validated user need changes that decision, treat external audio processing, consent, service rights, config and API changes as a separate implementation design.

The registered Hacktoberfest 2026 offer listing checked 2026-10-20 showed three months of Creator, no card required, one code/account and non-stackable. The Week 3 event-specific list was empty. An available offer is not a redeemed entitlement; no code was claimed in these tasks. Verify the owner's existing redemption/remaining allowance and publication rights before generation. Free-plan audio has noncommercial/attribution restrictions; do not assume a cash-prize demo settles its licensing. Sources: [official promos](https://hacktoberfest.com/my/promos), [publication terms](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform).

The sponsor skill listing exposes [elevenlabs/skills](https://github.com/elevenlabs/skills), including text-to-speech and setup-api-key. It was inspected as a reference, not installed. Do not install the entire bundle merely to narrate a demo; any installation follows an explicitly requested scope and the current official skill workflow.

## 8. Rollout and gates

The original rollout is retained below with its present outcome; it is not a new implementation queue. Current next work is demo recording, final post evidence/disclosures and owner eligibility/publication (DEP-03, REL-05, REL-04).

| Stage | Work | Exit evidence / boundary |
|---|---|---|
| 0 — preserve independent evaluation | Completed: isolated ChatGPT session plus owner edits produced 24 fictional C messages; manifest frozen before implementing agents saw them. | First score retained from 2026-10-21; C is now seen and protected, not a new unseen test. |
| 1 — necessary correctness work | COR-03/COR-10/COR-02 implemented; D-30 keeps unsupported-phrase flags without holds. | Invented regression tests, cached comparisons and frozen evidence preserved. No Entire/Copilot-tool contribution is claimed. |
| 2 — usefulness and evaluation | C first score and later post-hoc results recorded; EVAL-09 fixed with historical metrics preserved. | Real coordinator feedback and human timing remain unmeasured; optional studies require separate authorization. |
| 3 — optional technical diagnostics | Sentry code, real trace delivery/finding and targeted geo-value filtering verified. | INT-03 retains the explicit wider privacy/account/export-span limits in its handoff. |
| 4 — demonstration | Hosted fictional replay verified; two-message local live workflow passed. Recording remains open. | Owner voice/captions replace ElevenLabs; domain eligibility/routing is unverified and not claimed. |
| 5 — submission | Release clone/CI/live checks complete for `d4b2f76`; draft exists. | Owner confirms eligibility, supplies final artifacts/disclosures and publishes. No publication is authorized by this documentation update. |

These stages express dependencies, not a promise to implement every integration. Actual task ordering/IDs are in TASKS.md. If an optional integration misses its gate, keep the completed local project and omit that category claim.

## 9. Free budget, authorization and evidence discipline

Additional budget is ₹0: existing resources, verified free plans or actual sponsor credits only. No paid fallback, top-up, upgrade or auto-renewal. Optional features are off by default and stop/degrade when allowances end. Recheck account state before every external activation; the word free on a plan does not establish a hard spending cap.

Documentation is authorized here. Installation/downloads, accounts, credit claims, network instrumentation, application changes, deployment, sharing sessions and publication follow the owner's actual scoped request; do not request permission twice if existing session authorization already covers the exact action. Never print/store keys or promo codes in docs, logs or commits. The app reads `SENTRY_DSN` (opt-in tracing) and, in the replay, `LEDGER_DEMO` and `PORT`. `.env.example` is a usable shell template with local mode and empty tracing value; `server.py` does not load `.env` automatically (CFG-01). No proposed flag, secret name, dependency, API endpoint or deployment command is an implemented interface until code exists.

For each claimed technology record: actual role, version/plan when relevant, code/commit/run or artifact evidence, free allowance/rights, data boundary, observed result, limitations, and the official category supporting it. Successful setup, generic badges, author-entered category headings and a tool's logo are not proof of a qualifying completed use or a win.

## 10. Sources and related documents

- [Official Week 3 challenge](https://dev.to/challenges/hacktoberfest-week3-2026-10-19) and [HF26 category hub](https://dev.to/challenges/hf26): genuine multi-category use, one win maximum, sponsor routes and writing-heavy rubric. Rules/history/competition uncertainty: [COMPETITION.md](COMPETITION.md).
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [Entire source](https://github.com/entireio/cli), [R-CLI source](https://github.com/Backboard-io/Backboard-R-CLI), [Render FAQ](https://render.com/docs/faq), [Sentry manual AI example](https://github.com/getsentry/llm-manual-agent-monitoring-example). These support feasibility research; they do not establish this owner's quotas or that the integrations exist.
- [Architecture](ARCHITECTURE.md), [API](API.md), [final export specification](specs/final-export.md), [PRD](PRD.md), [decisions](DECISIONS.md), [measurement protocol](../evaluation/MEASUREMENT.md).
