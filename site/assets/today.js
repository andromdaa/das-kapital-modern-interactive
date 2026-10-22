// Start from today: filter the topic list; flag stale parallels.
(function () {
  "use strict";
  var input = document.getElementById("topic-filter");
  var items = document.querySelectorAll(".topic-index li");
  var sections = document.querySelectorAll(".topic");
  var count = document.getElementById("topic-count");
  input.addEventListener("input", function () {
    var q = input.value.trim().toLowerCase(), n = 0;
    items.forEach(function (li) {
      var ok = !q || li.dataset.label.indexOf(q) !== -1;
      li.hidden = !ok;
      if (ok) n++;
    });
    sections.forEach(function (s) { s.hidden = !!q && s.dataset.label.indexOf(q) === -1; });
    count.textContent = n;
  });
  var now = new Date();
  document.querySelectorAll(".asof[data-date]").forEach(function (a) {
    var d = new Date(a.dataset.date + "T00:00:00");
    if (isNaN(d)) return;
    d.setMonth(d.getMonth() + 6);
    if (now > d) a.textContent += " (over 6 months old; may be out of date)";
  });
})();
