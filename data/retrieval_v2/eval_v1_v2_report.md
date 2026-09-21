# Phase 4E — production v1 versus RAG v2 evaluation

- Timestamp UTC: `2026-09-20T21:46:23.524057+00:00`
- Evaluation is read-only; no collection, production retriever, prompt, API, semantic JSON, or retrieval JSONL was modified.

## Executive summary

- Queries evaluated: 55
- Languages: FR/EN/AR/ES
- Generation evaluation: Generation was circuit-broken after the first connection/configuration failure; retrieval evaluation remains complete.
- Dataset SHA-256: `229FD5097CD5643CFDCFC440D24E7DFECB5123857BEA339650841F500A1B1A4C`
- Retrieval JSONL SHA-256: `5062E2135C8856EB5BE03D68F0D065C8460825B6899F52E839487FD0519011F2`

## Configuration

- v1: current production adapter; candidate K 10; final K 5; threshold from production config; production deduplication/temporal behavior preserved.
- v2: finalized V2Retriever and ContextBuilderV2; candidate K 30; final K 5; no hard threshold; Phase-4C weights unchanged.
- Generation model: `qwen/qwen3.8-27b`; temperature: `0.0`; max tokens: `1024`.

## Reproducibility

{
  "collections": {
    "v1": {
      "name": "cri_chunks_multilingual_e5_base",
      "point_count": 1893
    },
    "v2": {
      "name": "cri_chunks_multilingual_e5_v2",
      "point_count": 1894
    }
  },
  "source_hashes": {
    "evaluation_module": "ED1D3073D4C132778E661D5866C4864774D00465261C404F2AE943AE6C309052",
    "evaluation_script": "8B8F3574388D742666A29505BBF11BF5602C681B4B345377392D6EF793F5F86F"
  },
  "packages": {
    "sentence-transformers": "6.0.0",
    "transformers": "5.15.1",
    "qdrant-client": "1.19.0",
    "torch": "2.13.0",
    "openai": "3.8.0"
  }
}

## Retrieval comparison

| Metric | v1 | v2 |
|---|---:|---:|
| family_recall_at_1 | 0.36 | 0.6 |
| family_recall_at_3 | 0.56 | 0.76 |
| family_recall_at_5 | 0.64 | 0.86 |
| topic_recall_at_5 | None | 0.82 |
| family_mrr | 0.469 | 0.693 |
| topic_mrr | None | 0.6573333333333333 |

## Language comparison

{
  "v1": {
    "fr": {
      "family_recall_at_5": 1.0,
      "family_mrr": 0.7799999999999999
    },
    "en": {
      "family_recall_at_5": 0.5333333333333333,
      "family_mrr": 0.3555555555555555
    },
    "ar": {
      "family_recall_at_5": 0.5,
      "family_mrr": 0.35833333333333334
    },
    "es": {
      "family_recall_at_5": 0.4,
      "family_mrr": 0.2833333333333333
    }
  },
  "v2": {
    "fr": {
      "family_recall_at_5": 1.0,
      "family_mrr": 0.9022222222222223
    },
    "en": {
      "family_recall_at_5": 0.8666666666666667,
      "family_mrr": 0.6355555555555555
    },
    "ar": {
      "family_recall_at_5": 0.6,
      "family_mrr": 0.425
    },
    "es": {
      "family_recall_at_5": 0.9,
      "family_mrr": 0.7333333333333333
    }
  }
}

## Temporal comparison

{
  "v1": {
    "requested_year_top1": 0.1,
    "requested_year_top5": 0.7,
    "conflicting_year_top1": 0.02,
    "conflicting_year_top5": 0.4
  },
  "v2": {
    "requested_year_top1": 0.16,
    "requested_year_top5": 0.9,
    "conflicting_year_top1": 0.04,
    "conflicting_year_top5": 0.8
  }
}

## Cross-language success

{
  "v1": 0.22,
  "v2": 0.38
}

## Threshold analysis

Scores are reported without selecting a production threshold. The old v1 threshold is not applied to v2.

