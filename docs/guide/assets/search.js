(function () {
  var input = document.getElementById("search-input");
  var box = document.getElementById("search-results");
  if (!input || !box) return;
  var docs = null;
  var loading = null;
  var active = -1;

  function load() {
    if (docs) return Promise.resolve(docs);
    if (!loading) {
      loading = fetch(input.getAttribute("data-index"))
        .then(function (r) { return r.json(); })
        .then(function (d) { docs = d; return d; })
        .catch(function () { docs = []; return docs; });
    }
    return loading;
  }

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function score(doc, terms) {
    var title = doc.title.toLowerCase();
    var text = doc.text.toLowerCase();
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      var inTitle = title.indexOf(t) !== -1;
      var at = text.indexOf(t);
      if (!inTitle && at === -1) return 0;
      total += (inTitle ? 10 : 0) + (at !== -1 ? 1 + Math.min(text.split(t).length - 1, 5) : 0);
    }
    return total;
  }

  function snippet(doc, terms) {
    var lower = doc.text.toLowerCase();
    var at = -1;
    for (var i = 0; i < terms.length && at === -1; i++) at = lower.indexOf(terms[i]);
    if (at === -1) return esc(doc.text.slice(0, 120));
    var start = Math.max(0, at - 50);
    var out = esc(doc.text.slice(start, start + 150));
    terms.forEach(function (t) {
      var re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
      out = out.replace(re, "<mark>$1</mark>");
    });
    return (start > 0 ? "… " : "") + out + " …";
  }

  function render(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { box.hidden = true; box.innerHTML = ""; return; }
    var hits = docs
      .map(function (d) { return { d: d, s: score(d, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, 6);
    active = -1;
    box.innerHTML = hits.length
      ? hits.map(function (h) {
          return '<a class="search-hit" href="' + h.d.url + '"><strong>' + esc(h.d.title) + "</strong><span>" + snippet(h.d, terms) + "</span></a>";
        }).join("")
      : '<p class="search-empty">No matches for “' + esc(query) + "”.</p>";
    box.hidden = false;
  }

  input.addEventListener("focus", load);
  input.addEventListener("input", function () {
    var q = input.value;
    load().then(function () { render(q); });
  });
  input.addEventListener("keydown", function (e) {
    var links = box.querySelectorAll(".search-hit");
    if (e.key === "Escape") { box.hidden = true; input.blur(); }
    else if (e.key === "ArrowDown" && links.length) { e.preventDefault(); active = Math.min(active + 1, links.length - 1); links[active].focus(); }
    else if (e.key === "Enter" && links.length) { window.location.href = links[Math.max(active, 0)].href; }
  });
  box.addEventListener("keydown", function (e) {
    var links = Array.prototype.slice.call(box.querySelectorAll(".search-hit"));
    var i = links.indexOf(document.activeElement);
    if (e.key === "ArrowDown" && i < links.length - 1) { e.preventDefault(); links[i + 1].focus(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); (i > 0 ? links[i - 1] : input).focus(); }
    else if (e.key === "Escape") { box.hidden = true; input.focus(); }
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".site-search")) box.hidden = true;
  });
  document.addEventListener("keydown", function (e) {
    var tag = (document.activeElement && document.activeElement.tagName) || "";
    if (e.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA") { e.preventDefault(); input.focus(); }
  });
})();
