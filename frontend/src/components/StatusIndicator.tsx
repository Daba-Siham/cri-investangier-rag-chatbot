import type { ServiceStatus } from "../types/chat";
export function StatusIndicator({ status }: { status: ServiceStatus }) {
  const connected = status.status === "ready" || status.status === "ok";
  return <span className={`ghaitta-status ${connected ? "ghaitta-status--connected" : ""}`}><i aria-hidden="true" />{connected ? "Connecté" : status.status === "checking" ? "Connexion…" : "Indisponible"}</span>;
}
