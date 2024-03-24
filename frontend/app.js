import App from "./services/App.js";
import hideNavigationLinks from "./services/ManageNav.js";
import { updateAuthenticationStatus } from "./services/Permissions.js";
import Router from "./services/Router.js";

// Importing components
import Error404 from "./components/Error404.js";
import HomePage from "./components/HomePage.js";
import ContactPage from "./components/ContactPage.js";
import TermsPage from "./components/TermsPage.js";
import AboutPage from "./components/AboutPage.js";
import LoginPage from "./components/LoginPage.js";
import RegisterPage from "./components/RegisterPage.js";
import AllPosts from "./components/AllPostsPage.js";
import PostItem from "./components/PostItem.js";

// Expose App to the window object
window.App = App;
window.Router = Router;
window.App.authenticated = true;

window.addEventListener("DOMContentLoaded", () => {
  updateAuthenticationStatus();
  window.Router.init();
  hideNavigationLinks();
  let path = window.location.pathname;
  window.Router.go(path);
});

window.addEventListener("user:loggedOut", () => {
  Router.go("/login");
});

window.addEventListener("user:loggedIn", () => {
  Router.go("/");
});
