# Phase 4E.3 — final evidence-based evaluation gate

- Timestamp UTC: `2026-09-21T13:05:17.579380+00:00`
- Phase 4E, 4E.1, and 4E.2 artifacts were read-only inputs.

## Frozen retrieval evidence

- Frozen 4E.2 results SHA-256: `B18ADA928032C5C26C60FBB48294708C337325C424855876897C969A2E62AAAF`
- Frozen 4E.2 queries SHA-256: `1FB72325471FC45E2401F13DB7BA2637B7EC3EB036DF44B69DF1720540097BFE`
- Query composition: 70 total / 50 answerable / 20 no-answer.
- Frozen context citation validation: `1.000`.

## LLM preflight

{
  "status": "PASS",
  "configuration": {
    "endpoint_host": "api.groq.com",
    "model": "qwen/qwen3.8-27b",
    "api_key_configured": true
  },
  "checks": [
    {
      "name": "trivial_request",
      "status": "PASS"
    },
    {
      "name": "rag_style_request",
      "status": "PASS"
    }
  ]
}

## Generation execution

{
  "status": "RATE_LIMIT_PAUSED",
  "pause_reason": "rate-limit retries exhausted for Q024/v1/generation",
  "subset_count": 30,
  "completed_queries": 0,
  "attempted": 15,
  "succeeded": 0,
  "failed": 0,
  "success_rate": 0.0,
  "system_success": {},
  "stats": {
    "actual_llm_calls": 15,
    "avoided_llm_calls": 0,
    "rate_limit_events": [
      {
        "query_id": "Q019",
        "system": "v1",
        "phase": "generation",
        "retry_number": 1,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q019",
        "system": "v1",
        "phase": "generation",
        "retry_number": 2,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q019",
        "system": "v1",
        "phase": "generation",
        "retry_number": 3,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q019",
        "system": "v1",
        "phase": "generation",
        "retry_number": 4,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q024",
        "system": "v1",
        "phase": "generation",
        "retry_number": 1,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q024",
        "system": "v1",
        "phase": "generation",
        "retry_number": 2,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q024",
        "system": "v1",
        "phase": "generation",
        "retry_number": 3,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q024",
        "system": "v1",
        "phase": "generation",
        "retry_number": 4,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q024",
        "system": "v1",
        "phase": "generation",
        "retry_number": 5,
        "status": "429",
        "retry_delay_seconds": 60.0
      },
      {
        "query_id": "Q024",
        "system": "v1",
        "phase": "generation",
        "retry_number": 6,
        "status": "429",
        "retry_delay_seconds": 60.0
      }
    ],
    "total_rate_limit_wait_seconds": 600.0,
    "resumed_queries": 1
  }
}

## Groundedness, relevance, completeness, and language

{
  "v1": {
    "status": "NOT_EVALUATED",
    "supported_claim_rate": null,
    "unsupported_claim_rate": null,
    "language_compliance_rate": null,
    "relevance_pass_rate": null,
    "completeness_pass_rate": null
  },
  "v2": {
    "status": "NOT_EVALUATED",
    "supported_claim_rate": null,
    "unsupported_claim_rate": null,
    "language_compliance_rate": null,
    "relevance_pass_rate": null,
    "completeness_pass_rate": null
  },
  "v2_experimental": {
    "status": "NOT_EVALUATED",
    "supported_claim_rate": null,
    "unsupported_claim_rate": null,
    "language_compliance_rate": null,
    "relevance_pass_rate": null,
    "completeness_pass_rate": null
  }
}

## Evidence-derived gate measurements

{
  "v2_family_recall_at_5": 0.86,
  "frozen_v2_family_recall_at_5": 0.86,
  "language_breakdown": {
    "fr": {
      "count": 15,
      "frozen_recall_at_5": 1.0,
      "evaluated_recall_at_5": 1,
      "not_worse": true
    },
    "en": {
      "count": 15,
      "frozen_recall_at_5": 0.8666666666666667,
      "evaluated_recall_at_5": 0.8666666666666667,
      "not_worse": true
    },
    "ar": {
      "count": 10,
      "frozen_recall_at_5": 0.6,
      "evaluated_recall_at_5": 0.6,
      "not_worse": true
    },
    "es": {
      "count": 10,
      "frozen_recall_at_5": 0.9,
      "evaluated_recall_at_5": 0.9,
      "not_worse": true
    }
  },
  "generation_success_rate": 0.0,
  "frozen_context_citation_pass_rate": 1.0
}

## Final 4E.3 gate

{
  "unicode_dataset_validation": true,
  "retrieval_at_least_frozen_v2": true,
  "multilingual_acceptable": true,
  "abstention_calibrated": true,
  "temporal_improvement_preserved": true,
  "generation_evaluation_completed": false,
  "generation_success_rate": 0.0,
  "judge_success_requirement_met": false,
  "v1_supported_claim_rate": null,
  "v2_supported_claim_rate": null,
  "v1_unsupported_claim_rate": null,
  "v2_unsupported_claim_rate": null,
  "groundedness_at_least_v1": false,
  "answer_relevance_at_least_v1": false,
  "answer_completeness_at_least_v1": false,
  "answer_language_at_least_v1": false,
  "citation_validation_pass_rate": null,
  "exact_citations": false,
  "critical_regressions": 1,
  "status": "V2_NOT_READY"
}

No production cutover was performed; no corpus, collection, or ranking artifact was modified.

Generation is `NOT_EVALUATED`; groundedness, answer quality, and generated-answer citation validity are not claimed.
