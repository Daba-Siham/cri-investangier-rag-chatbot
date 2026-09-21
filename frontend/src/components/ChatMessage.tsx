import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { isArabic } from "../utils/language";
import type { ChatMessage as Message } from "../types/chat";
import { TypewriterText } from "./TypewriterText";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";

function UserIcon() { return <span className="ghaitta-user-icon" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><circle cx="12" cy="8" r="3.5" /><path d="M5.5 20c.7-3.5 3-5.2 6.5-5.2s5.8 1.7 6.5 5.2" /></svg></span>; }

export function ChatMessage({ message, animate = false, characterMode = false, onProgress, onComplete }: { message: Message; animate?: boolean; characterMode?: boolean; onProgress?: () => void; onComplete?: () => void }) {
  const [complete, setComplete] = useState(!animate);
  const speech = useSpeechSynthesis();
  const canSpeak = speech.canSpeak(message.content);
  const finish = () => { setComplete(true); onComplete?.(); };
  const assistantError = message.role === "assistant" && message.status !== "answered";
  const renderedContent = message.role === "assistant" && message.status === "answered" && complete
    ? <ReactMarkdown>{message.content}</ReactMarkdown>
    : <p><TypewriterText text={message.content} animate={animate} characterMode={characterMode} onProgress={onProgress} onComplete={finish} /></p>;
  const unavailableReason = speech.unavailableReason(message.content);
  return <article className={`ghaitta-message-row ghaitta-message-row--${message.role}`}>{message.role === "assistant" && <img className="ghaitta-message__avatar" src="/assets/chat/ghaitta-avatar.jpg" alt="GH-AI-TTA" />}<div className={`ghaitta-message message-bubble ${assistantError ? "ghaitta-message--error" : ""}`} dir={isArabic(message.content) ? "rtl" : "ltr"}>{renderedContent}{message.role === "assistant" && message.status === "answered" && complete && <button type="button" className="ghaitta-message__speak" disabled={!canSpeak} aria-label={speech.speaking ? "Arrêter la lecture" : canSpeak ? "Lire la réponse" : "Lecture audio non disponible"} title={unavailableReason} onClick={() => speech.toggle(message.content)}><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{speech.speaking ? <path d="M8 7v10M16 7v10" /> : <path d="M4 10v4h4l5 4V6l-5 4H4m12 1.5a3 3 0 0 1 0 3" />}</svg></button>}</div>{message.role === "user" && <UserIcon />}</article>;
}
