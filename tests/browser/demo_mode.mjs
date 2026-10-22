// Optional browser check for the hosted read-only replay (DEP-02, not part of `python3 -m unittest`): with
// LEDGER_DEMO=1 the page shows the replay banner, hides the paste and upload inputs, loads fictional set A, replays
// saved Gemma outputs for both model readers, and review, accept and both exports work. Pasted text is refused.
// No model call is possible: the demo server has no route to Ollama.
//   node tests/browser/demo_mode.mjs [screenshot-dir]    # from the project folder; Node 22+ and Chrome
import { openApp, sleep } from "./harness.mjs";

const SHOTS = process.argv[2];
const app = await openApp(8772, 9340, { LEDGER_DEMO: "1" });
const { js, send, check, suggest, viewport, exportFinal, exportLog } = app;
const shotView = async (file) => {  // what a visitor sees in the window, not the whole (very long) page
  const r = await send("Page.captureScreenshot", { format: "png" });
  (await import("node:fs")).writeFileSync(file, Buffer.from(r.result.data, "base64"));
};
const visible = (sel) => js(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); return !!e && e.getClientRects().length > 0; })()`);

// load
const banner = await js(`(() => { const b = document.getElementById("replay-banner"); return { hidden: b.hidden,
  text: b.innerText.replace(/\\s+/g, " ").trim(), href: b.querySelector("a")?.href }; })()`);
check(!banner.hidden && banner.text === "Replay: fictional messages and saved Gemma 4 outputs. To read your own messages, run it locally, where they are processed on your own computer.",
  "banner shown with the exact wording: " + banner.text);
check(banner.href === "https://github.com/bipul724/availability-ledger", "banner links the repo");
check(!(await visible("#text")) && !(await visible("#roster")) && !(await visible("#file")) && !(await visible("#demo")) && !(await visible("#dayfirst")),
  "paste box, roster box, file upload, demo button and day-first option are hidden");
check(await js(`document.getElementById("week").disabled && document.getElementById("week").value === "2026-11-09" && document.getElementById("tz").disabled`),
  "week and timezone are the fictional set's and cannot be changed");
check(await js(`[...document.getElementById("model").options].map((o) => o.value).join() === "gemma4:e2b-it-qat"`), "only the saved model is offered");
check(/Fictional demo week loaded/.test(await js(`document.getElementById("progress").textContent`)), "set A is loaded on arrival");

// pasted text is refused by the server, and the page keeps nothing from it
await js(`document.getElementById("text").value = "2026-11-03 09:00 | Ana Example | Tuesday 10-12 works"`);
await suggest();
check(/run the app locally/.test(await js(`document.getElementById("progress").textContent`)) && await js(`document.getElementById("workspace").hidden`),
  "a pasted message is refused (403) and no session starts");
const other = await js(`fetch("/api/suggest", { method: "POST", body: JSON.stringify({ message: { id: "m02", sent: "2026-11-02 10:00", sender: "Ana Example",
  text: "Tuesday 10-12 works", duplicate_of: null }, roster: [], week_start: "2026-11-09", timezone: "UTC", extractor: "model" }) }).then((r) => r.status)`);
check(other === 403, "a message the replay did not serve is refused: " + other);
await js(`loadDemo()`); await sleep(300);

// suggest: Model only, then Model + rules
for (const [reader, label] of [["model", "Model only"], ["hybrid", "Model + rules"]]) {
  await js(`document.getElementById("extractor").value = "${reader}"`);
  await suggest();
  const r = await js(`({ progress: document.getElementById("progress").textContent, failures: state.failures.size, claims: state.claims.length,
    cards: document.querySelectorAll(".card").length, sources: [...new Set(state.claims.map((c) => c.source))].sort().join() })`);
  check(/^Replayed 50 messages in \d+ s from saved outputs\./.test(r.progress) && r.failures === 0 && r.claims > 40 && r.cards === r.claims,
    `${label}: 50 messages replayed, ${r.claims} suggestions, no failures (${r.progress.slice(0, 60)}…)`);
  check(reader === "model" ? r.sources === "model" : r.sources.includes("model"), `${label}: suggestions come from the saved model outputs (${r.sources})`);
}

// accept and review
const msgs = await js(`[...document.querySelectorAll('button[data-act="accept-mark"]')].slice(0, 4).map((b) => b.dataset.msg)`);
for (const m of msgs) { await js(`document.querySelector('button[data-act="accept-mark"][data-msg="${m}"]').click()`); await sleep(400); }
const firstCard = await js(`(() => { const c = document.querySelector('.card[data-id] button[data-act="reject"]'); const id = c.closest(".card").dataset.id; c.click(); return id; })()`);
await sleep(500);
const accepted = await js(`state.resolved.filter((c) => c.review === "accepted").length`);
check(msgs.length === 4 && accepted >= 4, `accepted and marked ${msgs.join(", ")} (${accepted} accepted suggestions)`);
check(await js(`state.resolved.find((c) => c.id === "${firstCard}").review === "rejected"`), `rejected ${firstCard}`);
check(await js(`document.querySelectorAll("#sheet .seg").length > 0 && document.querySelectorAll("#chart rect").length > 0 && document.querySelectorAll("#changes li").length > 0`),
  "sheet, chart and history are drawn");
check(await js(`document.querySelectorAll("#issues li").length > 0`), "warnings are listed");

// both exports
const fin = await exportFinal();
check(fin.name === "availability-final-2026-11-09-provisional.csv" && fin.text.startsWith("# availability-final v1; week=2026-11-09; status=provisional")
  && /,confirmed,/.test(fin.text), "final sheet exports accepted records, marked provisional: " + fin.name);
const log = await exportLog();
check(log.name === "availability-log-2026-11-09.csv" && log.text.split("\n").length > 2, "review log exports: " + log.name);

// layout at 1400 px and 390 px; the banner stays on screen while scrolling
for (const width of [1400, 390]) {
  await viewport(width);
  await js(`window.scrollTo(0, 0)`); await sleep(200);
  if (SHOTS) await shotView(`${SHOTS}/demo-${width}-top.png`);
  const ui = await js(`(() => { window.scrollTo(0, 1200); return new Promise((r) => setTimeout(() => r({ page: document.documentElement.scrollWidth,
    inner: innerWidth, top: document.getElementById("replay-banner").getBoundingClientRect().top, y: scrollY }), 200)); })()`);
  check(ui.page <= ui.inner, `${width}px: no horizontal page scroll (${ui.page} <= ${ui.inner})`);
  check(ui.y > 0 && ui.top === 0, `${width}px: banner stays at the top while scrolled (${ui.y}px down)`);
  if (SHOTS) await shotView(`${SHOTS}/demo-${width}-scrolled.png`);
}

check(app.problems.length === 0, "no console errors or exceptions: " + JSON.stringify(app.problems));
app.done();
