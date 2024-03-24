class ContactPage extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // Fetch the html
    fetch("templates/contact.html")
      .then((request) => {
        if (!request.ok) {
          throw new Error("Network response was not ok");
        }
        return request.text();
      })
      .then((html) => {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;
        this.root.appendChild(tempDiv.content.cloneNode(true));
      });

    // Fetch the css
    fetch("static/styles/contact.css")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((css) => {
        const style = document.createElement("style");
        style.textContent = style;
        this.root.appendChild(style);
      });

    // Fetch javascript
    fetch("static/scripts/contact.js")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((js) => {
        const script = document.createElement("script");
        script.textContent = js;
        this.root.appendChild(script);
      });
  }

  connectedCallback() {
    console.log("Contact Page connected");
  }
}

customElements.define("contact-page", ContactPage);

export default ContactPage;
