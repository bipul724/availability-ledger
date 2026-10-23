# Start here: instructions for all agents

Read [context.md](context.md), then [CLAUDE.md](CLAUDE.md), before planning or changing the project. CLAUDE.md is the canonical detailed agent guide; this file is its discovery entry point.

- Product requirements: [docs/PRD.md](docs/PRD.md).
- Current implementation and evidence: [PROGRESS.md](PROGRESS.md); source wins over prose.
- Next work and prerequisites: [TASKS.md](TASKS.md). Set C has been frozen and scored once (2026-10-21); its frozen results are protected and all later changes are post-hoc. Test status and commands: [TESTING.md](TESTING.md).
- Agreed technology roles, scope and evidence gates: [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md).
- Verified competition rules, historical research, recommendations and unknowns: [docs/COMPETITION.md](docs/COMPETITION.md).
- Architecture/API: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/API.md](docs/API.md).
- Decisions: [docs/DECISIONS.md](docs/DECISIONS.md).

Current implementation includes Gemma for local phrase extraction, GitHub Actions for CI, a hosted fictional Render replay and optional Sentry tracing. These roles are distinct; they do not establish use of Copilot coding agents, Entire or dropped ElevenLabs narration. Category targets remain subject to owner eligibility and actual evidence. A docs/planning request does not authorize installing tools, changing application behavior or configuration, sending private data, claiming credits, deploying or publishing. Follow the owner's actual scope and existing session authorization.

Preserve private data boundaries, accepted-only export, human review, frozen evidence and the additional ₹0 budget. Recheck current status rather than assuming every planned integration is present.

Documentation inventory and the latest file-by-file review are in [docs/DOCUMENTATION_AUDIT.md](docs/DOCUMENTATION_AUDIT.md). Archived handoffs and dated implementation prompts preserve history; they are not current work orders. Use the current context, task status and superseding decisions before acting.

## Mandatory task documentation

The owner requires every project task completed, attempted or newly identified to be recorded in the docs. Keep TASKS.md current, record outcomes and verification in PROGRESS.md, and refresh context.md plus affected detailed contracts when knowledge changes. Do this before handing work back; follow CLAUDE.md for the required fields. New backlog items do not authorize implementation.
