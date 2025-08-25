import React, { useEffect, useMemo, useRef, useState } from "react";

const Message = ({ role, content, messageIndex, animate = false, typingOnly = false, timestamp, botName }) => {
  const extractSegments = (text) => {
    if (typeof text !== "string") return [String(text ?? "")];
    const regex = /<msg>([\s\S]*?)<\/msg>/g;
    const segments = [];
    let match;
    while ((match = regex.exec(text)) !== null) {
      const segment = match[1].trim();
      if (segment.length > 0) segments.push(segment);
    }
    if (segments.length === 0) {
      return [text];
    }
    return segments;
  };

  const segments = useMemo(() => extractSegments(content), [content]);

  const messageClass = role === "user" ? "me" : role === "system" ? "system" : "other";
  const showAvatar = role !== "system";
  const avatarText = role === "user" ? "U" : botName?.[0].toUpperCase() || "B";

  const formatTimestamp = (ts) => {
    if (!ts) return "";
    try {
      const d = new Date(ts);
      return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    } catch {
      return "";
    }
  };
  const senderLabel = role === "user" ? "You" : role === "assistant" ? (botName || "Bot") : "";
  const formattedTime = formatTimestamp(timestamp);

  const shouldAnimate = animate && role !== "user" && segments.length > 1;
  const [visibleCount, setVisibleCount] = useState(shouldAnimate ? 1 : segments.length);
  const timeoutsRef = useRef([]);
  const typingTimerRef = useRef(null);
  const [showTyping, setShowTyping] = useState(false);

  useEffect(() => {
    // Reset visible segments and timers whenever content or role changes
    timeoutsRef.current.forEach((id) => clearTimeout(id));
    timeoutsRef.current = [];

    if (!shouldAnimate) {
      setVisibleCount(segments.length);
      return () => {};
    }

    setVisibleCount(1);


    const msPerChar = 150; // typing-like delay per character
    const minDelay = 2500; // minimum delay per segment
    const maxDelay = 10000; // cap to avoid excessive waits
    const afterSegmentDelay = 500; // wait after each shown segment before showing dots

    // After the first segment is shown, schedule the typing dots for the gap before the next segment
    setShowTyping(false);
    if (typingTimerRef.current) clearTimeout(typingTimerRef.current);
    typingTimerRef.current = setTimeout(() => setShowTyping(true), afterSegmentDelay);

    let cumulative = 0;
    for (let i = 1; i < segments.length; i += 1) {
      const seg = segments[i];
      const segDelay = Math.min(Math.max(seg.length * msPerChar, minDelay), maxDelay);
      cumulative += segDelay;
      const id = setTimeout(() => {
        setVisibleCount((prev) => Math.max(prev, i + 1));
        // Hide dots immediately after revealing a segment; the separate effect will re-show after delay
        setShowTyping(false);
        if (typingTimerRef.current) clearTimeout(typingTimerRef.current);
        typingTimerRef.current = setTimeout(() => setShowTyping(true), afterSegmentDelay);
      }, cumulative);
      timeoutsRef.current.push(id);
    }

    return () => {
      timeoutsRef.current.forEach((id) => clearTimeout(id));
      timeoutsRef.current = [];
      if (typingTimerRef.current) clearTimeout(typingTimerRef.current);
    };
  }, [role, shouldAnimate, segments]);

  // Also guard the typing bubble at boundaries
  useEffect(() => {
    if (!shouldAnimate || visibleCount >= segments.length) {
      setShowTyping(false);
      if (typingTimerRef.current) clearTimeout(typingTimerRef.current);
      return () => {};
    }
    return () => {};
  }, [shouldAnimate, visibleCount, segments.length]);

  // No per-message scrolling; container handles stick-to-bottom

  const segmentsToRender = shouldAnimate ? segments.slice(0, visibleCount) : segments;

  if (typingOnly) {
    return (
      <div className={`message ${messageClass} typing`}>
        {showAvatar && <div className="message-avatar">{avatarText}</div>}
        <div className="message-content">
          <div className="message-bubble typing-bubble">
            <div className="typing-dots">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      {segmentsToRender.map((seg, index) => (
        <div key={`${messageIndex}-${index}`} className={`message ${messageClass}`}>
          {showAvatar && <div className="message-avatar">{avatarText}</div>}
          <div className="message-content">
            <div className="message-bubble">
              {(senderLabel) && (
                <div className="message-meta muted" style={{ fontSize: "0.75em",color:"#FF69B4", marginBottom: "0px", opacity: 0.75, fontWeight: "bold" }}>
                  {senderLabel}
                </div>
              )}
              <p style={{ margin:"2px"}}>{seg}</p>
              {(formattedTime) && (
                <div className="message-meta muted" style={{ fontSize: "0.60em", marginBottom: "0px", opacity: 0.50, textAlign: "right" }}>
                  {formattedTime}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
      {shouldAnimate && visibleCount < segments.length && showTyping && (
        <div className={`message ${messageClass} typing`}>
          {showAvatar && <div className="message-avatar">{avatarText}</div>}
          <div className="message-content">
            <div className="message-bubble typing-bubble">
              <div className="typing-dots">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Message;


