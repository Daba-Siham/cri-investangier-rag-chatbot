import { useEffect, useState } from "react";
import { type SupportedLocale } from "../config/branding";
import type { ChatMessage as Message, ServiceStatus } from "../types/chat";
import { ActiveChat } from "./ActiveChat";
import { ChatHeader } from "./ChatHeader";
import { ChatInput } from "./ChatInput";
import { ChatLauncher } from "./ChatLauncher";
import { ChatModal } from "./ChatModal";
import { WelcomeScreen } from "./WelcomeScreen";

export interface ChatWidgetProps {
  messages: Message[];
  loading: boolean;
  error: string | null;
  serviceStatus: ServiceStatus;
  onSend: (message: string) => void;
  onNewConversation: () => void;
  initialOpen?: boolean;
  locale?: SupportedLocale;
}

export function ChatWidget({ messages, loading, error, serviceStatus, onSend, onNewConversation, initialOpen = false, locale = "fr" }: ChatWidgetProps) {
  const [open, setOpen] = useState(initialOpen);
  const [started, setStarted] = useState(false);

  useEffect(() => {
    if (!open) return;
    const close = (event: KeyboardEvent) => { if (event.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, [open]);

  const newConversation = () => { onNewConversation(); setStarted(true); };
  const send = (message: string) => { setStarted(true); onSend(message); };

  return <div className="ghaitta-widget" dir={locale === "ar" ? "rtl" : "ltr"}>
    {!open && <ChatLauncher onOpen={() => setOpen(true)} />}
    {open && <ChatModal onClose={() => setOpen(false)}>
      {!started ? <WelcomeScreen locale={locale} onStart={() => setStarted(true)} onClose={() => setOpen(false)} /> : <div className="ghaitta-active-chat">
        <ChatHeader onClose={() => setOpen(false)} onNewConversation={newConversation} />
        <ActiveChat messages={messages} loading={loading} error={error} serviceStatus={serviceStatus} />
        <ChatInput loading={loading} onSend={send} locale={locale} />
        <p className="ghaitta-privacy ghaitta-widget__privacy">Les réponses sont générées à partir des documents internes fournis.</p>
      </div>}
    </ChatModal>}
  </div>;
}
