export const SPEECH_LANGUAGE_OPTIONS = [
  { value: "fr-FR", label: "FR" },
  { value: "ar-MA", label: "AR" },
  { value: "en-US", label: "EN" },
  { value: "es-ES", label: "ES" },
] as const;

const RECOGNITION_LOCALES: Record<string, string> = {
  fr: "fr-FR",
  "fr-fr": "fr-FR",
  ar: "ar",
  "ar-ma": "ar-MA",
  en: "en-US",
  "en-us": "en-US",
  es: "es-ES",
  "es-es": "es-ES",
};

export const DEFAULT_SPEECH_LOCALE = "fr-FR";
export const SPEECH_LOCALE_STORAGE_KEY = "ghaitta-speech-locale";

export function getRecognitionLocale(locale: string): string | undefined {
  const normalized = locale.toLowerCase();
  return RECOGNITION_LOCALES[normalized] ?? RECOGNITION_LOCALES[normalized.split("-")[0]];
}

export function getInitialSpeechLocale(interfaceLocale: string): string {
  const preferred = { fr: "fr-FR", ar: "ar-MA", en: "en-US", es: "es-ES" }[interfaceLocale.toLowerCase().split("-")[0]];
  return preferred ?? DEFAULT_SPEECH_LOCALE;
}

export function detectSpeechSynthesisLocale(text: string): string | undefined {
  if (/[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]/u.test(text)) return "ar-MA";
  if (/[\u2d30-\u2d7f]/u.test(text)) return undefined;
  if (/[\u00bf\u00a1]|\b(qu[eé]|c[oó]mo|cu[aá]l|cu[aá]les|gracias|hola|proyecto|resoluci[oó]n|acompa[nñ]amiento|maneras|puede|ayudarle|siguientes|empresa|conflictos)\b/i.test(text)) return "es-ES";
  if (/[éèêëàâùûüîïçœ]|\b(bonjour|merci|projet|comment|quelle|quelles)\b/i.test(text)) return "fr-FR";
  return "en-US";
}
