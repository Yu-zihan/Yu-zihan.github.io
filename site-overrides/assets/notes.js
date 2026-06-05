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

  function headingTextForToc(heading) {
    var clone = heading.cloneNode(true);

    clone.querySelectorAll(".slug, .edit").forEach(function (node) {
      node.remove();
    });

    clone.querySelectorAll(".math").forEach(function (mathNode) {
      var annotation = mathNode.querySelector('annotation[encoding="application/x-tex"]');
      var text = annotation ? annotation.textContent : mathNode.textContent;
      mathNode.replaceWith(document.createTextNode(text));
    });

    return clone.textContent.replace(/\s+/g, " ").trim();
  }

  function rebuildToc() {
    if (!document.documentElement.classList.contains("notes-article")) return;

    var toc = document.querySelector("nav#toc");
    if (!toc) return;

    toc.querySelectorAll(".generated-toc").forEach(function (node) {
      node.remove();
    });

    var headings = Array.from(document.querySelectorAll("article h2, article h3"));
    if (!headings.length) return;

    var container = document.createElement("div");
    container.className = "block generated-toc";

    var details = document.createElement("details");
    details.open = true;

    var summary = document.createElement("summary");
    var title = document.createElement("h1");
    title.textContent = "Table of Contents";
    summary.appendChild(title);
    details.appendChild(summary);

    var list = document.createElement("ul");

    headings.forEach(function (heading, index) {
      if (!heading.id) {
        heading.id = "section-" + (index + 1);
      }

      var item = document.createElement("li");
      item.className = "toc-level-" + heading.tagName.toLowerCase().slice(1);

      var link = document.createElement("a");
      link.href = "#" + heading.id;
      link.textContent = headingTextForToc(heading);

      item.appendChild(link);
      list.appendChild(item);
    });

    details.appendChild(list);
    container.appendChild(details);
    toc.appendChild(container);
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.documentElement.classList.contains("notes-site")) return;

    relabelAcademicNav();
    relabelArticleBacklink();
    addArticleNav();
    disableDetailsCollapse();
    rebuildToc();
  });
})();
