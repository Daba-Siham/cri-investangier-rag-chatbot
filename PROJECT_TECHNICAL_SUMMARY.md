# Project Technical Summary — CRI / Investangier Multilingual RAG

## Purpose and scope

This project is a multilingual CRI documentary assistant for French, Arabic, English, and Spanish. Amazigh/Tamazight retrieval is experimental. Answers are intended to be grounded in retrieved CRI evidence with source/page provenance.

The repository contains a functional V1 baseline and a separately evaluated V2 semantic retrieval path. V2 is the recommended architecture for future extension; V1 is retained for historical comparison. The final generated-answer comparison was incomplete because of provider quotas, so production V2 cutover was not performed.

## Evolution timeline

### V1 functional baseline

- Page-level raw JSON extracted from PDFs.
- Character-based, page-preserving chunks of about 2,800 characters with 400-character overlap.
- `intfloat/multilingual-e5-base` and collection `cri_chunks_multilingual_e5_base`.
- Candidate K≈10, final K=5, historical threshold `0.823114`.
- FastAPI, React, structured generation, source-ID validation, temporary conversation memory, and multilingual UI.

### Semantic JSON 2.2

- 33 semantic documents under `data/semantic_json`.
- Sections, subsections, semantic parents, content types, canonical tags, document families, temporal scope, and exact source spans.
- Raw JSON remains the immutable extraction layer; semantic JSON is the V2 knowledge layer.

### Retrieval chunks V2

- `data/retrieval_v2/retrieval_chunks.jsonl` generated from semantic parents.
- 1,901 retrieval records, 913 semantic parents, 1,894 indexable points.
- Semantic-aware splitting and exact page mapping.
- Final E5 embedding inputs validated below the 512-token model limit; maximum 499 tokens.

### Qdrant V2

- Separate collection: `cri_chunks_multilingual_e5_v2`.
- Dense multilingual E5 vectors, dimension 768, cosine distance.
- V1 collection remains untouched.

### Retriever V2

- Candidate K=30, final K=5.
- Semantic-parent grouping limits sibling domination.
- Document-family diversity is soft, not a hard two-document cap.
- Same-language preference is small and cross-language retrieval remains enabled.
- Semantic and temporal metadata provide transparent weak ranking signals.
- No V1 threshold is reused.

### Context Builder V2

- `src/retrieval/context_builder_v2.py` is separate from ranking.
- Provenance is resolved from retrieval JSONL rather than reconstructed from Qdrant text.
- Exact source spans are clipped to the selected retrieval ranges.
- Sibling expansion is conservative and cannot displace selected primary evidence.
- Citation objects and page labels are deterministic.

### Comparative evaluation

V2 retrieval results improved over V1:

| Metric | V1 | V2 |
|---|---:|---:|
| Family Recall@1 | 0.36 | 0.60 |
| Family Recall@3 | 0.56 | 0.76 |
| Family Recall@5 | 0.64 | 0.86 |
| Family MRR | 0.469 | 0.693 |
| Cross-language success | 0.22 | 0.38 |

V2 Recall@5 by language is FR `1.00`, EN `0.8667`, AR `0.60`, ES `0.90`. Arabic is the weakest measured group.

### Abstention and temporal experiments

- Corrected evaluation composition: 50 answerable and 20 no-answer queries.
- `top1_dense >= 0.825` was a conservative evaluation-only proposal, not production configuration.
- Strict-year context selection preserved requested-year evidence and reduced conflicting-year evidence in the experiment.

### Final generation benchmark

The V1/V2 generated-answer comparison did not complete because Groq token quotas interrupted the benchmark. The final gate remained `V2_NOT_READY`. This does not invalidate the V2 retrieval result. A company-controlled provider/quota is required before generation superiority can be assessed.

## Architecture diagram

