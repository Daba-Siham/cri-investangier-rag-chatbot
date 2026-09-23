# Multilingual Document RAG Chatbot — CRI / Investangier

## Overview

This repository contains a multilingual Retrieval-Augmented Generation (RAG) chatbot for CRI Tanger-Tétouan-Al Hoceima / Investangier documentary sources.

The main supported languages are French, Arabic, English, and Spanish. Amazigh/Tamazight support is experimental. Documentary answers are grounded in retrieved CRI evidence; the LLM is not intended to provide external web knowledge.

The repository contains two generations of the pipeline:

- **V1** is the functional historical baseline and remains available for comparison.
- **V2** is the semantic retrieval architecture that should be extended by the receiving CRI team.

V2 retrieval has been evaluated successfully. The final V1/V2 generated-answer comparison was not completed because of provider token quotas, and production V2 cutover was not performed during the internship.

## Architecture

```text
PDF / CRI sources
        |
        v
Raw JSON (V1 extraction representation)
        |
        v
Semantic JSON 2.2
        |
        v
Retrieval chunks v2
        |
        v
multilingual-E5-base
        |
        v
Qdrant v2: cri_chunks_multilingual_e5_v2
        |
        v
Retriever V2
        |
        v
Context Builder V2 + exact provenance
        |
        v
Generic OpenAI-compatible LLM client
        |
        v
FastAPI backend
        |
        v
React / TypeScript frontend
```

V1 remains isolated around `cri_chunks_multilingual_e5_base`. V2 was built separately so that retrieval and generation could be compared without silently changing the historical system.

## Document data formats

### V1 — page-level/raw JSON

```json
{
  "document_id": "...",
  "filename": "...",
  "language": "fr",
  "pages": [{"page": 1, "text": "..."}]
}
```

V1 represents one document as extracted PDF pages. This gives direct page provenance and is the source format used by the initial character-based pipeline.

### V2 — semantic JSON 2.2

```json
{
  "schema_version": "2.2",
  "document_id": "...",
  "document_family_id": "...",
  "metadata": {
    "title": "...",
    "filename": "...",
    "language": "fr",
    "document_type": "statistics",
    "publisher": "CRI Tanger-Tétouan-Al Hoceima",
    "region": "Tanger-Tétouan-Al Hoceima",
    "publication_year": 2025,
    "reference_period": {},
    "topics": []
  },
  "sections": [{
    "section_id": "...",
    "title": "...",
    "topic_id": "business_creation",
    "subsections": [{
      "subsection_id": "...",
      "title": "...",
      "chunks": [{
        "chunk_id": "...",
        "content_type": "statistics",
        "semantic_tags": ["business_creation"],
        "heading_path": ["..."],
        "page_start": 1,
        "page_end": 1,
        "source_spans": [{"page": 1, "text": "..."}],
        "text": "...",
        "keywords": [],
        "entities": [],
        "temporal_scope": {}
      }]
    }]
  }]
}
```

V1 is an extraction/layout representation with simple page metadata. V2 adds document families for translations, sections and subsections, canonical topic IDs, semantic content types, semantic tags, temporal scope, exact source spans, and semantic-parent provenance. Raw JSON remains the immutable extraction layer; semantic JSON is the canonical V2 knowledge layer.

## V1 and V2 retrieval

| Aspect | V1 baseline | V2 semantic pipeline |
|---|---|---|
| Collection | `cri_chunks_multilingual_e5_base` | `cri_chunks_multilingual_e5_v2` |
| Points / records | 1,893 points | 1,901 retrieval records; 1,894 indexed points |
| Parents | Page/character chunks | 913 semantic parents |
| Chunking | About 2,800 characters, overlap 400 | Semantic parents with token-safe retrieval subchunks |
| Embeddings | `intfloat/multilingual-e5-base` | `intfloat/multilingual-e5-base` |
| Maximum embedding input | Character-based design | 499 tokens in the final validated artifact |
| Candidates / final | K≈10 / K=5 | K=30 / K=5 |
| Diversity | Document-based deduplication | Semantic-parent handling and soft family diversity |
| Temporal logic | Limited historical logic | Structured temporal metadata and strict-year experiment |
| Provenance | Filename/page metadata | Exact source spans and citation resolution |
| Threshold | Historical `0.823114` | No reused V1 threshold; `0.825` is evaluation-only |

