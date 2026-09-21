import { SPEECH_LANGUAGE_OPTIONS } from "../config/speech";

export function SpeechLanguageSelect({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return <label className="ghaitta-speech-language"><span className="ghaitta-sr-only">Langue de dictée</span><select aria-label="Langue de dictée" value={value} onChange={(event) => onChange(event.target.value)}>{SPEECH_LANGUAGE_OPTIONS.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>;
}
