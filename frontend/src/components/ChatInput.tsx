import { useCallback, useLayoutEffect, useRef, useState } from "react";
import { getInitialSpeechLocale, SPEECH_LOCALE_STORAGE_KEY } from "../config/speech";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { SpeechLanguageSelect } from "./SpeechLanguageSelect";
const MAX = 5000;
const MIN_HEIGHT = 40;
const MAX_HEIGHT = 130;
export function ChatInput({ loading, onSend, placeholder = "Posez votre question…", locale = "fr" }: { loading: boolean; onSend: (message: string) => void; placeholder?: string; locale?: string }) {
  const [value, setValue] = useState("");
  const [speechLocale, setSpeechLocale] = useState(() => {
    try { return sessionStorage.getItem(SPEECH_LOCALE_STORAGE_KEY) ?? getInitialSpeechLocale(locale); } catch { return getInitialSpeechLocale(locale); }
  });
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const appendTranscript = useCallback((transcript: string) => {
    const spoken = transcript.trim();
    if (!spoken) return;
    setValue((current) => current.trim() ? `${current.replace(/\s+$/u, "")} ${spoken}` : spoken);
  }, []);
  const speech = useSpeechRecognition({ speechLocale, onTranscript: appendTranscript });
  const changeSpeechLocale = (nextLocale: string) => {
    setSpeechLocale(nextLocale);
    try { sessionStorage.setItem(SPEECH_LOCALE_STORAGE_KEY, nextLocale); } catch { /* session persistence is optional */ }
  };
  useLayoutEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = "auto";
    const nextHeight = Math.min(Math.max(textarea.scrollHeight, MIN_HEIGHT), MAX_HEIGHT);
    textarea.style.height = `${nextHeight}px`;
    textarea.style.overflowY = textarea.scrollHeight > MAX_HEIGHT ? "auto" : "hidden";
  }, [value]);
  const submit = () => { if (value.trim() && value.length <= MAX && !loading) { onSend(value); setValue(""); } };
  return <form className="ghaitta-composer" onSubmit={(event) => { event.preventDefault(); submit(); }}>
    <label className="ghaitta-sr-only" htmlFor="chat-message">Votre question</label>
    <textarea ref={textareaRef} dir={locale === "ar" ? "rtl" : "ltr"} id="chat-message" value={value} maxLength={MAX} disabled={loading} onChange={(event) => setValue(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); submit(); } }} placeholder={placeholder} rows={1} />
    <div className="ghaitta-composer__footer"><span className={value.length > MAX - 250 ? "ghaitta-near-limit" : ""}>{value.length} / {MAX}</span><SpeechLanguageSelect value={speechLocale} onChange={changeSpeechLocale} /><button className={`ghaitta-composer__mic ${speech.listening ? "ghaitta-composer__mic--listening" : ""}`} type="button" disabled={loading || !speech.supported} aria-label={speech.listening ? "Arrêter la dictée vocale" : speech.supported ? "Démarrer la dictée vocale" : "Dictée vocale non disponible"} title={speech.error || !speech.supported ? "Dictée vocale non disponible sur ce navigateur." : undefined} onClick={speech.toggle}><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="9" y="3" width="6" height="11" rx="3" /><path d="M5 11a7 7 0 0 0 14 0M12 18v3M8 21h8" /></svg></button><button className="ghaitta-composer__send" type="submit" disabled={loading || !value.trim()} aria-label="Envoyer"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 12h14M13 6l6 6-6 6" /></svg></button></div>
  </form>;
}
