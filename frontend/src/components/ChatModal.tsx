import type { ReactNode } from "react";

export function ChatModal({ children, onClose }: { children: ReactNode; onClose: () => void }) {
  return <div className="ghaitta-overlay" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}><section className="ghaitta-modal" role="dialog" aria-modal="true" aria-label="GH-AI-TTA">{children}</section></div>;
}
