# Retrieval evaluation dataset

`retrieval_questions.json` intentionally starts empty. Add only manually validated CRI cases using this schema:

```json
[
  {
    "id": "q001",
    "question": "...",
    "query_language": "fr",
    "answerable": true,
    "cross_lingual": false,
    "expected_sources": [{"document_id": "...", "page": 25}],
    "expected_chunk_ids": []
  }
]
```

Include validated answerable and out-of-corpus (`answerable: false`) cases before using benchmark or threshold results for model selection.
