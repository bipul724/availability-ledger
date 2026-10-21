"use strict";

const $ = (id) => document.getElementById(id);
const state = { messages: [], claims: [], resolved: [], ledger: null, roster: [], week: "", tz: "", read: new Set(), cur: null,
  demo: false,  // hosted replay (DEP-02): fictional set A and saved model outputs only
  reviewed: new Set(), confirmed: null,  // message ids the reviewer explicitly marked; export status from the server
  failures: new Map(),  // message id -> why its suggestions could not be read (COR-03)
  stats: { reviewStart: null, accepts: 0, edits: 0, rejects: 0, adds: 0, bulk: 0, marks: 0 } };

const FLAG_TEXT = {
  who_ambiguous: "Which volunteer? The name matches more than one",
  who_unknown: "Person is not on the roster",
  similar_name: "A similar name is on the roster",
  date_ambiguous: "Which day? The message does not settle it",
  outside_week: "Outside the selected week",
  date_unreadable: "Could not read a day",
  time_unreadable: "Could not read a time, so not applied",
  time_unstated: "No time given",
  excerpt_missing: "Quote not found in the message",
  excerpt_approx: "Quote only roughly matches the message",
  phrase_not_in_message: "Some words are not in this message",
  readers_disagree: "Model and rules read this differently",
  one_reader: "Only one of the two readers found this",
  added_by_rules: "Added by the rules: possible cancellation the model missed",
  replace_cue: "Replaces this person's earlier answer for the day",
  days_not_in_quote: "The quote does not mention these days",
  days_narrowed_to_quote: "Days narrowed to the ones the quote mentions",
  day_modifier_from_quote: "Day read with 'this' / 'next' / 'last' from the quote",
  time_from_same_message: "Times copied from earlier in this message",
  conditional: "Conditional",
  edited: "Edited by you",
};
const INFO_FLAGS = new Set(["time_unstated", "conditional", "edited", "replace_cue", "similar_name", "time_from_same_message"]);
// "Accept all and mark reviewed" is offered only when every undecided suggestion in a message passes this.
const bulkEligible = (c) => c.review === "pending" && c.flags.every((f) => INFO_FLAGS.has(f)) &&
  c.person_state === "resolved" && c.date_state === "resolved" && c.time_state !== "unparsed";
const DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

async function api(path, body) {
  const res = await fetch(path, body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok || data.error) throw new Error(data.error || res.statusText);
  return data;
}

function weekDates() {
  const [y, m, d] = state.week.split("-").map(Number);
  return Array.from({ length: 7 }, (_, i) => {
    const dt = new Date(Date.UTC(y, m - 1, d + i));
    return dt.toISOString().slice(0, 10);
  });
}

function dayLabel(iso) {
  const dt = new Date(iso + "T12:00:00Z");
  return `${DAY_NAMES[(dt.getUTCDay() + 6) % 7]} ${dt.getUTCDate()}`;
}

function nextMonday() {
  const t = new Date();
  t.setDate(t.getDate() + ((8 - t.getDay()) % 7 || 7));
  const pad = (n) => String(n).padStart(2, "0");
  return `${t.getFullYear()}-${pad(t.getMonth() + 1)}-${pad(t.getDate())}`;  // local date, not UTC
}

// ------------------------------------------------------------ setup

async function init() {
  $("week").value = nextMonday();
  try { $("tz").value = Intl.DateTimeFormat().resolvedOptions().timeZone || $("tz").value; } catch (e) { /* keep default */ }
  try {
    const st = await api("/api/status");
    const models = st.models.length ? st.models : [st.default_model];
    $("model").innerHTML = models.map((m) => `<option ${m === st.default_model ? "selected" : ""}>${esc(m)}</option>`).join("");
    if (!st.models.length) $("progress").textContent = "Ollama is not reachable: only 'Rules only' will work.";
    if (st.demo) {  // the server refuses anything else, so the inputs for other messages are hidden
      state.demo = true;
      document.body.classList.add("demo");
      $("replay-banner").hidden = false;
      $("week").disabled = $("tz").disabled = true;
      await loadDemo();
      $("progress").textContent = "Fictional demo week loaded (50 messages). Pick a reader and press Suggest records.";
    }
  } catch (e) {
    $("progress").textContent = "Could not reach the local server.";
  }
  $("demo").onclick = loadDemo;
  $("file").onchange = (ev) => {
    const f = ev.target.files[0];
    if (!f) return;
    const r = new FileReader();
    r.onload = () => { $("text").value = r.result; };
    r.readAsText(f);
  };
  $("run").onclick = run;
  $("export").onclick = exportCsv;
  $("export-final").onclick = exportFinal;
  $("accept-clean").onclick = acceptClean;
  $("rows").addEventListener("change", onFieldChange);
  $("rows").addEventListener("click", onClick);
  document.addEventListener("keydown", onKey);
}

