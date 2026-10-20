// Shared harness for the optional browser checks: starts server.py and headless Chrome, drives the
// page over the DevTools protocol, captures downloads and can stub API responses. Installs nothing.
// Needs Node 22+ (built-in WebSocket) and a local Google Chrome (override the path with CHROME=...).
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function openApp(port, dbg) {
  const server = spawn("python3", ["server.py", String(port)], { cwd: ROOT, stdio: "ignore" });
  const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${dbg}`,
    `--user-data-dir=${mkdtempSync(join(tmpdir(), "ledger-cdp-"))}`, "about:blank"], { stdio: "ignore" });
  let failures = 0;
  const problems = [];
  const done = (code) => { server.kill(); chrome.kill(); process.exit(code ?? (failures ? 1 : 0)); };

  let tabs;
  for (let i = 0; i < 50 && !tabs; i++) {
    await sleep(200);
    try { tabs = await (await fetch(`http://127.0.0.1:${dbg}/json`)).json(); } catch { /* starting */ }
  }
  if (!tabs) { console.error("Chrome did not start"); done(2); }
  const ws = new WebSocket(tabs.find((t) => t.type === "page").webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r));
  let nextId = 1;
  const waiting = new Map();
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

  await send("Runtime.enable");
  await send("Page.navigate", { url: `http://127.0.0.1:${port}/` });
  await sleep(1500);
  // Downloads are captured instead of saved. window.__stub(path, fn) may answer an API call itself:
  // fn(body) returns {status, json} to replace the response, or undefined to let the real server answer.
  await js(`(() => { window.__dl = []; window.__names = []; window.__stubs = {};
    URL.createObjectURL = (b) => { b.text().then((t) => window.__dl.push(t)); return "blob:captured"; };
    URL.revokeObjectURL = () => {};
    HTMLAnchorElement.prototype.click = function () { window.__names.push(this.download); };
    const realFetch = window.fetch;
    window.fetch = (url, opts) => {
      const stub = window.__stubs[new URL(url, location.href).pathname];
      const answer = stub && stub(opts && opts.body ? JSON.parse(opts.body) : undefined);
      return answer ? Promise.resolve(new Response(JSON.stringify(answer.json), { status: answer.status,
        headers: { "Content-Type": "application/json" } })) : realFetch(url, opts);
    }; })()`);

  const setInputs = (text, week, tz = "Europe/London", roster = "Ana Example\\nBen Example", extractor = "rules") =>
    js(`(() => { document.getElementById("text").value = ${JSON.stringify(text)};
      document.getElementById("roster").value = "${roster}"; document.getElementById("week").value = "${week}";
      document.getElementById("tz").value = "${tz}"; document.getElementById("extractor").value = "${extractor}"; })()`);
  const suggest = async () => {
    await js(`document.getElementById("run").click()`);
    for (let i = 0; i < 80; i++) { await sleep(150); if (!(await js(`document.getElementById("run").disabled`))) break; }
    await sleep(500);
  };
  const exportVia = async (buttonId) => {
    const n = await js(`window.__dl.length`);
    await js(`document.getElementById("${buttonId}").click()`);
    for (let i = 0; i < 30 && (await js(`window.__dl.length`)) === n; i++) await sleep(100);
    return js(`({ name: window.__names.at(-1), text: window.__dl.at(-1), progress: document.getElementById("progress").textContent })`);
  };
  return { js, send, check, problems, done, setInputs, suggest, exportFinal: () => exportVia("export-final"),
    exportLog: () => exportVia("export"), failures: () => failures };
}
