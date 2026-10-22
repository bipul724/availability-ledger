# BRAND-01: rebrand Availability Ledger to Availazy

## Owner-approved name and scope

The owner selected this public identity:

- Product name: **Availazy**
- Exact headline/tagline: **Local AI for Coordinators Who Have Better Things to Do**
- Full presentation: **Availazy — Local AI for Coordinators Who Have Better Things to Do**

Implement this branding change in the existing project. This is a presentation/documentation change, not a rewrite or new product scope. Keep the current design and application behavior. Do not ask the owner to reconfirm this selected name.

## Start with the current checkout

Repository: `/Users/bipulchamoli/Desktop/week 3/availability-ledger`.

Read `AGENTS.md`, `context.md`, `CLAUDE.md`, `TASKS.md`, relevant current UI docs, and `docs/SENTRY_HANDOFF.md`. Check `git status` and inspect the actual files first. There is existing uncommitted work, including the landing page/guide/404 changes; preserve it and do not reset, overwrite, stage or revert unrelated work. Do not rely on older handoffs that describe only one page.

Current routes/pages observed when this brief was written:

- `/`: `ui/home.html`, `ui/home.css`, `ui/home.js`.
- `/app`: review app in `ui/index.html`, `ui/style.css`, `ui/app.js`.
- `/docs`: `ui/docs.html`, `ui/docs.css`.
- Unknown paths: `ui/404.html`.

Recheck routing in `server.py`; preserve `/`, `/app`, `/docs`, API/static routes and the existing local/replay behavior.

## Branding changes

1. Update visible current-product branding across landing page, app, guide and 404: navigation, footer, browser titles, title/ARIA labels, descriptive metadata/Open Graph text and the illustrated app/browser preview where applicable. Update server startup display strings, README product introduction and demo/narration script references. Search for other current user-facing occurrences instead of replacing only `<h1>`.
2. Use **Availazy** as the short wordmark and compact app title. Make the exact approved headline prominent in the landing hero and README. Keep it as separate readable text where a combined title would be too long. Other pages may use short titles such as `Guide · Availazy` and `Not found · Availazy`.
3. Retain the existing typography, colors, layout, glyph/favicon and UI interactions. Only make small spacing/wrapping changes needed for the longer headline. No new visual redesign, mascot, generated images, dependencies, CDN or analytics. Check light/dark themes and phone widths; navigation and primary actions must remain visible without horizontal overflow.
4. Keep the product philosophy accurate: local Gemma suggests phrases, ordinary code checks/reconciles dates and history, and a person reviews. It records **availability**, not shift assignments. Optional supporting line: “Let AI read. You decide.” Do not replace the owner's approved headline with that line.
5. Retain warnings, pending/provisional states, source quotes, accepted-only final export and the clear fictional saved-output replay label. Do not turn rebranding into new claims of accuracy, guaranteed trust, automatic scheduling, measured time saved, unlimited free service or blanket privacy. Messages/model inference stay local in the core workflow; optional Sentry metadata leaves the machine when enabled. Use the existing Sentry handoff for the verified privacy scope.

## Intentional identifiers to preserve

Do not globally replace every lowercase `availability-ledger` string. Leave these operational interfaces/identifiers unchanged:

- GitHub repository/clone URL and checkout directory: `bipul724/availability-ledger`.
- Render service name/hostname, `render.yaml` service identity and existing published links: `availability-ledger-replay.onrender.com` (the replay is at `/app`). Do not rename/redeploy remote resources.
- Sentry organization `availability-ledger`, project `python`, agent `availability-reader`, release `availability-ledger-tracing@1`, env variable `SENTRY_DSN` and existing trace history. Do not touch tracing allowlists or version/identifiers for a copy change.
- Python `ledger` modules, API routes, request/response keys, environment variables, internal DOM IDs/JS selectors and file paths unless a display-only change truly requires it and is verified.
- CSV filenames, headers, metadata/version markers such as `availability-final v1`, parsers and export contracts. Sample CSV/fixture content stays exact.
- Fixtures, references, `fixtures/setC.manifest`, saved model outputs, `evaluation/results/frozen/`, `frozen-setC/`, `tuning/`, `evaluation/runs/`, and `SYSTEM`/`EXAMPLES`/`PROMPT_VERSION` in `ledger/model.py`.
- Historical PROGRESS/decision records, old screenshots/attachments, evidence names, trace IDs and old results. Record that the app was formerly Availability Ledger; do not rewrite history to pretend earlier artifacts were already branded Availazy.

Do not rename accounts, create a domain, add payment/PAYG, install/download, make fresh model calls, send Sentry events, change application semantics, publish, deploy, commit or push. No secrets/DSN inspection. The owner handles commits and external publication/deployment separately.

## Documentation and checks

- Update BRAND-01 in TASKS and add a dated PROGRESS outcome. Update current README/context and affected present-tense docs so the new public name is discoverable; preserve historical records and technical identifiers. Distinguish implementation verified locally from changes actually deployed.
- Run appropriate **existing** unit/page/browser checks from TESTING; report actual results. The existing landing/guide/404 checks are relevant. If a test expects the old display name, update only that presentation expectation; do not weaken behavioral assertions. Do not add tests that merely mirror a string replacement. Keep checks offline, tracing disabled and without fresh model calls. Do not read/print secrets to disable tracing.
- Inspect `/`, `/app`, `/docs` and a 404 locally at desktop and phone width (about 390 px), in supported light/dark themes. Verify title/headline wrapping, visible branding, unchanged links/routes/actions, replay labels and no horizontal overflow. Keep existing screenshots/protected artifacts untouched.
- Search remaining old-name occurrences and classify each as intentional identifier/history or a missed current brand reference. Do not remove legitimate old names simply to make the search empty. Review the diff and run `git diff --check`.
- Report changed files, exact branding used, intentional retained identifiers, checks actually run and their outcomes, and any unverified/live-deployment limits. Make the result reviewable; do not commit/push/deploy it.

## Acceptance

All four current pages, relevant metadata, startup display and current project introduction/script consistently identify **Availazy**. The landing/README use the exact approved headline. Existing user workflows and data/evaluation contracts are unchanged. The long headline works on phone and desktop. Historical/service identifiers remain truthful. Documentation and actual check results are current, with no claim that the live site has changed before an owner deploy.
