// Optional browser regression check (not part of `python3 -m unittest`): a failed or rejected
// "Suggest records" must leave the previous reviewed session, and its final-sheet export, unchanged;
// a successful run must start a fresh session. Invented messages only.
//
// Needs Node 22+ (built-in WebSocket) and a local Google Chrome; installs nothing.
//   node tests/browser/session_rerun.mjs            # from the project folder
//   CHROME=/path/to/chrome node tests/browser/session_rerun.mjs
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 8767, DBG = 9335;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const server = spawn("python3", ["server.py", String(PORT)], { cwd: ROOT, stdio: "ignore" });
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${DBG}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "ledger-cdp-"))}`, "about:blank"], { stdio: "ignore" });
const done = (code) => { server.kill(); chrome.kill(); process.exit(code); };

let tabs;
for (let i = 0; i < 50 && !tabs; i++) {
  await sleep(200);
  try { tabs = await (await fetch(`http://127.0.0.1:${DBG}/json`)).json(); } catch { /* starting */ }
}
if (!tabs) { console.error("Chrome did not start"); done(2); }
const ws = new WebSocket(tabs.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let nextId = 1, failures = 0;
const waiting = new Map(), problems = [];
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
  if (m.method === "Runtime.exceptionThrown") problems.push(JSON.stringify(m.params.exceptionDetails.exception?.description));
  if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error") problems.push(m.params.args.map((a) => a.value).join(" "));
});
const send = (method, params = {}) => new Promise((r) => { const id = nextId++; waiting.set(id, r); ws.send(JSON.stringify({ id, method, params })); });
const js = async (expr) => {
  const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result.exceptionDetails) throw new Error(expr + " -> " + JSON.stringify(r.result.exceptionDetails));
  return r.result.result.value;
};
const check = (ok, label) => { console.log((ok ? "PASS " : "FAIL ") + label); if (!ok) failures++; };
const setInputs = (text, week, tz = "Europe/London") => js(`(() => { document.getElementById("text").value = ${JSON.stringify(text)};
  document.getElementById("roster").value = "Ana Example\\nBen Example"; document.getElementById("week").value = "${week}";
  document.getElementById("tz").value = "${tz}"; document.getElementById("extractor").value = "rules"; })()`);
const suggest = async () => {
  await js(`document.getElementById("run").click()`);
  for (let i = 0; i < 50; i++) { await sleep(150); if (!(await js(`document.getElementById("run").disabled`))) break; }
  await sleep(500);
};
const session = () => js(`JSON.stringify({ week: state.week, tz: state.tz, messages: state.messages, roster: state.roster,
  claims: state.claims, reviewed: [...state.reviewed].sort() })`);
const exportFinal = async () => {
  const n = await js(`(window.__dl || []).length`);
  await js(`document.getElementById("export-final").click()`);
  for (let i = 0; i < 30 && (await js(`(window.__dl || []).length`)) === n; i++) await sleep(100);
  return js(`({ name: window.__names.at(-1), text: window.__dl.at(-1), progress: document.getElementById("progress").textContent })`);
};

await send("Runtime.enable");
await send("Page.navigate", { url: `http://127.0.0.1:${PORT}/` });
await sleep(1500);
await js(`(() => { window.__dl = []; window.__names = [];
  URL.createObjectURL = (b) => { b.text().then((t) => window.__dl.push(t)); return "blob:captured"; };
  URL.revokeObjectURL = () => {};
  HTMLAnchorElement.prototype.click = function () { window.__names.push(this.download); };
  const realFetch = window.fetch;  // failParse makes /api/parse answer like a server error
  window.fetch = (url, opts) => window.__failParse && String(url).endsWith("/api/parse")
    ? Promise.resolve(new Response(JSON.stringify({ error: "simulated parse failure" }), { status: 400, headers: { "Content-Type": "application/json" } }))
    : realFetch(url, opts); })()`);

// 1. A fully reviewed session for the week of 9 Nov.
await setInputs("2026-11-03 09:00 | Ana Example | Tuesday 10-12 works\n2026-11-04 09:00 | Ana Example | Thanks, see you then!", "2026-11-09");
await suggest();
await js(`document.querySelector('button[data-act="accept-mark"][data-msg="m01"]').click()`); await sleep(500);
await js(`document.querySelector('button[data-act="mark"][data-msg="m02"]').click()`); await sleep(500);
const base = await exportFinal(), baseSession = await session();
check(base.name === "availability-final-2026-11-09-complete.csv" && base.text.includes("status=complete"), "baseline export is complete for 2026-11-09");

// 2. Failed reruns must change nothing: parse error, non-Monday week, input with no messages.
const attempts = [
  ["parse failure for a new week", async () => { await js(`window.__failParse = true`); await setInputs("2026-11-17 09:00 | Ben Example | Friday after 3", "2026-11-16", "Asia/Kolkata"); }],
  ["non-Monday week", async () => { await js(`window.__failParse = false`); await setInputs("2026-11-17 09:00 | Ben Example | Friday after 3", "2026-11-17", "Asia/Kolkata"); }],
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
check(problems.length === 0, "no console errors or exceptions: " + JSON.stringify(problems));
done(failures ? 1 : 0);