The V2 threshold candidate `0.825` must not be copied into production configuration without a future approved calibration exercise.

## V2 evaluation snapshot

| Metric | V1 | V2 |
|---|---:|---:|
| Family Recall@1 | 0.36 | 0.60 |
| Family Recall@3 | 0.56 | 0.76 |
| Family Recall@5 | 0.64 | 0.86 |
| Family MRR | 0.469 | 0.693 |
| Cross-language success | 0.22 | 0.38 |

V2 Recall@5 by query language: French `1.00`, English `0.8667`, Arabic `0.60`, Spanish `0.90`. Arabic is the weakest evaluated language.

These are retrieval results, not proof that V2 generated better answers. The final generation comparison remained incomplete because of provider quotas.

## Adding new CRI documents

```text
New PDF → extraction/raw JSON → semantic JSON 2.2
         → retrieval build → V2 Qdrant ingestion → validation
```

Use stable `document_id` values. Genuine language versions of the same source should share a meaningful `document_family_id`; similar subjects alone are not sufficient. Preserve source text, source language, dates, numbers, and exact provenance. Use `scripts/build_retrieval_chunks_v2.py` and `scripts/ingest_qdrant_v2.py`; do not manually insert vectors.

## Integrating the historical FAQ knowledge base

The historical FAQ knowledge base is **not integrated in this repository**. It is a company handoff point.

```text
FAQ database/export → conversion adapter → semantic FAQ evidence
                    → content_type="faq" → retrieval chunks → V2 Qdrant
```

Suggested mapping: category to topic, question to title/tags/keywords, approved answer to original evidence text, language to `metadata.language`, dates to `temporal_scope`, and the original FAQ identifier to stable provenance. Do not invent PDF pages for FAQ records without PDF origins; preserve their real provenance type.

Two future strategies are possible: unified RAG evidence, or a high-confidence canonical FAQ match before document-RAG fallback. Canonical FAQ priority is **not implemented**.

## LLM provider handoff

`src/generation/llm_client.py` is a generic OpenAI-compatible client. Groq was the development provider, not an architectural requirement. Development used `qwen/qwen3.8-27b`; the final large generation benchmark was limited by Groq token quotas.

For OpenAI, configure the existing generic client through the variables used by `src/utils/config.py`:

```env
LLM_API_KEY=<company-owned OpenAI key>
LLM_BASE_URL=<OpenAI-compatible base URL>
LLM_MODEL=<model selected by CRI>
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=1024
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
```

Do not hard-code an unselected model. Changing the generation provider should not require rebuilding semantic JSON, E5 embeddings, Qdrant, or retrieval logic, but generation, language, structured-output, and citation tests must be rerun.

## Environment and launch

Create `.env` from `.env.example`. The current code uses `LLM_*`, not obsolete `GROQ_*`, names as its primary configuration.

```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
E5_COLLECTION=cri_chunks_multilingual_e5_base
LLM_API_KEY=
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=qwen/qwen3.8-27b
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=1024
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
```

The Groq values above are development examples only; company handoff should replace them with the selected OpenAI configuration.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
python scripts/run_api.py
```

In another terminal: `cd frontend`, `npm install`, `npm run dev`. The backend is normally at `http://127.0.0.1:8000`; the frontend is normally at `http://localhost:5173`.

## Testing and current status

```powershell
python -m pytest tests -p no:cacheprovider
cd frontend
npm test
npm run build
```

