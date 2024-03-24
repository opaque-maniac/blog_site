import loginUser from "../services/Login.js";

class LoginPage extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // fetch the css
    fetch("static/styles/login.css")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((css) => {
        const style = document.createElement("style");
        style.textContent = css;
        this.root.appendChild(style);
      });

    // Fetching the template
    fetch("templates/login.html")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((html) => {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;
        const homeTemplate = tempDiv.querySelector("template");
        this.root.appendChild(homeTemplate.content.cloneNode(true));
      });

    // Fetching the javascript
    fetch("static/scripts/login.js")
      .then((resposne) => {
        if (!resposne.ok) {
          throw new Error("Network response was not okay");
        }
        return resposne.text();
      })
      .then((js) => {
        const scripts = document.createElement("script");
        scripts.textContent = js;
        this.root.appendChild(scripts);
      });
  }

  connectedCallback() {
    return;
  }

  disconnectedCallback() {
    return;
  }
}

customElements.define("login-page", LoginPage);

export default LoginPage;
