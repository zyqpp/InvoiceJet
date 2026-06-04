from __future__ import annotations

from pathlib import Path
import unittest

from oracle_invoicejet.agents import OracleOrchestrator, VerifierAgent
from oracle_invoicejet.config import AppConfig, SourceConfig
from oracle_invoicejet.retrieval import SearchHit


class FakeRetriever:
    def __init__(self, hits: list[SearchHit]) -> None:
        self.hits = hits

    def retrieve(self, question, rag_profile):  # noqa: ANN001
        from oracle_invoicejet.agents import AgentTraceStep

        return self.hits, AgentTraceStep("Retriever", "fake")


class FakeAnswerer:
    def __init__(self) -> None:
        self.called = False

    def stream(self, prompt: str):  # noqa: ANN201
        self.called = True
        yield {"response": "Pierwszy "}
        yield {"response": "drugi."}
        yield {"done": True, "prompt_eval_count": 10, "eval_count": 2, "eval_duration": 123}


class FailingAnswerer:
    def stream(self, prompt: str):  # noqa: ANN201
        raise TimeoutError("timeout")
        yield {}


class ThinkingAnswerer:
    def stream(self, prompt: str):  # noqa: ANN201
        yield {"response": "<think>ukryte rozumowanie</think>"}
        yield {"response": "Finalna odpowiedz."}
        yield {"done": True}


class StreamingTests(unittest.TestCase):
    def test_stream_answer_emits_phases_tokens_and_completed(self) -> None:
        orchestrator = OracleOrchestrator(_config())
        orchestrator.retriever = FakeRetriever([_hit()])
        orchestrator.answerer = FakeAnswerer()

        events = list(orchestrator.stream_answer("Jakie API ma ekran?", requested_rag_profile="cross_reference"))
        event_types = [event["type"] for event in events]
        token_events = [event for event in events if event["type"] == "token"]
        completed = events[-1]

        self.assertEqual(event_types[0], "phase_started")
        self.assertIn("phase_completed", event_types)
        self.assertEqual(token_events[0]["accumulated_text"], "Pierwszy ")
        self.assertEqual(token_events[-1]["accumulated_text"], "Pierwszy drugi.")
        self.assertEqual(completed["type"], "completed")
        self.assertEqual(completed["answer"], "Pierwszy drugi.")
        self.assertIsNotNone(completed["stats"]["time_to_first_token_sec"])
        self.assertEqual(completed["stats"]["eval_count"], 2)

    def test_no_context_completes_without_calling_ollama(self) -> None:
        orchestrator = OracleOrchestrator(_config())
        orchestrator.retriever = FakeRetriever([])
        answerer = FakeAnswerer()
        orchestrator.answerer = answerer

        events = list(orchestrator.stream_answer("Brak kontekstu", requested_rag_profile="full_app_qa"))

        self.assertFalse(answerer.called)
        self.assertEqual(events[-1]["type"], "completed")
        self.assertEqual(events[-1]["answer"], "Nie znalazłem tego w dokumentacji.")
        self.assertEqual(events[-1]["sources"], [])

    def test_ollama_error_emits_error_event(self) -> None:
        orchestrator = OracleOrchestrator(_config())
        orchestrator.retriever = FakeRetriever([_hit()])
        orchestrator.answerer = FailingAnswerer()

        events = list(orchestrator.stream_answer("Błąd modelu", requested_rag_profile="full_app_qa"))

        self.assertEqual(events[-1]["type"], "error")
        self.assertIn("timeout", events[-1]["technical_details"])

    def test_stream_answer_strips_thinking_blocks(self) -> None:
        orchestrator = OracleOrchestrator(_config())
        orchestrator.retriever = FakeRetriever([_hit()])
        orchestrator.answerer = ThinkingAnswerer()

        events = list(orchestrator.stream_answer("Jak liczy sie dokument?", requested_rag_profile="algorithm_calculation"))
        tokens = [event for event in events if event["type"] == "token"]
        completed = events[-1]

        self.assertEqual(tokens[-1]["accumulated_text"], "Finalna odpowiedz.")
        self.assertNotIn("<think>", completed["answer"])
        self.assertEqual(completed["answer"], "Finalna odpowiedz.")

    def test_verifier_rejects_mixed_fallback(self) -> None:
        verified, warnings, _ = VerifierAgent().verify(
            "Odpowiedz merytoryczna.\nNie znalazłem tego w dokumentacji.",
            [_citation()],
        )

        self.assertFalse(verified)
        self.assertTrue(warnings)


def _hit() -> SearchHit:
    return SearchHit(
        id="1",
        text="Opis ekranu i endpointu.",
        metadata={
            "source_path": "InvoiceJet/doc_AI/01_ekrany/E-01_LoginComponent/E-01_ekran.md",
            "source_group": "doc_ai",
            "source_type": "screen",
            "heading_path": "ROOT",
            "priority": 100,
        },
        distance=0.1,
    )


def _citation():
    from oracle_invoicejet.rag import Citation

    return Citation(
        source_path="InvoiceJet/doc_AI/source.md",
        source_group="doc_ai",
        source_type="algorithm",
        heading_path="ROOT",
        distance=0.1,
    )


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
