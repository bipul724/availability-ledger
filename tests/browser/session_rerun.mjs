// Optional browser regression check (not part of `python3 -m unittest`): a failed or rejected
// "Suggest records" must leave the previous reviewed session, and its final-sheet export, unchanged;
// a successful run must start a fresh session. Invented messages only.
//   node tests/browser/session_rerun.mjs            # from the project folder; Node 22+ and Chrome
import { openApp, sleep } from "./harness.mjs";

const app = await openApp(8767, 9335);
const { js, check, setInputs, suggest, exportFinal } = app;
const session = () => js(`JSON.stringify({ week: state.week, tz: state.tz, messages: state.messages, roster: state.roster,
  claims: state.claims, reviewed: [...state.reviewed].sort() })`);

// 1. A fully reviewed session for the week of 9 Nov.
await setInputs("2026-11-03 09:00 | Ana Example | Tuesday 10-12 works\n2026-11-04 09:00 | Ana Example | Thanks, see you then!", "2026-11-09");
await suggest();
await js(`document.querySelector('button[data-act="accept-mark"][data-msg="m01"]').click()`); await sleep(500);
await js(`document.querySelector('button[data-act="mark"][data-msg="m02"]').click()`); await sleep(500);
const base = await exportFinal(), baseSession = await session();
check(base.name === "availability-final-2026-11-09-complete.csv" && base.text.includes("status=complete"), "baseline export is complete for 2026-11-09");

// 2. Failed reruns must change nothing: parse error, non-Monday week, input with no messages.
const attempts = [
  ["parse failure for a new week", async () => {
    await js(`window.__stubs["/api/parse"] = () => ({ status: 400, json: { error: "simulated parse failure" } })`);
    await setInputs("2026-11-17 09:00 | Ben Example | Friday after 3", "2026-11-16", "Asia/Kolkata");
  }],
  ["non-Monday week", async () => {
    await js(`delete window.__stubs["/api/parse"]`);
    await setInputs("2026-11-17 09:00 | Ben Example | Friday after 3", "2026-11-17", "Asia/Kolkata");
  }],
  ["input with no dated messages", async () => { await setInputs("no dates here", "2026-11-16", "Asia/Kolkata"); }],
];
for (const [label, prepare] of attempts) {
  await prepare();
  await suggest();
  const progress = await js(`document.getElementById("progress").textContent`);
  check((await session()) === baseSession, `${label}: previous session kept (${progress})`);
  const again = await exportFinal();
  check(again.name === base.name && again.text === base.text, `${label}: export identical to before (${again.name})`);
}

// 3. A successful run commits the new week and settings together and starts review afresh.
await setInputs("2026-11-17 09:00 | Ben Example | Friday after 3", "2026-11-16", "Asia/Kolkata");
await suggest();
const fresh = JSON.parse(await session());
check(fresh.week === "2026-11-16" && fresh.tz === "Asia/Kolkata" && fresh.messages.length === 1
  && fresh.messages[0].text === "Friday after 3" && fresh.reviewed.length === 0
  && fresh.claims.every((c) => c.msg === "m01" && c.review === "pending"), "successful run starts a fresh session for 2026-11-16");
const next = await exportFinal();
check(next.name === "availability-final-2026-11-16-provisional.csv" && next.text.includes("unreviewed=m01;"),
  "new session export is provisional with nothing carried over: " + next.name);
check(app.problems.length === 0, "no console errors or exceptions: " + JSON.stringify(app.problems));
app.done();
