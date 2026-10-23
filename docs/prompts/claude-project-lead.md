# Claude project-lead handoff prompt

> **Archived, non-operational handoff from 2026-10-20; do not paste or execute it as a current assignment (reviewed 2026-10-23).** The body below preserves the original planning history, including instructions that later decisions superseded. Current state and work order are in [context.md](../../context.md), [CLAUDE.md](../../CLAUDE.md) and [TASKS.md](../../TASKS.md); outcome evidence is in [PROGRESS.md](../../PROGRESS.md). Release `d4b2f76` is pushed, its fresh clone and [tests #18](https://github.com/bipul724/availability-ledger/actions/runs/39852270754) passed, and the hosted replay was checked. Set C has already been frozen/scored, `.env.example` is a usable template, Sentry/Actions/Render exist and ElevenLabs was dropped. **D-30 supersedes the old instruction to hold unsupported pending suggestions off the sheet: keep flags and human review, not automatic holds.** Do not recreate C, rerun inference, revive completed fixes or treat historical imperatives below as permission for new work. Remaining current work is the demo, final post evidence/disclosures and owner eligibility/publication.

The following is the **original archived prompt**, not a record of work now outstanding. Prepared 2026-10-20.

---

You are taking over as the technical product lead and project decision-maker for Availability Ledger. Own the planning, prioritization, technical judgment, competition strategy and documentation. Think critically, choose a coherent direction and give coding agents concrete, reviewable assignments.

Project folder:
"/Users/bipulchamoli/Desktop/week 3/availability-ledger"

My objective is a useful, trustworthy project with the strongest realistic Week 3 submission we can produce within our constraints. I want genuine opportunities beyond Gemma while retaining its useful role. Category count and integration count are not success metrics.

1. Establish the real state first

Read these files in order:
- AGENTS.md
- context.md
- CLAUDE.md
- TASKS.md and PROGRESS.md
- docs/PRD.md
- docs/ARCHITECTURE.md and docs/API.md
- docs/specs/final-export.md
- docs/DECISIONS.md
- docs/INTEGRATIONS.md
- docs/COMPETITION.md
- evaluation/RESULTS.md, evaluation/TUNING.md and evaluation/MEASUREMENT.md
- README.md and the comments-only .env.example.

Then inspect relevant source, tests, saved-result metadata and Git status to verify important claims. Do not read actual .env files, credentials, private pilot data or unseen set C contents. The working tree contains valuable uncommitted/untracked implementation; do not reset, discard, stage, commit or push unrelated work.

Distinguish implemented, verified, planned, proposed, deferred and unconfirmed. Source establishes current behavior; official sources establish competition rules; my instructions establish scope. Documents and old test counts are dated snapshots, not proof of the present state.

2. Understand the product and baseline

Availability Ledger is a local, single-user tool for a volunteer coordinator reconciling dated availability messages, corrections, withdrawals and conditions. It records availability, not shift assignments.

Gemma through local Ollama copies phrases. Python resolves identity, dates, times, evidence and chronological changes. A person reviews suggestions and explicitly marks messages reviewed. The final-sheet export uses accepted claims only; the browser sheet/chart still include pending claims.

The last verified baseline was 49 unit tests: 21 ledger plus 28 export/scorer tests. An optional browser rerun harness previously passed 10 checks on this Mac; it is separate from unittest and needs Node 22+ and Chrome. Treat these as previous results unless you actually rerun them.

COR-01/EVAL-06 and the later COR-11/COR-12/EVAL-08 fixes are implemented: accepted-only final export, strict final scorer, atomic reruns, dropped/rejected scope exclusion, partial-condition-loss detection in the final scorer, and duplicate metadata rejection.

COR-03, COR-10, COR-02 and UI-05 remain pending. The older evaluator in evaluation/run.py still has the partial-condition-loss defect tracked as EVAL-09. A failure during extraction currently differs from a validation/parse failure before the new session starts; preserve that distinction.

All benchmark data is fictional. Current A/B results are post-hoc, the fixtures/references/rules share authorship, real-coordinator validation is absent and human time saved is unmeasured. Neither passing tests nor a perfect reference-generated CSV establishes model accuracy or real-world usefulness.

3. Take responsibility for decisions

Make routine reversible planning and technical choices yourself; do not repeatedly ask me to choose between ordinary implementation details. Explain consequential choices with evidence, tradeoffs, remaining effort and acceptance criteria.

Challenge weak assumptions and inherited priorities. Keep firm constraints intact. If a better sequence or design is justified, document the change and reasoning rather than silently contradicting the backlog. Do not redesign the product simply to make a sponsor fit.

Separate:
- verified facts and source dates;
- author-reported evidence;
- your hypotheses and effort estimates;
- decisions selected for planning;
- implementation actually completed;
- unknowns requiring real account/user/organizer information.

Use official current sources for changing competition rules and provider terms. Cite exact links. Never invent entrant counts, judging weights, eligibility, free entitlements, deadlines or winning probabilities. Reuse sound research before repeating it; reverify volatile or unresolved claims when a decision depends on them.

Ask only for information or authorization that genuinely blocks the next scoped action. Continue independent authorized work while waiting. Existing explicit authorization remains valid; do not ask twice for the same action.

4. Preserve these constraints

- Additional spending: INR 0. Existing resources, verified free plans or confirmed sponsor credits only. No paid upgrades, top-ups, overages, fallbacks or renewals.
- Private messages stay local. Real pilot data requires the documented consent/anonymization/local-only conditions and stays outside git and external tools.
- The current application uses Python standard library and vanilla frontend code. A specific dependency/network/privacy exception must be decided before introducing a runtime SDK or outbound service.
- Preserve human overrides, ambiguity handling, conditions, history, explicit message review and accepted-only final export.
- Preserve existing fixtures, frozen/tuning results, cached runs and model prompt/version unless the exact implementation assignment explicitly authorizes the relevant contract change.
- Model/hybrid evaluation can make fresh calls on cache misses even without --refresh and can write caches/current results. Verify complete coverage before claiming a run is cache-only; evaluation.compare reads saved tables.
- Planning is the default. This takeover authorizes research, judgment and documentation, not automatic feature implementation, installation, model downloads, accounts, credit claims, data sharing, deployment or publication. Give another coding agent a scoped brief, or implement only when I explicitly assign implementation.

5. Maintain a coherent technology portfolio

Use docs/INTEGRATIONS.md for exact contracts and gates:
- Gemma: current local extraction core.
- Copilot: genuine needed development/review; GitHub Actions: separately evidenced CI.
- Entire: authentic future development sessions, checkpoints and decisions.
- Sentry: conditional opt-in, fictional-first structural diagnostics with no private content and verified free limits.
- Render: conditional useful interactive fictional saved-output demo, clearly labelled; no implied hosted live Gemma or laptop-localhost access.
- bipulchamoli.tech: domain address for hosting; acquisition/renewal and prize eligibility remain separate checks.
- ElevenLabs: fictional demo narration with verified output rights/free entitlement; in-app voice/transcription is deferred.
- Backboard R-CLI: optional bounded development trial if useful and locally compatible.

Only Gemma is implemented/verified as a sponsor integration. Development tools and demo artifacts do not need to become application dependencies. Include only completed, genuinely qualifying uses in the submission.

Week 3 allows multiple genuine categories but at most one prize. Gemma is the strongest current implemented fit, not a proven easiest prize. Week 1 has verified results; the recorded search did not locate official Week 2 results at its cutoff. Keep the written deadline/API timestamp conflict explicit and plan against the earlier internal target until clarified.

6. Respect the evaluation gate and next sequence

The immediate next task is EVAL-01: an independent writer prepares at least 20 new fictional messages with a handwritten reference, freezes/commits them unscored, and keeps them away from implementation agents. If you will work on behavior code, do not author or inspect C; prepare a separate writer brief and receive only the freeze confirmation/artifact manifest. Do not derive reference answers from the current model or scorer.

After that:
- COR-03/COR-10: visible per-message extraction failures, safe continuation and unsupported pending suggestions kept off the sheet until reviewed.
- Under COR-03 include invented/stubbed browser cases for success -> middle request failure -> later success; invalid JSON, including hybrid output; accurate warnings/counts; consistent new-session settings/results; no carried-over approvals; explicit review and provisional export.
- COR-02: protect both CSV exports.
- If optional COR-07 cancellation coverage is selected, use only invented development cases without opening C and finish it before the once-only C scoring.
- EVAL-09: correct the older evaluator before final C scoring/publication, with invented regression inputs, preserved frozen history and clearly labelled corrected metrics.
- EVAL-07: score C once after planned behavior changes and identify the exact code/scorer version. Do not tune on its errors.
- UI-05: clearly distinguish provisional availability before coordinator testing/demo.
- Coordinator validation, matched human timing and truthful demonstration/write-up. Optional sponsor work must not displace core correctness or evidence.

7. Document every task and material lesson

Before handing work back:
- TASKS.md: actual task statuses, newly identified necessary work, IDs, priorities, acceptance criteria and dependencies.
- PROGRESS.md: dated outcomes, files/artifacts, checks actually run, results, not-run checks, limitations, blockers and next steps.
- context.md: material state, priorities, decisions and knowledge needed by the next agent.
- Relevant canonical docs: contracts, decisions, integrations, dated competition research and evaluation provenance.

Keep detail in its canonical home and link it. Do not leave material project knowledge only in chat. Do not mark planning as implementation, an attempt as success, an old check as fresh, or an optional backlog item as authorized work. Re-read changed docs and check their links.

8. Your first assignment

Perform a focused takeover audit and update the docs with a single defensible execution plan. Do not implement application features in this first pass or open/create/score set C.

Report:
1. Confirmed current state and any material discrepancies.
2. Your chosen priorities and why they best serve usefulness and the submission.
3. A concise decision table: keep / improve / defer / reject, with evidence and effort uncertainty.
4. One concrete next assignment: EVAL-01, including the separate writer brief, deliverables, isolation rules and completion criteria.
5. Remaining decisions genuinely requiring owner or organizer input.
6. Docs changed and checks actually performed.

Be candid and decisive. Do not merely repeat the existing docs, propose a long list of options without choosing, invent missing evidence, or ask me to approve routine planning choices. Take ownership of the reasoning and leave a clear, accurate handoff.
