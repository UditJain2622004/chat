import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signInWithEmail } from "../firebase";
import GoogleSignIn from "../components/GoogleSignIn";
import axios from "axios";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const result = await signInWithEmail(email, password);
      const user = result.user;
      const idToken = await user.getIdToken();

      await axios.post(
        "http://127.0.0.1:5000/auth/sync-user",
        {},
        {
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
        }
      );

      navigate("/welcome");
    } catch (error) {
      console.error("Error logging in:", error);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
      <hr />
      <GoogleSignIn onSignInSuccess={() => navigate("/welcome")} />
    </div>
  );
};

export default Login;
