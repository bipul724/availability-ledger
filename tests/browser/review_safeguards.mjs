// Optional browser regression check for COR-10 (D-30) and COR-07a (not part of `python3 -m unittest`): a suggestion
// whose day or time words are not in its message still counts provisionally, keeps its flag and is listed as a
// non-blocking wording check; it reaches the final export only once accepted. A change word on a day with open time
// but no matching suggestion is listed as a possible missed change. Invented messages; the two
// suggestions that need inventing are stubbed in the page, the rest come from the rules reader (no model calls).
//   node tests/browser/review_safeguards.mjs      # from the project folder; Node 22+ and Chrome
import { openApp, sleep } from "./harness.mjs";

const app = await openApp(8773, 9341);
const { js, check, setInputs, suggest, exportFinal } = app;
const sheetCell = (date) => js(`(() => { const col = [...document.querySelectorAll("#sheet th")].findIndex((th) => th.dataset.date === "${date}");
  const tr = [...document.querySelectorAll("#sheet tr")].find((r) => r.cells[0]?.innerText.trim() === "Ana Example");
  return tr && col > 0 ? tr.cells[col].innerText.replace(/\\s+/g, " ").trim() : null; })()`);
const issues = () => js(`document.getElementById("issues").innerText`);

await js(`window.__stubs["/api/suggest"] = (b) => ({
  m02: { status: 200, json: { stats: {}, claims: [{ id: "m02.1", msg: "m02", n: 1, source: "model", review: "pending",
         said: { person: "SENDER", day_text: "Tuesday", time_text: "2-4", status: "available", condition: "",
                 replaces_earlier: false, excerpt: "Happy to help" } }] } },
  m03: { status: 200, json: { stats: {}, claims: [] } },
})[b.message.id]`);
await setInputs(["2026-11-02 09:00 | Ana Example | Thursday 9-12 works",
  "2026-11-03 09:00 | Ana Example | Happy to help",
  "2026-11-04 18:00 | Ana Example | Sorry, I have to cancel Thursday"].join("\n"), "2026-11-09");
await suggest();

const card = await js(`document.querySelector('.card[data-id="m02.1"]')?.innerText || ""`);
check(/Some words are not in this message/.test(card) && !/not counted until/.test(card), "flagged suggestion keeps its warning badge (not held)");
check(/14:00\s*–\s*16:00/.test(await sheetCell("2026-11-10")) && /pending/.test(await sheetCell("2026-11-10")),
  "flagged suggestion counts on the provisional sheet as pending: " + JSON.stringify(await sheetCell("2026-11-10")));
const open = await issues();
check(/Check the wording: Ana Example: some day or time words are not in this message/.test(open), "Needs a decision lists it as a wording check");
check(/Possible missed change: Possible change not applied \(m03 mentions Thu 12 Nov\)/.test(open), "Needs a decision lists the possible missed change");
check(/09:00\s*–\s*12:00/.test(await sheetCell("2026-11-12")), "the warning does not edit the sheet: " + await sheetCell("2026-11-12"));
check(await js(`!document.querySelector('button[data-act="accept-mark"][data-msg="m02"]')`), "no 'Accept all and mark reviewed' for the flagged suggestion");
for (const m of ["m01", "m02", "m03"]) { await js(`document.querySelector('button[data-act="mark"][data-msg="${m}"]').click()`); await sleep(400); }
let fin = await exportFinal();
check(!/2026-11-10,14:00/.test(fin.text) && /status=provisional; unreviewed=; pending=/.test(fin.text),
  "final export leaves it out while pending (provisional only because it is pending): " + fin.text.split("\n")[0]);

await js(`document.querySelector('.card[data-id="m02.1"] button[data-act="accept"]').click()`); await sleep(600);
check(/14:00\s*–\s*16:00/.test(await sheetCell("2026-11-10")) && !/Check the wording/.test(await issues()), "accepting clears the wording check");
await js(`document.querySelector('.card[data-id="m01.1"] button[data-act="accept"]').click()`); await sleep(600);
fin = await exportFinal();
check(/2026-11-10,14:00,16:00,available,,confirmed,m02.1/.test(fin.text) && /status=complete/.test(fin.text),
  "once accepted it is in the final export, and the open change warning does not block a complete file: " + fin.text.split("\n")[0]);
// COR-18 (D-32): a replacement caused only by a change word in the message is listed for review; the sheet follows COR-15.
await js(`window.__stubs = {}`);
await setInputs(["2026-11-02 09:00 | Ana Example | Wednesday 10-12", "2026-11-04 09:00 | Ana Example | help move tables Wednesday 6-8 too"].join("\n"), "2026-11-09");
await suggest();
const cueIssues = await issues();
check(/Earlier answer replaced — check: Ana Example Wed 11 Nov: m02 contains a change word, so it replaced the earlier answer \(10:00-12:00 available\)/.test(cueIssues),
  "a cue-only replacement is listed with the removed time: " + cueIssues.split("\n").find((l) => /replaced/.test(l)));
check(/18:00\s*–\s*20:00/.test(await sheetCell("2026-11-11")) && !/10:00/.test(await sheetCell("2026-11-11")), "the warning does not change the sheet (COR-15 replacement stands)");

check(app.problems.length === 0, "no console errors or exceptions: " + JSON.stringify(app.problems));
app.done();
