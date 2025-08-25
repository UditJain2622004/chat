/* eslint-disable no-unused-vars */
import React, { useEffect, useMemo, useState, useRef, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext.jsx";
import Message from "../components/Message.jsx";
import useStickToBottom from "../hooks/useStickToBottom";
import { getLatestUserMessages } from "../utils/utils";

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

  const { scrollToBottom } = useStickToBottom({
    containerRef: listRef,
    bottomRef,
    enabled: true,
    threshold: 40,
    behaviorPinned: "smooth",
  });

  const [chatList, setChatList] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);

  // Single initial load: fetch bot and chats together
  useEffect(() => {
    const fetchBotAndChats = async () => {
      if (!isAuthReady || !dbUserId) return;
      setLoading(true);
      try {
        const res = await axios.get(`http://127.0.0.1:5000/chats/bot`, {
          params: { bot_id: botId, user_id: dbUserId },
        });
        const botDoc = res?.data?.bot || null;
        const chats = Array.isArray(res?.data?.chats) ? res.data.chats : [];
        setBot(botDoc);
        setChatList(chats);
        if (chats.length > 0) {
          const firstChat = chats[0];
          setActiveChatId(firstChat._id || null);
          const history = Array.isArray(firstChat.chat_history) ? firstChat.chat_history : [];
          const transformed = history.map((m) => ({
            role: m.role,
            content: m.content,
            timestamp: m.timestamp,
            animate: false,
          }));
          setMessages(transformed);
        } else {
          setMessages([
            {
              role: "assistant",
              content: `Hi, I'm your bot. Ask me anything!`,
              timestamp: new Date().toISOString(),
              animate: false,
            },
          ]);
        }
      } catch (e) {
        setError("Failed to load bot/chats");
      } finally {
        setLoading(false);
      }
    };
    fetchBotAndChats();
  }, [botId, isAuthReady, dbUserId]);

  // Allow switching the visible chat by clicking an id in sidebar
  const handleSelectChat = useCallback((chatId) => {
    if (!chatList || chatList.length === 0) return;
    const found = chatList.find((c) => c._id === chatId);
    if (!found) return;
    setActiveChatId(chatId);
    // Optimistic local render
    const history = Array.isArray(found.chat_history) ? found.chat_history : [];
    const transformed = history.map((m) => ({
      role: m.role,
      content: m.content,
      timestamp: m.timestamp,
      animate: false,
    }));
    setMessages(transformed);
    requestAnimationFrame(() => scrollToBottom("auto"));

    // Fetch latest from backend to ensure freshness
    axios
      .get(`http://127.0.0.1:5000/chats/id/${chatId}`)
      .then((res) => {
        const latest = Array.isArray(res?.data?.chat_history) ? res.data.chat_history : [];
        const transformedLatest = latest.map((m) => ({
          role: m.role,
          content: m.content,
          timestamp: m.timestamp,
          animate: false,
        }));
        setMessages(transformedLatest);
        requestAnimationFrame(() => scrollToBottom("auto"));
      })
      .catch(() => {
        // keep optimistic state on failure
      });
  }, [chatList, scrollToBottom]);

  const handleNewChat = useCallback(async () => {
    if (!isAuthReady || !dbUserId) return;
    try {
      const res = await axios.post(`http://127.0.0.1:5000/chats/`, {
        user_id: dbUserId,
        bot_id: botId,
        chat_history: [],
      });
      const newId = res?.data?._id;
      if (newId) {
        const newChat = { _id: newId, user_id: dbUserId, bot_id: botId, chat_history: [] };
        setChatList((prev) => [newChat, ...prev]);
        setActiveChatId(newId);
        setMessages([]);
        requestAnimationFrame(() => scrollToBottom("auto"));
      }
    } catch (e) {
      setError("Failed to create chat");
    }
  }, [isAuthReady, dbUserId, botId, scrollToBottom]);

  // Keep pinned on initial loads
  useEffect(() => {
    scrollToBottom("auto");
  }, [isAuthReady, dbUserId, botId, scrollToBottom]);

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

    const currentMessages = messagesRef.current || [];
    const latestUserMessages = getLatestUserMessages(currentMessages);
    const payloadMessages = latestUserMessages.map(({ role, content, timestamp }) => ({ role, content, timestamp }));

    try {
      // Ensure we have a chat to send to
      let chatIdToUse = activeChatId;
      if (!chatIdToUse) {
        await handleNewChat();
        chatIdToUse = activeChatId;
        if (!chatIdToUse) {
          setIsBotTyping(false);
          return;
        }
      }
      const res = await axios.post("http://127.0.0.1:5000/chats/send", {
        user_id: dbUserId,
        bot_id: botId,
        chat_id: chatIdToUse,
        messages: payloadMessages,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
      });
      const reply = res?.data?.reply;
      if (reply) {
        // Hide typing indicator before rendering the new assistant message
        setIsBotTyping(false);
        const replyWithAnimate = { ...reply, animate: true, timestamp: reply.timestamp || new Date().toISOString() };
        setMessages((prev) => [...prev, replyWithAnimate]);
        requestAnimationFrame(() => scrollToBottom("smooth"));
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "system", content: "Failed to send message", animate: false }]);
    } finally {
      setIsBotTyping(false);
    }
  }, [isAuthReady, dbUserId, botId, activeChatId, handleNewChat, scrollToBottom, clearSendTimer]);

  const scheduleBackendSend = useCallback(() => {
    hasPendingSendRef.current = true;
    clearSendTimer();
    sendTimerRef.current = setTimeout(() => {
      performSend();
    }, SEND_IDLE_MS);
  }, [clearSendTimer, performSend]);

  // Stick-to-bottom hook handles scrolling; no per-message progress scrolling needed

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !isAuthReady || !dbUserId) return;

    const currentTimestamp = new Date();
    // console.log(currentTimestamp);  Mon Aug 25 2025 13:50:28 GMT+0530 (India Standard Time)
    // console.log(currentTimestamp.toLocaleString()); 8/25/2025, 1:50:28 PM
    
    
    const message = `<timestamp>${currentTimestamp}</timestamp>\n<msg>${input.trim()}</msg>`
    const userMessage = { role: "user", content: message, timestamp: new Date().toISOString(), animate: false };
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
            <h3>Chats</h3>
            <button type="button" className="btn btn-primary btn-block" onClick={handleNewChat}>+ New chat</button>
          </div>
          <div className="sidebar-content">
            {chatList && chatList.length > 0 ? (
              <ul className="list">
                {chatList.map((c) => (
                  <li key={c._id}>
                    <button
                      type="button"
                      className={`btn btn-link ${activeChatId === c._id ? 'active-chat' : ''}`}
                      onClick={() => handleSelectChat(c._id)}
                      title={c._id}
                    >
                      {c._id}
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="muted">No chats yet.</p>
            )}
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
                  timestamp={m.timestamp}
                  botName={bot?.name}
                />
              ))}
              {isBotTyping && (
                <Message role="assistant" content="" messageIndex="typing" typingOnly botName={bot?.name} />
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


