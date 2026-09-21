import { useEffect, useRef } from "react";
import { WELCOME_MESSAGE } from "../config/chat";
import type { ChatMessage as Message, ServiceStatus } from "../types/chat";
import { ChatMessage } from "./ChatMessage";
import { StatusIndicator } from "./StatusIndicator";
import { TypingIndicator } from "./TypingIndicator";

export function ActiveChat({ messages, loading, error, serviceStatus }: { messages: Message[]; loading: boolean; error: string | null; serviceStatus: ServiceStatus }) {
  const visibleMessages = messages.some((message) => message.id === WELCOME_MESSAGE.id) ? messages : [WELCOME_MESSAGE, ...messages];
  const seen = useRef(new Set(visibleMessages.filter((message) => message.id !== WELCOME_MESSAGE.id).map((message) => message.id)));
  const scrollRef = useRef<HTMLElement>(null);
  const shouldStick = useRef(true);
  const scrollToEnd = () => { if (shouldStick.current && scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight; };
  useEffect(() => { scrollToEnd(); }, [messages, loading]);
  const onProgress = () => scrollToEnd();
  return <>
    <div className="ghaitta-active-status"><StatusIndicator status={serviceStatus} /></div>
    <section ref={scrollRef} className="ghaitta-messages" aria-label="Conversation" aria-live="polite" onScroll={(event) => { const element = event.currentTarget; shouldStick.current = element.scrollHeight - element.scrollTop - element.clientHeight < 80; }}>
      {visibleMessages.map((message) => <ChatMessage key={message.id} message={message} animate={message.id === WELCOME_MESSAGE.id || (message.role === "assistant" && !seen.current.has(message.id))} characterMode={message.id === WELCOME_MESSAGE.id} onProgress={onProgress} onComplete={() => seen.current.add(message.id)} />)}
      {loading && <TypingIndicator />}
      {error && <ChatMessage message={{ id: "error", role: "assistant", content: "Une erreur est survenue lors de la génération de la réponse.", status: "generation_error" }} />}
    </section>
  </>;
}
