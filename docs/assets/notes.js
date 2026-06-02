(function () {
  function relabelAcademicNav() {
    var labels = {
      "/": "Home",
      "/notes/index.html": "Notes archive",
      "/blog/index.html": "Essays",
    };

    document.querySelectorAll("main.academic nav a").forEach(function (link) {
      var href = link.getAttribute("href");
      if (labels[href]) {
        link.textContent = labels[href];
      } else {
        link.remove();
      }
    });
  }

  function relabelArticleBacklink() {
    var logo = document.querySelector(".header .logo span");
    if (!logo) return;

    logo.textContent = "« Zihan Yu";
    logo.title = "Back to homepage";
  }

  function addArticleNav() {
    if (!document.documentElement.classList.contains("notes-article")) return;

    var article = document.querySelector("#grid-wrapper > article");
    if (!article || article.querySelector(".notes-breadcrumb")) return;
    var path = window.location.pathname;
    var isEssay = /\/blog\//.test(path);

    var nav = document.createElement("nav");
    nav.className = "notes-breadcrumb";
    nav.setAttribute("aria-label", "Notes navigation");

    var archive = document.createElement("a");
    archive.href = isEssay ? "/blog/index.html" : "/notes/index.html";
    archive.textContent = isEssay ? "← Back to essays" : "← Back to notes";

    var home = document.createElement("a");
    home.href = "/";
    home.textContent = "Home";

    nav.appendChild(archive);
    nav.appendChild(home);
    article.insertBefore(nav, article.firstChild);
  }

  function disableDetailsCollapse() {
    if (!document.documentElement.classList.contains("notes-article")) return;

    document.querySelectorAll("article details").forEach(function (details) {
      details.open = true;
      details.addEventListener("toggle", function () {
        if (!details.open) {
          details.open = true;
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.documentElement.classList.contains("notes-site")) return;

    relabelAcademicNav();
    relabelArticleBacklink();
    addArticleNav();
    disableDetailsCollapse();
  });
})();
