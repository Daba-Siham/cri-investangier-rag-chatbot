import { useEffect, useRef, useState } from "react";
import { getRecognitionLocale } from "../config/speech";

interface RecognitionAlternativeLike { transcript: string; }
interface RecognitionResultLike { isFinal: boolean; 0: RecognitionAlternativeLike; }
interface RecognitionEventLike extends Event { resultIndex: number; results: { length: number; [index: number]: RecognitionResultLike }; }
interface RecognitionErrorEventLike extends Event { error: string; }
interface RecognitionLike {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onend: (() => void) | null;
  onerror: ((event: RecognitionErrorEventLike) => void) | null;
  onresult: ((event: RecognitionEventLike) => void) | null;
  start: () => void;
  stop: () => void;
  abort: () => void;
}
type RecognitionConstructor = new () => RecognitionLike;

declare global {
  interface Window {
    SpeechRecognition?: RecognitionConstructor;
    webkitSpeechRecognition?: RecognitionConstructor;
  }
}

function getRecognitionConstructor(): RecognitionConstructor | undefined {
  if (typeof window === "undefined") return undefined;
  return window.SpeechRecognition ?? window.webkitSpeechRecognition;
}

export function useSpeechRecognition({ speechLocale, onTranscript }: { speechLocale: string; onTranscript: (text: string) => void }) {
  const recognitionRef = useRef<RecognitionLike | null>(null);
  const transcriptRef = useRef(onTranscript);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState(false);
  const supported = Boolean(getRecognitionConstructor() && getRecognitionLocale(speechLocale));
  transcriptRef.current = onTranscript;

  useEffect(() => () => {
    recognitionRef.current?.abort();
    recognitionRef.current = null;
  }, []);

  const stop = () => {
    recognitionRef.current?.stop();
    setListening(false);
  };

  const start = () => {
    const Recognition = getRecognitionConstructor();
    const language = getRecognitionLocale(speechLocale);
    if (!Recognition || !language) { setError(true); return; }
    recognitionRef.current?.abort();
    setError(false);
    setListening(true);
    const begin = (selectedLanguage: string, allowArabicFallback: boolean) => {
      const recognition = new Recognition();
      recognition.lang = selectedLanguage;
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.onresult = (event) => {
        const transcripts: string[] = [];
        for (let index = event.resultIndex; index < event.results.length; index += 1) {
          const result = event.results[index];
          if (result.isFinal && result[0]?.transcript.trim()) transcripts.push(result[0].transcript.trim());
        }
        if (transcripts.length) transcriptRef.current(transcripts.join(" "));
      };
      recognition.onerror = (event) => {
        if (allowArabicFallback && selectedLanguage === "ar-MA" && event.error === "language-not-supported") {
          recognition.abort();
          begin("ar", false);
          return;
        }
        setError(true);
        setListening(false);
      };
      recognition.onend = () => setListening(false);
      recognitionRef.current = recognition;
      try { recognition.start(); } catch { setError(true); setListening(false); }
    };
    begin(language, language === "ar-MA");
  };

  return { supported, listening, error, start, stop, toggle: listening ? stop : start };
}
