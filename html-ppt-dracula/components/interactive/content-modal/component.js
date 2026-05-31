(function () {
  var modal = document.getElementById("content-modal");
  var titleEl = document.getElementById("content-modal-title");
  var bodyEl = document.getElementById("content-modal-code");
  var closeBtn = document.getElementById("content-modal-close");
  var backdrop = document.getElementById("content-modal-backdrop");
  var deck = document.getElementById("deck");
  if (!modal || !titleEl || !bodyEl) return;

  function highlightBody(text, lang) {
    lang = lang || "plaintext";
    bodyEl.removeAttribute("data-highlighted");
    if (lang === "plaintext") {
      bodyEl.className = "";
      bodyEl.textContent = text;
      return;
    }
    bodyEl.className = "language-" + lang;
    if (typeof hljs !== "undefined" && hljs.getLanguage && hljs.getLanguage(lang)) {
      try {
        var out = hljs.highlight(text, { language: lang, ignoreIllegals: true });
        bodyEl.innerHTML = out.value;
        bodyEl.classList.add("hljs");
        return;
      } catch (err) {}
    }
    bodyEl.textContent = text;
  }

  window.openContentModal = function (title, body, lang) {
    titleEl.textContent = title;
    highlightBody(body, lang || "plaintext");
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("lightbox-open");
    if (deck) deck.style.overflow = "hidden";
    if (closeBtn) closeBtn.focus();
  };

  function closeModal() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    var lightbox = document.getElementById("lightbox");
    if (!lightbox || !lightbox.classList.contains("is-open")) {
      document.documentElement.classList.remove("lightbox-open");
      if (deck) deck.style.overflow = "";
    }
  }

  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  if (backdrop) backdrop.addEventListener("click", closeModal);
  document.addEventListener("keydown", function (e) {
    if (modal.classList.contains("is-open") && e.key === "Escape") {
      e.preventDefault();
      e.stopPropagation();
      closeModal();
    }
  }, true);
})();
