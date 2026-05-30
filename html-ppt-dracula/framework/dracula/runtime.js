(function () {
  "use strict";

  /* Configure slide ids — must match <section id="…"> and nav href order */
  var SLIDE_IDS = ["s-slide-1", "s-slide-2"];

  var deck = document.getElementById("deck");
  var dots = document.querySelectorAll(".nav-dots a");
  var ids = SLIDE_IDS.slice();

  var katexOpts = {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false }
    ],
    throwOnError: false
  };

  function renderMath(root) {
    if (typeof renderMathInElement === "function") {
      renderMathInElement(root || document.body, katexOpts);
    }
  }

  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  onReady(function () { renderMath(document.body); });

  dots.forEach(function (dot, dotIndex) {
    dot.addEventListener("click", function (e) {
      e.preventDefault();
      var targetId = ids[dotIndex];
      var el = targetId ? document.getElementById(targetId) : null;
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  if (deck) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var idx = ids.indexOf(en.target.id);
        if (idx < 0) return;
        dots.forEach(function (d, j) { d.classList.toggle("active", j === idx); });
      });
    }, { root: deck, threshold: 0.35, rootMargin: "-4% 0px -4% 0px" });

    ids.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) obs.observe(el);
    });
  }

  var lightbox = document.getElementById("lightbox");
  var lightboxImg = document.getElementById("lightbox-img");
  var lightboxCap = document.getElementById("lightbox-cap");
  var lightboxClose = document.getElementById("lightbox-close");
  var lightboxBackdrop = document.getElementById("lightbox-backdrop");

  var detailOverlay = document.getElementById("detail-overlay");
  var detailTitle = document.getElementById("detail-title");
  var detailBody = document.getElementById("detail-body");
  var detailClose = document.getElementById("detail-close");
  var detailBackdrop = document.getElementById("detail-backdrop");

  var lastFocus = null;

  function anyOverlayOpen() {
    return (lightbox && lightbox.classList.contains("is-open")) ||
      (detailOverlay && detailOverlay.classList.contains("is-open"));
  }

  function syncScrollLock() {
    if (!deck) return;
    if (anyOverlayOpen()) {
      document.documentElement.classList.add("lightbox-open");
      deck.style.overflow = "hidden";
    } else {
      document.documentElement.classList.remove("lightbox-open");
      document.documentElement.classList.remove("detail-open");
      deck.style.overflow = "";
    }
  }

  function openLightbox(src, cap) {
    if (!lightbox || !lightboxImg || !lightboxCap || !lightboxClose) return;
    lastFocus = document.activeElement;
    lightboxImg.classList.remove("lightbox-img--diagram");
    lightboxImg.src = src;
    lightboxImg.alt = cap || "预览";
    lightboxCap.textContent = cap || "";
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    syncScrollLock();
    lightboxClose.focus();
  }

  function openLightboxSvg(svgEl, cap) {
    if (!lightbox || !lightboxImg || !lightboxCap || !lightboxClose) return;
    var str = new XMLSerializer().serializeToString(svgEl);
    if (str.indexOf("xmlns=") === -1) str = str.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"');
    lastFocus = document.activeElement;
    lightboxImg.classList.add("lightbox-img--diagram");
    lightboxImg.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(str);
    lightboxImg.alt = cap || "流程图";
    lightboxCap.textContent = cap || "";
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    syncScrollLock();
    lightboxClose.focus();
  }

  function closeLightbox() {
    if (!lightbox || !lightbox.classList.contains("is-open")) return;
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    lightboxImg.classList.remove("lightbox-img--diagram");
    lightboxImg.removeAttribute("src");
    syncScrollLock();
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function openDetail(trigger) {
    if (!detailOverlay || !detailTitle || !detailBody || !detailClose) return;
    var tplId = trigger.getAttribute("data-detail-id");
    var tpl = tplId ? document.getElementById(tplId) : null;
    if (!tpl) return;
    lastFocus = document.activeElement;
    var titleEl = trigger.querySelector("h3, strong");
    detailTitle.textContent = titleEl ? titleEl.textContent.trim() : "详情";
    detailBody.innerHTML = tpl.innerHTML;
    detailOverlay.classList.add("is-open");
    detailOverlay.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("detail-open");
    syncScrollLock();
    renderMath(detailBody);
    detailClose.focus();
  }

  function closeDetail() {
    if (!detailOverlay || !detailOverlay.classList.contains("is-open")) return;
    detailOverlay.classList.remove("is-open");
    detailOverlay.setAttribute("aria-hidden", "true");
    detailBody.innerHTML = "";
    syncScrollLock();
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.querySelectorAll(".shot-tile").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var src = btn.getAttribute("data-src");
      var cap = btn.getAttribute("data-cap") || "";
      if (src) openLightbox(src, cap);
    });
  });

  document.querySelectorAll(".arch-panel").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var svg = btn.querySelector("svg");
      if (svg) openLightboxSvg(svg, btn.getAttribute("data-diagram-cap") || "");
    });
  });

  document.querySelectorAll(".detail-trigger").forEach(function (btn) {
    btn.addEventListener("click", function () { openDetail(btn); });
  });

  if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
  if (lightboxBackdrop) lightboxBackdrop.addEventListener("click", closeLightbox);
  if (detailClose) detailClose.addEventListener("click", closeDetail);
  if (detailBackdrop) detailBackdrop.addEventListener("click", closeDetail);

  document.addEventListener("keydown", function (e) {
    if (lightbox && lightbox.classList.contains("is-open")) {
      if (e.key === "Escape") { e.preventDefault(); closeLightbox(); }
      return;
    }
    if (detailOverlay && detailOverlay.classList.contains("is-open")) {
      if (e.key === "Escape") { e.preventDefault(); closeDetail(); }
      return;
    }
    if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA")) return;
    var cur = 0;
    dots.forEach(function (d, j) { if (d.classList.contains("active")) cur = j; });
    if (e.key === "ArrowDown" || e.key === "PageDown") {
      e.preventDefault();
      var nextId = ids[cur + 1];
      if (nextId) {
        var next = document.getElementById(nextId);
        if (next) next.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    } else if (e.key === "ArrowUp" || e.key === "PageUp") {
      e.preventDefault();
      var prevId = ids[cur - 1];
      if (prevId) {
        var prev = document.getElementById(prevId);
        if (prev) prev.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    } else if (e.key === "Home") {
      e.preventDefault();
      var first = document.getElementById(ids[0]);
      if (first) first.scrollIntoView({ behavior: "smooth", block: "start" });
    } else if (e.key === "End") {
      e.preventDefault();
      var last = document.getElementById(ids[ids.length - 1]);
      if (last) last.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
})();
