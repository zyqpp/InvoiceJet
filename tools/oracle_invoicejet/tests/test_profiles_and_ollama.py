from __future__ import annotations

from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from oracle_invoicejet.agent_profiles import get_agent_profile, list_agent_profiles
from oracle_invoicejet.embeddings import OllamaClient
from oracle_invoicejet.profiles import get_model_profile, get_prompt_profile


TOOL_ROOT = Path(__file__).resolve().parents[1]


class ProfilesAndOllamaTests(unittest.TestCase):
    def test_agent_profiles_are_loaded_from_config_shape(self) -> None:
        profiles = list_agent_profiles()
        mietek = get_agent_profile("mietek")
        db_sql = get_agent_profile("db_sql")
        klara = get_agent_profile("klara")
        zosia = get_agent_profile("zosia")

        self.assertGreaterEqual(len(profiles), 1)
        self.assertEqual(mietek.model_profile, "balanced")
        self.assertEqual(mietek.prompt_profile, "oracle_rag_default")
        self.assertEqual(mietek.rag_profile, "full_app_qa")
        self.assertEqual(db_sql.prompt_profile, "database_sql_assistant")
        self.assertEqual(db_sql.rag_profile, "database_sql")
        self.assertIn("SELECT", " ".join(db_sql.capabilities or []))
        self.assertIn("read-only", db_sql.notes)
        self.assertEqual(klara.prompt_profile, "algorithm_explainer")
        self.assertEqual(klara.rag_profile, "algorithm_calculation")
        self.assertEqual(klara.llm_model, "gemma3:12b")
        self.assertFalse(zosia.think)
        self.assertTrue(zosia.strip_thinking)

    def test_model_and_prompt_profiles_load(self) -> None:
        model = get_model_profile(TOOL_ROOT, "strict")
        quality_model = get_model_profile(TOOL_ROOT, "quality_local_12b")
        qwen_model = get_model_profile(TOOL_ROOT, "qwen3_no_think")
        prompt = get_prompt_profile(TOOL_ROOT, "cross_reference")
        sql_prompt = get_prompt_profile(TOOL_ROOT, "database_sql_assistant")
        algorithm_prompt = get_prompt_profile(TOOL_ROOT, "algorithm_explainer")

        self.assertEqual(model.llm_model, "gemma3:4b")
        self.assertEqual(quality_model.llm_model, "gemma3:12b")
        self.assertFalse(qwen_model.think)
        self.assertEqual(prompt.key, "cross_reference")
        self.assertIn("Kontekstu", prompt.rag_instruction)
        self.assertIn("SELECT", sql_prompt.rag_instruction)
        self.assertIn("```sql```", sql_prompt.answer_style)
        self.assertIn("frontendzie", algorithm_prompt.rag_instruction)

    @patch("oracle_invoicejet.embeddings.requests.post")
    def test_generate_maps_profile_options_to_ollama_payload(self, post: Mock) -> None:
        response = Mock()
        response.json.return_value = {"response": "ok"}
        response.raise_for_status.return_value = None
        post.return_value = response

        OllamaClient("http://ollama").generate(
            model="gemma3:4b",
            prompt="prompt",
            num_ctx=4096,
            temperature=0.0,
            num_predict=256,
            top_p=0.85,
            llm_top_k=30,
            repeat_penalty=1.2,
            seed=11,
            timeout_sec=123,
            think=False,
        )

        kwargs = post.call_args.kwargs
        self.assertEqual(kwargs["timeout"], 123)
        self.assertFalse(kwargs["json"]["think"])
        options = kwargs["json"]["options"]
        self.assertEqual(options["top_p"], 0.85)
        self.assertEqual(options["top_k"], 30)
        self.assertEqual(options["repeat_penalty"], 1.2)
        self.assertEqual(options["seed"], 11)


if __name__ == "__main__":
    unittest.main()
