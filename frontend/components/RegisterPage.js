import registerUser from "../services/Register.js";

class RegisterPage extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // fetch the css
    fetch("static/styles/register.css")
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
    fetch("templates/register.html")
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
    fetch("static/scripts/register.js")
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

customElements.define("register-page", RegisterPage);

export default RegisterPage;
