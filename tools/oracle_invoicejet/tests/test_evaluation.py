from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from oracle_invoicejet.config import AppConfig, SourceConfig
from oracle_invoicejet.evaluation import EvalCase, load_eval_cases, run_eval_set, summarize_results
from oracle_invoicejet.rag import Citation
from oracle_invoicejet.retrieval import SearchHit


class FakeRetrievalService:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def search_with_profile(self, question, profile, top_k=None):  # noqa: ANN001
        return [
            SearchHit(
                id="hit-1",
                text="tekst",
                metadata={
                    "source_path": "InvoiceJet/doc_AI/01_ekrany/E-01_LoginComponent/E-01_ekran.md",
                    "source_type": "screen",
                    "source_group": "doc_ai",
                },
                distance=0.1,
            )
        ]


class FakeOracleOrchestrator:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def answer(self, question, requested_rag_profile=None):  # noqa: ANN001
        return SimpleNamespace(
            answer="UnitPrice Quantity dto.TotalPrice\nNie znalazłem tego w dokumentacji.",
            citations=[
                Citation(
                    source_path="InvoiceJet/doc_AI/03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md",
                    source_group="doc_ai",
                    source_type="algorithm",
                    heading_path="ROOT",
                    distance=0.1,
                )
            ],
            rag_profile=requested_rag_profile or "algorithm_calculation",
        )


class EvaluationTests(unittest.TestCase):
    def test_load_eval_cases_from_tool_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tool_root = Path(tmp)
            (tool_root / "eval").mkdir()
            (tool_root / "eval" / "golden_set.json").write_text(
                '[{"id":"case-1","question":"q","expected_source_types":["screen"]}]',
                encoding="utf-8",
            )

            cases = load_eval_cases(tool_root)

        self.assertEqual(cases[0].id, "case-1")
        self.assertEqual(cases[0].expected_source_types, ["screen"])

    def test_load_eval_cases_reads_answer_quality_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tool_root = Path(tmp)
            (tool_root / "eval").mkdir()
            (tool_root / "eval" / "golden_set.json").write_text(
                '[{"id":"case-1","question":"q","expected_answer_terms":["UnitPrice"],"forbidden_answer_terms":["Nie znalazlem"]}]',
                encoding="utf-8",
            )

            cases = load_eval_cases(tool_root)

        self.assertEqual(cases[0].expected_answer_terms, ["UnitPrice"])
        self.assertEqual(cases[0].forbidden_answer_terms, ["Nie znalazlem"])

    @patch("oracle_invoicejet.evaluation.RetrievalService", FakeRetrievalService)
    def test_run_eval_set_reports_passed_retrieval_case(self) -> None:
        config = _config()

        results = run_eval_set(config, mode="retrieval", limit=1)
        summary = summarize_results(results)

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].passed)
        self.assertEqual(summary["passed"], 1)

    @patch("oracle_invoicejet.evaluation.OracleOrchestrator", FakeOracleOrchestrator)
    @patch(
        "oracle_invoicejet.evaluation.load_eval_cases",
        lambda tool_root: [
            EvalCase(
                id="mixed-fallback",
                question="q",
                rag_profile="algorithm_calculation",
                expected_sources=["obliczanie_ceny_pozycji.md"],
                expected_source_types=["algorithm"],
                expected_answer_terms=["Document.TotalPrice"],
                forbidden_answer_terms=["Nie znalazłem tego w dokumentacji"],
            )
        ],
    )
    def test_answer_eval_fails_mixed_fallback_and_missing_terms(self) -> None:
        results = run_eval_set(_config(), mode="answer", limit=1)

        self.assertFalse(results[0].passed)
        self.assertTrue(results[0].mixed_fallback)
        self.assertIn("Document.TotalPrice", results[0].missing_answer_terms)
        self.assertIn("Nie znalazłem tego w dokumentacji", results[0].forbidden_answer_terms_found)


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
