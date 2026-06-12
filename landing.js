(function () {
  const preloader = document.querySelector("[data-preloader]");
  const nav = document.querySelector(".navbar");
  const menuButton = document.querySelector("[data-menu-button]");
  const navLinks = document.querySelector("[data-nav-links]");
  let preloaderHidden = false;

  function hidePreloader() {
    if (preloaderHidden) return;
    preloaderHidden = true;
    document.body.classList.add("is-loaded");
    if (preloader) {
      window.setTimeout(function () {
        preloader.remove();
      }, 420);
    }
  }

  if (document.readyState === "complete") {
    window.requestAnimationFrame(hidePreloader);
  } else {
    window.addEventListener("load", hidePreloader, { once: true });
    window.setTimeout(hidePreloader, 1200);
  }

  function setScrolled() {
    if (!nav) return;
    nav.classList.toggle("scrolled", window.scrollY > 12);
  }

  setScrolled();
  window.addEventListener("scroll", setScrolled, { passive: true });

  if (menuButton && navLinks) {
    menuButton.addEventListener("click", function () {
      const isOpen = navLinks.classList.toggle("open");
      menuButton.setAttribute("aria-expanded", String(isOpen));
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
        menuButton.setAttribute("aria-expanded", "false");
      });
    });
  }
})();
