import type { ChatMessage } from "../types/chat";

export const WELCOME_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content: "Bonjour\nBienvenue sur l'espace d'assistance du CRI Tanger-Tétouan-Al Hoceima.\nComment puis-je vous accompagner ?",
  status: "answered",
  citations: [],
};
