class ContactPage extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // fetch the css
    fetch("static/styles/contact.css")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((css) => {
        const style = document.createElement("style");
        style.textContent = css;
      });

    // Fetching the template
    fetch("templates/contact.html")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((html) => {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;
        const homeTemplate = tempDiv.querySelector("#contact");
        this.root.appendChild(homeTemplate.content.cloneNode(true));
      });

    // Fetching the javascript
    fetch("static/scripts/contact.js")
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
}

customElements.define("contact-page", ContactPage);

export default ContactPage;
