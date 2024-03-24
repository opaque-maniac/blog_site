import RenderPosts from "./RenderPosts.js";

export function getNextPostList(next, result_size, current_page) {
  if (next) {
    const url = next;
  } else {
    const url = `http://127.0.0.1:8000/api/posts/posts/?page_size=${
      result_size ? result_size : 10
    }`;
  }

  fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      RenderPosts(data);
      return;
    });
}
