# Sentry handoff: setup, evidence, lessons and open checks

Updated 2026-10-22 after the owner's 00:37 IST pricing screenshot. This is the consolidated INT-03 handoff for the 2026-10-21/22 session. Read it before repeating setup, inference or billing navigation. [PROGRESS](../PROGRESS.md) retains the dated chronology, including earlier hypotheses and their later corrections. [TASKS](../TASKS.md) controls remaining work; a backlog item does not authorize execution.

## 1. Current state and evidence boundaries

- **Implemented, source inspected:** optional Sentry tracing, two client-side allowlists, default/automatic instrumentation disabled, no tracing in hosted replay.
- **Verified in owner UI:** real failed and successful fictional-demo traces reached Traces/Agents during the Business trial. A later one-message trace verifies targeted geo-value redaction on inspected chat and parent attributes; the chat's Input and Output tabs show no content.
- **Owner reported:** service shutdown and `SENTRY_DSN` removal from the shell. No process/environment inspection established cleanup independently.
- **Verified in owner billing UI:** account still on Business Plan Trial, no billing details/payment method on file; visible additional span spend $0.00. The paid checkout was left and trial overview shown again.
- **Official public pricing screenshot:** Developer is Free, one user, with 5M tracing spans and 5K errors. This account has not been observed after trial expiry. Specialized Agents-screen entitlement after expiry is unverified.
- **Not established:** complete received/raw-payload privacy, origin of the specific geo enrichment, retroactive scrubbing, export-specific span delivery, controlled cold/warm or memory causation, accuracy improvement or human time saved. INT-03 remains **in progress** for these explicit limits.

Evidence labels in this file: **source** = code read in this documentation audit; **owner UI** = supplied screenshot or pasted UI text; **owner report** = conversation confirmation; **historical check** = earlier recorded test/log/CSV inspection, not repeated now; **official policy** = dated source research, not an account experiment. Times below are owner screenshot captions/recorded IST, not an independent audit of event epoch timestamps. Rounded UI values are kept rounded.

## 2. Account, environment and safe operation

| Item | Observed value / boundary |
|---|---|
| Organization | `availability-ledger` |
| Actual project | `python`, platform Python; do not mistake the organization slug or the originally suggested project name for the actual project |
| Agent / provider / model | `availability-reader` / `ollama` / `gemma4:e2b-it-qat` |
| SDK / release / environment | `sentry.python` 2.72.0 / `availability-ledger-tracing@1` / `local` |
| Local runtime shown | CPython 3.15.0; Ollama 0.40.6 on Apple M2; 8 GB Mac from prior environment records |
| Addresses | Python app `http://127.0.0.1:8765`; Ollama `http://127.0.0.1:11434` |
| Project checkout | `/Users/bipulchamoli/Desktop/week 3/availability-ledger` (paths with spaces need quoting) |
| Public replay | `https://availability-ledger-replay.onrender.com`; saved fictional outputs, no live model calls, no Sentry initialization |
| Additional budget | ₹0: no payment method, paid upgrade, PAYG, top-up or paid fallback |

Onboarding used plain Python / “Nope, Vanilla.” Error Monitoring remained selected when the owner could not deselect it; this is not authorization to add error capture. Existing code deliberately drops error events and records safe error categories on spans instead. No repository connection or chat integration was needed. Do not paste Sentry's onboarding example into the app or run an intentional `1/0` error merely to complete onboarding.

### DSN handling and clipboard lesson

The DSN remains owner-operated. Never request, print, read from clipboard/environment, put in docs, commit or share it. This handoff contains commands and locations, never its value. Earlier session context records a DSN-bearing onboarding capture; it was not reopened for this audit and must not be reused as public evidence without redaction. No DSN rotation or exposure-remediation outcome is claimed. Use **Settings → Projects → python → Client Keys (DSN)**. Onboarding's Configure screen also offers Copy DSN. Copy the complete URL, excluding `dsn=`, surrounding quotes and trailing commas; a long URL may extend offscreen.

