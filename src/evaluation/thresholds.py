"""Model-specific score-threshold calibration helpers."""

from typing import Any


def calibrate_threshold(rows: list[dict[str, Any]], thresholds: list[float]) -> list[dict[str, Any]]:
    """Evaluate evidence acceptance without declaring a universal threshold.

    Rows should contain ``answerable``, ``results`` and optionally a precomputed
    ``expected_sources`` list. A result is accepted when its top score meets the
    candidate threshold.
    """
    output = []
    # Benchmark rows keep the question metadata under ``question``; accept the
    # flat shape too so this helper remains convenient in unit tests.
    positives = [r for r in rows if (r.get("answerable", r.get("question", {}).get("answerable"))) is True]
    negatives = [r for r in rows if (r.get("answerable", r.get("question", {}).get("answerable"))) is False]
    for threshold in thresholds:
        accepted_positive = sum(_top1_score(r) >= threshold for r in positives)
        accepted_negative = sum(_top1_score(r) >= threshold for r in negatives)
        tp = accepted_positive
        fn = len(positives) - tp
        fp = accepted_negative
        tn = len(negatives) - fp
        tpr = tp / len(positives) if positives else None
        tnr = tn / len(negatives) if negatives else None
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tpr if tpr is not None else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        output.append({"threshold": threshold,
            "answerable_acceptance_rate": tpr,
            "unanswerable_rejection_rate": tnr,
            "false_acceptance_rate": fp / len(negatives) if negatives else None,
            "false_rejection_rate": fn / len(positives) if positives else None,
            "balanced_accuracy": ((tpr + tnr) / 2) if tpr is not None and tnr is not None else None,
            "precision": precision if positives or negatives else None,
            "recall": recall if positives else None,
            "f1": f1 if positives else None,
            "confusion_matrix": {"true_positive": tp, "false_positive": fp,
                                  "true_negative": tn, "false_negative": fn}})
    return output


def _top1_score(row: dict[str, Any]) -> float:
    results = row.get("results") or []
    score = results[0].get("score") if results else None
    return float("-inf") if score is None else float(score)


def threshold_candidates(rows: list[dict[str, Any]], step: float = 0.01) -> list[float]:
    """Build candidates from this model's observed top-1 score distribution."""
    scores = sorted({_top1_score(row) for row in rows if _top1_score(row) != float("-inf")})
    if not scores:
        return []
    candidates = set(scores)
    candidates.add(scores[0] - step)
    candidates.add(scores[-1] + step)
    candidates.update((a + b) / 2 for a, b in zip(scores, scores[1:]))
    return sorted(round(value, 6) for value in candidates)
