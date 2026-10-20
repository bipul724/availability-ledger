// Optional browser regression check for UI-05 and UI-01 (not part of `python3 -m unittest`): the sheet and chart
// tell accepted availability apart from pending (unreviewed) suggestions, the sheet says "Provisional" until the
// final export would be complete, and the sheet does not overflow horizontally at 1400 px or 390 px.
// Invented messages; rules reader only (no model calls).
//   node tests/browser/sheet_display.mjs [screenshot-dir]    # from the project folder; Node 22+ and Chrome
import { openApp, sleep } from "./harness.mjs";

const SHOTS = process.argv[2];
const app = await openApp(8770, 9338);
const { js, check, setInputs, suggest, viewport, shot } = app;
const click = async (sel) => { await js(`document.querySelector('${sel}').click()`); await sleep(450); };

const week = [
  "2026-11-02 09:00 | Ana Example | Tuesday 10-12 works",          // accepted offer
  "2026-11-02 10:00 | Ben Example | Wednesday 2-4",                // pending offer
  "2026-11-02 11:00 | Ana Example | Thursday mornings",            // accepted offer ...
  "2026-11-03 09:00 | Ana Example | Can't do Thursday after all",  // ... hidden by a pending cancellation
  "2026-11-03 10:00 | Cleo Example | Saturday 9-12 maybe",         // pending conditional
  "2026-11-03 11:00 | Ben Example | Friday 9-11. Friday 11-1 too", // accepted + pending, merged into one segment
  "2026-11-03 12:00 | Cleo Example | Sunday 2-5 if it's dry",      // accepted conditional
].join("\n");
await setInputs(week, "2026-11-09", "Europe/London", "Ana Example\\nBen Example\\nCleo Example");
await suggest();
for (const m of ["m01", "m03", "m07"]) await click(`button[data-act="accept-mark"][data-msg="${m}"]`);
await click(`.card[data-id="m06.1"] button[data-act="accept"]`);

const cell = (person, date) => js(`(() => { const r = [...document.querySelectorAll("#sheet tr")].find((tr) => tr.cells[0]?.innerText.trim() === "${person}");
  const col = [...document.querySelectorAll("#sheet th")].findIndex((th) => th.dataset.date === "${date}");
  const td = r && col > 0 ? r.cells[col] : null;
  return td ? { text: td.innerText.replace(/\\s+/g, " ").trim(), segs: [...td.querySelectorAll(".seg")].map((s) => s.dataset.review + ":" + s.className) } : null; })()`);

for (const width of [1400, 390]) {
  await viewport(width);
  const tue = await cell("Ana Example", "2026-11-10"), wed = await cell("Ben Example", "2026-11-11");
  const thu = await cell("Ana Example", "2026-11-12"), fri = await cell("Ben Example", "2026-11-13");
  const sat = await cell("Cleo Example", "2026-11-14"), sun = await cell("Cleo Example", "2026-11-15");
  check(tue?.segs.length === 1 && tue.segs[0].startsWith("accepted:") && !/pending/i.test(tue.text), `${width}px accepted offer shown as accepted: ${JSON.stringify(tue)}`);
  check(wed?.segs[0]?.startsWith("pending:") && /pending/i.test(wed.text), `${width}px pending offer labelled pending: ${JSON.stringify(wed)}`);
  check(thu && thu.segs.length === 0 && /pending change/i.test(thu.text), `${width}px pending cancellation over an accepted offer is flagged: ${JSON.stringify(thu)}`);
  check(fri?.segs.length === 1 && fri.segs[0].startsWith("pending:") && /09:00/.test(fri.text) && /13:00/.test(fri.text),
    `${width}px merged accepted+pending segment shown as pending: ${JSON.stringify(fri)}`);
  check(sat?.segs[0]?.startsWith("pending:") && /conditional/.test(sat.segs[0]), `${width}px pending conditional: ${JSON.stringify(sat)}`);
  check(sun?.segs[0]?.startsWith("accepted:") && /conditional/.test(sun.segs[0]) && !/pending/i.test(sun.text), `${width}px accepted conditional: ${JSON.stringify(sun)}`);
  const ui = await js(`({ title: document.getElementById("sheet-title")?.innerText, sheetLegend: document.getElementById("sheet-legend")?.innerText || "",
    chartLegend: document.getElementById("chart-legend")?.innerText || "", chartTitle: document.getElementById("chart-title")?.innerText,
    table: document.querySelector("#sheet table").getBoundingClientRect().width, box: document.getElementById("sheet").getBoundingClientRect().width,
    right: document.getElementById("sheet").getBoundingClientRect().right, sheetScroll: document.getElementById("sheet").scrollWidth,
    cells: [...document.querySelectorAll("#sheet td, #sheet .seg")].filter((e) => e.scrollWidth > e.clientWidth + 1).length,
    page: document.documentElement.scrollWidth, inner: innerWidth })`);
  check(/Provisional/.test(ui.title) && /Provisional/.test(ui.chartTitle || ""), `${width}px sheet and chart titles say Provisional: ${ui.title} / ${ui.chartTitle}`);
  check(/accepted/i.test(ui.sheetLegend) && /pending/i.test(ui.sheetLegend) && /conditional/i.test(ui.sheetLegend), `${width}px sheet legend: ${ui.sheetLegend}`);
  check(/accepted/i.test(ui.chartLegend) && /pending/i.test(ui.chartLegend), `${width}px chart legend: ${ui.chartLegend}`);
  check(ui.inner === width && ui.table <= ui.box + 0.5 && ui.sheetScroll <= ui.box + 0.5 && ui.right <= width && ui.cells === 0,
    `${width}px sheet does not overflow (table ${ui.table.toFixed(0)} / box ${ui.box.toFixed(0)}, box ends at ${ui.right.toFixed(0)} of ${ui.inner}, cells overflowing ${ui.cells})`);
  console.log(`  info ${width}px page scrollWidth ${ui.page} vs viewport ${ui.inner}`);
  if (SHOTS) await shot(`${SHOTS}/sheet-${width}.png`);
}

