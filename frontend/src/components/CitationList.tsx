import type { Citation } from "../types/chat";
export function CitationList({ citations }: { citations: Citation[] }) {
  const unique = citations.filter((citation, index, all) => all.findIndex((item) => item.document_id === citation.document_id && item.page === citation.page) === index);
  if (!unique.length) return null;
  return <section className="ghaitta-citations" aria-label="Sources"><h3>Sources</h3><ul>{unique.map((citation) => <li key={`${citation.document_id}-${citation.page}`}><span>{citation.filename}</span><span> — Page {citation.page}</span></li>)}</ul></section>;
}
