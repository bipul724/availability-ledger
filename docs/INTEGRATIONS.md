# Technology integration plan

> **Current Week 3 scope (2026-10-22, D-33 supersedes D-23):** five evidence-backed target categories including Overall: Overall, Gemma, Render, GitHub Copilot through GitHub Actions, and Sentry Agent Tracing. ElevenLabs is a planned sixth, pending actual narration/video and rights evidence. This is not a verified published entry or organizer acceptance. See [current category audit](COMPETITION.md#current-category-portfolio--2026-10-22) and the dated integration rows; historical planning below does not override current status.

**Planning direction agreed: 2026-10-20 (IST). Implementation snapshot: same date.** Availability Ledger remains a local review tool for a volunteer coordinator. The owner wants multiple genuine prize opportunities while preserving a useful, coherent product and an additional ₹0 budget.

This document defines the selected direction, boundaries and acceptance evidence. It does not claim that optional technologies are implemented, that they will win, or that this documentation request authorizes their installation, integration, deployment or publication. Follow the owner's actual implementation request and existing session authorization. Read [COMPETITION.md](COMPETITION.md) for verified rules, historical examples and unresolved eligibility; [../TASKS.md](../TASKS.md) for execution status and dependencies.

## 1. Product and architecture boundary

The coordinator supplies dated volunteer messages, a roster and a planning week. Gemma through local Ollama copies phrases; Python resolves people, dates, times, evidence and chronological changes. The coordinator reviews suggestions and explicitly marks messages. The confirmed final CSV uses accepted claims only. Availability is not a shift assignment.

The current browser sheet/chart still include pending claims. The confirmed export is separate. Visible extraction-failure warnings, stronger day/time evidence checks and CSV formula protection are still pending. The final-sheet scorer is implemented; human time saved and real-world usefulness remain unmeasured. Sponsor expansion does not resolve those gaps.

Keep the local workflow usable without the optional services. Private messages must stay local. Development provenance, diagnostics and demonstration artifacts have different data boundaries; they are not interchangeable evidence.

## 2. Roles and present state

| Technology | Distinct role in the agreed direction | Current verified state | Evidence required before claiming use |
|---|---|---|---|
| Gemma / Ollama | Local availability phrase extraction; deterministic Python and human review handle reconciliation. | Implemented; saved fictional benchmarks exist, with frozen/post-hoc limitations. No fresh inference was run in this documentation pass. | Actual local inference and a reproducible coordinator workflow; identify model/prompt/code/data versions and limitations. |
| GitHub Copilot | Genuine development or PR review on already-needed work. For this entry the category is claimed through its GitHub Actions route (D-33, INT-11). | No Copilot coding-agent, CLI or review use. Other agents' work must not be attributed to Copilot. | Real issue, contribution/review, resulting change, human assessment and relevant validation. Verify free access/quota first. |
| GitHub Actions | Automated regression checks and reproducibility. This is a separately permitted route in the Copilot category. | **Running (INT-10, INT-11):** unit tests, SHA-256 integrity of frozen evidence, cache-only re-score of A/B/C with a job-summary table. Run "tests #5" on `8c5f975` green (2026-10-21). | Committed workflow, genuine successful run, useful checks and actual failures when they occur. Do not manufacture a failure or claim Copilot authored the code. |
| Entire | Capture and explain genuine future agent work, checkpoints and decisions. | No qualifying capture/share verified. | Supported agent, authentic checkpoint/session provenance and a useful decision/bug explained. Inspect and redact before sharing. |
| Sentry Agent Tracing | Optional diagnostics for real extraction latency, schema/error behavior and useful debugging. | **Code added 2026-10-21 (INT-03, D-33):** opt-in via `SENTRY_DSN` and the optional `sentry-sdk`; two allowlists (transaction hook and transport) and leak tests. Owner screenshots now verify real delivery/Agents, four 300 s timeouts (positions 37–40), and a later successful trace (1.42 min, 49 calls, 0 errors, about 71K tokens); post-setting bounded trace bc88af7a (2026-10-22) shows city/country_code/region/subdivision values [Filtered] on its selected chat span and supplied parent transaction attributes. Selected chat Input/Output tabs both show no content; wider payload/privacy/account checks remain open. See PROGRESS live-trace entries. | Actual traces/screenshots and a genuine finding; fictional data initially, metadata allowlist, opt-in behavior, privacy validation and a documented dependency/network exception. |
| Render | A public, useful interactive demonstration of review and export using fictional saved outputs. | **Deployed (DEP-02, 2026-10-21):** https://availability-ledger-replay.onrender.com, free plan, `render.yaml`; checked live by the lead. Since UI-09 (D-34) the site root is a landing page and the replay is at `/app` (live after the next deploy); the landing page is an entry point to the replay, not a substitute for it. | Running review/export walkthrough, explicit saved-output label, free-account hard-stop checks and relevant hosting validation. |
| bipulchamoli.tech | An address pointing to the hosted project. DNS/domain ownership is separate from hosting. | Owner reports ownership; routing, Hacktoberfest acquisition and renewal settings unverified. | Live project, domain acquisition evidence satisfying the official offer condition and no paid renewal. Name need not match the project. |
| ElevenLabs | Narration for the finished fictional-data demonstration video. | Planned (INT-04): script ready in `docs/demo/script.md`; no narration generated yet. | Actual ElevenLabs-generated narration used in the demo, valid generation/publication rights, attribution where required and verified free credit/plan. |
| Backboard R-CLI | Optional bounded development assistance using a compatible local model. | Proposed/untried. No Backboard runtime API or memory layer exists. | A real useful task, local compatibility, reviewable contribution and validation. Stop the trial if it adds little value or needs paid access. |

Every optional row is a plan, not a new runtime dependency. Eligibility does not establish award strength: inspected historical Copilot/ElevenLabs winners used deeper capabilities than CI or narration alone. Retain Gemma and overall consideration while broadening only through completed meaningful uses.

## 3. Local core contract

- Preserve phrase-copying/model versus deterministic-code responsibilities, ambiguity handling, conditional availability, correction history and reviewer overrides.
- Preserve accepted-only final export and explicit message-review marks. Pending/rejected claims never add or cancel confirmed final availability.
- Keep the existing Python standard-library application and vanilla frontend until an explicitly scoped decision changes that boundary. Development tooling is not automatically an application dependency.
- No cloud model routing, external search, cloud database, authentication or agent orchestration is selected for the local core. All 20 sponsor categories were screened; the full screening and reasons for deferral live in [COMPETITION.md](COMPETITION.md).
- Do not turn the project into a rota assignment system, group-chat integration or multi-user cloud service to accommodate a sponsor.

## 4. Development evidence: Copilot, Actions, Entire and optional R-CLI

Use a genuine necessary task, such as an agreed correctness fix or regression check. Capture before/after behavior, the actual tool's contribution, review decisions and verification. A session transcript or installed tool alone is not proof of useful development. Evaluation commands are not automatically cache-only: a missing cache triggers fresh calls even without --refresh. Verify coverage and scope before running; evaluation.compare only reads saved tables. Published transcripts rebuilt from authentic records are acceptable evidence to assess; fabricated past sessions are not.

Entire must be configured before the task whose history it records. Verify its currently supported agent and integration path; existing use of Claude/Codex does not prove Entire captured it. Copilot IDE, CLI, agent and review routes have different access requirements. Check actual free access rather than assuming they are interchangeable.

Actions should run the meaningful existing offline regression/scorer checks from a reproducible checkout. The current working tree contains uncommitted/untracked implementation, so committed HEAD alone does not yet reproduce it. A release/CI implementation task must handle that explicitly; this docs task does not stage, commit or push it. Never tune against or expose unseen C to an implementation agent through CI logs, fixtures or session recordings before the evaluation protocol allows scoring.

Use public-repository standard hosted runners only if that setup and billing behavior are confirmed. Avoid paid/larger runners and unbounded artifacts/caches. R-CLI is an optional trial, not a second required coding stack or a reason to add a Backboard API/memory service.

## 5. Optional diagnostics contract: Sentry

**Status 2026-10-22:** implemented under D-33 (INT-03), with real owner-operated fictional trace delivery and a useful finding verified. Four 300 s timeouts at positions 37–40 account for about 20 of the initial 26.93 minutes; a later trace took 1.42 min, 49 calls, 0 errors. Cause remains unproven. A separate post-setting one-message trace showed four geo values `[Filtered]` on inspected chat/parent attributes, and no content in the chat Input/Output tabs. This is a bounded privacy observation, not complete received-payload validation. The actual account is still Business Trial / no payment method; public Developer Free / 1 user / 5M spans is verified. Post-trial Agents-screen entitlement and export-span delivery remain open. General retention/exhaustion policy is documented, not experimentally tested. Owner reports services stopped and DSN unset.

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

A later replay spec must define the saved-fixture/model-output allowlist, enabled interactions and API behavior. It must not silently infer arbitrary uploads using cached outputs. Exclude private-data upload flows from the replay; clearly explain the local app as the route for users' own messages. All public examples, captures, exports and narration use fictional data. The replay still needs meaningful review, correction-history and final-export interaction, with appropriate tests.

Before deployment verify free instance/runtime behavior, build/egress limits, cold-start behavior and hard-stop/no-billing settings. If a useful replay cannot be completed, a truthful local demonstration video remains an allowed submission path. Do not substitute a landing page for a completed interactive demo claim.

After a real host exists, route the chosen domain/subdomain and verify public resolution/TLS and project links. A project/domain name mismatch is acceptable; ownership alone does not satisfy the .tech category. The official description requires a domain claimed through Hacktoberfest, and advertises $29.99 renewal after the first year. Verify acquisition and disabled paid renewal before claiming eligibility.

## 7. Narration contract: ElevenLabs

Use narration to explain the actual problem, a fictional correction/cancellation/condition example, explicit review, the resulting final CSV and honest limitations. Demonstrate the product as implemented at recording time. Use a permitted voice; do not clone a real person's voice without proper permission.

Narration is explicitly an eligible route in the official category description. In-app voice entry, volunteer voice messages, transcription routes and cloud audio processing are **deferred**, not part of the selected product scope. If a later validated user need changes that decision, treat external audio processing, consent, service rights, config and API changes as a separate implementation design.

The registered Hacktoberfest 2026 offer listing checked 2026-10-20 showed three months of Creator, no card required, one code/account and non-stackable. The Week 3 event-specific list was empty. An available offer is not a redeemed entitlement; no code was claimed in these tasks. Verify the owner's existing redemption/remaining allowance and publication rights before generation. Free-plan audio has noncommercial/attribution restrictions; do not assume a cash-prize demo settles its licensing. Sources: [official promos](https://hacktoberfest.com/my/promos), [publication terms](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform).

The sponsor skill listing exposes [elevenlabs/skills](https://github.com/elevenlabs/skills), including text-to-speech and setup-api-key. It was inspected as a reference, not installed. Do not install the entire bundle merely to narrate a demo; any installation follows an explicitly requested scope and the current official skill workflow.

## 8. Rollout and gates

| Stage | Work | Exit evidence / boundary |
|---|---|---|
| 0 — preserve independent evaluation | Prepare at least 20 new fictional C messages and handwritten reference outside implementation work; freeze unscored and commit before further behavior changes. | Do not expose C contents to the coding agent or use it for tuning. No C is present yet. |
| 1 — necessary correctness work | COR-03/COR-10 visible extraction failures/evidence protection, then COR-02 formula protection. Capture genuine work with supported Entire/Copilot if setup is approved and feasible. | Invented regression inputs, tests, truthful cached comparisons and preserved frozen evidence; no sponsor quota blocks correctness. |
| 2 — usefulness and evaluation | Coordinator feedback/consented anonymized local pilot when authorized; matched manual/assisted timing protocol; once-only C scoring at its proper gate. | Equivalent final-sheet CSVs; separate active human time from inference. EVAL-09 old metric fix remains separate from the implemented strict final scorer. |
| 3 — optional technical diagnostics | Narrow Sentry implementation only if allowance, privacy, architecture and time gates pass. | Actual useful traces/findings with no private content. Any behavior changes must respect the C protocol; stop if this displaces core validation/write-up. |
| 4 — demonstration | Implement useful fictional replay if feasible; host with free hard stops; point eligible domain; generate licensed narration. | Real URL/video and verified walkthrough; label saved outputs. CI, doc work and fictional video preparation may proceed alongside other stages. |
| 5 — submission | Review exact code version, eligibility, sources, limits, category evidence, release reproducibility and final English write-up. | One truthful Week 3 submission listing only completed qualifying uses. No publication/deployment is authorized by the documentation update. |

These stages express dependencies, not a promise to implement every integration. Actual task ordering/IDs are in TASKS.md. If an optional integration misses its gate, keep the completed local project and omit that category claim.

## 9. Free budget, authorization and evidence discipline

Additional budget is ₹0: existing resources, verified free plans or actual sponsor credits only. No paid fallback, top-up, upgrade or auto-renewal. Optional features are off by default and stop/degrade when allowances end. Recheck account state before every external activation; the word free on a plan does not establish a hard spending cap.

Documentation is authorized here. Installation/downloads, accounts, credit claims, network instrumentation, application changes, deployment, sharing sessions and publication follow the owner's actual scoped request; do not request permission twice if existing session authorization already covers the exact action. Never print/store keys or promo codes in docs, logs or commits. The app reads `SENTRY_DSN` (opt-in tracing) and, in the replay, `LEDGER_DEMO` and `PORT`; .env.example remains comments only. No proposed flag, secret name, dependency, API endpoint or deployment command is an implemented interface until code exists.

For each claimed technology record: actual role, version/plan when relevant, code/commit/run or artifact evidence, free allowance/rights, data boundary, observed result, limitations, and the official category supporting it. Successful setup, generic badges, author-entered category headings and a tool's logo are not proof of a qualifying completed use or a win.

## 10. Sources and related documents

- [Official Week 3 challenge](https://dev.to/challenges/hacktoberfest-week3-2026-10-19) and [HF26 category hub](https://dev.to/challenges/hf26): genuine multi-category use, one win maximum, sponsor routes and writing-heavy rubric. Rules/history/competition uncertainty: [COMPETITION.md](COMPETITION.md).
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [Entire source](https://github.com/entireio/cli), [R-CLI source](https://github.com/Backboard-io/Backboard-R-CLI), [Render FAQ](https://render.com/docs/faq), [Sentry manual AI example](https://github.com/getsentry/llm-manual-agent-monitoring-example). These support feasibility research; they do not establish this owner's quotas or that the integrations exist.
- [Architecture](ARCHITECTURE.md), [API](API.md), [final export specification](specs/final-export.md), [PRD](PRD.md), [decisions](DECISIONS.md), [measurement protocol](../evaluation/MEASUREMENT.md).
