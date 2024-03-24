const postRegex = /^\/posts\/\d+$/;
const profileRegex = /^\/profile\/\d+$/;

// Handling various routes
const loadRoute = (route) => {
  let element = null;
  switch (true) {
    case route === "/":
      element = document.createElement("home-page");
      break;
    case route === "/about":
      element = document.createElement("about-page");
      break;
    case route === "/contact":
      element = document.createElement("contact-page");
      break;
    case route === "/terms":
      element = document.createElement("terms-page");
      break;
    case route === "/login":
      element = document.createElement("login-page");
      break;
    case route === "/register":
      element = document.createElement("register-page");
      break;
    case route === "/logout":
      break;
    case route === "/profile":
      break;
    case profileRegex.test(route):
      break;
    case route === "/profile/edit":
      break;
    case route === "/posts":
      break;
    case postRegex.test(route):
      id = route.split("-")[1];
      break;
    case route === "/posts/new":
      break;
    case route === "/error/500":
      break;
    default:
      element = document.createElement("error-404");
      break;
  }
  if (element) {
    document.querySelector("main").appendChild(element);
  }
};

export default loadRoute;
