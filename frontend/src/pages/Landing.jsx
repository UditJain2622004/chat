import React from "react";
import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className="page page-landing">
      <div className="container hero">
        <div className="hero-content">
          <div className="brand">Chat App</div>
          <h1 className="hero-title">Talk to your AI companion</h1>
          <p className="hero-subtitle">
            Create personas, remember moments, and keep the conversation flowing.
          </p>
          <div className="hero-actions">
            <Link className="btn btn-primary" to="/login">Log in</Link>
            <Link className="btn btn-secondary" to="/signup">Sign up</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
