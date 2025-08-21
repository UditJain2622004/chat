import { useCallback, useEffect, useRef, useState } from "react";

export default function useStickToBottom({ containerRef, bottomRef, enabled = true, threshold = 0, behaviorPinned = "smooth" } = {}) {
  const pinnedRef = useRef(true);
  const [isPinned, setIsPinned] = useState(true);

  const scrollToBottom = useCallback((behavior = behaviorPinned) => {
    const bottomEl = bottomRef?.current;
    if (bottomEl && typeof bottomEl.scrollIntoView === "function") {
      bottomEl.scrollIntoView({ behavior, block: "end" });
      return;
    }
    const root = containerRef?.current;
    if (root) root.scrollTo({ top: root.scrollHeight, behavior });
  }, [containerRef, bottomRef, behaviorPinned]);

  useEffect(() => {
    if (!enabled) return () => {};
    const root = containerRef?.current;
    const bottomEl = bottomRef?.current;
    if (!root || !bottomEl) return () => {};

    const setPinned = (val) => {
      pinnedRef.current = val;
      setIsPinned(val);
    };

    // Observe bottom sentinel visibility within container
    const io = new IntersectionObserver(
      (entries) => {
        const e = entries[0];
        const isVisible = e?.isIntersecting || (e?.intersectionRatio ?? 0) > 0;
        setPinned(isVisible);
      },
      { root, rootMargin: `0px 0px ${threshold}px 0px`, threshold: 0 }
    );
    io.observe(bottomEl);

    // On DOM mutations inside container, keep pinned if we were pinned
    const mo = new MutationObserver(() => {
      if (!enabled || !pinnedRef.current) return;
      requestAnimationFrame(() => scrollToBottom());
    });
    mo.observe(root, { childList: true, subtree: true, characterData: true });

    // On resize (e.g., fonts/images/layout), keep pinned if we were pinned
    let ro;
    if (typeof ResizeObserver !== "undefined") {
      ro = new ResizeObserver(() => {
        if (!enabled || !pinnedRef.current) return;
        requestAnimationFrame(() => scrollToBottom());
      });
      ro.observe(root);
    }

    return () => {
      io.disconnect();
      mo.disconnect();
      if (ro) ro.disconnect();
    };
  }, [containerRef, bottomRef, enabled, threshold, scrollToBottom]);

  return { isPinned, scrollToBottom };
}