The hidden-input command `read -rs SENTRY_DSN && export SENTRY_DSN` did not reliably enable tracing in the owner's attempts. The exact input error was not established. The successful alternative on this Mac was owner-only clipboard export:

```bash
export SENTRY_DSN="$(pbpaste)"
```

**Clipboard pitfall:** copying that command replaces the DSN in the clipboard. Either type the command manually after copying the DSN, or copy/run the command first, then recopy the DSN in Sentry, return to Terminal and use the Up arrow to recall the command before Enter. No output after export is normal; it does not prove the value is valid. Do not use `echo`, `printenv`, `pbpaste` alone or a screenshot containing the value to verify it.

For a separately authorized future live check, keep `ollama serve` running in its own terminal tab. A startup `Listening on 127.0.0.1:11434` line was observed; `address already in use` alone would require checking an existing service, not killing arbitrary processes. In a second tab, after owner DSN export:

```bash
cd "/Users/bipulchamoli/Desktop/week 3/availability-ledger"
.venv/bin/python server.py
```

Expected startup includes `Sentry tracing on: ...` and the local URL. **Initialization is not delivery evidence.** Absence of that line mattered in the 85-second run below. Even the startup promise about timings/tokens is not proof that Sentry's received records contain no enrichment. The optional SDK was already installed; do not reinstall it or download the existing model just to repeat setup. Earlier implementation records describe a project-only `.venv` install from `requirements-tracing.txt` (SDK 2.72.0, certifi 2026.10.19 and urllib3 2.8.0), not a global install; those dependency versions were not freshly queried in this audit.

**Cleanup used:** Ctrl+C in the Python server tab (source calls `tracing.flush()` on shutdown), then `unset SENTRY_DSN` in that shell; Ctrl+C in the separate Ollama tab when finished. Owner confirmed this after the first workflow and again after the bounded privacy check. It is reported cleanup, not proof that every process, another shell or clipboard was cleared. Unsetting the variable does not retroactively change already-sent traces.

## 3. Source contract and earlier review correction

Source files: [tracing adapter](../ledger/tracing.py), [server](../server.py), [evaluation runner](../evaluation/run.py), [optional requirements](../requirements-tracing.txt), [tracing tests](../tests/test_tracing.py). This audit read these paths; it did not run inference, tests, imports of the SDK or external account actions.

- No `SENTRY_DSN`: no tracing, with no SDK import on that path. Missing optional SDK: core application still works. `.env` is not loaded. Demo mode branches before tracing initialization.
- Manual agent operation `gen_ai.invoke_agent`, chat operation `gen_ai.chat`; additional ledger/hybrid/resolve/export/score stages at call sites. `ledger/model.py` is not itself the Sentry adapter. Evaluation emits chat spans only for fresh calls; cached/replay results are not live inference.
- Allowlisted data: `gen_ai.operation.name`, `gen_ai.agent.name`, `gen_ai.provider.name`, request/response model names and input/output/total token counts; `error.type`; `ledger.prompt_version`, `load_s`, `prompt_s`, `output_s`, `json_ok`, `claim_count`, `reader`, `stage`, `message_position`, `message_count`, `instrumentation_version`. Strings have restricted identifier shapes; booleans/numbers have explicit type checks. Names match the application's own span-name patterns.
- Streamed-span structural fields include trace/span/parent IDs, timestamps, status and segment flag; restricted SDK/runtime/release/environment/operation/segment attributes survive. Structural trace IDs and message **position** are not source message IDs. The browser's random run token is not intended to be transmitted.
- Content exclusions: messages, names, roster, quotes, source IDs, prompts, model replies, raw exception messages, request bodies, host/user details, logs and breadcrumbs. `before_send` drops all error events; default/auto integrations, sessions, logs, client reports and propagation are disabled. `send_default_pii=False` plus disabled `data_collection` are not substitutes for the explicit allowlists.
- Layer 1: `transaction_hook()` → `scrub()` reconstructs transactions and their spans. Layer 2: transport wrapper → `clean_envelope()` reconstructs transaction and streamed-v2-span items and drops all other envelope item types.