async function loadDemo() {
  const d = await api("/api/demo");
  $("text").value = d.text;
  $("roster").value = d.roster;
  $("week").value = d.week_start;
  $("tz").value = d.timezone;
}

async function run() {
  // Proposed settings stay local until the new input has parsed; a failure leaves the current session untouched.
  const week = $("week").value, tz = $("tz").value.trim();
  const kept = state.messages.length ? " The current review is unchanged." : "";
  if (!week || new Date(week + "T12:00:00Z").getUTCDay() !== 1) {
    $("progress").textContent = "Pick a Monday as the start of the week." + kept;
    return;
  }
  $("run").disabled = true;
  let parsed;
  try {
    parsed = await api("/api/parse", { text: $("text").value, roster: $("roster").value, day_first: $("dayfirst").checked });
    if (!parsed.messages.length) throw new Error("No dated messages found. Expected 'YYYY-MM-DD HH:MM | Sender | text'.");
  } catch (e) {
    $("progress").textContent = "Error: " + e.message.replace(/\.?$/, ".") + kept;
    $("run").disabled = false;
    return;
  }
  // Commit the new session as one unit: settings, messages and a fresh review state.
  Object.assign(state, { week, tz, messages: parsed.messages, roster: parsed.roster, claims: [], resolved: [], ledger: null,
    confirmed: null, read: new Set(), reviewed: new Set(), failures: new Map(), cur: null });
  try {
    $("workspace").hidden = false;
    await resolveNow();  // clear the previous session's cards, sheet and chart before reading
    const t0 = performance.now();
    // Optional tracing (INT-03) groups one run's requests: a random token plus positions, never message content.
    const run = { id: (crypto.randomUUID ? crypto.randomUUID() : String(Math.random()).slice(2)), index: 0,
      total: state.messages.filter((m) => !m.duplicate_of).length };
    for (const [i, msg] of state.messages.entries()) {
      $("progress").textContent = `Reading message ${i + 1} of ${state.messages.length}…`;
      if (!msg.duplicate_of) {  // a repeat of an earlier message is not read again
        try {  // one failed message must not stop the others (COR-03)
          const out = await api("/api/suggest", {
            message: msg, roster: state.roster, week_start: state.week, timezone: state.tz,
            extractor: $("extractor").value, model: $("model").value, run: { ...run, index: ++run.index },
          });
          state.claims.push(...out.claims);
          if (out.stats?.json_ok === false) state.failures.set(msg.id, { kind: "reply", rulesOnly: out.claims.length > 0 });
        } catch (e) {
          state.failures.set(msg.id, { kind: "request", error: e.message });
        }
      }
      state.read.add(msg.id);
      if (i % 5 === 4 || i === state.messages.length - 1) await resolveNow();
    }
    const failed = state.failures.size;
    const secs = ((performance.now() - t0) / 1000).toFixed(0);
    $("progress").textContent = (state.demo ? `Replayed ${state.messages.length} messages in ${secs} s from saved outputs.`
      : `Read ${state.messages.length} messages in ${secs} s on this computer.`) +
      (failed ? ` ${failed} of ${state.messages.length} messages could not be read fully; each has a warning.` : "") + " Review timer started.";
    state.stats = { reviewStart: performance.now(), accepts: 0, edits: 0, rejects: 0, adds: 0, bulk: 0, marks: 0 };
  } catch (e) {
    $("progress").textContent = "Error: " + e.message;
  } finally {
    $("run").disabled = false;
  }
}

