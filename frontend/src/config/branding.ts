export type SupportedLocale = "fr" | "ar" | "en" | "es";

export const branding = {
  assistantName: "GH-AI-TTA",
  assistantSubtitle: "Assistant virtuel",
  subtitle: "Assistant virtuel du CRI Tanger-Tétouan-Al Hoceima",
  organizationName: "CRI Tanger-Tétouan-Al Hoceima",
  welcomeTitle: "Bonjour, GH-AI-TTA à votre service",
  startButtonLabel: "Démarrer la discussion",
  welcome: {
    fr: { title: "Bonjour", message: "Je suis GH-AI-TTA, l’assistant virtuel du CRI. Posez-moi vos questions sur les informations disponibles dans les documents du CRI." },
    ar: { title: "مرحباً", message: "أنا GH-AI-TTA، المساعد الافتراضي للمركز الجهوي للاستثمار. اطرحوا أسئلتكم حول المعلومات المتاحة في وثائق المركز." },
    en: { title: "Hello", message: "I’m GH-AI-TTA, the CRI virtual assistant. Ask me about information available in the CRI documents." },
    es: { title: "Hola", message: "Soy GH-AI-TTA, el asistente virtual del CRI. Pregúntame sobre la información disponible en los documentos del CRI." },
  },
} as const;
