/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext.jsx";

const Welcome = () => {
  const [loading, setLoading] = useState(true);
  const [bots, setBots] = useState([]);
  const [error, setError] = useState("");

  const { isAuthReady, dbUserId, idToken } = useAuth();

  useEffect(() => {
    const loadBots = async () => {
      if (!isAuthReady) return; // wait for auth rehydration
      if (!dbUserId) {
        setLoading(false);
        return;
      }
      try {
        const botsRes = await axios.get(
          `http://127.0.0.1:5000/bots/?user_id=${dbUserId}`
        );
        setBots(Array.isArray(botsRes.data) ? botsRes.data : []);
      } catch (e) {
        setError("Failed to load bots");
      } finally {
        setLoading(false);
      }
    };
    loadBots();
  }, [isAuthReady, dbUserId]);

  return (
    <div className="page page-welcome">
      <div className="container">
        <div className="welcome-head">
          <div>
            <h1>Your Bots</h1>
            <p className="muted">Manage your companions or create a new one.</p>
          </div>
          <Link to="/bots/new" className="btn btn-primary">Create new bot</Link>
        </div>

        {loading ? (
          <div className="welcome-card"><p>Loading...</p></div>
        ) : error ? (
          <div className="welcome-card"><p>{error}</p></div>
        ) : bots.length === 0 ? (
          <div className="welcome-card empty-state">
            <div className="welcome-badge">🤖</div>
            <h2>No bots yet</h2>
            <p>Create your first bot to start chatting.</p>
            <Link to="/bots/new" className="btn btn-primary">Create a bot</Link>
          </div>
        ) : (
          <div className="bot-grid">
            {bots.map((bot) => (
              <Link key={bot._id} to={`/bots/${bot._id}/chat`} className="bot-card link-card">
                <div className="bot-card-head">
                  {bot.picture ? (
                    <img className="bot-avatar" src={bot.picture} alt={bot.name} />
                  ) : (
                    <div className="bot-avatar placeholder">{(bot.name || "?").slice(0,1).toUpperCase()}</div>
                  )}
                  <div className="bot-meta">
                    <h3>{bot.name}</h3>
                    <span className="tag">{bot.behaviour}</span>
                  </div>
                </div>
                {Array.isArray(bot.likings) && bot.likings.length > 0 && (
                  <div className="bot-tags">
                    {bot.likings.map((lk, idx) => (
                      <span key={idx} className="chip">{lk}</span>
                    ))}
                  </div>
                )}
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Welcome;
