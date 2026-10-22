// Landing page (UI-09): plays the hero demo, labels the page for the hosted replay or the local app, and small
// conveniences. No libraries; the page works without this file (the demo then shows its final state).
"use strict";
window.homeReady = true;

const REPLAY_URL = "https://availability-ledger-replay.onrender.com/app";  // the hosted app itself, not its landing page (UI-12)
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

// The same page is served by the local app and by the hosted replay (DEP-02). Locally the buttons open this
// machine's app, and "the replay" means the hosted one.
fetch("/api/status").then((r) => (r.ok ? r.json() : null)).then((st) => {
  if (!st || st.demo) return;
  document.querySelectorAll("[data-cta] > span").forEach((s) => { s.textContent = "Open the app"; });
  document.querySelectorAll("[data-replay-link]").forEach((a) => { a.href = REPLAY_URL; });
}).catch(() => {});

// Hero demo: each element appears at step data-in, leaves at data-out and is struck through at data-x.
const demo = document.getElementById("demo");
if (demo) {
  const parts = [...demo.querySelectorAll("[data-in]")];
  const dots = [...demo.querySelectorAll("[data-go]")];
  const LAST = dots.length;
  let timer = null;

  const show = (step, animate) => {
    demo.dataset.step = step;
    for (const el of parts) {
      const from = Number(el.dataset.in), to = Number(el.dataset.out || Infinity), x = Number(el.dataset.x || Infinity);
      el.classList.toggle("is-in", step >= from && step < to);
      el.classList.toggle("is-new", animate && step === from);
      el.classList.toggle("is-leaving", animate && step === to);
      el.classList.toggle("is-x", step >= x);
      el.classList.toggle("is-x-new", animate && step === x);
    }
    dots.forEach((b) => b.setAttribute("aria-pressed", String(Number(b.dataset.go) === step)));
  };
  const stop = () => { clearTimeout(timer); timer = null; };
  const play = () => {
    stop();
    if (reduceMotion) return show(LAST, false);
    let step = 0;
    show(0, false);
    const next = () => { step += 1; show(step, true); if (step < LAST) timer = setTimeout(next, 2800); };
    timer = setTimeout(next, 450);
  };

  dots.forEach((b) => b.addEventListener("click", () => { stop(); show(Number(b.dataset.go), !reduceMotion); }));
  demo.querySelector("[data-replay]").addEventListener("click", play);
  show(reduceMotion ? LAST : 0, false);
  requestAnimationFrame(() => demo.classList.add("ready"));
  if (!reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { io.disconnect(); play(); }
    }, { threshold: 0.3 });
    io.observe(demo);
  }
}

// A hairline under the header once the page scrolls.
const bar = document.querySelector(".top");  // not `top`: window.top cannot be redeclared
const onScroll = () => bar.classList.toggle("is-stuck", scrollY > 8);
addEventListener("scroll", onScroll, { passive: true });
onScroll();

// The nav (landing page) or the contents list (guide) marks the section in view.
const links = new Map([...document.querySelectorAll('.nav a[href^="#"], .toc a[href^="#"]')].map((a) => [a.hash.slice(1), a]));
const inView = new Set();
const spy = new IntersectionObserver((entries) => {
  for (const e of entries) e.isIntersecting ? inView.add(e.target.id) : inView.delete(e.target.id);
  links.forEach((a, id) => a.setAttribute("aria-current", String(inView.has(id))));
}, { rootMargin: "-45% 0px -50% 0px" });
links.forEach((_, id) => { const s = document.getElementById(id); if (s) spy.observe(s); });

// Copy the quick-start commands.
document.querySelectorAll("[data-copy]").forEach((b) => b.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(document.getElementById(b.dataset.copy).innerText.trim());
    b.textContent = "Copied";
  } catch {
    b.textContent = "Select to copy";
  }
  setTimeout(() => { b.textContent = "Copy"; }, 1800);
}));
