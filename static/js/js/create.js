(function () {
  const nav = document.getElementById("floating-nav");
  if (!nav) return;

  const THRESHOLD = 80;

  // Handle scroll → toggle circle state
  function updateNavbarState() {
    nav.classList.toggle("navbar-scrolled", window.scrollY > THRESHOLD);
  }

  // Initial check
  updateNavbarState();

  // Scroll listener
  window.addEventListener("scroll", updateNavbarState, { passive: true });

  // Click behavior: go home ONLY when circular
  nav.addEventListener("click", () => {
    if (nav.classList.contains("navbar-scrolled")) {
      window.location.href = "/";
    }
  });
})();