// ------------------------------------------------------------ resolve + render

let timer = null;
function scheduleResolve() {
  clearTimeout(timer);
  timer = setTimeout(resolveNow, 250);
}

function payload() {
  return { messages: state.messages, claims: state.claims, roster: state.roster, week_start: state.week, timezone: state.tz,
    reviewed_messages: [...state.reviewed] };
}

async function resolveNow() {
  const out = await api("/api/resolve", payload());
  state.resolved = out.claims;
  state.ledger = out.ledger;
  state.confirmed = out.confirmed;
  renderRows();
  renderSummary();
  renderReviewState();
}

function exportProblems(c) {
  return [c.unreviewed.length && `${c.unreviewed.length} message(s) not marked reviewed`, c.pending && `${c.pending} pending`,
    c.blocking_issues && `${c.blocking_issues} blocking issue(s)`].filter(Boolean).join(", ");
}

function renderReviewState() {
  const msgs = state.messages.filter((m) => !m.duplicate_of && state.read.has(m.id));
  const done = msgs.filter((m) => state.reviewed.has(m.id)).length, c = state.confirmed;
  $("review-state").textContent = `${done} of ${msgs.length} messages marked reviewed. Final sheet export: ` +
    (c ? (c.status === "complete" ? "complete." : `provisional (${exportProblems(c)}).`) : "not computed yet.") +
    (state.failures.size ? ` ${state.failures.size} message${state.failures.size === 1 ? "" : "s"} could not be read fully.` : "");
}

function failureText(f) {
  if (f.kind === "request") return `Could not read this message (${f.error}). It has no suggestions; read it yourself and add records if needed.`;
  return f.rulesOnly
    ? "The model's reply for this message could not be read. Only the rules' cancellations below were added; read the message yourself."
    : "The model's reply for this message could not be read, so it has no suggestions. Read the message yourself and add records if needed.";
}

function highlight(text, spans) {
  const s = spans.filter(Boolean).sort((a, b) => a[0] - b[0]);
  const merged = [];
  for (const [a, b] of s) {
    if (merged.length && a <= merged[merged.length - 1][1]) merged[merged.length - 1][1] = Math.max(b, merged[merged.length - 1][1]);
    else merged.push([a, b]);
  }
  let out = "", pos = 0;
  for (const [a, b] of merged) {
    out += esc(text.slice(pos, a)) + "<mark>" + esc(text.slice(a, b)) + "</mark>";
    pos = b;
  }
  return out + esc(text.slice(pos));
}

function renderRows() {
  const a = document.activeElement, aCard = a?.dataset?.f && a.closest(".card");  // keep focus in a field across re-renders
  const keep = aCard ? { id: aCard.dataset.id, f: a.dataset.f, value: a.value } : null;
  const byMsg = {};
  for (const c of state.resolved) (byMsg[c.msg] ||= []).push(c);
  $("rows").innerHTML = state.messages.filter((m) => state.read.has(m.id)).map((m) => {
    if (m.duplicate_of) {
      return `<div class="msgrow duplicate" id="row-${m.id}">
        <div class="msg"><div class="meta">${esc(m.id)} · ${esc(m.sent)} · <strong>${esc(m.sender)}</strong></div>
          <div class="body">${esc(m.text)}</div></div>
        <div class="cards"><div class="none">Same as <a href="#row-${esc(m.duplicate_of)}">${esc(m.duplicate_of)}</a>. Its suggestions cover this message, and marking ${esc(m.duplicate_of)} reviewed covers this one too.</div></div>
      </div>`;
    }
    const cs = (byMsg[m.id] || []).sort((a, b) => (a.n || 0) - (b.n || 0));
    const spans = cs.filter((c) => !["rejected", "dropped"].includes(c.review)).map((c) => c.excerpt_span);
    const reviewed = state.reviewed.has(m.id);
    const undecided = cs.filter((c) => c.review === "pending" || c.review === "dropped");
    const fail = state.failures.get(m.id);
    const bulk = !fail && undecided.length && undecided.every(bulkEligible);  // a failed read is never bulk-reviewed
    return `<div class="msgrow${reviewed ? " reviewed" : ""}${fail ? " failed" : ""}" id="row-${m.id}">
      <div class="msg"><div class="meta">${esc(m.id)} · ${esc(m.sent)} · <strong>${esc(m.sender)}</strong></div>
        <div class="body">${highlight(m.text, spans)}</div>
        <div class="msg-actions"><button type="button" data-act="mark" data-msg="${m.id}" aria-pressed="${reviewed}">${reviewed ? "✓ Reviewed" : "Mark message reviewed"}</button>
          ${bulk && !reviewed ? `<button type="button" data-act="accept-mark" data-msg="${m.id}">Accept all and mark reviewed</button>` : ""}</div></div>
      <div class="cards">${fail ? `<div class="failure" role="alert">${esc(failureText(fail))}</div>` : ""}${cs.map(card).join("") || (fail ? "" : `<div class="none">No availability found in this message.</div>`)}
        <div><button type="button" data-act="add" data-msg="${m.id}">+ Add a record from this message</button></div></div>
    </div>`;
  }).join("");
  markCurrent(false);
  if (keep) {
    const sel = `.card[data-id="${CSS.escape(keep.id)}"] [data-f="${keep.f}"]` + (keep.f === "day" ? `[value="${keep.value}"]` : "");
    document.querySelector(sel)?.focus({ preventScroll: true });
  }
}

