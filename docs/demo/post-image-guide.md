# Availazy post: exact image placement and captions

Use [the full article draft](post-draft.md). Its six inline image positions now have HTML comments naming the local file, followed by the image and a ready-to-use italic caption. Those comments are editing instructions, not article copy.

There are **seven existing image files: one cover and six body images**. All are in [post/](post/). The optional Sentry image has not been captured.

## Put the article into DEV

1. Copy the article below the opening owner-checklist comment in `post-draft.md`. The front matter contains the title, tags, draft status and cover URL; if your DEV editor presents these as separate fields, fill those fields and paste the body starting with “This is a submission…”.
2. Use [cover.png](post/cover.png) as the cover. It is already 2000 × 840 (the same aspect ratio as 1000 × 420). Do not repeat the cover inside the article.
3. The draft already has each body image in the correct place. If uploading files into DEV, **replace** the corresponding existing image line with the Markdown returned by the upload. Keep the caption underneath. An upload goes where the cursor is; place it on the existing image line first.
4. **Verified 23 October 2026:** all seven GitHub image URLs return HTTP 200 with `image/png`, and their downloaded bytes match the local files. The current links are live; pushing images again is unnecessary. If you later change an image, push the changed file or upload that version into DEV. Local file paths will not display images for DEV readers. Preview the uploaded or linked version before publishing.

## Image-by-image placement

### Cover — cover.png

**File:** [cover.png](post/cover.png)

**Location:** the article's cover-image field, above the title/body. The front matter already specifies it as `cover_image`.

**What to show:** the existing “Volunteer chat in. Checked sheet out.” artwork, with Maria's messages and the reviewed Tuesday/Thursday/Friday example. This is designed cover artwork, not a screenshot of the export.

**Caption:** none.

### Body image 1 — landing.png

**File:** [landing.png](post/landing.png)

**Section:** What I Built.

**Insert immediately after:** “Availazy is a local review tool for the person who asks ‘when can you help?’ and then has to make sense of the answers.”

**Insert before:** “You paste dated chat messages…”

**What to show:** the landing page and its “Local AI for Coordinators Who Have Better Things to Do” headline. It introduces the product; the later app screenshots demonstrate the review workflow.

**Caption to paste below:**

*Availazy turns volunteer messages into suggestions you can review beside their source.*

### Body image 2 — maria-change-of-plans.png

**File:** [maria-change-of-plans.png](post/maria-change-of-plans.png)

**Section:** Gemma missed Maria's cancellation. That's the point.

**Insert immediately after:** “When the rules see a cancellation the model didn't, the app adds it, flagged, so I can check it:”

**Insert before:** “Until I accept it, the sheet shows Thursday as a pending change.”

**What to show:** Maria's original message on the left and all three suggestions on the right, including the amber “Added by the rules: possible cancellation the model missed” badge. Keep that badge readable. This screenshot shows the suggestion awaiting review, not a completed export.

**Caption to paste below:**

*Gemma found Tuesday and Friday. The rules added the Thursday cancellation for review.*

### Body image 3 — priya-after-3.png

**File:** [priya-after-3.png](post/priya-after-3.png)

**Section:** How I Built It, point 1: Gemma copies words; it doesn't do dates.

**Insert immediately after:** “Open ranges are code too. ‘After 3’ runs to 20:00, the end of the planning day, and the card says so:”

**Insert before:** point 2, “Every quote is checked against the message.”

**What to show:** Priya's message beside the Monday 15:00–20:00 suggestion, including the note that “after 3” runs to 20:00. The existing image also includes her Wednesday suggestion and its disagreement warning; keep the warning visible.

**Caption to paste below:**

*“After 3” becomes 15:00–20:00, with the assumption written on the card.*

### Body image 4 — changes-over-time.png

**File:** [changes-over-time.png](post/changes-over-time.png)

**Section:** How I Built It, point 3: History is kept in order.

**Insert immediately after:** the paragraph ending “taking out his Thursday evening and Saturday morning:”

**Insert before:** point 4, “When the words don't settle it, it asks.”

**What to show:** the existing timeline crop, with message links and the dated replacement/cancellation entries. It shows an excerpt beginning at m27, not the entire history.

**Caption to paste below:**

*An excerpt of the change history, with replacements and cancellations linked to their source messages.*

### Body image 5 — needs-a-decision.png

**File:** [needs-a-decision.png](post/needs-a-decision.png)

**Section:** How I Built It, point 4: When the words don't settle it, it asks.

