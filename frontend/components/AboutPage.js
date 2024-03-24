class AboutPage extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // fetch the css
    fetch("static/styles/about.css")
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
    fetch("templates/about.html")
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
  }
}

customElements.define("about-page", AboutPage);

export default AboutPage;
