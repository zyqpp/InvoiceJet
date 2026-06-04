from __future__ import annotations

from pathlib import Path
import unittest

from oracle_invoicejet.config import AppConfig, SourceConfig
from oracle_invoicejet.rag_profiles import get_rag_profile
from oracle_invoicejet.retrieval import RetrievalService


class FakeEmbeddingProvider:
    def embed_query(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


class FakeCollection:
    def query(self, query_embeddings, n_results, where=None):  # noqa: ANN001
        rows = [
            ("screen", "screen-id", "screen text", 0.24),
            ("api", "api-id", "api text", 0.35),
            ("data_model", "db-id", "db text", 0.36),
            ("process", "process-id", "process text", 0.38),
            ("mapping", "mapping-id", "mapping text", 0.42),
        ]
        source_type = _source_type_from_where(where)
        if source_type:
            rows = [row for row in rows if row[0] == source_type]
        rows = rows[:n_results]
        return {
            "ids": [[row[1] for row in rows]],
            "documents": [[row[2] for row in rows]],
            "metadatas": [[_metadata(row[0], row[1]) for row in rows]],
            "distances": [[row[3] for row in rows]],
        }


class FakeCalculationCollection:
    def query(self, query_embeddings, n_results, where=None):  # noqa: ANN001
        rows = [
            (
                "algorithm",
                "calc-line",
                "TotalPrice = UnitPrice * Quantity * (1 + VatRate / 100)",
                "InvoiceJet/doc_AI/03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md",
                0.40,
            ),
            (
                "algorithm",
                "calc-update",
                "UpdateDocumentProducts sumuje dto.TotalPrice i UnitPrice * Quantity",
                "InvoiceJet/doc_AI/03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md",
                0.41,
            ),
            (
                "algorithm",
                "calc-total",
                "Document.TotalPrice to suma brutto dokumentu.",
                "InvoiceJet/doc_AI/03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md",
                0.42,
            ),
            (
                "data_model",
                "document-product",
                "DocumentProduct ma UnitPrice, Quantity, TotalPrice.",
                "InvoiceJet/doc_AI/05_model_danych/01_db/dbo/dbo.DocumentProduct.md",
                0.50,
            ),
            ("screen", "screen", "Ekran przelicza pozycje.", "InvoiceJet/doc_AI/01_ekrany/E-10_AddOrEditInvoiceComponent/E-10_ekran.md", 0.55),
        ]
        source_type = _source_type_from_where(where)
        if source_type:
            rows = [row for row in rows if row[0] == source_type]
        rows = rows[:n_results]
        return {
            "ids": [[row[1] for row in rows]],
            "documents": [[row[2] for row in rows]],
            "metadatas": [[_metadata_with_path(row[0], row[1], row[3]) for row in rows]],
            "distances": [[row[4] for row in rows]],
        }


class RetrievalProfileTests(unittest.TestCase):
    def test_cross_reference_profile_merges_preferred_source_types(self) -> None:
        service = object.__new__(RetrievalService)
        service.config = _config()
        service.embedding_provider = FakeEmbeddingProvider()
        service.collection = FakeCollection()

        hits = service.search_with_profile("ekran pole tabela api", get_rag_profile("cross_reference"), top_k=4)
        source_types = {hit.metadata["source_type"] for hit in hits}

        self.assertIn("screen", source_types)
        self.assertIn("api", source_types)
        self.assertIn("data_model", source_types)

    def test_database_sql_profile_prioritizes_data_model_context(self) -> None:
        service = object.__new__(RetrievalService)
        service.config = _config()
        service.embedding_provider = FakeEmbeddingProvider()
        service.collection = FakeCollection()

        hits = service.search_with_profile("select dokumenty status klient", get_rag_profile("database_sql"), top_k=3)
        source_types = [hit.metadata["source_type"] for hit in hits]

        self.assertEqual(source_types[0], "data_model")
        self.assertIn("mapping", source_types)

    def test_algorithm_calculation_profile_prioritizes_required_calculation_sources(self) -> None:
        service = object.__new__(RetrievalService)
        service.config = _config()
        service.embedding_provider = FakeEmbeddingProvider()
        service.collection = FakeCalculationCollection()

        hits = service.search_with_profile(
            "wyliczanie kwoty ceny produktu na pozycji dokumentu i suma dokumentu",
            get_rag_profile("algorithm_calculation"),
            top_k=5,
        )
        source_paths = [hit.source_path for hit in hits]

        self.assertIn("InvoiceJet/doc_AI/03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md", source_paths)
        self.assertIn("InvoiceJet/doc_AI/03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md", source_paths)
        self.assertIn("InvoiceJet/doc_AI/03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md", source_paths)
        self.assertIn("InvoiceJet/doc_AI/05_model_danych/01_db/dbo/dbo.DocumentProduct.md", source_paths)


def _source_type_from_where(where) -> str | None:  # noqa: ANN001
    if not where:
        return None
    if "source_type" in where:
        value = where["source_type"]
        return value if isinstance(value, str) else None
    for item in where.get("$and", []):
        if "source_type" in item:
            value = item["source_type"]
            return value if isinstance(value, str) else None
    return None


def _metadata(source_type: str, item_id: str) -> dict[str, object]:
    return _metadata_with_path(source_type, item_id, f"InvoiceJet/doc_AI/{item_id}.md")


def _metadata_with_path(source_type: str, item_id: str, source_path: str) -> dict[str, object]:
    return {
        "source_group": "doc_ai",
        "source_type": source_type,
        "source_path": source_path,
        "heading_path": "ROOT",
        "priority": 100,
    }


def _config() -> AppConfig:
    root = Path(__file__).resolve().parents[2]
    tool_root = Path(__file__).resolve().parents[1]
    return AppConfig(
        tool_root=tool_root,
        repo_root=root,
        chroma_path=tool_root / "chroma_data",
        manifest_path=tool_root / "index_manifest.json",
        collection_name="test",
        ollama_base_url="http://127.0.0.1:11434",
        llm_model="gemma3:4b",
        embedding_model="bge-m3",
        top_k=6,
        num_ctx=8192,
        temperature=0.1,
        num_predict=640,
        top_p=0.9,
        llm_top_k=40,
        repeat_penalty=1.1,
        seed=None,
        timeout_sec=900,
        chunk_size=1800,
        chunk_overlap=250,
        batch_size=24,
        min_hits=1,
        sources=[SourceConfig("doc_ai", "technical", 100, "InvoiceJet/doc_AI")],
        exclude_dirs=[],
        allowed_models=[],
    )


if __name__ == "__main__":
    unittest.main()
