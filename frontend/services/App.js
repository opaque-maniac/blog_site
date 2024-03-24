const App = {
  app: "Blogger",
  user: null,
  token: localStorage.getItem("token") ? localStorage.getItem("token") : null,
  authenticated: null,
};

export default App;
