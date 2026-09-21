import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import * as api from "./api/chatApi";

vi.mock("./api/chatApi", () => ({
  checkHealth: vi.fn(() => Promise.resolve({ status: "ok" })),
  checkReady: vi.fn(() => Promise.resolve({ status: "ready" })),
  sendMessage: vi.fn(),
  deleteSession: vi.fn(() => Promise.resolve({ status: "deleted", session_id: "s1" })),
}));

const openWidget = () => fireEvent.click(screen.getByRole("button", { name: /Ouvrir GH-AI-TTA/i }));
const startWidget = () => fireEvent.click(screen.getByRole("button", { name: "Démarrer la discussion" }));

describe("CRI chat UI", () => {
  beforeEach(() => { sessionStorage.clear(); vi.clearAllMocks(); });

  it("renders an empty chat and sends/stores a session", async () => {
    vi.mocked(api.sendMessage).mockResolvedValue({ session_id: "s1", status: "answered", answer: "379", citations: [{ document_id: "d", filename: "source.pdf", page: 2 }] });
    render(<App />);
    openWidget();
    startWidget();
    await waitFor(
      () => expect(screen.getByText(/Comment puis-je vous accompagner/)).toBeInTheDocument(),
      { timeout: 5000 },
    );
    fireEvent.change(screen.getByLabelText("Votre question"), { target: { value: "Combien de projets ?" } });
    fireEvent.click(screen.getByRole("button", { name: "Envoyer" }));
    await waitFor(() => expect(screen.getByText("379")).toBeInTheDocument());
    expect(api.sendMessage).toHaveBeenCalledWith({ message: "Combien de projets ?" }, expect.any(AbortSignal));
    expect(sessionStorage.getItem("cri-assistant-session-id")).toBeNull();
    expect(screen.queryByText(/source\.pdf/)).not.toBeInTheDocument();
  });

  it("reuses the session and clears it with a new conversation", async () => {
    vi.mocked(api.sendMessage)
      .mockResolvedValueOnce({ session_id: "s1", status: "answered", answer: "one", citations: [] })
      .mockResolvedValueOnce({ session_id: "s1", status: "answered", answer: "two", citations: [] });
    render(<App />);
    openWidget();
    startWidget();
    const input = screen.getByLabelText("Votre question");
    fireEvent.change(input, { target: { value: "one" } }); fireEvent.submit(input.closest("form")!);
    await waitFor(() => expect(screen.getByText("one")).toBeInTheDocument());
    fireEvent.change(input, { target: { value: "two" } }); fireEvent.submit(input.closest("form")!);
    await waitFor(() => expect(screen.getByText("two")).toBeInTheDocument());
    expect(api.sendMessage).toHaveBeenLastCalledWith({ message: "two", session_id: "s1" }, expect.any(AbortSignal));
    fireEvent.click(screen.getByRole("button", { name: "Lancer une nouvelle conversation" }));
    await waitFor(() => expect(api.deleteSession).toHaveBeenCalledWith("s1"));
    expect(screen.queryByText("one")).not.toBeInTheDocument();
    expect(sessionStorage.getItem("cri-assistant-session-id")).toBeNull();
  });

  it("shows refusal and Arabic messages in RTL without diagnostics", async () => {
    vi.mocked(api.sendMessage).mockResolvedValue({ session_id: "s2", status: "insufficient_evidence", answer: "Cette information n’est pas disponible.", citations: [] });
    render(<App />);
    openWidget();
    startWidget();
    const input = screen.getByLabelText("Votre question");
    fireEvent.change(input, { target: { value: "سؤال" } }); fireEvent.submit(input.closest("form")!);
    await waitFor(() => expect(screen.getByText("Cette information n’est pas disponible.")).toBeInTheDocument());
    expect(screen.queryByText(/top1_score|Qdrant|retrieval_score/i)).not.toBeInTheDocument();
    expect(screen.getByText("سؤال").closest(".message-bubble")).toHaveAttribute("dir", "rtl");
  });
});
