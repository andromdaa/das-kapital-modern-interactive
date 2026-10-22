// Reader: original toggles, footnotes, parallels side panel, topic trail.
(function () {
  "use strict";
  var data = JSON.parse(document.getElementById("site-data").textContent);
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  };

  // ---------- dates ----------
  function today() {
    return data.today ? new Date(data.today + "T00:00:00") : new Date();
  }
  function isStale(iso) {
    if (!iso) return false;
    var d = new Date(iso + "T00:00:00");
    if (isNaN(d)) return false;
    var limit = new Date(d);
    limit.setMonth(limit.getMonth() + 6);
    return today() > limit;
  }
  window.CapitalDates = { isStale: isStale };

  // ---------- original text ----------
  var allBtn = document.getElementById("toggle-all-orig");
  function setOrig(para, open) {
    var orig = para.querySelector(".orig");
    var btn = para.querySelector(".otoggle");
    if (!orig || !btn) return;
    orig.hidden = !open;
    para.classList.toggle("orig-open", open);
    btn.setAttribute("aria-pressed", String(open));
    btn.textContent = open ? "Hide original" : "Original";
  }
  function syncBody() {
    document.body.classList.toggle("any-orig", !!document.querySelector(".para.orig-open"));
  }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".otoggle");
    if (!btn) return;
    var para = btn.closest(".para");
    setOrig(para, btn.getAttribute("aria-pressed") !== "true");
    syncBody();
  });
  function setAll(open) {
    document.querySelectorAll(".para").forEach(function (p) { setOrig(p, open); });
    allBtn.setAttribute("aria-pressed", String(open));
    allBtn.textContent = open ? "Hide original" : "Show original alongside";
    document.body.classList.toggle("show-orig", open);
    syncBody();
    store.set("capital.showOrig", open ? "1" : "0");
  }
  if (allBtn) {
    allBtn.addEventListener("click", function () {
      setAll(allBtn.getAttribute("aria-pressed") !== "true");
    });
    if (store.get("capital.showOrig") === "1") setAll(true);
  }

  // ---------- text size and font ----------
  var root = document.documentElement;
  var range = document.getElementById("size-range");
  var out = document.getElementById("size-out");
  var fontSel = document.getElementById("font-choice");
  var MIN = 14, MAX = 32;
  function firstVisiblePara() {
    var paras = document.querySelectorAll(".para");
    for (var i = 0; i < paras.length; i++) {
      var r = paras[i].getBoundingClientRect();
      if (r.bottom > 0) return { el: paras[i], top: r.top };
    }
    return null;
  }
  // Re-pin the paragraph the reader is looking at, so resizing doesn't lose their place.
  function keepPlace(change) {
    var anchor = firstVisiblePara();
    change();
    if (anchor) window.scrollBy(0, anchor.el.getBoundingClientRect().top - anchor.top);
  }
  function setSize(px, save) {
    px = Math.max(MIN, Math.min(MAX, Math.round(px)));
    keepPlace(function () { root.style.setProperty("--text-size", px + "px"); });
    range.value = px;
    out.textContent = px + "px";
    if (save) store.set("capital.textSize", String(px));
  }
  if (range) {
    var start = parseInt(store.get("capital.textSize"), 10) ||
      parseInt(getComputedStyle(root).getPropertyValue("--text-size"), 10) || 20;
    range.value = start;
    out.textContent = start + "px";
    range.addEventListener("input", function () { setSize(+range.value, true); });
    document.getElementById("size-down").addEventListener("click", function () { setSize(+range.value - 1, true); });
    document.getElementById("size-up").addEventListener("click", function () { setSize(+range.value + 1, true); });
  }
  if (fontSel) {
    fontSel.value = root.dataset.font === "sans" ? "sans" : "serif";
    fontSel.addEventListener("change", function () {
      keepPlace(function () {
        if (fontSel.value === "sans") root.dataset.font = "sans";
        else delete root.dataset.font;
      });
      store.set("capital.font", fontSel.value);
    });
  }

  // ---------- notes ----------
  var notesBtn = document.getElementById("toggle-notes");
  if (notesBtn) {
    notesBtn.addEventListener("click", function () {
      var open = notesBtn.getAttribute("aria-pressed") !== "true";
      document.querySelectorAll("details.notes").forEach(function (d) { d.open = open; });
      notesBtn.setAttribute("aria-pressed", String(open));
      notesBtn.textContent = open ? "Close all notes" : "Open all notes";
    });
  }
  function flash(el) {
    el.classList.add("flash");
    setTimeout(function () { el.classList.remove("flash"); }, 1600);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest(".fnref a");
    if (!a) return;
    var li = document.getElementById(a.dataset.fn);
    if (!li) return;
    e.preventDefault();
    var det = li.closest("details");
    if (det) det.open = true;
    li.focus({ preventScroll: true });
    li.scrollIntoView({ block: "nearest" });
    flash(li);
  });

  // ---------- parallels panel ----------
  var panel = document.getElementById("panel");
  var panelBody = panel && panel.querySelector(".panel-body");
  var lastTrigger = null;

  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text != null) n.textContent = text;
    return n;
  }
  function field(parent, label, text) {
    if (!text) return;
    parent.appendChild(el("h4", null, label));
    parent.appendChild(el("p", null, text));
  }
  function renderParallel(p) {
    var s = el("section", { "aria-labelledby": "pp-" + p.id });
    var head = el("p");
    var badge = el("span", { "class": "verdict", "data-verdict": p.verdict || "none" },
      data.verdicts[p.verdict] || "Not yet judged");
    head.appendChild(badge);
    head.appendChild(document.createTextNode(" "));
    head.appendChild(el("span", { "class": "asof" }, "As of " + (p.researched_on || "unknown date")));
    s.appendChild(el("h3", { id: "pp-" + p.id }, p.title));
    s.appendChild(head);
    if (p.stub) s.appendChild(el("p", { "class": "stale" }, "Stub data: no research has been done for this item yet."));
    if (isStale(p.researched_on)) {
      s.appendChild(el("p", { "class": "stale" },
        "This parallel was researched on " + p.researched_on +
        ", more than 6 months ago. The present-day picture may have changed."));
    }
    field(s, "The book's claim", p.book_claim);
    field(s, "How it is tested", p.test);
    field(s, "The present", p.parallel);
    field(s, "Why this verdict", p.reasoning);
    if (p.sources && p.sources.length) {
      s.appendChild(el("h4", null, "Sources"));
      var ul = el("ul", { "class": "sources" });
      p.sources.forEach(function (src) {
        var li = el("li");
        if (src.url) {
          var a = el("a", { href: src.url, rel: "noopener noreferrer" }, src.title || src.url);
          li.appendChild(a);
        } else {
          li.textContent = src.title || "";
        }
        if (src.published) li.appendChild(document.createTextNode(" — published " + src.published));
        ul.appendChild(li);
      });
      s.appendChild(ul);
    }
    if (p.passages && p.passages.length > 1) {
      s.appendChild(el("h4", null, "All passages for this claim"));
      var pl = el("ul", { "class": "passages" });
      p.passages.forEach(function (ps) {
        var li = el("li");
        if (ps.href) li.appendChild(el("a", { href: "../" + ps.href + "#" + ps.id }, ps.label));
        else li.textContent = ps.label;
        pl.appendChild(li);
      });
      s.appendChild(pl);
    }
    var more = el("p");
    more.appendChild(el("a", { href: "../themes.html#" + p.id }, "See this claim in Themes"));
    s.appendChild(more);
    return s;
  }
  function openPanel(btn) {
    var ids = btn.dataset.parallels.split(" ");
    panelBody.textContent = "";
    ids.forEach(function (id) {
      var p = data.parallels[id];
      if (p) panelBody.appendChild(renderParallel(p));
    });
    document.getElementById("panel-title").textContent =
      ids.length > 1 ? ids.length + " present-day parallels" : "Present-day parallel";
    if (lastTrigger) lastTrigger.setAttribute("aria-expanded", "false");
    lastTrigger = btn;
    btn.setAttribute("aria-expanded", "true");
    panel.hidden = false;
    panel.scrollTop = 0;
    panel.focus();
  }
  function closePanel() {
    if (!panel || panel.hidden) return;
    panel.hidden = true;
    if (lastTrigger) {
      lastTrigger.setAttribute("aria-expanded", "false");
      lastTrigger.focus();
    }
  }
  if (panel) {
    document.querySelectorAll(".pmark").forEach(function (b) {
      b.setAttribute("aria-expanded", "false");
      b.setAttribute("aria-controls", "panel");
    });
    document.addEventListener("click", function (e) {
      var b = e.target.closest(".pmark");
      if (b) { openPanel(b); return; }
      if (e.target.closest(".panel-close")) closePanel();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closePanel();
    });
  }

  // ---------- topic trail (arrived from "Start from today") ----------
  var params = new URLSearchParams(location.search);
  var topic = params.get("topic");
  var trail = document.getElementById("topic-trail");
  if (topic && trail && data.topics && data.topics[topic]) {
    var t = data.topics[topic];
    var here = location.hash.slice(1);
    var i = Math.max(0, t.passages.findIndex(function (p) { return p.id === here; }));
    var link = function (j, text, rel) {
      var p = t.passages[j];
      var a = el("a", { href: "../" + p.href + "?topic=" + encodeURIComponent(topic) + "#" + p.id, rel: rel }, text);
      return a;
    };
    trail.appendChild(el("span", null, "Topic: "));
    trail.lastChild.appendChild(el("strong", null, t.label));
    trail.appendChild(el("span", null, "passage " + (i + 1) + " of " + t.passages.length));
    if (i > 0) trail.appendChild(link(i - 1, "← Previous", "prev"));
    if (i < t.passages.length - 1) trail.appendChild(link(i + 1, "Next →", "next"));
    trail.appendChild(el("a", { href: "../today.html#" + topic }, "All passages"));
    trail.hidden = false;
  }
})();