// The chart's accepted/pending split must add up to the server's own counts, slot by slot.
const split = await js(`(() => { const c = chartSplit(state.ledger, state.resolved); let bad = 0, acc = 0, pen = 0;
  state.ledger.counts.days.forEach((d, di) => d.available.forEach((a, i) => {
    const s = c[di][i]; acc += s.available.accepted + s.conditional.accepted; pen += s.available.pending + s.conditional.pending;
    if (s.available.accepted + s.available.pending !== a || s.conditional.accepted + s.conditional.pending !== d.conditional[i]) bad++; }));
  return { bad, acc, pen, layers: ["acc-a", "pen-a", "acc-c", "pen-c"].map((k) => document.querySelectorAll("#chart rect." + k).length) }; })()`);
check(split.bad === 0 && split.acc > 0 && split.pen > 0, `chart split sums to server counts in every slot (accepted ${split.acc}, pending ${split.pen} person-slots)`);
check(split.layers.every((n) => n > 0), `chart draws all four layers: ${split.layers}`);

// Decide everything and mark all messages reviewed: the titles switch to Complete and nothing is pending.
await click(`.card[data-id="m02.1"] button[data-act="accept"]`);
await click(`.card[data-id="m04.1"] button[data-act="reject"]`);
await click(`.card[data-id="m05.1"] button[data-act="accept"]`);
await click(`.card[data-id="m06.2"] button[data-act="accept"]`);
for (const m of ["m02", "m04", "m05", "m06"]) await click(`button[data-act="mark"][data-msg="${m}"]`);
const fin = await js(`({ status: state.confirmed.status, title: document.getElementById("sheet-title")?.innerText,
  pending: document.querySelectorAll('#sheet .seg[data-review="pending"], #sheet .pending-change').length })`);
check(fin.status === "complete" && /Complete/.test(fin.title) && !/Provisional/.test(fin.title) && fin.pending === 0,
  `after full review the sheet says Complete with no pending marks: ${JSON.stringify(fin)}`);

// UI-01 on the fictional demo (18 volunteers, longer names) at both widths.
await js(`document.getElementById("demo").click()`); await sleep(600);
await js(`document.getElementById("extractor").value = "rules"`);
await suggest();
for (const width of [1400, 390]) {
  await viewport(width);
  const m = await js(`({ table: document.querySelector("#sheet table").getBoundingClientRect().width, box: document.getElementById("sheet").getBoundingClientRect().width,
    right: document.getElementById("sheet").getBoundingClientRect().right, sheetScroll: document.getElementById("sheet").scrollWidth,
    cells: [...document.querySelectorAll("#sheet td, #sheet .seg")].filter((e) => e.scrollWidth > e.clientWidth + 1).length,
    page: document.documentElement.scrollWidth, inner: innerWidth })`);
  check(m.inner === width && m.table <= m.box + 0.5 && m.sheetScroll <= m.box + 0.5 && m.right <= width && m.cells === 0,
    `demo ${width}px sheet does not overflow (table ${m.table.toFixed(0)} / box ${m.box.toFixed(0)}, box ends at ${m.right.toFixed(0)} of ${m.inner}, cells overflowing ${m.cells})`);
  console.log(`  info demo ${width}px page scrollWidth ${m.page} vs viewport ${m.inner}`);
  if (SHOTS) await shot(`${SHOTS}/demo-${width}.png`);
}
check(app.problems.length === 0, "no console errors or exceptions: " + JSON.stringify(app.problems));
app.done();