**Important historical correction:** an earlier lead review wrongly claimed streamed `gen_ai` spans bypassed the transaction scrubber, and wrongly credited the SDK with removing injected content. The later source/transport experiment found that SDK 2.72.0 splits them **after** `before_send_transaction`; the hook already covered them. `before_send_span` was not the fix: it was not called on this path. The code pins `trace_lifecycle="static"`, leaves `stream_gen_ai_spans` at its default on for Agents, and adds a transport allowlist so protection does not depend only on ordering. Do not revive the superseded gap claim or switch hooks/modes without a separate reviewed change.

**Historical offline checks (PROGRESS, 2026-10-21; not re-run here):** 111 unit tests passed in `.venv`; without the SDK, 103 passed / 8 skipped on the recorded interpreters. A capturing transport used no DSN/network. Invented content was absent with both layers, hook alone and cleaner alone; with both disabled it appeared, proving the test can detect that leak. Token metadata survived. Recorded cache-only comparisons matched 9/9; protected checksums 17/17. These do not prove a cloud provider cannot add fields after ingestion. Existing browser results and exact earlier checks remain in PROGRESS/TESTING; none are fresh results from this handoff audit.

## 4. Run chronology: keep the experiments separate

| Owner observation | Local UI | Sentry / other evidence | Correct interpretation |
|---|---|---|---|
| Oct 21 initial fictional demo | 50 messages, 1,616 s, four extraction warnings | Trace `c26d2afd`: 26.93 min, 49 LLM calls, four errors, about 65K tokens; Explore view 130 spans, trace view 122 | Actual delivered slow/failing run; different span-count scopes are not missing-event proof |
| Small check after closing apps/restarting services | Two invented messages, 24 s, two pending suggestions | No independently established tracing activation for this restart | Local completion only; it also loaded the model before a later full retry |
| Oct 21 retry around 20:55 | 50 messages, 85 s, no extraction-failure summary; 49 unreviewed / 62 pending | Startup lacked tracing-enabled line; dashboard still showed earlier run | Do not claim this run was received by Sentry |
| Oct 21 traced retry, screenshot 21:11 | 50 messages, 86 s; no extraction-failure summary; normal review warnings remain | Trace `969d7ee9`: 1.42 min, 49 calls, zero errors, about 71K tokens | Real successful delivery after working DSN setup; no claim of correct final availability |
| Oct 22 bounded privacy check, screenshot 00:06 | One invented message, 17 s, one pending suggestion | Trace `bc88af7a`: root 16.39 s, three spans; chat 16.36 s | Separate post-setting check; not a new 50-message benchmark |

Fifty source messages versus 49 model calls is consistent with the duplicate-aware workflow; do not invent a skipped call or a new accuracy result. Rounded agent-root timings and UI wall times measure different scopes. Different token totals in a failed and a successful run are not a controlled cost comparison. A dashboard's $0 token estimate is not Sentry billing evidence or a hardware/energy cost measurement.

### Timeout finding and unresolved cause

Owner inspected four failed chat spans at message positions **37–40**, with `TimeoutError` / error status and durations **300.010, 300.047, 300.047, 300.038 seconds**: about 20 minutes combined. One inspected successful call took **72.086 s**, with **1,416 input + 177 output = 1,593 tokens**. Its Input tab showed no input; this was a selected-span observation, not an all-payload audit.

Historical supplied-log inspection: ordinary Ollama handlers near the interruption/recovery reported roughly 1–3 s. During one task, detailed runner output stopped mid-processing; HTTP 200 entries appeared around 19:51, 19:56, 20:01, 20:06 and 20:11 while reporting 2–3 s handlers. Detailed output and normal calls later resumed around 20:15. HTTP 200 on that server excerpt does not prove the Python client received responses within its deadline. Sleep/lid closure, terminal/output blocking, runner stalls, queueing and response delivery were hypotheses, not established causes.

