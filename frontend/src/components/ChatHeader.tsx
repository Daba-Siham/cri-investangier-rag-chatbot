import { useState } from "react";
import { branding } from "../config/branding";

export function ChatHeader({ onClose, onNewConversation }: { onClose: () => void; onNewConversation: () => void }) {
  const [logoFailed, setLogoFailed] = useState(false);
  return <header className="ghaitta-header"><div className="ghaitta-header__logo">{logoFailed ? <span className="ghaitta-logo-fallback">INVESTANGIER</span> : <img src="/assets/chat/investangier-logo.png" alt="Investangier" onError={() => setLogoFailed(true)} />}</div><div className="ghaitta-header__actions"><button className="ghaitta-header-button" type="button" onClick={onNewConversation}><span aria-hidden="true">✎</span> Lancer une nouvelle conversation</button><button className="ghaitta-close" type="button" aria-label="Fermer GH-AI-TTA" onClick={onClose}>×</button></div><span className="ghaitta-header__name">{branding.assistantName}</span></header>;
}
