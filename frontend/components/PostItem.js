class PostItem extends HTMLElement {
  constructor() {
    super();
    const imageContainer = document
      .createElement("div")
      .className("image-container");
    const image = document.createElement("img");
    imageContainer.appendChild(image);
    const detailsContainer = document
      .createElement("div")
      .classList.add("details-container");
    const title = document.createElement("h3").classList.add("title");
    const date_created = document
      .createElement("p")
      .classList.add("date-created");
    const date_updated = document
      .createElement("p")
      .classList.add("date-updated");
    const views = document.createElement("p").classList.add("views");
    const likes = document.createElement("div").classList.add("likes");
    const likeIcon = document.createElement("span").classList.add("fa-regular");
    likeIcon.classList.add("fa-thumbs-up");
    const likeCounter = document
      .createElement("span")
      .classList.add("likes-counter");
    likes.appendChild(likeIcon);
    likes.appendChild(likeCounter);
    const author = document.createElement("p").classList.add("author");
    const authorLink = document.createElement("a").classList.add("author-link");
    authorLink.innerHTML = `By ${author}`;
    detailsContainer.appendChild(title);
    detailsContainer.appendChild(date_created);
    detailsContainer.appendChild(date_updated);
    detailsContainer.appendChild(views);
    detailsContainer.appendChild(likes);
    detailsContainer.appendChild(authorLink);
    this.appendChild(imageContainer);
    this.appendChild(detailsContainer);
    this.style.cursor = "pointer";
  }

  connectedCallback() {
    this.addEventListener("click", () => {
      const id = this.getAttribute("data-id");
      window.Router.go(`/posts/${id}`);
    });
    this.querySelector(".author-link").addEventListener("click", () => {
      const id = this.getAttribute("data-author-id");
      window.Router.go(`/profile/${id}`);
    });
  }

  disconnectedCallback() {
    this.removeEventListener("click");
    this.querySelector(".author-link").removeEventListener("click");
  }
}

customElements.define("post-item", PostItem);

export default PostItem;
