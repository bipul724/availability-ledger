// Optional browser regression check for COR-02 (not part of `python3 -m unittest`): both CSV exports write
// cells that start with = + - @ (or tab/CR) with a leading apostrophe, so spreadsheets do not run them.
// Invented messages; rules reader only (no model calls).
//   node tests/browser/csv_safety.mjs               # from the project folder; Node 22+ and Chrome
import { openApp, sleep } from "./harness.mjs";

const app = await openApp(8769, 9337);
const { js, check, setInputs, suggest, exportFinal, exportLog } = app;

await setInputs("2026-11-03 09:00 | =Eve Example | =1+1 Tuesday 10-12 works", "2026-11-09", "Europe/London", "=Eve Example\\nBen Example");
await suggest();
await js(`document.querySelector('button[data-act="accept-mark"][data-msg="m01"]').click()`); await sleep(500);
const log = await exportLog(), fin = await exportFinal();
const logRow = log.text.split("\n")[1] || "";
check(logRow.includes(`"'=Eve Example"`) && logRow.includes(`"'=1+1 Tuesday 10-12 works"`) && !/(^|,)"=/.test(logRow),
  "review log neutralises formula-like cells: " + logRow);
check(fin.text.includes("'=Eve Example,2026-11-10,10:00,12:00,available,,confirmed,m01.1") && fin.name.endsWith("-complete.csv"),
  "final sheet neutralises the volunteer name and stays complete: " + fin.text.split("\n")[2]);
check(/=Eve Example/.test(await js(`document.getElementById("sheet").innerText`)) && !/'=Eve/.test(await js(`document.getElementById("sheet").innerText`)),
  "the page itself shows the name unchanged");
check(app.problems.length === 0, "no console errors or exceptions: " + JSON.stringify(app.problems));
app.done();