**Insert immediately after:** “A name that matches nobody on the roster isn't guessed:”

**Insert before:** point 5, “The calm wrong answer.”

**What to show:** the Needs a decision panel, including “next Tuesday” with its two possible dates and the outside-the-week warning. The existing screenshot contains all ten listed items.

**Caption to paste below:**

*Ambiguous dates, unmatched names and unresolved conditions stay on the decision list.*

### Body image 6 — m48-wrong-person.png

**File:** [m48-wrong-person.png](post/m48-wrong-person.png)

**Section:** How I Built It, point 5: The calm wrong answer.

**Insert immediately after:** the paragraph ending “Only one of the two readers found this”:

**Insert before:** “One click on Reject and Maria's Tuesday is firm again.”

**What to show:** the sender **Marta Lopes** on the left and the incorrect **Maria Lopez** selection on the right, together with the warning and Reject button. Both names are the evidence; keep them readable. The screenshot shows the error before rejection.

**Caption to paste below:**

*Marta wrote the message, but Gemma assigned the offer to Maria. Reviewing the source makes the mistake visible.*

## Optional extra — a real Sentry trace

**Existing file:** none. This is an optional addition, not one of the seven existing files.

**Location:** in Built with, immediately after the Sentry Agent Tracing bullet and before the GitHub repository embed. The draft has an HTML comment marking this location.

**What to show:** a real, redacted trace with the model-call stage, duration and status visible. Exclude DSN, location values, volunteer names, message text, prompts and replies. Describe the one run that is actually visible; a single trace need not demonstrate both the timeouts and the later successful run.

**Caption template, filled only from the screenshot:**

*Sentry trace of a local model call: [visible duration], [visible status].*

Omit the image if no suitable screenshot is available. No substitute dashboard is needed.

### Capture the existing timeout trace (owner steps)

Use an existing recorded run; a new model run is unnecessary for this screenshot.

1. Sign in to the `availability-ledger` Sentry organization and select the actual project **python**.
2. Open **Insights → AI Agents** (or Agents in the available navigation), choose agent **availability-reader**, and set the date range to include **21 October 2026**. If that screen is unavailable, use the project's Traces view. Sentry's [Agent Monitoring walkthrough](https://sentry-build-ai.sentry.dev/debugging-ai-agent-monitoring/) documents the Insights/AI Agents navigation and the View Full Trace waterfall action; account-specific labels/access have not been freshly inspected.
3. Find the trace whose ID begins **c26d2afd**. Recorded identifying values: **26.93 min, 49 LLM calls, 4 errors**. Only its prefix is retained in the project records, so no full deep link is supplied.
4. Open it (use View Full Trace if needed), select one failed **gen_ai.chat** span at message position **37–40**, and show its duration of about **300 seconds** plus **TimeoutError/error status**. Keep `ollama` and `gemma4:e2b-it-qat` visible if they fit without unrelated attributes.
5. Close unrelated attribute/content panels. This historical trace previously displayed actual geo values, so keep those values, DSN, account/email, names, messages, prompts and replies outside the capture. On macOS, press **Command + Shift + 4** and drag a rectangle around the useful timeline and selected-call details. Use opaque redaction for anything sensitive still visible.
6. Rename the resulting PNG **sentry-timeout.png**. Once reviewed/redacted, place it in `docs/demo/post/` or upload it directly to DEV at the optional image position. That file has not yet been captured or added by the agent.

**Caption for that selected timeout span:**

*One local Gemma 4 call hit the 300-second client timeout. Sentry made the stalled call visible.*

Place it after the Sentry bullet in Built with, before the GitHub embed. If uploading, use DEV's returned image Markdown; a new local filename will not load from GitHub until that file is pushed.

**Alternative if the failed span is hard to find:** capture the Agents activity table with both recorded rows, **c26d2afd** (49 calls, 4 errors, 26.93 min) and **969d7ee9** (49 calls, 0 errors, 1.42 min). Caption: *Two recorded runs: 49 calls and four errors in the first; 49 calls and zero errors in the later retry.* This table alone does not show that the errors were timeouts or establish the reason for the stalls.

## Other placements already in the draft

- The YouTube embed belongs directly under Demo. Keep it as a video embed, not another screenshot.
- Keep the architecture flow, JSON, Python defaults, CSV excerpt and results tables as selectable text. They do not need image replacements.
- No final-sheet screenshot was retained. The existing CSV excerpt is the evidence for Maria's confirmed Tuesday/Friday rows and the provisional export.