Owner recalled a macOS application-memory warning listing Claude/ChatGPT. Saved/quitted other apps and restarted services before recovery. The earlier Ollama startup reported 5.3 GiB available to its Metal inference device; that is not a measurement of total system memory pressure during the stalls. No contemporaneous memory/swap measurement, controlled comparison or causal isolation was done. The small check warmed the model before a full retry. Therefore “memory pressure caused all four timeouts,” “warm run is X% faster,” “cold load explains the whole run,” and “Sentry fixed the model” are unsupported.

Two retry log excerpts each contained 41 HTTP 200 `/api/chat` entries, not all 49 calls: 20:55:26–20:56:31 (about 0.257–2.541 s reported handlers), and 21:09:03–21:10:07. Neither excerpt contained the searched error-like text. Absence from partial logs is not proof of all-call success.

## 5. Privacy finding, settings and bounded verification

Earlier received span attributes contained actual `user.geo` values. Do not reproduce the personal values. Client-side source allowlists remove `user.*` before transmission, but that alone does not prove what the service stores after ingestion. Official Sentry help describes IP-derived geolocation; it supports an enrichment hypothesis, not proof of the precise origin of these particular attributes. No raw outgoing-versus-received comparison established that origin.

### Owner configuration observed

**Settings → Projects → python → Processing → Security & Privacy**:

- Data Scrubber: ON.
- Use Default Scrubbers: ON.
- Prevent Storing of IP Addresses: changed from OFF to ON; green save check visible at 22:09:52 Oct 21.
- Additional Sensitive Fields: six separate lines:

```text
city
subdivision
region
country_code
subregion
ip_address
```

The official geolocation help listed five of these; `subregion` was added because it had been observed in this owner's earlier trace. After instructions to leave the field, save and refresh, screenshot 22:14:43 still showed all six entries and the toggles ON. This is UI persistence after a requested refresh, not independent observation of the key press or a configuration API check.

Before entry, the UI displayed `email` and Safe Fields displayed `business-email`; actual saved values versus placeholders were not established. Do not infer an exemption was configured, or silently remove existing real entries. Safe Fields was not intentionally changed.

Official help allows **5–15 minutes** propagation. Owner waited longer and resumed after midnight. Do not assume old stored traces change retroactively. For a future authorized configuration check, one invented message is sufficient; do not rerun the long full demo merely to obtain a new trace.

### Exact bounded input and observations

Planning week **2026-10-26**, timezone label **Asia/Calcutta**, reader **Model + rules cross-check**, model **gemma4:e2b-it-qat**, roster **Ravi**:

```text
2026-10-22 00:05 | Ravi | I am available on Monday from 10:00 to 12:00.
```

Owner confirmed seeing tracing enabled; the startup screenshot for this restart was not supplied. The UI returned Monday 26 Oct **10:00–12:00 available**, one pending suggestion, one unreviewed message, in 17 s. No extraction warning was visible. This is one matching fictional example, not a score or accepted final export.

At 00:09 the owner screenshot showed delivered trace `bc88af7afa7741f4b4098bb92aea075b`, root 16.39 s, three spans and **0 Issues**. “Issues” is not being relabelled as a trace error count.

| Inspection | Supplied evidence |
|---|---|
| Chat span `99ded4d22add4a92` | `gen_ai.chat`, status `ok`, duration 16.36 s; provider `ollama`; model `gemma4:e2b-it-qat`; 1,386 input, 82 output, 1,468 total tokens; JSON OK; claim count 1; position 1; load 11.01 s, prompt 3.1 s, output 1.88 s |
| Chat Input | Screenshot explicitly says “No input for this span” |
| Chat Output | Screenshot 00:12:07 explicitly says “No output for this span” |
| Chat attributes | `user.geo.city`, `country_code`, `region`, `subdivision` values each `[Filtered]`; no `ip_address` or `subregion` key appears in supplied list |
| Parent `a2aa299db9e14fa3` | `gen_ai.invoke_agent`, transaction true, message_count 1, hybrid reader, prompt version 3; same four geo values `[Filtered]`, no `ip_address`/`subregion` key in supplied list |
| Parent status | `span.status` and `trace.status` shown as `unknown`; do not interpret as failure or success |

