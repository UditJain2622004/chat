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
    <div className="page page-auth">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Welcome back</h2>
          <p>Log in to continue your conversation</p>
        </div>
        <form onSubmit={handleLogin} className="auth-form">
          <div className="form-field">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>
          <div className="form-field">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          <button className="btn btn-primary btn-block" type="submit">Login</button>
        </form>
        <div className="divider"><span>or</span></div>
        <GoogleSignIn onSignInSuccess={() => navigate("/welcome")} />
      </div>
    </div>
  );
};

export default Login;
