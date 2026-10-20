# Measuring human effort (not yet done)

The 30% target is about **active human time at comparable final correctness**. Nothing in `evaluation/results/` measures human time. The "effort proxy" there counts clicks and typed fields; it does not count reading or checking, which probably dominate. This protocol is how to measure the real thing. The sponsor portfolio does not change the correctness target or constitute evidence of human benefit; see [INTEGRATIONS.md](../docs/INTEGRATIONS.md).

## Conditions

| Condition | What the person does | Output |
|---|---|---|
| Manual | Read the messages and type the **final** sheet into `evaluation/final_sheet_template.csv` (or the same columns in a spreadsheet): one row per available or conditional time range per person and day, after all corrections and cancellations | final-sheet CSV |
| Assisted | Open the app with suggestions already computed (the model's run time is unattended and reported separately), review, mark every message reviewed, then **Export final sheet (CSV)** | final-sheet CSV |
| Signup form | Not timed with volunteers. Time how long it takes to build a reusable form once. Then type in by hand only the answers that do not fit the form's checkboxes (`form_analysis` in the results lists them) | minutes + CSV |

## Before any timing (prerequisites, revised 2026-10-20)

Two prerequisites, both **in place since 2026-10-20** (COR-01, EVAL-06):

1. **Equivalent final outputs.** Both conditions hand in a final-sheet CSV: the assisted condition with **Export final sheet (CSV)**, the manual condition by filling `evaluation/final_sheet_template.csv` (set `week=` to the set's Monday; mark uncertain cells `needs_review`, which makes the file provisional).
2. **One scoring contract.** Both conditions must produce a **confirmed final-sheet CSV** in the format of [docs/specs/final-export.md](../docs/specs/final-export.md), scored by `evaluation/score_final.py` (TASKS EVAL-06). Provisional files are refused, and `needs_review` cells count as disagreement and are reported separately. The record-log scorer `evaluation/score_csv.py` sets `replaces_earlier` to false for every row (so "Tuesday 10-12" followed by "Tuesday 2-4 instead" scores as both ranges) and must not be used for timing.

Human time saved stays **unmeasured** until the procedure below has actually been run. `score_final.py` includes the partial-condition-loss fix; the older ledger metric in `evaluation/run.py` still needs EVAL-09 and is not a substitute for this scorer.

The parser/scorer checks file structure and availability/conditional slot states, not the semantic truth of condition text or whether a reviewer genuinely read the messages. Record these limitations and inspect meaningful conditions separately; do not describe a perfect synthetic slot score as a guarantee of safe scheduling.

## Procedure

1. **Comparable workloads.** The two message sets must have the same number of messages and a similar mix of corrections, cancellations, conditions and ambiguities. Set A (50) and set B (20) are **not** comparable and must not be timed against each other. Split one set into two matched halves, or write a matched pair of new fictional sets (and ideally a consented, anonymised real week split the same way).
2. **Balanced order.** Each participant does one set manually and the other assisted. Half the participants start with manual, half with assisted, and the set used in each condition is swapped between them. One participant cannot balance order or set difficulty; a single person's result is a pilot of the procedure, not evidence for or against the target.
3. **Time active work only.** Start when the person first reads a message. Stop when they say the final sheet is done. Pause the timer for breaks. In the assisted condition the model runs before timing starts; report its run time separately. The app's own review timer and action counts are supporting data, not the measure.
4. **Score both outputs with the same, corrected code** (see prerequisites). Compare slot agreement, cancellations still on the final sheet, and condition errors.
5. **Decision rule (set before measuring).** Proceed only if, across participants, assisted active time is at most 70% of manual active time **and** assisted slot agreement is no more than 2 percentage points below manual. Report every participant's numbers, not only the average. If assisted review takes about as long as typing, simplify the review screen or stop.

## Sponsor evidence and data boundaries

- A public Render demonstration is planned as an **interactive fictional replay of saved model outputs**, not a live inference benchmark or a timed participant study. Label its reader/output mode, code version and saved-output provenance. Public demo interaction counts and video narration do not measure human time saved.
- Sentry spans, if an optional opt-in integration is later approved and built, may explain latency/failures on fictional demonstrations. Traces, Copilot/Actions results, Entire checkpoints and Backboard R-CLI process evidence do not establish extraction accuracy, independent evaluation or coordinator usefulness. No such integration exists today other than core Gemma use.
- A real-message pilot requires written owner confirmation of consent and prior anonymisation, storage outside version control and local-only processing. Never copy pilot messages, names, conditions, quotes or replies into public hosting, screenshots, narration, telemetry, agent-session publication, development logs or remote agent tools. Report only approved aggregate outcomes.
- All studies must preserve the ₹0 additional-spend rule; no participant purchase, paid fallback or service overage is authorized by this protocol.

## Fresh evaluation gate

Freeze at least 20 new fictional set C messages and a handwritten reference, unscored and committed, before further behavior changes (EVAL-01). Implementation agents must not open those contents. Use separately invented development examples, then score C once after the planned changes with the exact code version recorded (EVAL-07). Set C is not present today and neither this protocol nor a sponsored demonstration creates it. Do not convert the known A/B post-hoc results into independent evidence. See [TASKS.md](../TASKS.md#evaluation-and-validation) for the current gate and dependencies.

## Record

For each condition record: who did it, the set used, the order, the active minutes, slot agreement, missed cancellations, condition errors and comments. Fictional sets measure the workflow mechanics only. Run at least one round on consented, anonymised real messages before claiming the tool saves time.
