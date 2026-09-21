import { useState } from "react";
import { branding, type SupportedLocale } from "../config/branding";

export function WelcomeScreen({ onStart, onClose, locale = "fr" }: { onStart: () => void; onClose: () => void; locale?: SupportedLocale }) {
  const [logoFailed, setLogoFailed] = useState(false);
  const [characterFailed, setCharacterFailed] = useState(false);
  return <section className="ghaitta-welcome" aria-label="Bienvenue">
    <button className="ghaitta-welcome-close" type="button" aria-label="Fermer GH-AI-TTA" onClick={onClose}>×</button>
    <div className="ghaitta-welcome__logo">{logoFailed ? <span className="ghaitta-logo-fallback">INVESTANGIER</span> : <img src="/assets/chat/investangier-logo.png" alt="Investangier" onError={() => setLogoFailed(true)} />}</div>
    <div className="ghaitta-welcome__main">
      <div className="ghaitta-welcome__copy">
        <h1 className="ghaitta-welcome__title">{branding.welcomeTitle}</h1>
        <p className="ghaitta-welcome__subtitle">Chatbot</p>
        <button className="ghaitta-start-button ghaitta-welcome__cta" type="button" onClick={onStart}>{branding.startButtonLabel}</button>
      </div>
    </div>
    <div className="ghaitta-welcome__character">{characterFailed ? <span className="ghaitta-logo-fallback">GH</span> : <img src="/assets/chat/CHAITTA.png" alt="GH-AI-TTA" onError={() => setCharacterFailed(true)} />}</div>
    <p className="ghaitta-terms ghaitta-welcome__legal"><span className="ghaitta-terms__icon" aria-hidden="true">i</span><span>L’utilisation du GH-AI-TTA Bot implique l’acceptation pleine et entière des conditions générales d’utilisation décrites ci-dessous : <a href="https://critta3.dev.dialtechnologies.net/mentions-legales-et-conditions-dutilisation/" target="_blank" rel="noreferrer">CGU</a></span></p>
  </section>;
}
