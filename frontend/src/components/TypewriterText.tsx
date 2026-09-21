import { useEffect, useMemo, useRef, useState } from "react";

export const TYPEWRITER_DELAY_MS = 30;
export const CHARACTER_TYPEWRITER_DELAY_MS = 24;
function reducedMotion() { return typeof window !== "undefined" && typeof window.matchMedia === "function" && window.matchMedia("(prefers-reduced-motion: reduce)").matches; }

export function TypewriterText({ text, animate, characterMode = false, onProgress, onComplete }: { text: string; animate: boolean; characterMode?: boolean; onProgress?: () => void; onComplete?: () => void }) {
  const tokens = useMemo(() => characterMode ? Array.from(text) : text.match(/\S+\s*/gu) ?? [], [text, characterMode]);
  const [count, setCount] = useState(() => animate && !reducedMotion() ? 0 : tokens.length);
  const progressRef = useRef(onProgress); const completeRef = useRef(onComplete);
  progressRef.current = onProgress; completeRef.current = onComplete;
  useEffect(() => {
    if (!animate || reducedMotion()) { setCount(tokens.length); completeRef.current?.(); return; }
    setCount(0); let current = 0;
    const timer = window.setInterval(() => { current += 1; setCount(current); progressRef.current?.(); if (current >= tokens.length) { window.clearInterval(timer); completeRef.current?.(); } }, characterMode ? CHARACTER_TYPEWRITER_DELAY_MS : TYPEWRITER_DELAY_MS);
    return () => window.clearInterval(timer);
  }, [animate, tokens]);
  return <>{tokens.slice(0, count).join("")}</>;
}
