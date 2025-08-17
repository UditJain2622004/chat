import React from "react";
import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div>
      <h1>Welcome to the Chat App</h1>
      <Link to="/login">Login</Link>
      <br />
      <Link to="/signup">Sign Up</Link>
    </div>
  );
};

export default Landing;
