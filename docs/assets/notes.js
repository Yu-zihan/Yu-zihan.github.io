(function () {
  function relabelAcademicNav() {
    var labels = {
      "/": "Home",
      "/notes/index.html": "Notes",
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

  function tagSlug(text) {
    return text.toLowerCase().trim().replace(/&/g, "and").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  function enableTagFiltering() {
    if (!document.documentElement.classList.contains("notes-list")) return;

    var params = new URLSearchParams(window.location.search);
    var activeTag = params.get("tag") || "all";
    var posts = Array.from(document.querySelectorAll(".post-item"));
    var visibleCount = 0;

    posts.forEach(function (post) {
      var tags = (post.getAttribute("data-tags") || "").split(/\s+/).filter(Boolean);
      var show = activeTag === "all" || tags.indexOf(activeTag) !== -1;
      post.classList.toggle("is-hidden", !show);
      if (show) visibleCount += 1;
    });

    document.querySelectorAll("[data-tag-filter]").forEach(function (link) {
      link.classList.toggle("is-current", link.getAttribute("data-tag-filter") === activeTag);
    });

    var activeLabel = "All";
    var activeLink = document.querySelector('[data-tag-filter="' + activeTag + '"]');
    if (activeLink) {
      activeLabel = activeLink.textContent.trim();
    }

    var current = document.querySelector(".tag-filter-current");
    if (current) {
      current.textContent = activeLabel;
    }

    var filter = document.querySelector(".tag-filter-menu") || document.querySelector(".tag-filter");
    if (filter) {
      var status = filter.querySelector(".tag-filter-status");
      if (!status) {
        status = document.createElement("span");
        status.className = "tag-filter-status";
        filter.appendChild(status);
      }
      status.textContent = activeTag === "all" ? "" : visibleCount + " note" + (visibleCount === 1 ? "" : "s");
    }
  }

  function cleanArticleMetadata() {
    if (!document.documentElement.classList.contains("notes-article")) return;

    document.querySelectorAll("article .metadata .meta-item").forEach(function (item) {
      var text = item.textContent.trim().toLowerCase();
      if (text === "note" || text === "blog") {
        item.remove();
      }
    });
  }

  function linkArticleTags() {
    if (!document.documentElement.classList.contains("notes-article")) return;
    if (!/\/notes\//.test(window.location.pathname)) return;

    document.querySelectorAll("article .metadata .meta-item").forEach(function (item) {
      var text = item.textContent.trim();
      if (!text || text === "note" || /^\d{4}-\d{2}-\d{2}$/.test(text) || item.querySelector("a")) return;
      if (text.length > 40) return;

      var link = document.createElement("a");
      link.className = "tag-pill article-tag";
      link.href = "/notes/index.html?tag=" + tagSlug(text);
      link.textContent = text;
      item.textContent = "";
      item.appendChild(link);
    });
  }

  function fallbackCopy(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
    } finally {
      textarea.remove();
    }
  }

  function addCodeCopyButtons() {
    if (!document.documentElement.classList.contains("notes-article")) return;

    document.querySelectorAll("article pre").forEach(function (pre) {
      if (pre.querySelector(".code-copy-button")) return;

      var code = pre.querySelector("code");
      var button = document.createElement("button");
      button.className = "code-copy-button";
      button.type = "button";
      button.textContent = "Copy";
      button.setAttribute("aria-label", "Copy code");

      button.addEventListener("click", function () {
        var text = code ? code.innerText : pre.innerText;
        var copied = function () {
          button.textContent = "Copied";
          button.classList.add("is-copied");
          window.setTimeout(function () {
            button.textContent = "Copy";
            button.classList.remove("is-copied");
          }, 1400);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(copied).catch(function () {
            fallbackCopy(text);
            copied();
          });
        } else {
          fallbackCopy(text);
          copied();
        }
      });

      pre.appendChild(button);
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
    enableTagFiltering();
    cleanArticleMetadata();
    linkArticleTags();
    addCodeCopyButtons();
    rebuildToc();
  });
})();
