class HomePage extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // Fetch home.html content
    fetch("templates/home.html")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((html) => {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;
        const homeTemplate = tempDiv.querySelector("#homePage");
        this.root.appendChild(homeTemplate.content.cloneNode(true));
      });

    // Fetch home.css content
    fetch("static/styles/home.css")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((css) => {
        const style = document.createElement("style");
        style.innerHTML = css;
        this.root.appendChild(style);
      });
  }
}

customElements.define("home-page", HomePage);

export default HomePage;