{
  "v1": [
    {
      "threshold": 0.7,
      "answerable_acceptance": 0.82,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.9099999999999999
    },
    {
      "threshold": 0.72,
      "answerable_acceptance": 0.82,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.9099999999999999
    },
    {
      "threshold": 0.74,
      "answerable_acceptance": 0.82,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.9099999999999999
    },
    {
      "threshold": 0.76,
      "answerable_acceptance": 0.82,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.9099999999999999
    },
    {
      "threshold": 0.78,
      "answerable_acceptance": 0.82,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.9099999999999999
    },
    {
      "threshold": 0.8,
      "answerable_acceptance": 0.82,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.9099999999999999
    },
    {
      "threshold": 0.82,
      "answerable_acceptance": 0.82,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.9099999999999999
    },
    {
      "threshold": 0.84,
      "answerable_acceptance": 0.64,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.8200000000000001
    },
    {
      "threshold": 0.86,
      "answerable_acceptance": 0.28,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.64
    },
    {
      "threshold": 0.88,
      "answerable_acceptance": 0.1,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.55
    },
    {
      "threshold": 0.9,
      "answerable_acceptance": 0.06,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.53
    },
    {
      "threshold": 0.92,
      "answerable_acceptance": 0.02,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.51
    },
    {
      "threshold": 0.94,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.96,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.98,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 1.0,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    }
  ],
  "v2": [
    {
      "threshold": 0.7,
      "answerable_acceptance": 1.0,
      "unanswerable_rejection": 0.0,
      "false_acceptance": 1.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.72,
      "answerable_acceptance": 1.0,
      "unanswerable_rejection": 0.0,
      "false_acceptance": 1.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.74,
      "answerable_acceptance": 1.0,
      "unanswerable_rejection": 0.0,
      "false_acceptance": 1.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.76,
      "answerable_acceptance": 1.0,
      "unanswerable_rejection": 0.0,
      "false_acceptance": 1.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.78,
      "answerable_acceptance": 1.0,
      "unanswerable_rejection": 0.0,
      "false_acceptance": 1.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.8,
      "answerable_acceptance": 0.96,
      "unanswerable_rejection": 0.6,
      "false_acceptance": 0.4,
      "balanced_accuracy": 0.78
    },
    {
      "threshold": 0.82,
      "answerable_acceptance": 0.88,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.94
    },
    {
      "threshold": 0.84,
      "answerable_acceptance": 0.72,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.86
    },
    {
      "threshold": 0.86,
      "answerable_acceptance": 0.24,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.62
    },
    {
      "threshold": 0.88,
      "answerable_acceptance": 0.18,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.59
    },
    {
      "threshold": 0.9,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.92,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.94,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.96,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 0.98,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    },
    {
      "threshold": 1.0,
      "answerable_acceptance": 0.0,
      "unanswerable_rejection": 1.0,
      "false_acceptance": 0.0,
      "balanced_accuracy": 0.5
    }
  ]
}

## Context, citation, and answer comparison

v2 citations use Phase-4D exact provenance. v1 citations and context are preserved from the production pipeline and are not upgraded for this comparison.

{
  "v1": {
    "latency": {
      "median_ms": 82.89089996833354,
      "p95_ms": 107.89919999660924
    },
    "answer_language_compliance": 1.0,
    "grounded_support_rate": null
  },
  "v2": {
    "latency": {
      "median_ms": 84.75779998116195,
      "p95_ms": 136.907699983567
    },
    "answer_language_compliance": 1.0,
    "grounded_support_rate": null
  }
}

Generated-answer comparison was not completed because the configured generation endpoint returned a connection error; no answer-quality win is claimed.

## Low-confidence queries

The 5 `no_answer` queries are retained in the result artifact; their top scores and selected contexts can be inspected without treating retrieval as an answer.

## Failure cases

{
  "v1_better_or_v2_missed": [
    "Q019",
    "Q024",
    "Q032"
  ],
  "v2_better_or_v1_missed": [
    "Q013",
    "Q018",
    "Q020",
    "Q022",
    "Q026",
    "Q028",
    "Q035",
    "Q038",
    "Q039",
    "Q041",
    "Q042",
    "Q044",
    "Q046",
    "Q050"
  ],
  "both_missed": [
    "Q027",
    "Q029",
    "Q036",
    "Q048"
  ]
}

## Final cutover gate

{
  "retrieval_better_or_equal": true,
  "multilingual_better_or_equal": true,
  "temporal_better": false,
  "citation_precision_better": true,
  "groundedness_better_or_equal": false,
  "answer_generation_evaluated": false,
  "critical_regressions": 0,
  "status": "V2_NOT_READY"
}
## Aggregate context comparison
{
  "v1": {
    "mean_characters": 3098.6545454545453,
    "mean_unique_documents": 2.4363636363636365,
    "mean_unique_families": 2.2,
    "mean_parent_duplicate_rate": 0.0
  },
  "v2": {
    "mean_characters": 5853.527272727273,
    "mean_unique_documents": 2.9454545454545453,
    "mean_unique_families": 2.8,
    "mean_parent_duplicate_rate": 0.0
  }
}
## Low-confidence score summary
[
  {
    "query_id": "Q051",
    "question": "Quel est le montant du salaire minimum au Japon en 2026 ?",
    "v1_top1_score": null,
    "v2_top1_dense_score": 0.78511524,
    "v1_selected_count": 0,
    "v2_selected_count": 5
  },
  {
    "query_id": "Q052",
    "question": "What is the stock price of Tesla today?",
    "v1_top1_score": null,
    "v2_top1_dense_score": 0.80013824,
    "v1_selected_count": 0,
    "v2_selected_count": 5
  },
  {
    "query_id": "Q053",
    "question": "ما هو سعر النفط العالمي اليوم؟",
    "v1_top1_score": null,
    "v2_top1_dense_score": 0.7835299,
    "v1_selected_count": 0,
    "v2_selected_count": 5
  },
  {
    "query_id": "Q054",
    "question": "¿Cuál es el PIB de España en 2026?",
    "v1_top1_score": null,
    "v2_top1_dense_score": 0.7933939,
    "v1_selected_count": 0,
    "v2_selected_count": 5
  },
  {
    "query_id": "Q055",
    "question": "Quelle est la procédure pour obtenir un visa de travail au Canada ?",
    "v1_top1_score": null,
    "v2_top1_dense_score": 0.8029805,
    "v1_selected_count": 0,
    "v2_selected_count": 5
  }
]

The gate is evidence-derived and does not switch production. Any future tuning must be a separate frozen-before/after experiment.
