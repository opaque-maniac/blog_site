import {
  userIsLoggedIn,
  userIsNotLoggedIn,
  handleNotAuthenticated,
  handleAreadyAuthenticated,
} from "./Permissions.js";
import loadRoute from "./RouterLoad.js";

const Router = {
  init: () => {
    document.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", (e) => {
        if (
          a.getAttribute("target") === "_blank" ||
          a.getAttribute("href") == "javascript:void(0)"
        )
          return;
        if (a.classList.contains("authenticated") && userIsNotLoggedIn()) {
          handleNotAuthenticated();
          return;
        }
        if (a.classList.contains("not-authenticated") && userIsLoggedIn()) {
          handleAreadyAuthenticated();
          return;
        }
        e.preventDefault();
        Router.go(a.getAttribute("href"));
      });
    });

    Router.go("/");
  },
  go: (route, addToHistory = true, posX = 0, posY = 0) => {
    if (addToHistory) {
      window.history.pushState(
        {
          route,
          posX,
          posY,
        },
        null,
        route
      );
    }

    document.querySelector("main").innerHTML = "";
    Router.load(route);
  },
  load: (route) => {
    loadRoute(route);
  },
};

export default Router;
