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

    window.addEventListener("popstate", () => {
      const state = window.history.state;
      if (state) {
        Router.go(state.route, false, state.posX, state.posY);
      }
    });
  },
  go: (route, addToHistory = true, posX = 0, posY = 0) => {
    console.log(`Going to: ${route}`);
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
    try {
      loadRoute(route);
    } catch (err) {
      console.error(err);
      Router.go("/error/500");
    }
  },
};

export default Router;
