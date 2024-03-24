const loginUser = (data) => {
    const { url, email, password } = data;
  console.log(`Logging in with: ${email} and ${password} to ${url}`);
  return;
};

export default loginUser;
