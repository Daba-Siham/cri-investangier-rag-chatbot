import type { ChatRequest, ChatResponse, ServiceStatus } from "../types/chat";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit, signal?: AbortSignal): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { ...init, signal });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") throw error;
    throw new Error("Le backend est indisponible.");
  }
  if (!response.ok) {
    let detail = "Le backend a refusé la requête.";
    try { detail = (await response.json()).detail ?? detail; } catch { /* safe generic error */ }
    throw new Error(detail);
  }
  try { return await response.json() as T; }
  catch { throw new Error("La réponse du backend est invalide."); }
}

export function sendMessage(payload: ChatRequest, signal?: AbortSignal) {
  return request<ChatResponse>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...payload, include_diagnostics: false })
  }, signal);
}

export function deleteSession(sessionId: string) {
  return request<{ status: string; session_id: string }>(`/sessions/${encodeURIComponent(sessionId)}`, { method: "DELETE" });
}

export function checkHealth() { return request<{ status: string }>("/health"); }
export function checkReady() { return request<ServiceStatus>("/ready"); }
