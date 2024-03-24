export const userIsLoggedIn = () => {
  if (localStorage.getItem("token")) {
    return true;
  }
  return false;
};

export const userIsNotLoggedIn = () => {
  if (!localStorage.getItem("token")) {
    return true;
  }
  return false;
};

export const handleNotAuthenticated = () => {
  dispatchEvent(new CustomEvent("user:loggedOut"));
  console.log("User is not authenticated");
};

export const handleAreadyAuthenticated = () => {
  dispatchEvent(new CustomEvent("user:loggedIn"));
  console.log("User is already authenticated");
};

export const updateAuthenticationStatus = () => {
  window.App.authenticated = userIsLoggedIn();
};
