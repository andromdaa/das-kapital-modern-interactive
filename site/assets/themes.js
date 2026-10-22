// Themes view: filter claims by verdict and specificity; flag stale parallels.
(function () {
  "use strict";
  var data = JSON.parse(document.getElementById("site-data").textContent);
  var now = data.today ? new Date(data.today + "T00:00:00") : new Date();
  var form = document.querySelector(".filters");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".claims .claim:not(.opponent)"));
  var shown = document.getElementById("shown-count");

  function checked(name) {
    var out = {};
    form.querySelectorAll('input[name="' + name + '"]').forEach(function (i) { out[i.value] = i.checked; });
    return out;
  }
  function apply() {
    var v = checked("verdict"), s = checked("specificity"), n = 0;
    cards.forEach(function (c) {
      var ok = v[c.dataset.verdict] !== false && s[c.dataset.specificity] !== false;
      c.hidden = !ok;
      if (ok) n++;
    });
    shown.textContent = n;
    var state = { v: v, s: s };
    try { history.replaceState(null, "", "#" + encodeURIComponent(JSON.stringify(state))); } catch (e) { /* ignore */ }
  }
  form.addEventListener("change", apply);
  document.getElementById("reset-filters").addEventListener("click", function () {
    form.querySelectorAll("input[type=checkbox]").forEach(function (i) { i.checked = true; });
    apply();
  });

  // restore filters from the URL, unless the hash is a claim id
  var h = decodeURIComponent(location.hash.slice(1));
  if (h.charAt(0) === "{") {
    try {
      var st = JSON.parse(h);
      ["v", "s"].forEach(function (k) {
        var name = k === "v" ? "verdict" : "specificity";
        Object.keys(st[k] || {}).forEach(function (val) {
          var i = form.querySelector('input[name="' + name + '"][value="' + val + '"]');
          if (i) i.checked = st[k][val];
        });
      });
      apply();
    } catch (e) { /* ignore */ }
  }

  document.querySelectorAll(".asof[data-date]").forEach(function (a) {
    var d = new Date(a.dataset.date + "T00:00:00");
    if (isNaN(d)) return;
    var limit = new Date(d);
    limit.setMonth(limit.getMonth() + 6);
    if (now > limit) {
      var note = a.closest("details").querySelector(".stale");
      note.textContent = "Researched on " + a.dataset.date + ", more than 6 months ago. The present-day picture may have changed.";
      note.hidden = false;
      a.textContent += " (over 6 months old)";
    }
  });
})();
