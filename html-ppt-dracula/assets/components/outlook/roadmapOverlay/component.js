      var roadmapFull = document.getElementById("roadmap-full");
      var roadmapFullTitle = document.getElementById("roadmap-full-title");
      var roadmapFullBody = document.getElementById("roadmap-full-body");
      var roadmapFullClose = document.getElementById("roadmap-full-close");
      var roadmapFullBackdrop = document.getElementById("roadmap-full-backdrop");
      var roadmapLastFocus = null;

      function openRoadmapFull(tile) {
        if (!roadmapFull || !roadmapFullTitle || !roadmapFullBody) return;
        var title = tile.querySelector("h3");
        var body = tile.querySelector(".roadmap-body");
        roadmapLastFocus = document.activeElement;
        roadmapFullTitle.textContent = title ? title.textContent : "";
        roadmapFullBody.innerHTML = body ? body.innerHTML : "";
        roadmapFull.classList.add("is-open");
        roadmapFull.setAttribute("aria-hidden", "false");
        document.documentElement.classList.add("lightbox-open");
        deck.style.overflow = "hidden";
        if (roadmapFullClose) roadmapFullClose.focus();
      }

      function closeRoadmapFull() {
        if (!roadmapFull || !roadmapFull.classList.contains("is-open")) return;
        roadmapFull.classList.remove("is-open");
        roadmapFull.setAttribute("aria-hidden", "true");
        document.documentElement.classList.remove("lightbox-open");
        deck.style.overflow = "";
        if (roadmapLastFocus && typeof roadmapLastFocus.focus === "function") roadmapLastFocus.focus();
      }

      document.querySelectorAll(".roadmap-tile").forEach(function (tile) {
        tile.addEventListener("click", function () { openRoadmapFull(tile); });
      });
      if (roadmapFullClose) roadmapFullClose.addEventListener("click", closeRoadmapFull);
      if (roadmapFullBackdrop) roadmapFullBackdrop.addEventListener("click", closeRoadmapFull);

