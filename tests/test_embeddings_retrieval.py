import numpy as np
import json

from src.embeddings.bge_m3 import BGEM3Provider
from src.embeddings.multilingual_e5 import MultilingualE5Provider
from src.evaluation.metrics import (is_cross_language_expected_source,
                                    is_expected_source, recall_at_k,
                                    reciprocal_rank)
from src.evaluation.thresholds import calibrate_threshold, threshold_candidates
from src.retrieval.semantic_retriever import SemanticRetriever
from src.vectorstore.qdrant_store import QdrantStore, point_id_for_chunk
from scripts.validate_retrieval_questions import (contains_arabic,
                                                   validate_question_text)


class FakeModel:
    def __init__(self):
        self.calls = []

    def encode(self, texts, **kwargs):
        self.calls.append(texts)
        return np.ones((len(texts), 3))


def test_provider_dimensions_and_e5_prefixes():
    bge = BGEM3Provider(model=FakeModel())
    e5_model = FakeModel()
    e5 = MultilingualE5Provider(model=e5_model)
    assert bge.dimension == 1024
    assert e5.dimension == 768
    e5.embed_documents(["مرحبا"])
    e5.embed_query("bonjour")
    assert e5_model.calls == [["passage: مرحبا"], ["query: bonjour"]]


def test_stable_ids_and_payload_preserve_unicode():
    chunk = {"chunk_id": "doc_p1_c1", "text": "نص عربي", "metadata":
             {"document_id": "doc", "filename": "x.pdf", "page": 1,
              "language": "ar", "chunk_index": 1}}
    assert point_id_for_chunk(chunk["chunk_id"]) == point_id_for_chunk(chunk["chunk_id"])
    payload = QdrantStore.payload_for_chunk(chunk)
    assert payload["text"] == "نص عربي"
    assert payload["source_type"] == "internal_cri_document"


def test_retriever_result_shape_top_k_and_threshold():
    class FakeStore:
        def search(self, *args, **kwargs):
            return [{"score": .9, "payload": {"chunk_id": "c1", "text": "نص", "document_id": "d",
                                                "filename": "f", "page": 1, "language": "ar"}}][:args[2]]
    results = SemanticRetriever(BGEM3Provider(model=FakeModel()), FakeStore(), "collection").search("سؤال", 1, .8)
    assert len(results) == 1 and results[0]["rank"] == 1 and results[0]["page"] == 1


def test_known_retrieval_metrics_and_threshold_metrics():
    results = [{"document_id": "wrong", "page": 1}, {"document_id": "right", "page": 2}]
    expected = [{"document_id": "right", "page": 2}]
    assert recall_at_k(results, expected, 1) == 0
    assert recall_at_k(results, expected, 3) == 1
    assert reciprocal_rank(results, expected) == .5
    threshold_rows = [{"answerable": True, "results": [{"score": .8}]},
                      {"answerable": False, "results": [{"score": .3}]}]
    calibrated = calibrate_threshold(threshold_rows, [.5])[0]
    assert calibrated["answerable_acceptance_rate"] == 1
    assert calibrated["unanswerable_rejection_rate"] == 1


def test_source_matching_ignores_language_but_rejects_wrong_page():
    expected = [{"document_id": "doc", "page": 25, "language": "ar"}]
    assert is_expected_source({"document_id": "doc", "page": 25, "language": "fr"}, expected)
    assert not is_expected_source({"document_id": "doc", "page": 26, "language": "ar"}, expected)


def test_normal_and_cross_language_matching_are_separate():
    expected = [{"document_id": "doc", "page": 2, "language": "fr"},
                {"document_id": "doc-ar", "page": 2, "language": "ar"}]
    same = {"document_id": "doc", "page": 2, "language": "fr"}
    other = {"document_id": "doc-ar", "page": 2, "language": "ar"}
    assert is_expected_source(same, expected)
    assert not is_cross_language_expected_source(same, expected, "fr")
    assert is_cross_language_expected_source(other, expected, "fr")
    assert recall_at_k([same], expected, 1) == 1
    assert reciprocal_rank([{"document_id": "wrong", "page": 1}, other], expected) == .5


def test_threshold_calibration_and_candidates_are_numeric_with_no_result_negative():
    rows = [{"answerable": True, "results": [{"score": .81}]},
            {"answerable": True, "results": [{"score": .72}]},
            {"answerable": False, "results": [{"score": .20}]},
            {"answerable": False, "results": []}]
    candidates = threshold_candidates(rows)
    calibrated = calibrate_threshold(rows, candidates)
    assert candidates and all(row["balanced_accuracy"] is not None for row in calibrated)
    assert all(row["f1"] is not None for row in calibrated)
    assert calibrated[0]["unanswerable_rejection_rate"] >= 0


def test_evaluation_text_encoding_validation_and_round_trip():
    arabic = "كم عدد الطلبات التي وافقت عليها اللجنة؟"
    assert contains_arabic(arabic)
    assert validate_question_text(arabic, "ar") == []
    assert validate_question_text("ÙƒÙ… Ø¹Ø¯Ø¯", "ar")

    data = {"fr": "Réponse : déjà validée", "es": "¿Qué ocurrió? Niño, acción" , "ar": arabic}
    encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
    loaded = json.loads(encoded.decode("utf-8"))
    assert loaded == data