function card(c) {
  const dates = weekDates();
  const warn = c.flags.filter((f) => !INFO_FLAGS.has(f));
  const info = c.flags.filter((f) => INFO_FLAGS.has(f));
  const who = state.roster.map((p) => `<option ${p === c.person ? "selected" : ""}>${esc(p)}</option>`).join("");
  const cand = (c.person_candidates || []).length ? ` (could be ${esc(c.person_candidates.join(" or "))})` : "";
  const dateNote = c.date_state === "ambiguous" ? `<div class="excerpt">Could be ${c.date_candidates.map(dayOrDate).join(" or ")}. ${esc(c.date_note)}</div>`
    : c.date_state === "outside_week" ? `<div class="excerpt">${c.date_candidates.map(dayOrDate).join(", ")} is outside this week.</div>`
    : c.date_note ? `<div class="excerpt">${esc(c.date_note)}</div>` : "";
  return `<div class="card ${c.status} ${c.review}" data-id="${esc(c.id)}">
    <div class="fields">
      <label>Volunteer${cand}<select data-f="person"><option value="" ${c.person ? "" : "selected"}>— not resolved —</option>${who}</select></label>
      <label>Status<select data-f="status">${["available", "conditional", "unavailable"].map((s) => `<option ${s === c.status ? "selected" : ""}>${s}</option>`).join("")}</select></label>
      <label>From<input type="time" step="900" data-f="start" value="${esc(c.start || "")}"></label>
      <label>To<input type="time" step="900" data-f="end" value="${esc(c.end || "")}"></label>
      ${c.status === "conditional" ? `<label>Condition<input data-f="condition" value="${esc(c.condition)}" size="22"></label>` : ""}
    </div>
    <div class="days">${dates.map((d) => `<label><input type="checkbox" data-f="day" value="${d}" ${c.dates.includes(d) ? "checked" : ""}>${dayLabel(d)}</label>`).join("")}</div>
    ${dateNote}
    <div class="excerpt">Source: “${esc(c.said?.excerpt || "")}”${c.time_note ? " · " + esc(c.time_note) : ""}${c.source ? " · read by " + esc(c.source) : ""}</div>
    <div class="badges">${warn.map((f) => `<span class="badge">${esc(FLAG_TEXT[f] || f)}</span>`).join("")}${info.map((f) => `<span class="badge info">${esc(FLAG_TEXT[f] || f)}</span>`).join("")}${c.drop_reason ? `<span class="badge">Not applied: ${esc(c.drop_reason)}</span>` : ""}</div>
    <div class="actions">
      ${c.review === "dropped" ? `<button type="button" data-act="restore">Use it anyway</button>`
        : `<button type="button" data-act="accept">${c.review === "accepted" ? "✓ Accepted" : "Accept"}</button><button type="button" data-act="reject">${c.review === "rejected" ? "Rejected" : "Reject"}</button>`}
      <button type="button" data-act="reset">Reset</button>
    </div>
  </div>`;
}

