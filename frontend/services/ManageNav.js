const navLinks = document.querySelectorAll(".nav-link");

// Function to hide links in the top navigation
// Show links depending on the user authentication status
function hideNavigationLinks() {
  var isAuthenticated = window.App.authenticated;
  if (isAuthenticated) {
    navLinks.forEach((link) => {
      if (link.classList.contains("authenticated")) {
        link.style.display = "block";
      } else if (link.classList.contains("not-authenticated")) {
        link.style.display = "none";
      }
    });
  } else {
    navLinks.forEach((link) => {
      if (link.classList.contains("not-authenticated")) {
        link.style.display = "block";
      } else if (link.classList.contains("authenticated")) {
        link.style.display = "none";
      }
    });
  }
}

export default hideNavigationLinks;
