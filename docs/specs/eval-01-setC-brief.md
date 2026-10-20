# EVAL-01 brief: write and freeze unseen set C

**Status:** brief ready (2026-10-20, project lead). Set C does not exist yet. This brief describes the work; it does not record it as done.
**Decision basis:** [D-24](../DECISIONS.md#d-24-set-c-is-frozen-outside-the-public-repository) (C stays outside the repository until scoring), [D-10](../DECISIONS.md#d-10-synthetic-evaluation-with-frozen-held-out-sets).

## Why this exists

Sets A and B have both shaped the code (see [TUNING.md](../../evaluation/TUNING.md)), so neither can test the next changes independently. Set C is the only data that can, and it is only useful if nobody working on behaviour code has seen it before it is scored once (EVAL-07).

## Roles and isolation

| Role | Who | May see C? |
|---|---|---|
| **Writer** | The project owner (a human). The writer must not be an AI that has worked on this project. | Yes: writes it. |
| **Steward** (optional helper) | A **new** Claude session started only for this task: no project history, not used before or afterwards for planning, briefs or code in this project. It turns the writer's notes into JSON and checks consistency. | Yes |
| Project lead (planning session) | Claude in the planning role | **No.** Receives only the manifest and the counts in "Completion" below. |
| Implementation agents | Any coding agent | **No.** Never search for, open or ask about C. |

Rules for everyone who sees C:
- Store it only in `~/Documents/availability-setC/`, outside `Desktop/week 3` and outside every git repository. The GitHub repository is **public**, so C must not be committed, not even temporarily.
- Do not upload C anywhere: no cloud drives, chat tools, issues or other AI services. The steward session is the only exception.
- Do not run the app, the model, the rules reader or any scorer on C messages. Scoring happens once, in EVAL-07.
- Do not describe C's contents or its difficult cases to the lead or to implementation agents, in chat or in docs.

## What to write

**Setting:** one fictional organisation, not a pantry or a tool library, and **not** based on sets A or B. Do not read `fixtures/riverside_week.txt` or `fixtures/setB_toolshed.txt` first.

| Item | Requirement |
|---|---|
| Planning week | Monday **2026-11-23** to Sunday **2026-11-29**. Timezone label `Asia/Kolkata` (labels only; the app reads times as local wall-clock). |
| Messages | **At least 20, target 24**, dated from about 2026-11-16 to 2026-11-26, in time order. |
| Volunteers | 10–15 fictional people on the roster (at most 20), plus one coordinator who is **not** on the roster and whose sender name contains "coordinator". |
| Wording | Your own natural phrasing, the way real volunteers text. Vary it. Don't copy example sentences from any project doc. |
| Fiction | No real people, phone numbers or private details. Invent everything. |

**Minimum coverage** (one message can cover several items):

| Situation | At least |
|---|---|
| Cancellation of an earlier offer, each phrased differently | 4 |
| Correction that changes hours or the day | 2 |
| Partial availability (odd hours, "after X", "until Y") | 3 |
| Conditional offer | 2, with one settled by a later message |
| Exact duplicate message (same sender, same text, within 24 h) | 1 |
| Two roster names that look alike | 1 pair, used in messages |
| Message about someone else ("my brother can…", a forwarded note) | 1 |
| Day that cannot be settled from the message and its date | 1 (e.g. "next <weekday>" sent where it could mean two dates) |
| Day outside the planning week | 1 |
| Not about availability (logistics, thanks, a question) | 3 |

## Files to produce (in `~/Documents/availability-setC/`)

1. `setC_messages.txt`: the same line format as the existing fixtures:
   ```
   # FICTIONAL TEST SET C. <organisation> does not exist; every name, message and event is invented.
   # Selected week: Monday 2026-11-23 to Sunday 2026-11-29, timezone Asia/Kolkata.
   # Format: YYYY-MM-DD HH:MM | Sender | Message
   2026-11-16 09:00 | Sam (coordinator) | ...
   ```
   Message IDs are assigned by time order: the first message is `m01`, the second `m02`, and so on. Avoid two messages with the same timestamp.
2. `setC_roster.txt`: one volunteer name per line, with a fictional header comment.
3. `setC_notes.md` (the writer's plain notes): for each message ID, what a careful coordinator should conclude: who, which day(s), which hours, and available / unavailable / conditional (with the condition), or "nothing". Mark anything genuinely unclear as unclear, with the possible answers.
4. `setC_reference.json`: the steward converts the notes into the **same schema as `fixtures/reference.json`**. Copy the `conventions` block verbatim from that file and apply it where wording leaves hours unstated (e.g. "morning" = 09:00–12:00; an available day with no hours and no earlier answer = 09:00–20:00). Set `"split": {"heldout": [every message id]}`. Include `withdrawals`, `conditions`, `ambiguities` and `expected_sheet` exactly as in that file. Give duplicates the same claims as their original and the category `"duplicate"`.

When the notes and the conventions disagree, the steward records the disagreement in `setC_notes.md` and the writer decides. **Never change an answer to make it easier for the software.**

## Steward's consistency checks (no scoring)

Do these in a **private copy** of the code, never in the project folder:

```bash
mkdir -p ~/Documents/availability-setC/code
git -C "/Users/bipulchamoli/Desktop/week 3/availability-ledger" archive HEAD | tar -x -C ~/Documents/availability-setC/code
```

Then, inside `~/Documents/availability-setC/code`, copy the three set C files into its `fixtures/` folder. Add a `"C"` entry to `SETS` in that copy's `evaluation/fixture.py`. Check:
- the reference JSON loads;
- every person is on the roster or listed as an unresolved candidate;
- every date is inside the week or recorded as outside/ambiguous with candidates;
- the reference claims replayed through `ledger.core.build_ledger` reproduce `expected_sheet` (the same check `tests/test_ledger.py` runs for A and B).

This checks the reference, not any reader. Do **not** run `evaluation.run`, the model, the rules or the app. Delete the private code copy afterwards.

## Freeze (the only thing that enters the repository now)

From `~/Documents/availability-setC/`:

```bash
shasum -a 256 setC_messages.txt setC_roster.txt setC_reference.json > setC.manifest
```

Copy `setC.manifest` into the project as `fixtures/setC.manifest` and commit only that file:

```bash
git add fixtures/setC.manifest && git commit -m "test(fixtures): freeze unseen set C by hash (contents held outside the repo)"
```

## Completion: what the lead receives

- The commit hash of the manifest commit.
- Counts only: number of messages, volunteers and reference units, and the number of items in each coverage row above.
- A yes/no statement that every isolation rule was followed, plus anything that went wrong (for example, a file opened in the wrong place).

EVAL-01 is **done** when that is recorded in [PROGRESS.md](../../PROGRESS.md) and [TASKS.md](../../TASKS.md). Until then, no further behaviour change starts.

## At EVAL-07 (later, once)

1. After the planned changes land, copy the three files into `fixtures/` and verify them with `shasum -a 256 -c fixtures/setC.manifest`. A mismatch stops the run.
2. Add set C to `evaluation/fixture.py`.
3. Score rules, Gemma and Gemma + rules once. Qwen is optional.
4. Record the exact commit and scorer version, copy the results to `evaluation/results/frozen-setC/`, and commit C at that point.
5. Do not tune on its errors afterwards.

**Time box:** about 1.5 h for the writer and 45 min for the steward.
