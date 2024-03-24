const menuIcon = document.querySelector("#menuIcon");
const closeIcon = document.querySelector("#closeIcon");
const header = document.querySelector("div#head");
const navbar = document.querySelector("nav#navbar");
const navLinks = document.querySelectorAll(".nav-link");

function toggleMenu() {
  menuIcon.classList.toggle("hidden");
  closeIcon.classList.toggle("hidden");
}

window.addEventListener("DOMContentLoaded", () => {
  menuIcon.addEventListener("click", () => {
    toggleMenu();
    header.classList.add("header-sticky");
    navbar.classList.add("nav-sticky");
  });

  closeIcon.addEventListener("click", () => {
    toggleMenu();
    header.classList.remove("header-sticky");
    navbar.classList.remove("nav-sticky");
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      toggleMenu();
      header.classList.remove("header-sticky");
      navbar.classList.remove("nav-sticky");
    });
  });
});