The chat attributes were pasted twice identically: one observation, not two independent checks. A pasted “gemini” model-icon label does not override the actual `gen_ai.provider.name=ollama` and Gemma model attributes. The parent's UI “97% faster than avg / 9.54 min” compares a mixed history, not a controlled benchmark.

**Supported outcome:** targeted redaction of the four visible geo values on inspected chat and parent attributes, plus no content displayed in either chat content tab. Keys still exist with filtered values; they were not removed. No source message, roster name, quote or model reply appears in the supplied attribute lists.

**Limits:** no complete raw-payload audit, no inspection of every span/content tab (including parent Input/Output and the third span), no proof of all possible IP locations, no proof of enrichment origin, no retroactive scrub and no legal/GDPR compliance claim. Do not simplify this to “no personal metadata ever reaches Sentry” or “all data is private.”

## 6. Review and provisional export exercised

The owner accepted **39 warning-free suggestions**, leaving **23 pending**. Accepted suggestions do not automatically mark their messages reviewed. Review means checking the source and decisions; never tell the owner to mark everything reviewed blindly. Screenshots still showed genuine warning cases, including an “except Friday” message with Friday selected, and pending cancellations; this session did not resolve every such case.

The attached fictional final-sheet CSV was checked earlier, read-only, using the project's strict `parse_final_csv` reader with its fictional roster and week **2026-11-09**:

| Result | Value |
|---|---|
| File | `availability-final-2026-11-09-provisional.csv` |
| Strict parse | PASS; file hash unchanged before/after |
| Review metadata | 47 unreviewed messages, 23 pending, 0 blocking issues; m02/m03 reviewed, not m01 |
| Rows | 45 total output rows, including markers; 44 `needs_review` rows/cells, one confirmed row |

This was a format/provisional-state check, not reference scoring or proof of complete/correct availability. Forty-five rows is not 45 accepted records. A provisional export is expected while those review conditions remain. No final CSV was created by the one-message privacy test.

**UI navigation lesson:** Export final sheet is in the **right aside below Changes over time**, not the end of the long message list. Browser Find for “Export final sheet”, then Escape, helped locate it. Review log is a separate artifact, not the reconciled final sheet. Export route instrumentation exists in source; actual delivery of its spans was not inspected in Sentry.

## 7. Usage, trial and paid-checkout lessons

| Evidence | What it establishes / does not establish |
|---|---|
| Oct 22 00:23 Stats & Usage, project python, Category Spans, 14D | 291 total, 291 accepted, 0 filtered, 0 rate-limited, 0 invalid. Errors category had zero counters. These are selected-view ingestion counts, not LLM failure counts, one-trace counts or free quota |
| Oct 22 00:25 and 00:32 Subscription Overview | Business Plan Trial, 14 Days Left, no billing details/payment method on file; usage period Oct 21–Nov 3; Spans 280 / 100M and $0.00 additional spend |
| Manage Subscription pasted view | Paid checkout draft: Team $29/mo, Business $89/mo, 5M spans in paid comparison, proposed PAYG $300/mo, Due today $0; recurring-charge authorization on Save Changes/Confirm |
| Return from checkout | Browser Back guided; 00:32 screenshot again shows trial/no payment method. No submitted paid change is evidenced |
| Trial Learn more at 00:35 | Marketing modal, trial features, Business Trial, Upgrade now / Maybe Later and compare-plans link; no free Agents entitlement established |
| Official pricing screenshot 00:37 | Developer Free, one user, Tracing 5M spans, 5K errors, 5GB logs, 5GB application metrics, 50 replays, 1GB attachments; visible free column/card also lists one uptime monitor, one cron monitor, 20 metric monitors, 100 size-analysis builds, 10 custom dashboards, email alerts and MCP access. Onboarding had described 5M spans/month; pricing screenshot alone does not demonstrate a reset occurring |

Navigation: **Settings → Organization → Stats & Usage**, then **Category: Spans**. For the plan, scroll the settings sidebar to **Usage & Billing → Subscription**. The Account section's plural **Subscriptions** is not the billing route used here. Overview URL: `https://availability-ledger.sentry.io/settings/billing/overview/`.

