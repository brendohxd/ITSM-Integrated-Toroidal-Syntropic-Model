/**
 * Simple full-size image lightbox for ITSM site.
 * Any element with [data-lightbox] opens the shared dialog.
 * data-lightbox = full image URL
 * data-caption  = optional caption
 */
(function () {
  function ensureLightbox() {
    var el = document.getElementById("itsm-lightbox");
    if (el) return el;

    el = document.createElement("div");
    el.id = "itsm-lightbox";
    el.className = "lightbox";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", "Expanded figure");
    el.innerHTML =
      '<div class="lightbox-inner">' +
      '<button type="button" class="lightbox-close" aria-label="Close">&times;</button>' +
      '<img src="" alt="" />' +
      '<p class="lightbox-cap"></p>' +
      "</div>";
    document.body.appendChild(el);

    function close() {
      el.classList.remove("is-open");
      document.body.classList.remove("lightbox-open");
      el.querySelector("img").src = "";
    }

    el.addEventListener("click", function (e) {
      if (e.target === el || e.target.classList.contains("lightbox-close")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && el.classList.contains("is-open")) close();
    });
    el._close = close;
    return el;
  }

  function openFrom(trigger) {
    var src = trigger.getAttribute("data-lightbox");
    if (!src) return;
    var cap = trigger.getAttribute("data-caption") || "";
    var alt = trigger.getAttribute("data-alt") || cap || "Figure";
    var box = ensureLightbox();
    var img = box.querySelector("img");
    var p = box.querySelector(".lightbox-cap");
    img.src = src;
    img.alt = alt;
    p.textContent = cap;
    box.classList.add("is-open");
    document.body.classList.add("lightbox-open");
    box.querySelector(".lightbox-close").focus();
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-lightbox]");
    if (!t) return;
    e.preventDefault();
    openFrom(t);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var t = e.target.closest("[data-lightbox]");
    if (!t) return;
    e.preventDefault();
    openFrom(t);
  });
})();