function dayOrDate(iso) {
  return weekDates().includes(iso) ? dayLabel(iso) : new Date(iso + "T12:00:00Z").toUTCString().slice(0, 11);
}

function rawClaim(id) { return state.claims.find((c) => c.id === id); }

function onFieldChange(ev) {
  const el = ev.target, cardEl = el.closest(".card");
  if (!cardEl || !el.dataset.f) return;
  const c = rawClaim(cardEl.dataset.id);
  c.override ||= {};
  const f = el.dataset.f;
  if (f === "day") {
    c.override.dates = [...cardEl.querySelectorAll('input[data-f="day"]:checked')].map((x) => x.value);
  } else if (f === "start" || f === "end") {
    c.override.start = cardEl.querySelector('[data-f="start"]').value;
    c.override.end = cardEl.querySelector('[data-f="end"]').value;
  } else if (f === "person") {
    if (el.value) c.override.person = el.value; else delete c.override.person;
  } else {
    c.override[f] = el.value;
  }
  c.review = "accepted";
  state.stats.edits++;
  scheduleResolve();
}

function onClick(ev) {
  const btn = ev.target.closest("button[data-act]");
  if (!btn) return;
  const act = btn.dataset.act;
  if (act === "add") {
    const msg = btn.dataset.msg, k = state.claims.filter((c) => c.msg === msg).length + 1;
    state.claims.push({ id: `${msg}.u${k}`, msg, n: 100 + k, source: "user", review: "accepted",
      said: { person: "", day_text: "", time_text: "", status: "available", condition: "", replaces_earlier: false, excerpt: "" },
      override: { dates: [] } });
    state.stats.adds++;
  } else if (act === "mark") {
    toggleReviewed(btn.dataset.msg);
  } else if (act === "accept-mark") {
    const undecided = state.resolved.filter((c) => c.msg === btn.dataset.msg && ["pending", "dropped"].includes(c.review));
    if (!undecided.length || !undecided.every(bulkEligible)) return;  // never accept anything flagged or unresolved
    for (const c of undecided) rawClaim(c.id).review = "accepted";
    state.reviewed.add(btn.dataset.msg);
    state.stats.bulk++;
    state.stats.marks++;
  } else {
    state.cur = btn.closest(".card").dataset.id;
    review(rawClaim(state.cur), act);
  }
  resolveNow();
}

function toggleReviewed(msg) {
  if (state.reviewed.has(msg)) state.reviewed.delete(msg);
  else { state.reviewed.add(msg); state.stats.marks++; }
}

function review(c, act) {
  if (act === "accept") { c.review = "accepted"; state.stats.accepts++; }
  if (act === "reject") { c.review = "rejected"; state.stats.rejects++; }
  if (act === "restore") { c.review = "accepted"; state.stats.accepts++; }
  if (act === "reset") { delete c.override; c.review = "pending"; }
}

// ------------------------------------------------------------ keyboard review

function markCurrent(scroll) {
  let found = null;
  for (const el of document.querySelectorAll("#rows .card")) {
    const on = el.dataset.id === state.cur;
    el.classList.toggle("current", on);
    if (on) found = el;
  }
  if (found && scroll) found.scrollIntoView({ block: "nearest" });
  return found;
}

function onKey(ev) {
  if ($("workspace").hidden || ev.ctrlKey || ev.metaKey || ev.altKey) return;
  const field = ev.target.closest?.("input, select, textarea, [contenteditable]");
  if (ev.key === "Escape") {
    const cardEl = field?.closest(".card");
    if (!cardEl) return;
    state.cur = cardEl.dataset.id;
    field.blur();
    markCurrent(false);
    ev.preventDefault();
    return;
  }
  if (field) return;  // typing in a field: no shortcuts
  const key = ev.key.toLowerCase();
  if (key === "j" || key === "k") {
    const all = [...document.querySelectorAll("#rows .card")];
    if (!all.length) return;
    const i = all.findIndex((el) => el.dataset.id === state.cur);
    const next = i < 0 ? 0 : Math.max(0, Math.min(all.length - 1, i + (key === "j" ? 1 : -1)));
    state.cur = all[next].dataset.id;
    markCurrent(true);
  } else if (key === "m") {
    if (!markCurrent(false)) return;
    toggleReviewed(rawClaim(state.cur).msg);
    resolveNow();
  } else if (key === "a" || key === "r" || key === "e") {
    const el = markCurrent(false);
    if (!el) return;
    if (key === "e") {
      el.querySelector("[data-f]")?.focus();
    } else if (key === "a" && state.resolved.find((r) => r.id === state.cur)?.review === "dropped") {
      $("progress").textContent = "This suggestion was not applied. Use its 'Use it anyway' button to apply it.";
    } else {
      review(rawClaim(state.cur), key === "a" ? "accept" : "reject");
      resolveNow();
    }
  } else {
    return;
  }
  ev.preventDefault();
}

