import React, { useEffect, useMemo, useRef, useState } from "react";

const Message = ({ role, content, messageIndex, animate = false, onProgress, typingOnly = false }) => {
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
  const avatarText = role === "user" ? "U" : "B";

  const shouldAnimate = animate && role !== "user" && segments.length > 1;
  const [visibleCount, setVisibleCount] = useState(shouldAnimate ? 1 : segments.length);
  const timeoutsRef = useRef([]);
  const onProgressRef = useRef(onProgress);

  useEffect(() => {
    onProgressRef.current = onProgress;
  }, [onProgress]);

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

    let cumulative = 0;
    for (let i = 1; i < segments.length; i += 1) {
      const seg = segments[i];
      const segDelay = Math.min(Math.max(seg.length * msPerChar, minDelay), maxDelay);
      cumulative += segDelay;
      const id = setTimeout(() => {
        setVisibleCount((prev) => {
          // Only increase, in case of overlapping timers
          return Math.max(prev, i + 1);
        });
      }, cumulative);
      timeoutsRef.current.push(id);
    }

    return () => {
      timeoutsRef.current.forEach((id) => clearTimeout(id));
      timeoutsRef.current = [];
    };
  }, [role, shouldAnimate, segments]);

  // Notify parent to scroll after each reveal commit
  useEffect(() => {
    if (!shouldAnimate || typeof onProgressRef.current !== "function") return () => {};
    const isDone = visibleCount >= segments.length;
    const rafId = requestAnimationFrame(() => {
      onProgressRef.current && onProgressRef.current(isDone ? "done" : "step");
    });
    return () => cancelAnimationFrame(rafId);
  }, [visibleCount, shouldAnimate, segments.length]);

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
            <div className="message-bubble"><p>{seg}</p></div>
          </div>
        </div>
      ))}
      {shouldAnimate && visibleCount < segments.length && (
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


