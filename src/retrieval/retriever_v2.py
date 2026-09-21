"""Independent Phase 4C retriever for the dense E5 v2 collection."""
from __future__ import annotations

import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
COLLECTION = "cri_chunks_multilingual_e5_v2"
MODEL_NAME = "intfloat/multilingual-e5-base"


def _model_source() -> str:
    configured = os.getenv("E5_MODEL_PATH")
    if configured and Path(configured).exists():
        return configured
    cache = Path.home() / ".cache" / "huggingface" / "hub" / "models--intfloat--multilingual-e5-base" / "snapshots"
    snapshots = sorted((path for path in cache.glob("*") if path.is_dir()), key=lambda path: path.stat().st_mtime, reverse=True)
    return str(snapshots[0]) if snapshots else MODEL_NAME


def _payload(point: Any) -> dict[str, Any]:
    return getattr(point, "payload", None) or (point.get("payload", {}) if isinstance(point, dict) else {})


def _score(point: Any) -> float:
    value = getattr(point, "score", None)
    if value is None and isinstance(point, dict):
        value = point.get("score", 0.0)
    return float(value or 0.0)


def _detect_language(query: str) -> str | None:
    arabic_letters = len(re.findall(r"[\u0621-\u064a\u0671-\u06d3]", query))
    latin_letters = len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]", query))
    if arabic_letters >= 3 and arabic_letters >= max(1, latin_letters):
        return "ar"
    lowered = query.casefold()
    if any(token in lowered for token in ("qué", "cuáles", "para los", "ofrece", "inversores", "inversión", "servicios", "condiciones", "financiación")):
        return "es"
    if any(token in lowered for token in ("quels", "quelles", "pour les", "branchement", "entreprises", "investissement")):
        return "fr"
    if any(token in lowered for token in ("what", "which", "requirements", "investment", "services", "investors")):
        return "en"
    return None


def _obsolete_query_concepts(query: str) -> set[str]:
    lowered = query.casefold()
    mapping = {
        "eligibility_conditions": ("condition", "conditions", "eligibility", "éligib", "شروط", "condiciones"),
        "cost_information": ("coût", "cout", "cost", "tarif", "prix", "رسوم", "costes"),
        "procedure": ("démarche", "demarche", "étapes", "steps", "procedure", "procédure", "إجراءات", "trámites"),
        "investment_opportunity": ("opportunit", "opportunidad", "فرص الاستثمار", "project", "projet"),
        "business_support": ("support", "accompagnement", "services", "خدمات", "apoyo"),
        "financial_product": ("financement", "financing", "financement", "تمويل", "financiación", "programme"),
        "automotive": ("automotive", "automobile", "automoción", "سيارات"),
        "tourism": ("tourism", "tourisme", "turismo", "السياحة"),
        "crui_activity": ("crui", "approved", "approuv", "projets", "المشاريع"),
        "electricity_connection": ("électricité", "electricity", "electricidad", "الكهرباء"),
    }
    return {tag for tag, terms in mapping.items() if any(term in lowered for term in terms)}


def _query_concepts(query: str) -> set[str]:
    """Normalize multilingual concept cues, including Spanish variants."""
    lowered = query.casefold()
    mapping = {
        "eligibility_conditions": ("condition", "conditions", "eligibility", "\u00e9ligib", "requisito", "requisitos", "elegibilidad", "beneficiarse", "\u0634\u0631\u0648\u0637"),
        "cost_information": ("co\u00fbt", "cout", "cost", "tarif", "prix", "\u0631\u0633\u0648\u0645", "costes"),
        "procedure": ("d\u00e9marche", "demarche", "\u00e9tapes", "steps", "procedure", "proc\u00e9dure", "\u0625\u062c\u0631\u0627\u0621\u0627\u062a", "tr\u00e1mites"),
        "investment_opportunity": ("opportunit", "oportunidad", "oportunidades", "\u0641\u0631\u0635 \u0627\u0644\u0627\u0633\u062a\u062b\u0645\u0627\u0631", "project", "projet"),
        "business_support": ("support", "accompagnement", "service", "services", "asesoramiento", "apoyo", "acompa\u00f1amiento", "inversor", "inversores", "\u062e\u062f\u0645\u0627\u062a"),
        "financial_product": ("financement", "financing", "\u062a\u0645\u0648\u064a\u0644", "financiaci\u00f3n", "financiamiento", "programme", "programas"),
        "automotive": ("automotive", "automobile", "automoci\u00f3n", "\u0633\u064a\u0627\u0631\u0627\u062a"),
        "tourism": ("tourism", "tourisme", "turismo", "tur\u00edst", "\u0627\u0644\u0633\u064a\u0627\u062d\u0629"),
        "crui_activity": ("crui", "approved", "approuv", "projets", "\u0627\u0644\u0645\u0634\u0627\u0631\u064a\u0639"),
        "electricity_connection": ("\u00e9lectricit\u00e9", "electricity", "electricidad", "\u0627\u0644\u0643\u0647\u0631\u0628\u0627\u0621"),
    }
    return {tag for tag, terms in mapping.items() if any(term in lowered for term in terms)}


