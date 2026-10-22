// Optional browser check for the landing page (UI-09, D-34; not part of `python3 -m unittest`): served as on Render
// (LEDGER_DEMO=1), the page loads nothing from another site, its hero demo plays to the sheet the replay shows and can
// be stepped through, every in-page link resolves, the layout fits at 1400 px and 390 px, and its button opens the
// replay at /app. Run locally (no demo flag), the buttons say "Open the app" and the replay card points to Render.
//   node tests/browser/landing.mjs [screenshot-dir]    # from the project folder; Node 22+ and Chrome
import { openApp, sleep } from "./harness.mjs";

const SHOTS = process.argv[2];
const app = await openApp(8774, 9342, { LEDGER_DEMO: "1" }, "/");
const { js, send, check, viewport } = app;
const shotView = async (file) => {
  const r = await send("Page.captureScreenshot", { format: "png" });
  (await import("node:fs")).writeFileSync(file, Buffer.from(r.result.data, "base64"));
};
const state = () => js(`(() => {
  const d = document.getElementById("demo"), on = (sel) => [...d.querySelectorAll(sel)].filter((e) => e.classList.contains("is-in")).length;
  const kofi = d.querySelectorAll(".sh-row")[2].querySelectorAll(".cell")[1];  // Thursday
  return { step: d.dataset.step, bubbles: on(".bubble"), log: on(".log li"), segs: on(".seg"), struck: d.querySelectorAll(".seg.is-x").length,
    tag: on(".tag-x"), kofi: [...kofi.querySelectorAll(".seg.is-in")].map((s) => s.classList.contains("ok") ? "available" : "conditional").join() };
})()`);

// served as on Render
check(await js(`document.title`) === "Availazy — Local AI for Coordinators Who Have Better Things to Do", "landing page at /");
check(await js(`document.querySelector("h1").textContent.replace(/\\s+/g, " ").trim()`) === "Local AI for Coordinators Who Have Better Things to Do", "headline");
const ctas = await js(`[...document.querySelectorAll("[data-cta], [data-replay-link]")].map((a) => [a.textContent.trim(), new URL(a.href).pathname])`);
check(ctas.length === 4 && ctas.every(([t, p]) => t === "Open the replay" && p === "/app"), "replay buttons say 'Open the replay' and open /app: " + JSON.stringify(ctas));
const foreign = await js(`performance.getEntriesByType("resource").map((e) => e.name).filter((u) => !u.startsWith(location.origin))`);
check(foreign.length === 0, "nothing loaded from another site: " + JSON.stringify(foreign));
const dangling = await js(`[...document.querySelectorAll('a[href^="#"]')].filter((a) => !document.getElementById(a.hash.slice(1))).map((a) => a.hash)`);
check(dangling.length === 0, "every in-page link has a target: " + JSON.stringify(dangling));

// the hero demo plays when it is in view, then can be stepped through
await js(`document.getElementById("demo").scrollIntoView({ block: "center" })`);
await sleep(12500);
let s = await state();
check(s.step === "4" && s.bubbles === 4 && s.log === 4 && s.struck === 1 && s.tag === 1 && s.kofi === "available",
  "demo plays to the final sheet: Maria's Thursday struck, Kofi's Thursday available " + JSON.stringify(s));
const go = async (n) => { await js(`document.querySelector('[data-go="${n}"]').click()`); await sleep(1900); return state(); };
s = await go(1);
check(s.bubbles === 1 && s.segs === 2 && s.struck === 0 && s.kofi === "", "step 1 (m02): Maria's Tuesday and Thursday " + JSON.stringify(s));
s = await go(2);
check(s.bubbles === 2 && s.kofi === "conditional", "step 2 (m13): Kofi's Thursday conditional " + JSON.stringify(s));
s = await go(3);
check(s.bubbles === 3 && s.struck === 1 && s.tag === 1 && s.segs === 4 && s.kofi === "conditional", "step 3 (m28): Thursday struck, Friday added " + JSON.stringify(s));
s = await go(4);
check(s.kofi === "available" && await js(`document.querySelector('[data-go="4"]').getAttribute("aria-pressed")`) === "true", "step 4 (m29): Kofi's Thursday available");

// layout
for (const width of [1400, 390]) {
  await viewport(width);
  await js(`window.scrollTo(0, 0)`); await sleep(300);
  if (SHOTS) await shotView(`${SHOTS}/landing-${width}.png`);
  const w = await js(`({ page: document.documentElement.scrollWidth, inner: innerWidth })`);
  check(w.page <= w.inner, `${width}px: no horizontal page scroll (${w.page} <= ${w.inner})`);
}
await viewport(1400);

// the button opens the replay
await js(`document.querySelector(".hero [data-cta]").dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }))`);  // the harness replaces <a>.click()
await sleep(1500);
const replay = await js(`({ path: location.pathname, banner: !document.getElementById("replay-banner").hidden, home: document.querySelector("header h1 a")?.getAttribute("href") })`);
check(replay.path === "/app" && replay.banner && replay.home === "/", "hero button opens the replay at /app, whose title links home: " + JSON.stringify(replay));

// run locally, the same page labels its buttons for the local app (simulated: /api/status answers demo: false)
await send("Page.enable");
await send("Page.addScriptToEvaluateOnNewDocument", { source: `const realFetch = window.fetch;
  window.fetch = (u, o) => String(u).endsWith("/api/status") ? Promise.resolve(new Response(JSON.stringify({ models: [], default_model: "gemma4:e2b-it-qat" }),
    { headers: { "Content-Type": "application/json" } })) : realFetch(u, o);` });
await send("Page.navigate", { url: "http://127.0.0.1:8774/" });
await sleep(1500);
const local = await js(`({ ctas: [...document.querySelectorAll("[data-cta]")].map((a) => a.textContent.trim()), replay: document.querySelector("[data-replay-link]").href })`);
check(local.ctas.length === 3 && local.ctas.every((t) => t === "Open the app") && local.replay === "https://availability-ledger-replay.onrender.com/",
  "locally the buttons say 'Open the app' and the replay card links to Render: " + JSON.stringify(local));

// the guide (UI-10) and the styled 404 page
await send("Page.navigate", { url: "http://127.0.0.1:8774/docs" });
await sleep(1200);
for (const width of [1400, 390]) {
  await viewport(width); await sleep(300);
  const g = await js(`({ page: document.documentElement.scrollWidth, inner: innerWidth, arch: !!document.querySelector(".arch"),
    dangling: [...document.querySelectorAll('a[href^="#"]')].filter((a) => !document.getElementById(a.hash.slice(1))).length,
    foreign: performance.getEntriesByType("resource").map((e) => e.name).filter((u) => !u.startsWith(location.origin)).length })`);
  check(g.arch && g.page <= g.inner && !g.dangling && !g.foreign, `guide at /docs, ${width}px: diagrams shown, no overflow, links resolve, nothing from another site ` + JSON.stringify(g));
}
await send("Page.navigate", { url: "http://127.0.0.1:8774/no-such-page" });
await sleep(800);
check(await js(`document.title === "Not found · Availazy" && !!document.querySelector('a[href="/app"]')`), "unknown address shows the styled 404 page with a way back");

check(app.problems.length === 0, "no console errors or exceptions: " + JSON.stringify(app.problems));
app.done();