function acceptClean() {
  let n = 0;
  for (const r of state.resolved) {
    if (r.review === "pending" && r.flags.every((f) => INFO_FLAGS.has(f))) {
      rawClaim(r.id).review = "accepted";
      n++;
    }
  }
  state.stats.bulk++;
  $("progress").textContent = `Accepted ${n} suggestions that had no warnings. Suggestions with warnings still need you.`;
  resolveNow();
}

// ------------------------------------------------------------ summary

function renderSummary() {
  const L = state.ledger;
  const order = { conflict: 0, unanswered_change: 1, cue_replacement: 2, who: 3, date: 4, time: 5, check_wording: 6, condition: 7, outside: 8 };
  const kindLabel = { unanswered_change: "Possible missed change", cue_replacement: "Earlier answer replaced — check",  // COR-07a, COR-18
    check_wording: "Check the wording" };  // COR-10 (D-30)
  const issues = [...L.issues].sort((a, b) => (order[a.kind] ?? 9) - (order[b.kind] ?? 9));
  $("issues").innerHTML = issues.map((i) => `<li><a href="#row-${esc(i.msg)}">${esc(i.msg)}</a> ` +
    `${kindLabel[i.kind] ? `<strong class="issue-kind">${kindLabel[i.kind]}:</strong> ` : ""}${esc(i.text)}</li>`).join("")
    || "<li>Nothing open.</li>";

  const dates = weekDates();
  const notes = L.review_notes || {};
  // UI-05: a segment counts as accepted only if every claim behind it is accepted; a cell is flagged when a pending
  // suggestion removed availability that day (cancelled, condition declined, replaced), which no segment can show.
  const accepted = new Set(state.resolved.filter((c) => c.review === "accepted").map((c) => c.id));
  const pendingIds = new Set(state.resolved.filter((c) => c.review === "pending").map((c) => c.id));
  const removal = /cancelled|condition declined|replaced earlier answer/;
  const label = state.confirmed?.status === "complete" ? "Complete" : "Provisional";
  $("sheet-title").textContent = `Availability sheet · ${label}`;
  $("chart-title").textContent = `People available · ${label}`;
  $("sheet").innerHTML = `<table class="sheet"><tr><th>Volunteer</th>${dates.map((d) => `<th data-date="${d}">${dayLabel(d)}</th>`).join("")}</tr>` +
    state.roster.map((p) => `<tr><td>${esc(p)}</td>${dates.map((d) => {
      const segs = (L.sheet[p] || {})[d] || [];
      const note = notes[`${p}|${d}`];
      const shown = new Set(segs.flatMap((s) => s.claims));
      const hidden = [...new Set((L.history[`${p}|${d}`] || []).filter((e) => removal.test(e.what)).map((e) => e.claim))]
        .filter((id) => pendingIds.has(id) && !shown.has(id));
      const empty = !segs.length && !hidden.length && !note;
      return `<td data-day="${dayLabel(d)}"${empty ? ' class="empty"' : ""}>${segs.map((s) => {
        const pending = !s.claims.every((id) => accepted.has(id));
        const tip = [pending ? "Includes suggestions not yet accepted" : "Accepted", ...(note || [])].join("\n");
        return `<span class="seg ${s.status}${pending ? " pending" : ""}${note ? " review" : ""}" data-review="${pending ? "pending" : "accepted"}" title="${esc(tip)}"><span class="t">${s.start}</span><wbr><span class="t">–${s.end}</span>${s.status === "conditional" ? " ?" : ""}${pending ? "<small>pending</small>" : ""}</span>`;
      }).join("")}${hidden.length ? `<span class="pending-change" title="${esc(`Not yet accepted: ${hidden.join(", ")} removes availability on this day`)}">pending change</span>` : ""}${!segs.length && note ? `<span title="${esc(note.join("\n"))}">⚠</span>` : ""}</td>`;
    }).join("")}</tr>`).join("") + "</table>";

  const interesting = /cancelled|condition|replaced|now /;
  const changes = [];
  for (const [key, events] of Object.entries(L.history)) {
    const [person, d] = key.split("|");
    for (const e of events) if (interesting.test(e.what)) changes.push({ person, d, ...e });
  }
  changes.sort((a, b) => a.msg.localeCompare(b.msg));
  $("changes").innerHTML = changes.map((c) => `<li><a href="#row-${esc(c.msg)}">${esc(c.msg)}</a> ${esc(c.sent)}: ${esc(c.person)}, ${dayLabel(c.d)} ${esc(c.span)} ${esc(c.what)}</li>`).join("")
    || "<li>No cancellations or corrections yet.</li>";

  renderChart(L, state.resolved);
}