```text
PDF / CRI sources
  → raw JSON V1
  → semantic JSON 2.2
  → retrieval chunks V2
  → multilingual-E5-base
  → cri_chunks_multilingual_e5_v2
  → Retriever V2
  → Context Builder / exact provenance
  → generic OpenAI-compatible LLM client
  → FastAPI
  → React / TypeScript frontend
```

## Major V2 files

```text
src/retrieval/retriever_v2.py
src/retrieval/context_builder_v2.py
src/retrieval/evaluation_v2.py
src/retrieval/evaluation_4e1.py
src/retrieval/evaluation_4e2.py
scripts/build_retrieval_chunks_v2.py
scripts/ingest_qdrant_v2.py
scripts/evaluate_retriever_v2.py
scripts/evaluate_context_v2.py
scripts/evaluate_rag_v1_vs_v2.py
scripts/evaluate_rag_4e1.py
scripts/evaluate_rag_4e2.py
scripts/evaluate_rag_4e3.py
scripts/test_llm_preflight.py
```

V1/application modules remain under `src/ingestion`, `src/chunking`, `src/embeddings`, `src/vectorstore`, `src/retrieval`, `src/generation`, `src/rag`, `src/conversation`, `src/api`, and `frontend`.

## Data model handoff

V1 raw JSON is page-level:

```json
{"document_id":"...","filename":"...","language":"fr","pages":[{"page":1,"text":"..."}]}
```

V2 semantic JSON 2.2 adds `document_family_id`, metadata, sections, subsections, `topic_id`, `content_type`, `semantic_tags`, `temporal_scope`, `source_spans`, and page bounds. Retrieval subchunks inherit `parent_semantic_chunk_id`; they do not replace the semantic parent.

## Adding documents

```text
PDF → extraction/raw JSON → validated semantic JSON 2.2
    → retrieval_chunks.jsonl → tokenizer/provenance validation
    → V2 embeddings/Qdrant → retrieval/context evaluation
```

Use stable document and family IDs. Do not manually insert vectors or discard source provenance.

## Historical FAQ integration

The company FAQ knowledge base is not in this repository. A future adapter should map FAQ categories to topics, questions to titles/tags, approved answers to original evidence text, languages to metadata, dates to temporal scope, and the original FAQ ID to provenance. FAQ records without PDF pages must not receive fabricated page numbers.

The preferred default is unified FAQ evidence with `content_type: "faq"` in V2. A canonical FAQ-priority layer may be added if approved historical answers must be reproduced exactly; it is not implemented.

## LLM handoff

The current client is generic and OpenAI-compatible: `src/generation/llm_client.py`. Groq and `qwen/qwen3.8-27b` were development choices. OpenAI configuration is a handoff task:

```env
LLM_API_KEY=<company key>
LLM_BASE_URL=<selected compatible endpoint>
LLM_MODEL=<selected OpenAI model>
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=1024
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
```

This should not require rebuilding semantic JSON, E5 vectors, Qdrant, or retrieval. Generation, language, structured-output, citation, and quota tests must be rerun.

## Status

| Component | Status |
|---|---|
| V1 pipeline | Functional historical baseline |
| Semantic JSON 2.2 | Implemented and validated |
| Retrieval chunks V2 | Implemented and validated |
| Qdrant V2 | Ingested separately |
| Retriever V2 | Evaluated |
| Context/provenance V2 | Exact provenance validated |
| FAQ integration | Not implemented |
| OpenAI production configuration | Not configured |
| Final generated-answer benchmark | Incomplete due to provider quota |
| Production V2 cutover | Not performed |

## Execution and tests

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
python scripts/run_api.py
```

```powershell
python -m pytest tests -p no:cacheprovider
cd frontend
npm test
npm run build
```

## Security handoff

Do not commit `.env`, keys, private PDFs, confidential JSON, local Qdrant storage, `.venv`, `node_modules`, or caches. Provide `.env.example`, use company-owned OpenAI credentials, do not transfer personal Groq credentials, verify internal-data Git policy, and inspect Git history for secrets.
