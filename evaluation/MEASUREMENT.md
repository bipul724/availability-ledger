# Measuring human effort (not yet done)

The 30% target is about **active human time at comparable final correctness**. Nothing in `evaluation/results/` measures human time. The "effort proxy" there counts clicks and typed fields; it does not count reading or checking, which probably dominate. This protocol is how to measure the real thing.

## Conditions

| Condition | What the person does | Output |
|---|---|---|
| Manual | Read the messages and type records into `fixtures/manual_entry_template.csv` (or the same columns in a spreadsheet), editing or deleting rows when people change their answers | CSV |
| Assisted | Open the app with suggestions already computed (the model's run time is unattended and reported separately), review until satisfied, export | CSV |
| Signup form | Not timed with volunteers. Time how long it takes to build a reusable form once. Then type in by hand only the answers that do not fit the form's checkboxes (`form_analysis` in the results lists them) | minutes + CSV |

## Before any timing (prerequisites, revised 2026-10-20)

The protocol below cannot produce a valid result yet. Two things must be fixed first:

1. **Equivalent final outputs.** The manual condition produces a final sheet; the app's export is a log of reviewed records. Both conditions must be scored on the same thing: a confirmed final sheet (TASKS COR-01).
2. **One scoring contract.** Both conditions must produce a **confirmed final-sheet CSV** in the format of [docs/specs/final-export.md](../docs/specs/final-export.md), scored by `evaluation/score_final.py` (TASKS EVAL-06). Provisional files are refused, and `needs_review` cells count as disagreement and are reported separately. The record-log scorer `evaluation/score_csv.py` sets `replaces_earlier` to false for every row (so "Tuesday 10-12" followed by "Tuesday 2-4 instead" scores as both ranges) and must not be used for timing.

Until then, human time saved stays **unmeasured**.

## Procedure

1. **Comparable workloads.** The two message sets must have the same number of messages and a similar mix of corrections, cancellations, conditions and ambiguities. Set A (50) and set B (20) are **not** comparable and must not be timed against each other. Split one set into two matched halves, or write a matched pair of new fictional sets (and ideally a consented, anonymised real week split the same way).
2. **Balanced order.** Each participant does one set manually and the other assisted. Half the participants start with manual, half with assisted, and the set used in each condition is swapped between them. One participant cannot balance order or set difficulty; a single person's result is a pilot of the procedure, not evidence for or against the target.
3. **Time active work only.** Start when the person first reads a message. Stop when they say the final sheet is done. Pause the timer for breaks. In the assisted condition the model runs before timing starts; report its run time separately. The app's own review timer and action counts are supporting data, not the measure.
4. **Score both outputs with the same, corrected code** (see prerequisites). Compare slot agreement, cancellations still on the final sheet, and condition errors.
5. **Decision rule (set before measuring).** Proceed only if, across participants, assisted active time is at most 70% of manual active time **and** assisted slot agreement is no more than 2 percentage points below manual. Report every participant's numbers, not only the average. If assisted review takes about as long as typing, simplify the review screen or stop.

## Record

For each condition record: who did it, the set used, the order, the active minutes, slot agreement, missed cancellations, condition errors and comments. Fictional sets measure the workflow mechanics only. Run at least one round on consented, anonymised real messages before claiming the tool saves time.