**Do not conflate:**
- 0 “Filtered Spans” means an ingestion-outcome count; it does not contradict individual geo values displaying `[Filtered]`.
- 0 error-event counters does not negate `TimeoutError` on a chat span; the adapter deliberately drops error events.
- Stats 291 versus billing 280 is unreconciled. Different view/accounting timing or scope is possible but not established; do not claim data loss or a billing bug.
- 100M is the **trial** allowance, not the Developer allowance. The first 5M evidence inside paid checkout did not prove free quota; the later public Developer column did.
- The pasted checkout also offered Seer at +$40 per active contributor/month (defined there as opening at least two PRs in a connected repository), and a yearly Business option displaying $1,068 before discount / $960 after discount. These were unsubmitted offer text, not purchased entitlements or costs incurred. No repositories were connected here.
- Paid checkout's proposed $300 limit is not evidence PAYG is active. “Due today $0” is not a free plan or a guarantee of no future charges. Do not select/confirm/Save Changes/add payment, or cancel an account based on unsubmitted draft values.
- Overview 14 Days Left versus checkout 13 days is not an exact expiry timestamp. The usage-period end and “billed on the 4th” text do not independently establish automatic trial transition.
- A Replay credit of +5K/mo ending Feb 21, 2027 was visible; the public page advertised 5,000 replays for new users for three months. These are separate observations; entitlement dates were not reconciled. No credit was claimed here, and Replay credits are not tracing quota.
- Annual/monthly display differences on public paid cards are not free-plan charges. Seer AI debugger is a separate paid add-on, not the manually instrumented `availability-reader` or evidence of Gemini use.

**Official policy researched, not experimentally tested:** Developer/Team spans retained 30 days (no sampled tier); Business/Enterprise policy describes full fidelity up to 30 days plus a sampled tier thereafter. Exhausted-quota new events are dropped, not queued/recoverable, until the next period unless capacity is added. Developer has no PAYG option. Do not exhaust quota, wait 30 days, buy capacity or promise automatic trial downgrade merely to check a box. Public sources are dated evidence, not a guarantee of future terms or an account-specific setting.

The web tool could not fetch several Sentry pricing/docs pages because they returned unsupported `text/markdown`; that was a tool limitation, not a missing product/page. Official help was readable. The owner-supplied official pricing screenshot resolved the numeric free-plan question; third-party pricing claims were not used as proof.

## 8. Evidence provenance and official references

The durable record is the observations above and dated PROGRESS entries. Original screenshots are conversation attachments in temporary macOS screenshot folders, not committed evidence assets or guaranteed to survive. The local CSV/log paths below are retrieval hints, not portable repository artifacts. Do not publish unredacted screenshots, logs, source messages, location values or any DSN. A final evidence package should use owner-selected redacted captures; that packaging has not been done here.

Relevant owner screenshots: Oct 21 20:19–20:21 failed trace; 21:11:15 local retry and 21:11:39 Agents; 21:24:41 review/export area; 22:09:52 IP toggle; 22:14:43 saved fields. Oct 22 **00:01:53** Ollama listening, **00:04:40** input form, **00:06:01** one-message result, **00:09:12** delivered chat/Input, **00:12:07** Output, **00:22:04/00:22:42/00:23:37** usage navigation/Spans, **00:25:11** subscription, **00:32:27** checkout exit, **00:35:24** modal, **00:37:09** public pricing. Chat/parent attribute lists and paid checkout were pasted as text. Trace prefixes in §4 and span IDs in §5 distinguish observations; do not merge them.

Earlier locally inspected attachments (not reopened or changed in this audit):
- Initial Ollama log: `/Users/bipulchamoli/.codex/attachments/a6c430c8-d0fb-4ed0-abaa-a784ad93f7a4/Pasted text.txt`.
- 85-second retry excerpt: `/Users/bipulchamoli/.codex/attachments/1c68ada2-484c-4b8f-8706-79542bb2c172/Pasted text.txt`.
- 86-second traced retry excerpt: `/Users/bipulchamoli/.codex/attachments/7e40e9f4-cd4b-4fdd-8e6f-57641ad5ad90/Pasted text.txt`.
- Fictional final CSV: `/Users/bipulchamoli/Downloads/availability-final-2026-11-09-provisional.csv`.

