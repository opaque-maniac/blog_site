const postRegex = /^\/posts-\d+$/;

const loadRoute = (route) => {
  let element = null;
  switch (true) {
    case route === "/":
      element = document.createElement("home-page");
      break;
    case route === "/about":
      break;
    case route === "/contact":
      element = document.createElement("contact-page");
      break;
    case route === "/terms":
      break;
    case route === "/login":
      break;
    case route === "/register":
      break;
    case route === "/logout":
      break;
    case route === "/profile":
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
