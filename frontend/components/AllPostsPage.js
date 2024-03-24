import { getNextPostList } from "../services/GetPosts.js";

class AllPosts extends HTMLElement {
  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });

    // fetch the css
    fetch("static/styles/allPosts.css")
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
    fetch("templates/allPosts.html")
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
    getNextPostList(null, 10, 1);
  }
}

customElements.define("all-posts-page", AllPosts);

export default AllPosts;
