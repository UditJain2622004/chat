/* eslint-disable no-unused-vars */
import React, { useEffect, useMemo, useState, useRef, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext.jsx";
import Message from "../components/Message.jsx";

const BotChat = () => {
  const { botId } = useParams();
  const [bot, setBot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const { dbUserId, isAuthReady } = useAuth();
  const bottomRef = useRef(null);
  const listRef = useRef(null);
  const messagesRef = useRef([]);
  const sendTimerRef = useRef(null);
  const hasPendingSendRef = useRef(false);
  const SEND_IDLE_MS = 2000; // idle window before sending to backend
  const [isBotTyping, setIsBotTyping] = useState(false);

  const scrollToBottom = useCallback((behavior = "smooth") => {
    if (bottomRef.current && bottomRef.current.scrollIntoView) {
      bottomRef.current.scrollIntoView({ behavior, block: "end" });
      return;
    }
    const el = listRef.current || document.getElementById("botchat-messages");
    if (el) el.scrollTo({ top: el.scrollHeight, behavior });
  }, []);

  useEffect(() => {
    const fetchBot = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/bots/${botId}`);
        setBot(res.data || null);
      } catch (e) {
        setError("Failed to load bot");
      } finally {
        setLoading(false);
      }
    };
    fetchBot();
  }, [botId]);

  // Load chat history for this user+bot, if any
  useEffect(() => {
    const loadHistory = async () => {
      if (!isAuthReady || !dbUserId) return;
      try {
        const res = await axios.get(`http://127.0.0.1:5000/chats/`, {
          params: { bot_id: botId, user_id: dbUserId },
        });
        const history = Array.isArray(res.data?.chat_history) ? res.data.chat_history : [];
        const transformed = history.map((m) => ({
          role: m.role,
          content: m.content,
          timestamp: m.timestamp,
          animate: false,
        }));
        setMessages(transformed);
      } catch (err) {
        console.log(err)
        // No chat found; seed a local opener (not persisted until first send)
        setMessages([
          {
            role: "assistant",
            content: `Hi, I'm your bot. Ask me anything!`,
            animate: false,
          },
        ]);
      }
    };
    loadHistory();
  }, [isAuthReady, dbUserId, botId, scrollToBottom]);

  // Auto-scroll on history load or when messages length changes
  useEffect(() => {
    scrollToBottom("auto");
  }, [isAuthReady, dbUserId, botId, scrollToBottom]);

  useEffect(() => {
    scrollToBottom("smooth");
  }, [messages.length, scrollToBottom]);

  // Ensure we scroll into view right after the typing indicator mounts
  useEffect(() => {
    if (isBotTyping) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          scrollToBottom("smooth");
        });
      });
    }
  }, [isBotTyping, scrollToBottom]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (sendTimerRef.current) {
        clearTimeout(sendTimerRef.current);
      }
    };
  }, []);

  // Keep a ref of messages for debounced send
  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);

  const clearSendTimer = useCallback(() => {
    if (sendTimerRef.current) {
      clearTimeout(sendTimerRef.current);
      sendTimerRef.current = null;
    }
  }, []);

  const performSend = useCallback(async () => {
    if (!isAuthReady || !dbUserId) return;
    clearSendTimer();
    if (!hasPendingSendRef.current) return;
    hasPendingSendRef.current = false;
    setIsBotTyping(true);
    requestAnimationFrame(() => scrollToBottom("smooth"));

    const currentMessages = messagesRef.current || [];
    const payloadMessages = currentMessages.map(({ role, content, timestamp }) => ({ role, content, timestamp }));

    try {
      const res = await axios.post("http://127.0.0.1:5000/chats/send", {
        user_id: dbUserId,
        bot_id: botId,
        messages: payloadMessages,
      });
      const reply = res?.data?.reply;
      if (reply) {
        const replyWithAnimate = { ...reply, animate: true };
        setMessages((prev) => [...prev, replyWithAnimate]);
        requestAnimationFrame(() => scrollToBottom("smooth"));
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "system", content: "Failed to send message", animate: false }]);
    } finally {
      setIsBotTyping(false);
    }
  }, [isAuthReady, dbUserId, botId, scrollToBottom, clearSendTimer]);

  const scheduleBackendSend = useCallback(() => {
    hasPendingSendRef.current = true;
    clearSendTimer();
    sendTimerRef.current = setTimeout(() => {
      performSend();
    }, SEND_IDLE_MS);
  }, [clearSendTimer, performSend]);

  const handleProgress = useCallback((phase) => {
    if (phase === "done") {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          scrollToBottom("auto");
          setTimeout(() => scrollToBottom("auto"), 0);
        });
      });
    } else {
      requestAnimationFrame(() => scrollToBottom("smooth"));
    }
  }, [scrollToBottom]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !isAuthReady || !dbUserId) return;

    const userMessage = { role: "user", content: input.trim(), timestamp: new Date().toISOString(), animate: false };
    const pending = [...messages, userMessage];
    setMessages(pending);
    setInput("");
    // Debounce backend send to allow multi-message bursts
    scheduleBackendSend();
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

            <div className="botchat-messages" id="botchat-messages" ref={listRef}>
              {error && (
                <Message role="system" content={error} messageIndex="error" animate={false} />
              )}
              {messages.map((m, idx) => (
                <Message
                  key={idx}
                  role={m.role}
                  content={m.content}
                  messageIndex={idx}
                  animate={m.animate}
                  onProgress={handleProgress}
                />
              ))}
              {isBotTyping && (
                <Message role="assistant" content="" messageIndex="typing" typingOnly />
              )}
              <div ref={bottomRef} />
            </div>

            <form className="botchat-input" onSubmit={sendMessage}>
              <div className="input-container">
                <button type="button" className="attachment-btn" title="Attach">📎</button>
                <input
                  className="message-input"
                  value={input}
                  onChange={(e) => {
                    setInput(e.target.value);
                    if (hasPendingSendRef.current) {
                      scheduleBackendSend();
                    }
                  }}
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