const toMinutes = (hhmm) => Number(hhmm.slice(0, 2)) * 60 + Number(hhmm.slice(3, 5));

// Display only (UI-05): the server's half-hour counts split into accepted and pending, recomputed from the sheet with
// the server's rule (every 15-minute slot available -> available; every slot available or conditional -> conditional).
// A person counts as pending when any claim behind those slots is not accepted. The parts add up to L.counts.
function chartSplit(L, resolved) {
  const accepted = new Set(resolved.filter((c) => c.review === "accepted").map((c) => c.id));
  const start = toMinutes(L.counts.start), step = L.counts.step;
  return L.counts.days.map((d) => d.available.map((_, i) => {
    const out = { available: { accepted: 0, pending: 0 }, conditional: { accepted: 0, pending: 0 } };
    for (const p of state.roster) {
      const segs = (L.sheet[p] || {})[d.date] || [], covering = [];
      for (let t = start + i * step; t < start + (i + 1) * step; t += 15) covering.push(segs.find((s) => toMinutes(s.start) <= t && t < toMinutes(s.end)));
      if (covering.some((s) => !s)) continue;
      const kind = covering.every((s) => s.status === "available") ? "available" : "conditional";
      out[kind][covering.some((s) => !s.claims.every((id) => accepted.has(id))) ? "pending" : "accepted"]++;
    }
    return out;
  }));
}

