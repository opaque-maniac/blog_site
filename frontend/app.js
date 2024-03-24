import App from "./services/App.js";
import hideNavigationLinks from "./services/ManageNav.js";
import { updateAuthenticationStatus } from "./services/Permissions.js";
import Router from "./services/Router.js";

// Importing components
import Error404 from "./components/Error404.js";
import HomePage from "./components/HomePage.js";
import ContactPage from "./components/ContactPage.js";

// Expose App to the window object
window.App = App;
window.Router = Router;
window.App.authenticated = true;

window.addEventListener("DOMContentLoaded", () => {
  updateAuthenticationStatus();
  window.Router.init();
  hideNavigationLinks();
});

window.addEventListener("user:loggedOut", () => {
  Router.go("/login");
});

window.addEventListener("user:loggedIn", () => {
  Router.go("/");
});
