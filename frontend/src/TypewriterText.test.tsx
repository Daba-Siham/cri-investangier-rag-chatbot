import { act, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ChatMessage } from "./components/ChatMessage";
import { TypewriterText, TYPEWRITER_DELAY_MS } from "./components/TypewriterText";

describe("GH-AI-TTA progressive answers", () => {
  afterEach(() => vi.useRealTimers());

  it("reveals complete words and eventually preserves the exact answer", () => {
    vi.useFakeTimers();
    const answer = "709 projets approuvés.";
    render(<p><TypewriterText text={answer} animate /></p>);
    expect(screen.getByText("", { selector: "p" })).toBeInTheDocument();
    act(() => { vi.advanceTimersByTime(TYPEWRITER_DELAY_MS * 3); });
    expect(screen.getByText(answer, { selector: "p" })).toBeInTheDocument();
  });

  it("keeps Arabic content RTL without rendering sources", () => {
    vi.useFakeTimers();
    render(<ChatMessage message={{ id: "ar-new", role: "assistant", content: "وافقت اللجنة الجهوية", status: "answered", citations: [{ document_id: "d", filename: "source.pdf", page: 7 }] }} animate />);
    expect(screen.getByText("", { selector: ".ghaitta-message p" }).closest(".ghaitta-message")).toHaveAttribute("dir", "rtl");
    expect(screen.queryByText("source.pdf")).not.toBeInTheDocument();
    act(() => { vi.advanceTimersByTime(TYPEWRITER_DELAY_MS * 3); });
  });
});
