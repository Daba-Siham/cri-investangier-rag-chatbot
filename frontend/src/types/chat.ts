export interface Citation {
  source_id?: string;
  document_id: string;
  filename: string;
  page: number;
  url?: string;
  language?: string | null;
  chunk_id?: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  include_diagnostics?: boolean;
}

export interface ChatResponse {
  session_id: string;
  status: "answered" | "insufficient_evidence" | "model_unavailable" | "generation_error" | string;
  answer: string;
  citations: Citation[];
  retrieval?: Record<string, unknown>;
  llm?: Record<string, unknown>;
  kind?: "document" | "social" | "control" | "error";
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  status?: ChatResponse["status"];
  kind?: "document" | "social" | "control" | "error";
}

export interface ServiceStatus {
  status: string;
  qdrant?: boolean;
  collection?: boolean;
  groq_configured?: boolean;
  model?: string;
}