| Component | Status |
|---|---|
| Raw JSON V1 | Available |
| Semantic JSON V2 | Implemented |
| Retrieval chunks V2 | Implemented |
| Qdrant V2 | Implemented |
| Retriever V2 | Evaluated |
| Exact context provenance | Validated |
| Abstention V2 | Experimentally calibrated |
| Temporal V2 context | Experimentally evaluated |
| Generation | Functional |
| Final V1/V2 generation benchmark | Incomplete because of provider quota |
| Historical FAQ integration | Not implemented — company integration point |
| OpenAI production configuration | Not configured yet |
| Production V2 cutover | Not performed |

The final gate remained `V2_NOT_READY`; this means generated-answer comparison was incomplete, not that V2 retrieval failed. No production-readiness claim is made.

## Security and handoff

Never commit `.env`, API keys, private/internal PDFs, confidential JSON, local Qdrant storage, `.venv`, `node_modules`, or generated caches. Before handoff, provide/update `.env.example`, use a company-owned OpenAI key, do not transfer personal Groq credentials, verify internal-data Git policy, and inspect Git history for accidentally committed secrets.


# Rebuild Qdrant

This section explains how to rebuild the Qdrant vector database for both V1 and V2 from the project data.

## V1

### 1. Start Qdrant

```bash
docker compose up -d
```

### 2. Prepare the V1 documents

The V1 source files must be available in the following directory:

```text
data/
└── raw/
    ├── pdf/
    │   ├── document_1.pdf
    │   ├── document_2.pdf
    │   └── ...
    │
    └── json/
        ├── document_1.json
        ├── document_2.json
        └── ...
```

The `pdf/` directory contains the original PDF documents, while the `json/` directory contains the corresponding JSON files used by the V1 processing pipeline.

Make sure the required JSON files are available in:

```text
data/raw/json/
```

Then run:

```bash
python scripts/prepare_documents.py
```

This step processes the V1 JSON files and generates the processed chunks used by the V1 indexing pipeline.

### 3. Build the V1 Qdrant collection

```bash
python scripts/build_vector_index.py --model multilingual-e5-base
```

The expected Qdrant collection is:

```text
cri_chunks_multilingual_e5_base
```

### 4. Start the backend API

```bash
python scripts/run_api.py
```

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

---

## V2

### 1. Clone the chatbot repository

Clone the repository and move to the project directory.

### 2. Add the V2 semantic JSON files

The V2 JSON files must be placed in:

```text
data/semantic_json/
```

The expected structure is:

```text
data/
├── raw/
│   ├── pdf/
│   │   ├── document_1.pdf
│   │   ├── document_2.pdf
│   │   └── ...
│   │
│   └── json/
│       ├── document_1.json
│       ├── document_2.json
│       └── ...
│
└── semantic_json/
    ├── document_1.json
    ├── document_2.json
    └── ...
```

The `data/semantic_json/` directory contains the V2 semantic JSON files used to generate the retrieval chunks.

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the environment

Create a `.env` file from `.env.example` and configure the required variables.

Do not commit API keys or other secrets.

### 5. Start Qdrant

```bash
docker compose up -d
```

### 6. Generate the V2 retrieval chunks

```bash
python scripts/build_retrieval_chunks_v2.py
```

This step generates the V2 retrieval artifacts, including:

```text
data/retrieval_v2/retrieval_chunks.jsonl
data/retrieval_v2/retrieval_manifest.json
```

### 7. Build the V2 Qdrant collection

```bash
python scripts/ingest_qdrant_v2.py
```

The expected Qdrant collection is:

```text
cri_chunks_multilingual_e5_v2
```

### 8. Start the backend API

```bash
python scripts/run_api.py
```

### 9. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Expected Qdrant collections

After rebuilding both versions, Qdrant should contain:

```text
cri_chunks_multilingual_e5_base   # V1
cri_chunks_multilingual_e5_v2     # V2
```

V1 is kept as the historical baseline, while V2 is the semantic retrieval architecture used for evaluation and future extension.
