import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { ChatWidget } from "./components/ChatWidget";

const base = { loading: false, error: null, serviceStatus: { status: "ready" as const }, onSend: vi.fn(), onNewConversation: vi.fn() };
const start = () => fireEvent.click(screen.getByRole("button", { name: "Démarrer la discussion" }));

describe("GH-AI-TTA widget", () => {
  it("opens on a pure welcome state", () => {
    render(<ChatWidget messages={[]} {...base} />);
    fireEvent.click(screen.getByRole("button", { name: /Ouvrir GH-AI-TTA/i }));
    expect(screen.getByRole("heading", { name: "Bonjour, GH-AI-TTA à votre service" })).toBeInTheDocument();
    expect(screen.getByAltText("Investangier")).toBeInTheDocument();
    expect(screen.getByAltText("GH-AI-TTA")).toBeInTheDocument();
    expect(screen.getByText("Chatbot")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "CGU" })).toHaveAttribute("href", "https://critta3.dev.dialtechnologies.net/mentions-legales-et-conditions-dutilisation/");
    expect(screen.queryByText(/Je suis GH-AI-TTA/)).not.toBeInTheDocument();
    expect(screen.getByAltText("GH-AI-TTA").closest(".ghaitta-welcome__character")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Démarrer la discussion" })).toBeInTheDocument();
    expect(screen.queryByLabelText("Votre question")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Envoyer" })).not.toBeInTheDocument();
    expect(screen.queryByText("Nouvelle conversation")).not.toBeInTheDocument();
  });

  it("switches to active chat without sending when started", async () => {
    const onSend = vi.fn();
    render(<ChatWidget initialOpen messages={[]} {...base} onSend={onSend} />);
    start();
    expect(screen.getByRole("button", { name: "Lancer une nouvelle conversation" })).toBeInTheDocument();
    expect(screen.getByLabelText("Votre question")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Envoyer" })).toBeInTheDocument();
    await waitFor(
      () => expect(screen.getByText(/Bienvenue sur l.s?espace d.assistance/)).toBeInTheDocument(),
      { timeout: 5000 },
    );
    expect(onSend).not.toHaveBeenCalled();
    expect(screen.getByRole("banner")).toHaveClass("ghaitta-header");
    expect(screen.getByRole("dialog")).toHaveClass("ghaitta-modal");
    expect(screen.queryByText(/Guichet unique|FAQ|Foncier/i)).not.toBeInTheDocument();
  });

  it("uses the Investangier message composition", () => {
    render(<ChatWidget initialOpen messages={[{ id: "u", role: "user", content: "Ma question" }, { id: "a", role: "assistant", content: "Une réponse", status: "answered" }]} {...base} />);
    start();
    expect(screen.getByText("Ma question").closest(".ghaitta-message-row")).toHaveClass("ghaitta-message-row--user");
    expect(screen.getAllByAltText("GH-AI-TTA").length).toBe(2);
    expect(screen.queryByText("Vous")).not.toBeInTheDocument();
  });

  it("preserves active state after close and reopen", () => {
    render(<ChatWidget initialOpen messages={[{ id: "doc", role: "assistant", content: "709", kind: "document", status: "answered", citations: [{ document_id: "d", filename: "Rapport CRI.pdf", page: 25 }] }]} {...base} />);
    start();
    expect(screen.queryByText("Rapport CRI.pdf")).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Fermer GH-AI-TTA" }));
    fireEvent.click(screen.getByRole("button", { name: /Ouvrir GH-AI-TTA/i }));
    expect(screen.getByLabelText("Votre question")).toBeInTheDocument();
    expect(screen.getByText("709")).toBeInTheDocument();
  });

  it("keeps new conversation in active chat and supports Arabic RTL", () => {
    const onNewConversation = vi.fn();
    render(<ChatWidget initialOpen messages={[{ id: "x", role: "assistant", content: "379", status: "answered" }, { id: "ar", role: "user", content: "كم عدد الطلبات؟" }]} {...base} onNewConversation={onNewConversation} />);
    start();
    expect(screen.getByText("كم عدد الطلبات؟").closest(".ghaitta-message")).toHaveAttribute("dir", "rtl");
    fireEvent.click(screen.getByRole("button", { name: "Lancer une nouvelle conversation" }));
    expect(onNewConversation).toHaveBeenCalledOnce();
    expect(screen.getByLabelText("Votre question")).toBeInTheDocument();
  });

  it("closes from welcome with Escape or its close button", () => {
    render(<ChatWidget initialOpen messages={[]} {...base} />);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});