function renderChart(L, resolved) {
  const counts = L.counts, split = chartSplit(L, resolved);
  const W = 700, H = 170, top = 10, bottom = 26, left = 18, gap = 6;
  const slots = counts.days[0].available.length;
  const max = Math.max(1, ...counts.days.flatMap((d) => d.available.map((a, i) => a + d.conditional[i])));
  const gw = (W - left - gap * 6) / 7, bw = gw / slots, ph = H - top - bottom;
  const y = (v) => top + ph - (v / max) * ph;
  const hhmm = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
  const layers = [["acc-a", "available", "accepted", "available (accepted)"], ["pen-a", "available", "pending", "available (pending review)"],
    ["acc-c", "conditional", "accepted", "conditional (accepted)"], ["pen-c", "conditional", "pending", "conditional (pending review)"]];
  let svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="People available per half hour, accepted and pending shown separately"><defs>
    <pattern id="hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="4" height="4" fill="none"/><line x1="0" y1="0" x2="0" y2="4" style="stroke: var(--chart-maybe)" stroke-width="2"/></pattern>
    <pattern id="hatch-pending" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="4" height="4" style="fill: var(--chart-maybe); fill-opacity: 0.3"/><line x1="0" y1="0" x2="0" y2="4" style="stroke: var(--chart-maybe)" stroke-width="1"/></pattern></defs>`;
  for (let v = 0; v <= max; v += Math.max(1, Math.ceil(max / 4))) {
    svg += `<line class="grid" x1="${left}" x2="${W}" y1="${y(v)}" y2="${y(v)}"/><text class="axis" x="0" y="${y(v) + 3}">${v}</text>`;
  }
  counts.days.forEach((d, di) => {
    const x0 = left + di * (gw + gap);
    d.available.forEach((_, i) => {
      const s = split[di][i], x = x0 + i * bw, t0 = toMinutes(counts.start) + i * counts.step;
      const parts = layers.filter(([, k, r]) => s[k][r]).map(([, k, r, name]) => `${s[k][r]} ${name}`);
      const tip = `<title>${dayLabel(d.date)} ${hhmm(t0)}–${hhmm(t0 + counts.step)}: ${parts.join(", ") || "nobody"}</title>`;
      let base = 0;
      for (const [cls, k, r] of layers) {
        const v = s[k][r];
        if (v) svg += `<rect class="${cls}" x="${x}" y="${y(base + v)}" width="${bw - 0.5}" height="${y(base) - y(base + v)}">${tip}</rect>`;
        base += v;
      }
      if (!base) svg += `<rect x="${x}" y="${top}" width="${bw}" height="${ph}" fill="transparent">${tip}</rect>`;
    });
    svg += `<text class="axis" x="${x0 + gw / 2}" y="${H - 12}" text-anchor="middle">${dayLabel(d.date)}</text>`;
    svg += `<text class="axis" x="${x0}" y="${H - 2}">${counts.start}</text>`;
  });
  $("chart").innerHTML = svg + "</svg>";
}

// ------------------------------------------------------------ export

const FORMULA_START = /^[=+\-@\t\r]/;  // a spreadsheet would run a cell starting with these (COR-02)
const csvCell = (v) => {
  const s = String(v);
  return `"${(FORMULA_START.test(s) ? "'" + s : s).replace(/"/g, '""')}"`;
};

function buildCsv(withPending) {
  const msgs = Object.fromEntries(state.messages.map((m) => [m.id, m]));
  const cols = ["record_id", "review", "volunteer", "date", "start", "end", "status", "condition", "message_id", "message_time", "sender", "excerpt", "warnings"];
  const rows = [cols];
  for (const c of state.resolved) {
    if (c.review === "rejected" || c.review === "dropped") continue;
    if (c.review !== "accepted" && !withPending) continue;
    const m = msgs[c.msg];
    const warnings = c.flags.filter((f) => !INFO_FLAGS.has(f)).map((f) => FLAG_TEXT[f] || f).join("; ");
    for (const d of (c.dates.length ? c.dates : [""])) {
      rows.push([c.id, c.review, c.person || "", d, c.start || "", c.end || "", c.status, c.condition || "", c.msg, m.sent, m.sender, c.said?.excerpt || "", warnings]);
    }
  }
  return { rows: rows.length - 1, csv: rows.map((r) => r.map(csvCell).join(",")).join("\n") };
}

function download(filename, text) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([text], { type: "text/csv" }));
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

function reviewSoFar() {
  const s = state.stats, mins = s.reviewStart ? (performance.now() - s.reviewStart) / 60000 : 0;
  return `Review so far: ${mins.toFixed(1)} min, ${s.accepts} accepts, ${s.edits} field edits, ${s.rejects} rejects, ` +
    `${s.adds} added, ${s.bulk} bulk accepts, ${s.marks} messages marked reviewed.`;
}

function exportCsv() {
  const { rows, csv } = buildCsv($("include-pending").checked);
  download(`availability-log-${state.week}.csv`, csv);
  $("progress").textContent = `Exported the review log (${rows} rows). ${reviewSoFar()}`;
}

async function exportFinal() {
  try {
    const out = await api("/api/export", payload());
    download(out.filename, out.csv);
    const rows = `${out.rows} row${out.rows === 1 ? "" : "s"}`;
    $("progress").textContent = (out.status === "complete" ? `Exported the final sheet (${rows}, complete). `
      : `Exported a PROVISIONAL final sheet (${rows}): ${exportProblems(out)}. `) + reviewSoFar();
  } catch (e) {
    $("progress").textContent = "Export failed: " + e.message;
  }
}

init();
