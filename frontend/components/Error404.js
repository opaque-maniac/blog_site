// In Error404.js

class Error404 extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // Fetch error404.html content
    fetch("templates/error404.html")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((html) => {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;
        const errorTemplate = tempDiv.querySelector("#error404");
        this.root.appendChild(errorTemplate.content.cloneNode(true));
      })
      .catch((error) => {
        console.error("Error fetching error404.html:", error);
      });

    // Fetch error404.css content
    fetch("static/styles/error404.css")
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
  }
}

// Define the custom element
customElements.define("error-404", Error404);

// Export the custom element
export default Error404;
