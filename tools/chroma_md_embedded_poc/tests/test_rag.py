from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chroma_md_poc import rag  # noqa: E402


class FakeOllamaResponse:
    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    def __enter__(self) -> "FakeOllamaResponse":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def raise_for_status(self) -> None:
        return None

    def iter_lines(self, decode_unicode: bool = True):
        yield from self._lines


def _stream(rows, lines):
    with patch("chroma_md_poc.rag.query_rows", return_value=rows), patch(
        "chroma_md_poc.rag.requests.post",
        return_value=FakeOllamaResponse(lines),
    ):
        return list(
            rag.stream_rag_answer(
                question="Jak dziala logowanie?",
                model_name="test-model",
                top_k=5,
                source_contains="",
                temperature=0.2,
                num_ctx=4096,
                max_tokens=256,
                timeout_sec=30,
            )
        )


class StreamRagAnswerTests(unittest.TestCase):
    def test_emits_pipeline_events_in_expected_order(self) -> None:
        events = _stream(
            rows=[("1", "Fragment dokumentacji.", {"source_path": "docs/login.md", "heading": "Login"}, 0.1)],
            lines=[
                json.dumps({"response": "A", "done": False}),
                json.dumps({"done": True, "prompt_eval_count": 4, "eval_count": 1, "eval_duration": 1000}),
            ],
        )

        self.assertEqual(
            [event["type"] for event in events],
            [
                "phase_started",
                "phase_completed",
                "phase_started",
                "phase_completed",
                "phase_started",
                "token",
                "phase_completed",
                "completed",
            ],
        )
        self.assertEqual(events[0]["phase"], "retrieval")
        self.assertEqual(events[2]["phase"], "prompt_build")
        self.assertEqual(events[4]["phase"], "generation")
        self.assertEqual(events[-1]["answer"], "A")

    def test_no_context_finishes_without_ollama_call(self) -> None:
        with patch("chroma_md_poc.rag.query_rows", return_value=[]), patch(
            "chroma_md_poc.rag.requests.post"
        ) as post_mock:
            events = list(
                rag.stream_rag_answer(
                    question="Brakujace pytanie",
                    model_name="test-model",
                    top_k=5,
                    source_contains="",
                    temperature=0.2,
                    num_ctx=4096,
                    max_tokens=256,
                    timeout_sec=30,
                )
            )

        post_mock.assert_not_called()
        self.assertEqual(events[-1]["type"], "completed")
        self.assertEqual(events[-1]["answer"], rag.NO_CONTEXT_ANSWER)
        self.assertEqual(events[-1]["sources"], [])

    def test_ollama_stream_accumulates_tokens_and_sets_ttft(self) -> None:
        events = _stream(
            rows=[("1", "Fragment.", {"source_path": "docs/a.md"}, 0.1)],
            lines=[
                json.dumps({"response": "Pierwszy ", "done": False}),
                json.dumps({"response": "drugi", "done": False}),
                json.dumps({"done": True, "prompt_eval_count": 8, "eval_count": 2, "eval_duration": 2000}),
            ],
        )

        token_events = [event for event in events if event["type"] == "token"]
        self.assertEqual(token_events[0]["accumulated_text"], "Pierwszy ")
        self.assertEqual(token_events[1]["accumulated_text"], "Pierwszy drugi")
        self.assertGreater(events[-1]["stats"]["time_to_first_token_sec"], 0.0)

    def test_ollama_error_emits_error_without_completed_event(self) -> None:
        with patch(
            "chroma_md_poc.rag.query_rows",
            return_value=[("1", "Fragment.", {"source_path": "docs/a.md"}, 0.1)],
        ), patch("chroma_md_poc.rag.requests.post", side_effect=TimeoutError("timeout")):
            events = list(
                rag.stream_rag_answer(
                    question="Pytanie",
                    model_name="test-model",
                    top_k=5,
                    source_contains="",
                    temperature=0.2,
                    num_ctx=4096,
                    max_tokens=256,
                    timeout_sec=30,
                )
            )

        self.assertEqual(events[-1]["type"], "error")
        self.assertIn("timeout", events[-1]["technical_details"])
        self.assertNotIn("completed", [event["type"] for event in events])

    def test_sources_are_deduplicated_in_stable_order(self) -> None:
        events = _stream(
            rows=[
                ("1", "A", {"source_path": "docs/a.md"}, 0.1),
                ("2", "B", {"source_path": "docs/b.md"}, 0.2),
                ("3", "C", {"source_path": "docs/a.md"}, 0.3),
            ],
            lines=[
                json.dumps({"response": "Odpowiedz", "done": False}),
                json.dumps({"done": True}),
            ],
        )

        self.assertEqual(events[-1]["sources"], ["docs/a.md", "docs/b.md"])


if __name__ == "__main__":
    unittest.main()