class V2Retriever:
    """Dense-only v2 retriever with auditable, deliberately small adjustments."""

    def __init__(self, url: str | None = None, api_key: str | None = None, collection: str = COLLECTION,
                 candidate_k: int = 30, final_k: int = 5, max_per_parent: int = 1,
                 max_per_family: int | None = None, family_repeat_penalty: float = 0.002,
                 language_bonus: float = 0.005, semantic_bonus: float = 0.004, temporal_bonus: float = 0.012,
                 device: str | None = None, model: Any | None = None, client: Any | None = None):
        load_dotenv(ROOT / ".env", override=False)
        self.url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.api_key = api_key if api_key is not None else (os.getenv("QDRANT_API_KEY") or None)
        self.collection = collection
        self.candidate_k = candidate_k
        self.final_k = final_k
        self.max_per_parent = max_per_parent
        self.max_per_family = max_per_family
        self.family_repeat_penalty = family_repeat_penalty
        self.language_bonus_value = language_bonus
        self.semantic_bonus_value = semantic_bonus
        self.temporal_bonus_value = temporal_bonus
        self.client = client or QdrantClient(url=self.url, api_key=self.api_key)
        self._model = model
        self.device = device

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(_model_source(), device=self.device) if self.device else SentenceTransformer(_model_source())
        return self._model

    def collection_exists(self) -> bool:
        return bool(self.client.collection_exists(self.collection))

    def _query_vector(self, query: str):
        return self.model.encode([f"query: {query}"], normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)[0].tolist()

    def _normalize(self, point: Any) -> dict[str, Any]:
        payload = _payload(point)
        return {
            "dense_score": _score(point),
            "ranking_score": _score(point),
            "retrieval_chunk_id": payload.get("retrieval_chunk_id"),
            "parent_semantic_chunk_id": payload.get("parent_semantic_chunk_id"),
            "document_id": payload.get("document_id"),
            "document_family_id": payload.get("document_family_id"),
            "filename": payload.get("filename"),
            "language": payload.get("language"),
            "topic_id": payload.get("topic_id"),
            "content_type": payload.get("content_type"),
            "semantic_tags": payload.get("semantic_tags", []),
            "heading_path": payload.get("heading_path", []),
            "page_start": payload.get("page_start"),
            "page_end": payload.get("page_end"),
            "source_pages": payload.get("source_pages", []),
            "primary_year": payload.get("primary_year"),
            "years_mentioned": payload.get("years_mentioned", []),
            "reference_period_type": payload.get("reference_period_type"),
            "reference_period_year": payload.get("reference_period_year"),
            "reference_period_end_date": payload.get("reference_period_end_date"),
            "retrieval_chunk_index": payload.get("retrieval_chunk_index"),
            "retrieval_chunk_count": payload.get("retrieval_chunk_count"),
            "text": payload.get("text", ""),
        }

    def _adjust(self, result: dict[str, Any], query: str, query_language: str | None, concepts: set[str], query_year: int | None):
        same_language = bool(query_language and result.get("language") == query_language)
        # This is intentionally a tie-breaker only; no language is filtered.
        language_bonus = self.language_bonus_value if same_language else 0.0
        matching_tags = sorted(concepts.intersection(set(result.get("semantic_tags") or [])))
        semantic_bonus = min(self.semantic_bonus_value * len(matching_tags), 0.012)
        if result.get("topic_id") in concepts:
            semantic_bonus = min(semantic_bonus + self.semantic_bonus_value, 0.012)
        content_type = result.get("content_type")
        content_type_match = content_type in concepts or (content_type == "service" and "business_support" in concepts)
        if content_type_match:
            semantic_bonus = min(semantic_bonus + self.semantic_bonus_value, 0.012)
        supports_year = query_year is not None and (query_year == result.get("primary_year") or query_year == result.get("reference_period_year") or query_year in (result.get("years_mentioned") or []))
        primary_or_reference_years = {year for year in (result.get("primary_year"), result.get("reference_period_year")) if isinstance(year, int)}
        strong_temporal_conflict = bool(query_year is not None and primary_or_reference_years and query_year not in primary_or_reference_years)
        weak_temporal_conflict = bool(query_year is not None and not primary_or_reference_years and result.get("years_mentioned") and query_year not in result.get("years_mentioned", []))
        temporal_conflict_type = "strong" if strong_temporal_conflict else ("weak" if weak_temporal_conflict else "none")
        temporal_bonus = self.temporal_bonus_value if supports_year else 0.0
        temporal_penalty = 0.010 if strong_temporal_conflict and not supports_year else (0.008 if weak_temporal_conflict and not supports_year else 0.0)
        base_score = result["dense_score"] + language_bonus + semantic_bonus + temporal_bonus - temporal_penalty
        result.update({"language_bonus": language_bonus, "semantic_bonus": semantic_bonus, "temporal_bonus": temporal_bonus, "temporal_penalty": temporal_penalty, "family_penalty": 0.0, "ranking_score": base_score, "base_ranking_score": base_score, "matched_semantic_tags": matching_tags, "content_type_match": content_type_match, "temporal_conflict_type": temporal_conflict_type, "temporal_evidence": {"query_year": query_year, "primary_year": result.get("primary_year"), "reference_period_year": result.get("reference_period_year"), "years_mentioned": result.get("years_mentioned", []), "supports_year": supports_year, "conflict_type": temporal_conflict_type}})

    def retrieve(self, query: str, candidate_k: int | None = None, final_k: int | None = None, debug: bool = False):
        candidate_k = candidate_k or self.candidate_k
        final_k = final_k or self.final_k
        if candidate_k <= 0 or final_k <= 0:
            return {"query": query, "raw_dense_top10": [], "results": [], "debug": {}}
        vector = self._query_vector(query)
        if hasattr(self.client, "query_points"):
            response = self.client.query_points(collection_name=self.collection, query=vector, limit=candidate_k, with_payload=True)
            points = list(response.points)
        else:
            points = list(self.client.search(collection_name=self.collection, query_vector=vector, limit=candidate_k, with_payload=True))
        candidates = [self._normalize(point) for point in points]
        query_language = _detect_language(query)
        concepts = _query_concepts(query)
        years = [int(year) for year in re.findall(r"\b(20\d{2})\b", query)]
        query_year = years[0] if years else None
        for candidate in candidates:
            self._adjust(candidate, query, query_language, concepts, query_year)
            candidate["decision"] = "candidate"
            candidate["parent_decision"] = "candidate"
            candidate["family_decision"] = "candidate"
        ranked = sorted(candidates, key=lambda item: (-item["ranking_score"], -item["dense_score"], item["retrieval_chunk_id"] or ""))
        raw_top10 = sorted(candidates, key=lambda item: (-item["dense_score"], item["retrieval_chunk_id"] or ""))[:10]
        parent_counts = Counter()
        family_counts = Counter()
        selected = []
        remaining = list(ranked)
        while remaining and len(selected) < final_k:
            eligible = []
            for candidate in remaining:
                parent = candidate.get("parent_semantic_chunk_id")
                family = candidate.get("document_family_id")
                if parent_counts[parent] >= self.max_per_parent:
                    candidate["decision"] = "sibling_collapsed"
                    candidate["parent_decision"] = "sibling_collapsed"
                    continue
                if self.max_per_family is not None and family_counts[family] >= self.max_per_family:
                    candidate["decision"] = "family_cap"
                    candidate["family_decision"] = "family_cap"
                    continue
                candidate["family_penalty"] = self.family_repeat_penalty * max(0, family_counts[family] - 1)
                candidate["ranking_score"] = candidate["base_ranking_score"] - candidate["family_penalty"]
                eligible.append(candidate)
            if not eligible:
                break
            chosen = max(eligible, key=lambda item: (item["ranking_score"], item["dense_score"], item["retrieval_chunk_id"] or ""))
            chosen["decision"] = "kept"
            chosen["parent_decision"] = "kept"
            chosen["family_decision"] = "soft_penalty" if chosen["family_penalty"] > 0 else "kept"
            parent_counts[chosen.get("parent_semantic_chunk_id")] += 1
            family_counts[chosen.get("document_family_id")] += 1
            selected.append(chosen)
            remaining.remove(chosen)
        for candidate in remaining:
            if candidate["decision"] == "candidate":
                candidate["decision"] = "final_k_cut"
                candidate["parent_decision"] = "final_k_cut"
                candidate["family_decision"] = "final_k_cut"
        debug_candidates = ranked if debug else [candidate for candidate in ranked if candidate["decision"] == "kept"]
        diagnostics = {
            "query_language": query_language,
            "query_year": query_year,
            "concepts": sorted(concepts),
            "raw_candidate_count": len(candidates),
            "raw_top10_parent_duplicates": len(candidates[:10]) - len({item.get("parent_semantic_chunk_id") for item in candidates[:10]}),
            "raw_top30_parent_duplicates": len(candidates) - len({item.get("parent_semantic_chunk_id") for item in candidates}),
            "raw_top30_family_duplicates": len(candidates) - len({item.get("document_family_id") for item in candidates}),
            "sibling_collapsed": sum(item["decision"] == "sibling_collapsed" for item in candidates),
            "family_cap": sum(item["decision"] == "family_cap" for item in candidates),
            "family_soft_penalties": sum(item.get("family_penalty", 0.0) > 0 for item in candidates),
            "family_penalty_total": sum(item.get("family_penalty", 0.0) for item in candidates),
            "final_k_cut": sum(item["decision"] == "final_k_cut" for item in candidates),
            "final_language_diversity": len({item.get("language") for item in selected}),
            "final_family_diversity": len({item.get("document_family_id") for item in selected}),
            "final_unique_parent_count": len({item.get("parent_semantic_chunk_id") for item in selected}),
            "same_family_results_retained": max(Counter(item.get("document_family_id") for item in selected).values(), default=0),
            "debug_candidates": debug_candidates,
        }
        return {"query": query, "raw_dense_top10": raw_top10, "results": selected, "debug": diagnostics}
