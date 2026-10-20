// Optional browser regression check for COR-03 (not part of `python3 -m unittest`): a message whose
// /api/suggest request fails, or whose model reply is unreadable (json_ok: false), gets a visible warning;
// reading continues with the next message and the run reports a failure count. Invented messages only;
// failures are stubbed in the page, real responses come from the rules reader (no model calls).
//   node tests/browser/extraction_failures.mjs      # from the project folder; Node 22+ and Chrome
import { openApp, sleep } from "./harness.mjs";

const app = await openApp(8768, 9336);
const { js, check, setInputs, suggest, exportFinal } = app;
const row = (id) => js(`document.getElementById("row-${id}")?.innerText || ""`);

// An earlier, fully reviewed session for another week: none of its approvals may survive.
await setInputs("2026-11-03 09:00 | Ana Example | Tuesday 10-12 works", "2026-11-09");
await suggest();
await js(`document.querySelector('button[data-act="accept-mark"][data-msg="m01"]').click()`); await sleep(500);

// New week: success, request failure, success, unreadable reply with hybrid rules output, unreadable reply.
const week = [
  "2026-11-16 08:00 | Ana Example | Tuesday 10-12 works",
  "2026-11-16 09:00 | Ben Example | Wednesday after 3",
  "2026-11-16 10:00 | Ben Example | Friday 9-12 is fine",
  "2026-11-16 11:00 | Ana Example | Sorry, can't do Thursday",
  "2026-11-16 12:00 | Ana Example | Saturday maybe",
].join("\n");
await js(`window.__stubs["/api/suggest"] = (b) => ({
  m02: { status: 400, json: { error: "URLError: simulated model timeout" } },
  m04: { status: 200, json: { stats: { json_ok: false }, claims: [{ id: "m04.1", msg: "m04", n: 1, source: "rules",
         review: "pending", hints: ["added_by_rules"], said: { person: "SENDER", day_text: "Thursday", time_text: "",
         status: "unavailable", condition: "", replaces_earlier: false, excerpt: "can't do Thursday" } }] } },
  m05: { status: 200, json: { stats: { json_ok: false }, claims: [] } },
})[b.message.id]`);
await setInputs(week, "2026-11-16", "Asia/Kolkata");
await suggest();

const st = JSON.parse(await js(`JSON.stringify({ week: state.week, tz: state.tz, read: state.read.size,
  reviewed: state.reviewed.size, claims: state.claims.map((c) => [c.msg, c.review]) })`));
const progress = await js(`document.getElementById("progress").textContent`);
check(st.read === 5, "reading continued after the failure: 5 of 5 messages read");
check(/3 of 5 messages could not be read fully/.test(progress), "run reports the failure count: " + progress);
check(/3 messages could not be read fully/.test(await js(`document.getElementById("review-state").textContent`)), "failure count stays visible above the list");
check(/Could not read this message \(URLError: simulated model timeout\)/.test(await row("m02")) && !/No availability found/.test(await row("m02")),
  "request failure: warning instead of 'No availability found'");
check(/model's reply for this message could not be read\. Only the rules' cancellations below were added/.test(await row("m04")),
  "unreadable reply with hybrid rules output: warning names the rules-only suggestions");
check(/model's reply for this message could not be read, so it has no suggestions/.test(await row("m05")) && !/No availability found/.test(await row("m05")),
  "unreadable reply with no suggestions: warning instead of 'No availability found'");
check(!/could not be read/.test(await row("m01") + await row("m03")), "successful messages carry no warning");
const fromMsgs = [...new Set(st.claims.map((c) => c[0]))].sort().join(" ");
check(fromMsgs === "m01 m03 m04", "claims from successful messages (and the rules output) retained: " + fromMsgs);
check(st.week === "2026-11-16" && st.tz === "Asia/Kolkata" && st.reviewed === 0 && st.claims.every((c) => c[1] === "pending"),
  "new week and settings committed; no old approvals carried over");
check(await js(`!document.querySelector('button[data-act="accept-mark"][data-msg="m04"]') && !document.querySelector('button[data-act="accept-mark"][data-msg="m05"]')
  && !!document.querySelector('button[data-act="accept-mark"][data-msg="m01"]')`), "no 'Accept all and mark reviewed' on failed messages");
const exp = await exportFinal();
check(exp.name === "availability-final-2026-11-16-provisional.csv" && exp.text.includes("unreviewed=m01 m02 m03 m04 m05;"),
  "export is provisional while messages remain unreviewed");

// COR-11 still holds: a later parse failure keeps this session, warnings included.
const before = await js(`JSON.stringify([state.week, state.claims, [...state.failures.keys()]])`);
await js(`window.__stubs["/api/parse"] = () => ({ status: 400, json: { error: "simulated parse failure" } })`);
await setInputs(week, "2026-11-23", "Europe/London");
await suggest();
check((await js(`JSON.stringify([state.week, state.claims, [...state.failures.keys()]])`)) === before
  && /Could not read this message/.test(await row("m02")), "parse failure afterwards keeps the session and its warnings");

// A clean re-run clears the warnings.
await js(`window.__stubs = {}`);
await setInputs(week, "2026-11-16", "Asia/Kolkata");
await suggest();
check(!/could not be read/.test(await js(`document.getElementById("rows").innerText`)) && (await js(`state.failures.size`)) === 0
  && !/could not be read/.test(await js(`document.getElementById("progress").textContent`)), "a clean re-run clears failures");
check(app.problems.length === 0, "no console errors or exceptions: " + JSON.stringify(app.problems));
app.done();
