import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signUpWithEmail } from "../firebase";
import GoogleSignIn from "../components/GoogleSignIn";
import axios from "axios";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const result = await signUpWithEmail(email, password);
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
      console.error("Error signing up:", error);
    }
  };

  return (
    <div className="page page-auth">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Create your account</h2>
          <p>Join and start chatting with your AI companion</p>
        </div>
        <form onSubmit={handleSignup} className="auth-form">
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
          <button className="btn btn-primary btn-block" type="submit">Sign Up</button>
        </form>
        <div className="divider"><span>or</span></div>
        <GoogleSignIn onSignInSuccess={() => navigate("/welcome")} />
      </div>
    </div>
  );
};

export default Signup;