Official sources consulted in the session (dates in PROGRESS; do not silently present them as freshly rechecked):
- [Geolocation scrubbing help](https://www.sentry.help/en/articles/13964201-can-i-disable-ip-geolocation-for-gdpr-compliance): five sensitive fields, default IP-derived geo and 5–15 minute propagation; read Oct 21.
- [Project API](https://docs.sentry.io/api/projects/update-a-project/) and [organization API](https://docs.sentry.io/api/organizations/update-an-organization/): research on sensitive fields/IP controls, not API calls against this account.
- [Subscription/usage help](https://www.sentry.help/en/articles/15901850-how-can-i-manage-my-sentry-subscription-billing-and-pay-as-you-go-payg-usage) and [billing navigation](https://www.sentry.help/en/articles/13964886-if-i-downgrade-my-reserved-capacity-when-does-it-apply): read Oct 22.
- [Retention help](https://www.sentry.help/en/articles/17619175-how-does-trace-sampling-and-data-retention-affect-visibility-in-sentry-io-and-how-can-i-troubleshoot-related-issues), [quota exhaustion](https://www.sentry.help/en/articles/13964891-i-ve-exhausted-my-quota-what-now?code=firesideswiftFireside), [Developer has no PAYG](https://www.sentry.help/en/articles/13965037-can-i-set-up-an-on-demand-pay-as-you-go-budget-for-my-free-developer-plan): read Oct 22. The query on the exhaustion URL is the accessible source reference, not an offer claimed by the owner.
- [Official pricing](https://sentry.io/pricing/): owner screenshot Oct 22 00:37, after web content-type failure.
- [Manual instrumentation](https://docs.sentry.io/platforms/python/agent-tracing/manual-instrumentation) and [Agents setup](https://docs.sentry.io/product/agents/getting-started/): earlier implementation references, not a fresh entitlement check.

## 9. Resume without repeating completed work

No more inference or billing clicks are needed to prove setup, the four timeouts, successful retry delivery, targeted geo redaction or the public free quota. Services are currently **reported stopped**, not expected to be kept running for another agent. Give the owner one action at a time, refer to visible exact labels, and inspect the supplied result before advancing. Avoid making the owner repeat an entire run or navigate checkout merely because a public page fetch failed.

Open checks under INT-03, each requiring its own scoped evidence:

| Check | Existing evidence / completion criterion |
|---|---|
| Wider privacy / enrichment origin | Client source and historical offline leak checks exist; inspected cloud chat/parent geo values filtered. If stronger claims are needed, compare authorized fictional outgoing/received metadata without recording sensitive values; inspect other necessary span/content surfaces. Do not claim all payloads audited from the current UI sample |
| Post-trial Agents entitlement / transition | Public Free tracing quota is known; actual account still Business Trial. Obtain authoritative feature entitlement or owner post-trial UI before promising the specialized Agents screen. Exact automatic downgrade/expiry behavior was not verified |
| Export span delivery | Instrumentation exists and local CSV export was exercised. Inspect existing matching `ledger request` / export spans first; no new full inference run is needed. Do not describe a CSV parser PASS as telemetry delivery |
| Timeout mechanism | Four timeouts are a useful truthful finding already. Only pursue a bounded, authorized reproduction if needed; measure memory/conditions and correlate timestamps rather than assert a cause from recovery |
| Retention / exhaustion | General official policy is documented; no actual expiry/exhaustion experiment. Explicitly separate policy from account observation |
| Public evidence packaging | Select/redact owner screenshots, preserve trace scopes and factual limits; do not publish automatically or claim eligibility/winning odds from setup alone |

For the remaining project sequence, see TASKS: demo recording/narration and the post remain separate tasks. This documentation request authorizes no new account changes, installs, code fixes, model runs, credit claims, deployment, publishing, commits or pushes. Preserve all fixtures, prompt/version, saved model outputs and frozen evaluation evidence.
