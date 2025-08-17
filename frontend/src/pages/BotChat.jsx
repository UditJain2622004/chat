/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

const BotChat = () => {
  const { botId } = useParams();
  const [bot, setBot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    const fetchBot = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/bots/${botId}`);
        setBot(res.data || null);
        // seed a friendly opener once
        setMessages([
          {
            role: "assistant",
            content: `Hi, I'm ${res.data?.name || "your bot"}. Ask me anything!`,
          },
        ]);
      } catch (e) {
        setError("Failed to load bot");
      } finally {
        setLoading(false);
      }
    };
    fetchBot();
  }, [botId]);

  const sendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((prev) => [
      ...prev,
      { role: "user", content: input.trim() },
    ]);
    setInput("");
  };

  return (
    <div className="chat-page">
      <div className="chat-layout">
        <aside className="sidebar">
          <div className="sidebar-header">
            <Link to="/welcome" className="btn btn-secondary btn-block">← Back</Link>
            <h3>Tasks</h3>
          </div>
          <div className="sidebar-content">
            <p className="muted">No tasks yet.</p>
          </div>
        </aside>

        <main className="chat-main">
          <div className="botchat-container">
            <div className="botchat-header">
              <div className="header-content">
                <div className="user-info">
                  {bot?.picture ? (
                    <img className="avatar" src={bot.picture} alt={bot?.name} />
                  ) : (
                    <div className="avatar">{(bot?.name || "?").slice(0,1).toUpperCase()}</div>
                  )}
                  <div className="user-details">
                    <h3>{loading ? "Loading..." : bot?.name || "Bot"}</h3>
                    {!loading && (
                      <div className="status">
                        {bot?.behaviour}
                        {bot?.ethnicity ? ` • ${bot.ethnicity}` : ""}
                        {bot?.physique ? ` • ${bot.physique}` : ""}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div className="botchat-messages">
              {error && (
                <div className="message system">
                  <div className="message-content">
                    <div className="message-bubble"><p>{error}</p></div>
                  </div>
                </div>
              )}
              {messages.map((m, idx) => (
                <div key={idx} className={`message ${m.role === "user" ? "me" : "other"}`}>
                  <div className="message-avatar">{m.role === "user" ? "U" : "B"}</div>
                  <div className="message-content">
                    <div className="message-bubble"><p>{m.content}</p></div>
                  </div>
                </div>
              ))}
            </div>

            <form className="botchat-input" onSubmit={sendMessage}>
              <div className="input-container">
                <button type="button" className="attachment-btn" title="Attach">📎</button>
                <input
                  className="message-input"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Message the bot..."
                />
                <button type="button" className="emoji-btn" title="Emoji">😊</button>
                <button type="submit" className="send-btn">➤</button>
              </div>
            </form>
          </div>
        </main>
      </div>
    </div>
  );
};

export default BotChat;


