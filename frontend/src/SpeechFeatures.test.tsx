import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ChatInput } from "./components/ChatInput";
import { ChatMessage } from "./components/ChatMessage";

class MockRecognition {
  static instance: MockRecognition;
  continuous = false;
  interimResults = false;
  lang = "";
  onend: (() => void) | null = null;
  onerror: ((event: Event) => void) | null = null;
  onresult: ((event: Event) => void) | null = null;
  start = vi.fn();
  stop = vi.fn(() => this.onend?.());
  abort = vi.fn();

  constructor() { MockRecognition.instance = this; }
}

class MockUtterance {
  lang = "";
  onend: (() => void) | null = null;
  onerror: (() => void) | null = null;
  constructor(public text: string) {}
}

describe("voice features", () => {
  const synthesis = { speak: vi.fn(), cancel: vi.fn(), getVoices: vi.fn<() => SpeechSynthesisVoice[]>(() => []), addEventListener: vi.fn(), removeEventListener: vi.fn() };

  beforeEach(() => {
    sessionStorage.clear();
    window.SpeechRecognition = MockRecognition as never;
    Object.defineProperty(window, "speechSynthesis", { configurable: true, value: synthesis });
    Object.defineProperty(window, "SpeechSynthesisUtterance", { configurable: true, value: MockUtterance });
  });

  afterEach(() => {
    vi.clearAllMocks();
    delete window.SpeechRecognition;
    delete window.webkitSpeechRecognition;
    Object.defineProperty(window, "speechSynthesis", { configurable: true, value: undefined });
    Object.defineProperty(window, "SpeechSynthesisUtterance", { configurable: true, value: undefined });
  });

  it("inserts editable recognition text without submitting", async () => {
    const onSend = vi.fn();
    render(<ChatInput loading={false} onSend={onSend} locale="fr" />);
    const textarea = screen.getByLabelText("Votre question");
    fireEvent.change(textarea, { target: { value: "Bonjour" } });
    fireEvent.click(screen.getByRole("button", { name: "Démarrer la dictée vocale" }));
    expect(MockRecognition.instance.lang).toBe("fr-FR");
    MockRecognition.instance.onresult?.({ resultIndex: 0, results: { length: 1, 0: { isFinal: true, 0: { transcript: "combien de projets" } } } } as never);
    await waitFor(() => expect(textarea).toHaveValue("Bonjour combien de projets"));
    expect(onSend).not.toHaveBeenCalled();
    fireEvent.submit(textarea.closest("form")!);
    expect(onSend).toHaveBeenCalledWith("Bonjour combien de projets");
  });

  it.each([
    ["fr-FR", "fr-FR"],
    ["ar-MA", "ar-MA"],
    ["en-US", "en-US"],
    ["es-ES", "es-ES"],
  ])("sets recognition language to %s before starting", (selected, expected) => {
    render(<ChatInput loading={false} onSend={vi.fn()} locale="fr" />);
    fireEvent.change(screen.getByRole("combobox", { name: "Langue de dictée" }), { target: { value: selected } });
    fireEvent.click(screen.getByRole("button", { name: "Démarrer la dictée vocale" }));
    expect(MockRecognition.instance.lang).toBe(expected);
    expect(sessionStorage.getItem("ghaitta-speech-locale")).toBe(selected);
  });

  it("shows a speaker only for assistant messages and can stop playback", () => {
    render(<><ChatMessage message={{ id: "assistant", role: "assistant", content: "Bonjour", status: "answered" }} /><ChatMessage message={{ id: "user", role: "user", content: "Question" }} /></>);
    const speaker = screen.getByRole("button", { name: "Lire la réponse" });
    expect(screen.queryByRole("button", { name: "Lire la question" })).not.toBeInTheDocument();
    fireEvent.click(speaker);
    expect(synthesis.speak).toHaveBeenCalledOnce();
    expect(synthesis.speak.mock.calls[0][0]).toMatchObject({ text: "Bonjour", lang: "fr-FR" });
    fireEvent.click(screen.getByRole("button", { name: "Arrêter la lecture" }));
    expect(synthesis.cancel).toHaveBeenCalledOnce();
  });

  it("chooses an Arabic voice instead of a French voice", () => {
    synthesis.getVoices.mockReturnValue([
      { lang: "fr-FR", name: "French", voiceURI: "fr", localService: true, default: true } as SpeechSynthesisVoice,
      { lang: "ar-SA", name: "Arabic", voiceURI: "ar", localService: true, default: false } as SpeechSynthesisVoice,
    ]);
    render(<ChatMessage message={{ id: "ar", role: "assistant", content: "وافقت اللجنة الجهوية", status: "answered" }} />);
    fireEvent.click(screen.getByRole("button", { name: "Lire la réponse" }));
    expect(synthesis.speak.mock.calls[0][0]).toMatchObject({ lang: "ar-SA", voice: { lang: "ar-SA" } });
  });

  it("chooses a Spanish voice and strips Markdown before speaking", () => {
    synthesis.getVoices.mockReturnValue([
      { lang: "en-US", name: "English", voiceURI: "en", localService: true, default: true } as SpeechSynthesisVoice,
      { lang: "es-ES", name: "Spanish", voiceURI: "es", localService: true, default: false } as SpeechSynthesisVoice,
    ]);
    render(<ChatMessage message={{ id: "es", role: "assistant", content: "**Resolución de conflictos**", status: "answered" }} />);
    expect(screen.getByText("Resolución de conflictos").tagName).toBe("STRONG");
    fireEvent.click(screen.getByRole("button", { name: "Lire la réponse" }));
    expect(synthesis.speak.mock.calls[0][0]).toMatchObject({ text: "Resolución de conflictos", lang: "es-ES", voice: { lang: "es-ES" } });
  });
});
