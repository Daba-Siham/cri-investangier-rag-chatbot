import { useState } from "react";

export function ChatLauncher({ onOpen }: { onOpen: () => void }) {
  const [failed, setFailed] = useState(false);
  return <button className="ghaitta-launcher" type="button" aria-label="Ouvrir GH-AI-TTA" onClick={onOpen}>
    <span className="ghaitta-launcher__greeting"><span>Bonjour,</span><strong>GH-AI-TTA à votre service</strong></span>
    <span className="ghaitta-launcher__character">{failed ? <span className="ghaitta-launcher__fallback">GH</span> : <img src="/assets/chat/CHAITTA.png" alt="" onError={() => setFailed(true)} />}</span>
  </button>;
}
