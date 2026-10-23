# Fixes for the published DEV post (REL-05)

Checked 2026-10-23 against the live page: <https://dev.to/bipul_chamoli_09b5f0cc719/availazy-gemma-4-reads-the-volunteer-group-chat-on-my-laptop-python-does-the-dates-and-i-just-1nm8>

**What's fine:**
- The text matches the fact-checked draft; every key number is present.
- No placeholders or editor comments show.
- The YouTube and GitHub embeds render.
- The cover (2000 × 840) and all seven images load, and they are the right files in the right order.
- Tags include `hf26challenge`.
- It was published 2026-10-23T15:19Z (8:49 PM IST), before both possible deadlines.
- The Sentry screenshot is safe: no DSN, location values, names or message text.

**Applied by the owner and verified on 2026-10-23.** Two edits to make in DEV: Edit → change → Save. Both are optional, but each takes a minute.

## 1. Give every image real alt text

Every image currently renders with an empty alt (`alt=" "`), so screen readers skip it. In the editor, each image line looks like `![Image description](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/XXXX.png)`. Replace only the text inside `[...]`, in this order:

| # | Image (file id in your editor may differ) | Alt text to put inside `[...]` |
|---|---|---|
| 1 | landing page | `Availazy landing page: Local AI for Coordinators Who Have Better Things to Do` |
| 2 | Maria's change of plans | `Maria's "change of plans" message with three suggestions; the Thursday cancellation is marked "Added by the rules: possible cancellation the model missed"` |
| 3 | Priya after 3 | `Priya's "Monday after 3 works, and Wednesday afternoon" becomes Monday 15:00–20:00 and Wednesday 13:00–17:00, with the note "'after 3' runs to 20:00"` |
| 4 | changes over time | `Changes over time: replacements and cancellations in order, each linked to its message` |
| 5 | needs a decision | `Needs a decision list with ten items, including "next tuesday" sent on Monday 9 Nov could be 10 or 17 Nov, and a date outside the selected week` |
| 6 | m48 wrong person | `Marta Lopes's message, with the model's suggestion wrongly filed under Maria Lopez as conditional Tuesday and flagged "Only one of the two readers found this"` |
| 7 | Sentry trace | `Sentry Agent Activity timeline: four consecutive Gemma chat calls each last 5.00 minutes and end in error; the selected call's Input tab says "No input for this span"` |

## 2. Add a caption under the Sentry screenshot

Put this on its own line directly below the Sentry image (above `{% github bipul724/availability-ledger %}`):

```markdown
*One traced run: four Gemma calls in a row each hit the 5-minute client timeout. The selected call shows "No input for this span": no message text was sent.*
```

Every claim is visible in the screenshot itself: four consecutive `gemma4:e2b-it-qat chat` spans of 5.00m with error icons (5 minutes = the 300-second client timeout in `ledger/model.py`); `availability-reader`; and "No input for this span".

## Don't change

- Don't add claims about *why* the calls stalled; the traces don't show it.
- Don't add a time-saved number; none has been measured.
