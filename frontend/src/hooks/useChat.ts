import { useCallback, useEffect, useRef, useState } from "react";
import { checkHealth, checkReady, deleteSession, sendMessage } from "../api/chatApi";
import { WELCOME_MESSAGE } from "../config/chat";
import type { ChatMessage, ChatResponse, ServiceStatus } from "../types/chat";

function messageId() { return crypto.randomUUID?.() ?? `${Date.now()}-${Math.random()}`; }

function fallbackAnswer(status: ChatResponse["status"], question: string): string {
  const arabic = /[\u0600-\u08ff]/u.test(question);
  if (status === "model_unavailable") return arabic ? "نموذج الإجابة غير متاح مؤقتاً." : "Le modèle de génération est temporairement indisponible.";
  if (status === "generation_error") return arabic ? "حدث خطأ أثناء إنشاء الإجابة." : "Une erreur est survenue lors de la génération de la réponse.";
  return "La réponse n’a pas pu être générée. Veuillez réessayer.";
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [serviceStatus, setServiceStatus] = useState<ServiceStatus>({ status: "checking" });
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    Promise.all([checkHealth(), checkReady()])
      .then(([, ready]) => setServiceStatus(ready))
      .catch(() => setServiceStatus({ status: "unavailable" }));
    return () => abortRef.current?.abort();
  }, []);

  const send = useCallback(async (content: string) => {
    const value = content.trim();
    if (!value || loading) return;
    setError(null);
    setMessages((current) => [...current, { id: messageId(), role: "user", content: value }]);
    const controller = new AbortController();
    abortRef.current = controller;
    setLoading(true);
    try {
      const response: ChatResponse = await sendMessage({ message: value, ...(sessionId ? { session_id: sessionId } : {}) }, controller.signal);
      setSessionId(response.session_id);
      const emptyAnswered = response.status === "answered" && !response.answer?.trim();
      const status = emptyAnswered ? "generation_error" : response.status;
      setMessages((current) => [...current, { id: messageId(), role: "assistant", content: emptyAnswered ? fallbackAnswer(status, value) : (response.answer || fallbackAnswer(status, value)), citations: response.citations, status, kind: response.kind ?? (status === "answered" ? "document" : "error") }]);
    } catch (caught) {
      if (!(caught instanceof DOMException && caught.name === "AbortError")) {
        setError(caught instanceof Error ? caught.message : "Une erreur réseau est survenue.");
      }
    } finally {
      setLoading(false);
      abortRef.current = null;
    }
  }, [loading, sessionId]);

  const newConversation = useCallback(async () => {
    abortRef.current?.abort();
    if (sessionId) {
      try { await deleteSession(sessionId); } catch { /* local reset remains safe */ }
    }
    setMessages([WELCOME_MESSAGE]); setSessionId(null); setError(null); setLoading(false);
  }, [sessionId]);

  return { messages, sessionId, loading, error, serviceStatus, send, newConversation };
}
