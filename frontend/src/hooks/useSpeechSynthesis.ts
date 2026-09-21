import { useEffect, useState } from "react";
import { detectSpeechSynthesisLocale } from "../config/speech";
import { stripMarkdownForSpeech } from "../utils/tts";

let activeStop: (() => void) | null = null;

export function findCompatibleVoice(voices: SpeechSynthesisVoice[], locale: string): SpeechSynthesisVoice | undefined {
  const target = locale.toLowerCase();
  const language = target.split("-")[0];
  if (language === "ar") {
    return voices.find((voice) => voice.lang.toLowerCase() === "ar-ma")
      ?? voices.find((voice) => voice.lang.toLowerCase().startsWith("ar-ma-"))
      ?? voices.find((voice) => voice.lang.toLowerCase() === "ar-sa")
      ?? voices.find((voice) => voice.lang.toLowerCase() === "ar-eg")
      ?? voices.find((voice) => voice.lang.toLowerCase().startsWith("ar-"))
      ?? voices.find((voice) => voice.lang.toLowerCase() === "ar");
  }
  return voices.find((voice) => voice.lang.toLowerCase() === target)
    ?? voices.find((voice) => voice.lang.toLowerCase().split("-")[0] === language);
}

export function useSpeechSynthesis() {
  const [speaking, setSpeaking] = useState(false);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [voicesLoaded, setVoicesLoaded] = useState(false);
  const supported = typeof window !== "undefined" && "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;

  useEffect(() => {
    if (!supported) return undefined;
    const synthesis = window.speechSynthesis;
    const updateVoices = (fromVoicesChanged = false) => {
      const nextVoices = synthesis.getVoices?.() ?? [];
      setVoices(nextVoices);
      setVoicesLoaded(nextVoices.length > 0 || fromVoicesChanged);
      if (import.meta.env.DEV) console.debug(`Available TTS voices:\n${nextVoices.map((voice) => voice.lang).join("\n")}`);
    };
    updateVoices();
    const onVoicesChanged = () => updateVoices(true);
    synthesis.addEventListener?.("voiceschanged", onVoicesChanged);
    return () => synthesis.removeEventListener?.("voiceschanged", onVoicesChanged);
  }, [supported]);

  const stop = () => {
    const wasActive = Boolean(activeStop);
    if (activeStop) activeStop();
    activeStop = null;
    if (wasActive && typeof window !== "undefined" && window.speechSynthesis) window.speechSynthesis.cancel();
    setSpeaking(false);
  };

  const toggle = (text: string) => {
    if (!supported) return;
    if (speaking) { stop(); return; }
    stop();
    const synthesis = window.speechSynthesis;
    const cleanText = stripMarkdownForSpeech(text);
    const language = detectSpeechSynthesisLocale(cleanText);
    if (!language) return;
    const voice = findCompatibleVoice(voices, language);
    if (voicesLoaded && !voice) return;
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = voice?.lang || (language === "ar-MA" ? "ar" : language);
    if (voice) utterance.voice = voice;
    if (voice && language === "ar-MA" && import.meta.env.DEV) console.debug(`Arabic TTS selected voice=${voice.name} lang=${voice.lang}`);
    const finish = () => {
      setSpeaking(false);
      if (activeStop === finish) activeStop = null;
    };
    utterance.onend = finish;
    utterance.onerror = finish;
    activeStop = () => setSpeaking(false);
    setSpeaking(true);
    synthesis.speak(utterance);
  };

  useEffect(() => () => {
    if (activeStop) activeStop();
    if (typeof window !== "undefined" && window.speechSynthesis) window.speechSynthesis.cancel();
    activeStop = null;
  }, []);

  const canSpeak = (text: string) => {
    const language = detectSpeechSynthesisLocale(stripMarkdownForSpeech(text));
    return supported && Boolean(language) && (!voicesLoaded || Boolean(findCompatibleVoice(voices, language!)));
  };
  const unavailableReason = (text: string) => {
    const language = detectSpeechSynthesisLocale(stripMarkdownForSpeech(text));
    if (!supported) return "Lecture audio non disponible sur ce navigateur.";
    if (!voicesLoaded || !language || findCompatibleVoice(voices, language)) return undefined;
    if (language === "ar-MA") return "Voix arabe non disponible sur cet appareil";
    return "Aucune voix compatible disponible sur cet appareil.";
  };

  return { supported, speaking, voicesLoaded, voicePending: supported && !voicesLoaded, canSpeak, unavailableReason, stop, toggle };
}
