function formatDate(dateString) {
  // Create a new Date object from the ISO 8601 formatted string
  const date = new Date(dateString);

  // Options for formatting the date
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    timeZone: "UTC",
  };
  return new Intl.DateTimeFormat("en-US", options).format(date);
}

console.log(formattedDate);

export default RenderPosts = (posts) => {
  const postList = document.querySelector(".post-list");
  postList.innerHTML = "";
  const posts = JSON.parse(posts);
  if (posts.count === 0) {
    postList.innerHTML = "<p class='no-posts-found'>No posts found</p>";
    return;
  }
  posts.results.map((post) => {
    const postLi = document.createElement("li");
    const postItem = document.createElement("post-item");
    postItem.setAttribute("data-id", post.id);
    postItem
      .querySelector("img")
      .setAttribute(
        "src",
        post.cover_image
          ? post.cover_image
          : "static/images/post-placeholder.png"
      );
    postItem.querySelector(".title").innerHTML = post.title;
    postItem.querySelector(".date-created").innerHTML = formatDate(
      post.date_created
    );
    postItem.querySelector(".date-updated").innerHTML = formatDate(
      post.date_updated
    );
    postItem.querySelector(".views").innerHTML = `Views: ${post.views}`;
    postItem.querySelector(".likes-counter").innerHTML = post.likes;
    postItem.querySelector(
      ".author"
    ).innerHTML = `${post.author.first_name} ${post.author.last_name}`;
    postItem
      .querySelector(".author-link")
      .setAttribute("data-author-id", post.author.id);
    postLi.appendChild(postItem);
    postList.appendChild(postLi);
  });
};
