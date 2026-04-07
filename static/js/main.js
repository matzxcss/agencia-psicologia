/**
 * Clarear Psicologia — Main JavaScript
 * GSAP scroll animations + Alpine.js interactivity + HTMX form
 */

/* ── GSAP ScrollTrigger ───────────────────────────────────────── */
gsap.registerPlugin(ScrollTrigger);

// Navbar scroll effect
ScrollTrigger.create({
  start: "top -60",
  onUpdate(self) {
    const nav = document.querySelector(".navbar");
    if (!nav) return;
    nav.classList.toggle("scrolled", self.direction === 1 && self.scroll() > 60 || self.scroll() > 60);
  },
});

// Smooth reveal for sections
document.querySelectorAll(".reveal").forEach((el) => {
  gsap.fromTo(
    el,
    { opacity: 0, y: 40 },
    {
      opacity: 1,
      y: 0,
      duration: 0.9,
      ease: "power3.out",
      scrollTrigger: {
        trigger: el,
        start: "top 85%",
        toggleActions: "play none none none",
      },
    }
  );
});

// Stagger children inside grid sections
document.querySelectorAll(".stagger-children").forEach((parent) => {
  gsap.fromTo(
    parent.children,
    { opacity: 0, y: 30 },
    {
      opacity: 1,
      y: 0,
      duration: 0.7,
      stagger: 0.15,
      ease: "power3.out",
      scrollTrigger: {
        trigger: parent,
        start: "top 80%",
        toggleActions: "play none none none",
      },
    }
  );
});

// Hero entrance animation
const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });
heroTl
  .from(".hero-badge",    { opacity: 0, y: 20, duration: 0.6, delay: 0.2 })
  .from(".hero h1",       { opacity: 0, y: 30, duration: 0.8 }, "-=0.3")
  .from(".hero-subtitle", { opacity: 0, y: 20, duration: 0.6 }, "-=0.4")
  .from(".hero-actions",  { opacity: 0, y: 20, duration: 0.6 }, "-=0.3");

// Método Clarear step numbers counter
document.querySelectorAll(".step-number").forEach((el) => {
  gsap.from(el, {
    scale: 0,
    rotation: -90,
    duration: 0.6,
    ease: "back.out(1.7)",
    scrollTrigger: {
      trigger: el,
      start: "top 85%",
    },
  });
});


/* ── Alpine.js mobile menu ────────────────────────────────────── */
document.addEventListener("alpine:init", () => {
  Alpine.data("mobileMenu", () => ({
    open: false,
    toggle() {
      this.open = !this.open;
    },
    close() {
      this.open = false;
    },
  }));
});


/* ── HTMX events ──────────────────────────────────────────────── */
document.body.addEventListener("htmx:afterSwap", (e) => {
  // Animate success card if it appears
  const success = e.detail.target.querySelector(".form-success");
  if (success) {
    gsap.from(success, { opacity: 0, scale: 0.9, duration: 0.5, ease: "back.out(1.4)" });
  }
});

// Reset form after successful submit (optional: redirect or show toast)
document.body.addEventListener("htmx:responseError", () => {
  alert("Ops! Algo deu errado. Tente novamente.");
});

/* ── Smooth anchor scroll with offset ─────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (e) => {
    const id = link.getAttribute("href");
    if (!id || id === "#") return;
    const target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    const offset = 80;
    const y = target.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top: y, behavior: "smooth" });
    
    // Close mobile menu if open
    const menuEl = document.querySelector("[x-data]");
    if (menuEl && menuEl.__x) {
      menuEl.__x.$data.open = false;
    }
  });
});
