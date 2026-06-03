from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Iterable, List, Sequence

from .config import AppConfig
from .embeddings import OllamaClient, OllamaEmbeddingProvider
from .profiles import PromptProfile, get_prompt_profile
from .rag import (
    NO_ANSWER,
    Citation,
    build_answer_prompt,
    build_citation_lines,
    build_classifier_prompt,
    build_decomposer_prompt,
    build_fact_check_prompt,
    has_mixed_no_answer,
    is_exact_no_answer,
    pack_context,
    remove_no_answer_markers,
    strip_thinking_sections,
)
from .rag_profiles import RAGProfile, filter_source_groups, infer_rag_profile
from .retrieval import RetrievalService, SearchHit


SCOPE_GROUPS: dict[str, List[str]] = {
    "full": ["doc_ai", "doc_user"],
    "technical": ["doc_ai"],
    "user": ["doc_user"],
    "backend": ["doc_ai"],
    "frontend": ["doc_ai"],
    "debt": ["doc_ai"],
}


@dataclass(frozen=True)
class AgentTraceStep:
    role: str
    message: str


@dataclass
class OracleAnswer:
    question: str
    answer: str
    scope: str
    citations: List[Citation]
    citation_lines: List[str]
    warnings: List[str] = field(default_factory=list)
    trace: List[AgentTraceStep] = field(default_factory=list)
    verified: bool = False
    rag_profile: str = "full_app_qa"
    prompt_profile: str = "oracle_rag_default"
    stats: dict[str, Any] = field(default_factory=dict)


class RouterAgent:
    def route(self, question: str, requested_scope: str | None = None) -> tuple[str, List[str], AgentTraceStep]:
        if requested_scope and requested_scope in SCOPE_GROUPS:
            return requested_scope, SCOPE_GROUPS[requested_scope], AgentTraceStep("Router", f"Zakres wymuszony: {requested_scope}.")

        normalized = question.lower()
        if any(word in normalized for word in ["wytyczne", "zasady", "standard", "agent", "skill", "dokumentacji"]):
            scope = "technical"
        elif any(word in normalized for word in ["api", "endpoint", "controller", "backend", "jwt", "ef core", "sql", "tabela"]):
            scope = "backend"
        elif any(word in normalized for word in ["angular", "frontend", "ekran", "ui", "komponent", "formularz", "pole"]):
            scope = "frontend"
        elif any(word in normalized for word in ["użytkownik", "instrukcja", "jak wystawić", "jak dodać"]):
            scope = "user"
        elif any(word in normalized for word in ["dług", "anomalia", "ryzyko", "bug", "problem"]):
            scope = "debt"
        else:
            scope = "full"
        return scope, SCOPE_GROUPS[scope], AgentTraceStep("Router", f"Zakres dobrany automatycznie: {scope}.")


class SourceAuditorAgent:
    def audit(self, hits: Sequence[SearchHit], rag_profile: RAGProfile) -> tuple[List[str], AgentTraceStep]:
        source_types = {str(hit.metadata.get("source_type", "")) for hit in hits if hit.metadata}
        source_groups = {str(hit.metadata.get("source_group", "")) for hit in hits if hit.metadata}
        warnings: List[str] = []
        if rag_profile.key == "cross_reference":
            required_any = {"mapping", "api", "data_model", "process"}
            if "screen" in source_types and not (source_types & required_any):
                warnings.append("Pytanie wygląda przekrojowo, ale retrieval nie znalazł źródeł API/modelu danych/procesu.")
        if rag_profile.key == "algorithm_calculation":
            if "algorithm" not in source_types:
                warnings.append("Profil wyliczeniowy nie znalazl dokumentu typu algorithm.")
            if "data_model" not in source_types:
                warnings.append("Profil wyliczeniowy nie znalazl modelu danych dla weryfikacji pol.")
        message = (
            f"Grupy: {', '.join(sorted(source_groups)) or 'brak'}; "
            f"typy: {', '.join(sorted(source_types)) or 'brak'}."
        )
        return warnings, AgentTraceStep("Source Auditor", message)


class RetrieverAgent:
    def __init__(self, config: AppConfig, embedding_provider: OllamaEmbeddingProvider) -> None:
        self.config = config
        self.embedding_provider = embedding_provider

    def retrieve(self, question: str, rag_profile: RAGProfile) -> tuple[List[SearchHit], AgentTraceStep]:
        service = RetrievalService(self.config, self.embedding_provider)
        hits = service.search_with_profile(question=question, top_k=self.config.top_k, profile=rag_profile)
        return hits, AgentTraceStep(
            "Retriever",
            f"Pobrano {len(hits)} fragmentów kontekstu profilem RAG `{rag_profile.key}`.",
        )


class AnswererAgent:
    def __init__(self, config: AppConfig, ollama: OllamaClient) -> None:
        self.config = config
        self.ollama = ollama

    def answer(self, prompt: str) -> tuple[str, dict[str, Any], AgentTraceStep]:
        payload = self.ollama.generate(
            model=self.config.llm_model,
            prompt=prompt,
            num_ctx=self.config.num_ctx,
            temperature=self.config.temperature,
            num_predict=self.config.num_predict,
            top_p=self.config.top_p,
            llm_top_k=self.config.llm_top_k,
            repeat_penalty=self.config.repeat_penalty,
            seed=self.config.seed,
            timeout_sec=self.config.timeout_sec,
            think=self.config.think,
        )
        answer = str(payload.get("response", ""))
        if self.config.strip_thinking:
            answer = strip_thinking_sections(answer)
        answer = answer.strip() or NO_ANSWER
        return answer, _ollama_stats(payload), AgentTraceStep("Answerer", "Wygenerowano odpowiedź z lokalnego modelu Ollama.")

    def stream(self, prompt: str) -> Iterable[dict[str, Any]]:
        return self.ollama.generate_stream(
            model=self.config.llm_model,
            prompt=prompt,
            num_ctx=self.config.num_ctx,
            temperature=self.config.temperature,
            num_predict=self.config.num_predict,
            top_p=self.config.top_p,
            llm_top_k=self.config.llm_top_k,
            repeat_penalty=self.config.repeat_penalty,
            seed=self.config.seed,
            timeout_sec=self.config.timeout_sec,
            think=self.config.think,
        )


class VerifierAgent:
    def verify(self, answer: str, citations: Sequence[Citation]) -> tuple[bool, List[str], AgentTraceStep]:
        warnings: List[str] = []
        stripped = answer.strip()
        if is_exact_no_answer(stripped):
            return True, warnings, AgentTraceStep("Verifier", "Odpowiedź poprawnie wskazuje brak danych w dokumentacji.")
        if has_mixed_no_answer(stripped):
            warnings.append("Model polaczyl odpowiedz z fallbackiem o braku danych. Odpowiedz wymaga ponownej generacji lub lepszego profilu.")
            return False, warnings, AgentTraceStep("Verifier", "Sprzeczny fallback w tresci odpowiedzi.")
        if not citations:
            warnings.append("Odpowiedź została zablokowana, bo nie ma żadnych cytowanych źródeł.")
            return False, warnings, AgentTraceStep("Verifier", "Brak cytowań źródłowych.")
        if "źródła" not in stripped.lower() and "zrodla" not in stripped.lower():
            warnings.append("Model nie dodał sekcji źródeł; cytowania pokazano osobno przez system.")
        return True, warnings, AgentTraceStep("Verifier", f"Zweryfikowano {len(citations)} cytowań.")


# ---------------------------------------------------------------------------
# RAG v2.0 — nowe klasy agentów
# ---------------------------------------------------------------------------

class QueryClassifierAgent:
    """Klasyfikuje intencję pytania przed wyszukiwaniem. Używa lekkiego LLM."""

    INTENT_TO_RAG_PROFILE: dict[str, str] = {
        "sql": "database_sql",
        "algorithm": "algorithm_calculation",
        "technical": "technical_deep_dive",
        "user_help": "user_help",
    }
    _VALID_INTENTS = {"user_help", "technical", "sql", "algorithm", "greeting", "unknown"}

    def __init__(self, config: AppConfig, ollama: OllamaClient) -> None:
        self.config = config
        self.ollama = ollama

    def classify(self, question: str) -> tuple[str, str | None, AgentTraceStep]:
        try:
            result = self.ollama.generate(
                model=self.config.light_llm_model,
                prompt=build_classifier_prompt(question),
                num_ctx=1024,
                temperature=0.0,
                num_predict=8,
                timeout_sec=30,
            )
            raw = result.get("response", "").strip().lower()
            intent = raw.split()[0] if raw.split() else "unknown"
            if intent not in self._VALID_INTENTS:
                intent = "unknown"
        except Exception:
            intent = "unknown"
        forced = self.INTENT_TO_RAG_PROFILE.get(intent)
        msg = f"Intencja: {intent}" + (f" → wymusza profil RAG: {forced}" if forced else "")
        return intent, forced, AgentTraceStep("Classifier", msg)


class QueryDecomposerAgent:
    """Rozbija złożone pytanie na pod-pytania dla lepszego retrieval."""

    def __init__(self, config: AppConfig, ollama: OllamaClient) -> None:
        self.config = config
        self.ollama = ollama

    def decompose(self, question: str) -> tuple[List[str], AgentTraceStep]:
        try:
            result = self.ollama.generate(
                model=self.config.light_llm_model,
                prompt=build_decomposer_prompt(question),
                num_ctx=1024,
                temperature=0.0,
                num_predict=128,
                timeout_sec=30,
            )
            raw = result.get("response", "").strip()
            lines = [line.strip() for line in raw.splitlines() if line.strip()]
            sub_queries: List[str] = lines[:3] if len(lines) > 1 else [question]
        except Exception:
            sub_queries = [question]
        if len(sub_queries) > 1:
            msg = f"Rozłożono na {len(sub_queries)} pod-pytań."
        else:
            msg = "Pytanie proste — bez dekompozycji."
        return sub_queries, AgentTraceStep("Decomposer", msg)


class ContextHygieneAgent:
    """Filtruje i deduplikuje chunki kontekstu. Bez LLM — czysta logika Python."""

    MAX_PER_TYPE: int = 3
    MIN_CHUNK_LEN: int = 80

    def clean(self, hits: List[SearchHit]) -> tuple[List[SearchHit], AgentTraceStep]:
        seen: set[tuple[str, str]] = set()
        type_counts: dict[str, int] = {}
        cleaned: List[SearchHit] = []
        removed = 0
        for hit in hits:
            key = (hit.source_path, str(hit.metadata.get("heading_path", "")))
            stype = str(hit.metadata.get("source_type", ""))
            if key in seen:
                removed += 1
                continue
            if len(hit.text.strip()) < self.MIN_CHUNK_LEN:
                removed += 1
                continue
            if type_counts.get(stype, 0) >= self.MAX_PER_TYPE:
                removed += 1
                continue
            seen.add(key)
            type_counts[stype] = type_counts.get(stype, 0) + 1
            cleaned.append(hit)
        msg = f"Hygiene: {len(cleaned)} chunków po filtracji (usunięto {removed})."
        return cleaned, AgentTraceStep("ContextHygiene", msg)


class MissingLinkAgent:
    """Wykrywa luki w wiedzy porównując retrieved chunks z potrzebami intencji."""

    INTENT_REQUIRES: dict[str, List[str]] = {
        "sql":       ["data_model"],
        "algorithm": ["algorithm"],
        "technical": ["api"],
    }

    def check(
        self,
        hits: Sequence[SearchHit],
        intent: str,
        rag_profile: RAGProfile,
    ) -> tuple[List[str], AgentTraceStep]:
        found_types = {str(h.metadata.get("source_type", "")) for h in hits}
        warnings: List[str] = []
        for req in self.INTENT_REQUIRES.get(intent, []):
            if req not in found_types:
                warnings.append(
                    f"Luka wiedzy: brakuje fragmentów typu `{req}` dla intencji `{intent}`."
                )
        for ptype in rag_profile.preferred_source_types[:2]:
            if ptype not in found_types:
                warnings.append(
                    f"Brakuje preferowanego typu `{ptype}` (profil {rag_profile.key})."
                )
        if warnings:
            msg = f"MissingLink: {len(warnings)} luk wykrytych."
        else:
            msg = "MissingLink: brak luk w wiedzy."
        return warnings, AgentTraceStep("MissingLink", msg)


class CodeSynthesizerAgent:
    """Wykrywa kontekst kodu/SQL i sugeruje właściwy prompt profile — bez LLM."""

    CODE_TYPES: set[str] = {"data_model", "algorithm"}
    CODE_PROFILE_MAP: dict[str, str] = {
        "data_model": "database_sql_assistant",
        "algorithm":  "algorithm_explainer",
    }
    GENERIC_PROFILES = {"oracle_rag_default", "cross_reference"}

    def detect_and_suggest(
        self,
        hits: Sequence[SearchHit],
        current_key: str,
    ) -> tuple[str, AgentTraceStep]:
        found_types = {str(h.metadata.get("source_type", "")) for h in hits}
        code_types_found = found_types & self.CODE_TYPES
        if code_types_found and current_key in self.GENERIC_PROFILES:
            dominant = max(
                code_types_found,
                key=lambda t: sum(1 for h in hits if h.metadata.get("source_type") == t),
            )
            suggested = self.CODE_PROFILE_MAP[dominant]
            return suggested, AgentTraceStep(
                "CodeSynth",
                f"Wykryto kontekst `{dominant}` → sugerowany prompt: `{suggested}`.",
            )
        return current_key, AgentTraceStep("CodeSynth", "Kontekst ogólny — prompt bez zmian.")


class FactCheckerAgent:
    """Weryfikuje odpowiedź pod kątem halucynacji. Używa lekkiego LLM."""

    def __init__(self, config: AppConfig, ollama: OllamaClient) -> None:
        self.config = config
        self.ollama = ollama

    def check(
        self,
        answer: str,
        context_text: str,
    ) -> tuple[bool, List[str], AgentTraceStep]:
        try:
            result = self.ollama.generate(
                model=self.config.light_llm_model,
                prompt=build_fact_check_prompt(answer, context_text[:2500]),
                num_ctx=4096,
                temperature=0.0,
                num_predict=4,
                timeout_sec=45,
            )
            raw = result.get("response", "").strip().upper()
            has_hallucination = raw.startswith("TAK")
        except Exception:
            return True, [], AgentTraceStep("FactChecker", "Weryfikacja pominięta (błąd modelu).")
        if has_hallucination:
            return (
                False,
                ["FactChecker: wykryto potencjalne informacje spoza dokumentacji."],
                AgentTraceStep("FactChecker", "UWAGA: odpowiedź może zawierać fakty spoza kontekstu."),
            )
        return True, [], AgentTraceStep("FactChecker", "Odpowiedź zgodna z kontekstem dokumentacji.")


class OracleOrchestrator:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.ollama = OllamaClient(config.ollama_base_url)
        self.embedding_provider = OllamaEmbeddingProvider(config, self.ollama)
        self.router = RouterAgent()
        self.retriever = RetrieverAgent(config, self.embedding_provider)
        self.answerer = AnswererAgent(config, self.ollama)
        self.auditor = SourceAuditorAgent()
        self.verifier = VerifierAgent()
        # v2 agents
        self.classifier = QueryClassifierAgent(config, self.ollama)
        self.decomposer = QueryDecomposerAgent(config, self.ollama)
        self.hygiene = ContextHygieneAgent()
        self.missing_link = MissingLinkAgent()
        self.code_synth = CodeSynthesizerAgent()
        self.fact_checker = FactCheckerAgent(config, self.ollama)

    def answer(
        self,
        question: str,
        requested_scope: str | None = None,
        requested_rag_profile: str | None = None,
        prompt_profile_key: str | None = None,
    ) -> OracleAnswer:
        start = time.perf_counter()
        trace: List[AgentTraceStep] = [AgentTraceStep("Orchestrator", "Start zapytania Oracle InvoiceJet.")]
        # v2: classify intent
        intent = "unknown"
        forced_rag_from_classifier: str | None = None
        if self.config.enable_query_classifier:
            intent, forced_rag_from_classifier, cls_step = self.classifier.classify(question)
            trace.append(cls_step)

        # v2: decompose complex question
        sub_queries: List[str] = [question]
        if self.config.enable_query_decomposer:
            sub_queries, decomp_step = self.decomposer.decompose(question)
            trace.append(decomp_step)

        scope, source_groups, router_step = self.router.route(question, requested_scope)
        trace.append(router_step)
        effective_rag = forced_rag_from_classifier or requested_rag_profile
        rag_profile = infer_rag_profile(question, scope=scope, requested_profile=effective_rag)
        rag_profile = _with_scope_fallback(rag_profile, source_groups)
        prompt_profile = get_prompt_profile(self.config.tool_root, prompt_profile_key)

        retrieval_start = time.perf_counter()
        if len(sub_queries) == 1:
            hits, retriever_step = self.retriever.retrieve(sub_queries[0], rag_profile)
        else:
            seen_ids: set[str] = set()
            hits = []
            for sq in sub_queries:
                sq_hits, _ = self.retriever.retrieve(sq, rag_profile)
                for h in sq_hits:
                    if h.id not in seen_ids:
                        seen_ids.add(h.id)
                        hits.append(h)
            retriever_step = AgentTraceStep(
                "Retriever",
                f"Pobrano {len(hits)} fragmentów z {len(sub_queries)} pod-zapytań profilem RAG `{rag_profile.key}`.",
            )
        retrieval_sec = time.perf_counter() - retrieval_start
        trace.append(retriever_step)

        # v2: hygiene
        if self.config.enable_context_hygiene:
            hits, hygiene_step = self.hygiene.clean(hits)
            trace.append(hygiene_step)

        if len(hits) < max(self.config.min_hits, rag_profile.min_hits):
            return self._fallback_answer(question, scope, rag_profile, prompt_profile, trace, start, retrieval_sec)

        # v2: missing link
        gap_warnings: List[str] = []
        if self.config.enable_missing_link:
            gap_warnings, missing_step = self.missing_link.check(hits, intent, rag_profile)
            trace.append(missing_step)

        audit_warnings, audit_step = self.auditor.audit(hits, rag_profile)
        trace.append(audit_step)
        audit_warnings = list(audit_warnings) + gap_warnings

        # v2: code synth auto-switch
        suggested_key, code_step = self.code_synth.detect_and_suggest(hits, prompt_profile.key)
        trace.append(code_step)
        if suggested_key != prompt_profile.key:
            prompt_profile = get_prompt_profile(self.config.tool_root, suggested_key)

        packed_context = pack_context(hits, max_chars=rag_profile.max_context_chars)
        portal_urls = {
            "doc_user": self.config.docs_portal_doc_user,
            "doc_ai":   self.config.docs_portal_doc_ai,
        }
        prompt = build_answer_prompt(question, packed_context, audit_warnings, prompt_profile=prompt_profile, portal_urls=portal_urls)

        generation_start = time.perf_counter()
        answer, model_stats, answerer_step = self.answerer.answer(prompt)
        generation_sec = time.perf_counter() - generation_start
        trace.append(answerer_step)

        answer_citations = packed_context.citations
        if is_exact_no_answer(answer):
            answer = NO_ANSWER
            answer_citations = []
        mixed_fallback = False
        if answer_citations and has_mixed_no_answer(answer):
            answer = remove_no_answer_markers(answer) or answer
            mixed_fallback = True

        # v2: fact checker
        fc_warnings: List[str] = []
        if self.config.enable_fact_checker and not is_exact_no_answer(answer):
            _, fc_warnings, fc_step = self.fact_checker.check(answer, packed_context.text)
            trace.append(fc_step)

        verified, verifier_warnings, verifier_step = self.verifier.verify(answer, answer_citations)
        trace.append(verifier_step)
        warnings = audit_warnings + verifier_warnings + fc_warnings
        if mixed_fallback:
            verified = False
            warnings.append("Model dopisal fallback o braku danych; fallback usunieto, a odpowiedz oznaczono jako niezweryfikowana.")
        if not verified and not mixed_fallback:
            answer = NO_ANSWER
            answer_citations = []

        stats = _base_stats(start, retrieval_sec, generation_sec)
        stats.update(model_stats)
        return OracleAnswer(
            question=question,
            answer=answer,
            scope=scope,
            citations=answer_citations,
            citation_lines=build_citation_lines(answer_citations),
            warnings=warnings,
            trace=trace,
            verified=verified,
            rag_profile=rag_profile.key,
            prompt_profile=prompt_profile.key,
            stats=stats,
        )

    def stream_answer(
        self,
        question: str,
        requested_scope: str | None = None,
        requested_rag_profile: str | None = None,
        prompt_profile_key: str | None = None,
    ) -> Iterable[dict[str, Any]]:
        start = time.perf_counter()
        trace: List[AgentTraceStep] = [AgentTraceStep("Orchestrator", "Start zapytania Oracle InvoiceJet.")]
        retrieval_sec = 0.0
        generation_sec = 0.0
        try:
            # v2: classify + decompose
            intent = "unknown"
            forced_rag_from_classifier: str | None = None
            if self.config.enable_query_classifier:
                yield _phase_started("classify", "Klasyfikuję intencję pytania...")
                intent, forced_rag_from_classifier, cls_step = self.classifier.classify(question)
                trace.append(cls_step)
                yield _phase_completed("classify", cls_step.message)

            sub_queries: List[str] = [question]
            if self.config.enable_query_decomposer:
                yield _phase_started("decompose", "Analizuję złożoność pytania...")
                sub_queries, decomp_step = self.decomposer.decompose(question)
                trace.append(decomp_step)
                yield _phase_completed("decompose", decomp_step.message)

            scope, source_groups, router_step = self.router.route(question, requested_scope)
            trace.append(router_step)
            effective_rag = forced_rag_from_classifier or requested_rag_profile
            rag_profile = infer_rag_profile(question, scope=scope, requested_profile=effective_rag)
            rag_profile = _with_scope_fallback(rag_profile, source_groups)
            prompt_profile = get_prompt_profile(self.config.tool_root, prompt_profile_key)

            yield _phase_started("retrieval", f"Wyszukuję kontekst profilem RAG `{rag_profile.key}`.")
            retrieval_start = time.perf_counter()
            if len(sub_queries) == 1:
                hits, retriever_step = self.retriever.retrieve(sub_queries[0], rag_profile)
            else:
                seen_ids: set[str] = set()
                hits = []
                for sq in sub_queries:
                    sq_hits, _ = self.retriever.retrieve(sq, rag_profile)
                    for h in sq_hits:
                        if h.id not in seen_ids:
                            seen_ids.add(h.id)
                            hits.append(h)
                retriever_step = AgentTraceStep(
                    "Retriever",
                    f"Pobrano {len(hits)} fragmentów z {len(sub_queries)} pod-zapytań profilem RAG `{rag_profile.key}`.",
                )
            retrieval_sec = time.perf_counter() - retrieval_start
            trace.append(retriever_step)
            yield _phase_completed(
                "retrieval",
                f"Znaleziono {len(hits)} fragmentów.",
                {"retrieval_sec": retrieval_sec, "rag_profile": rag_profile.key},
            )

            # v2: hygiene
            if self.config.enable_context_hygiene:
                hits, hygiene_step = self.hygiene.clean(hits)
                trace.append(hygiene_step)

            if len(hits) < max(self.config.min_hits, rag_profile.min_hits):
                answer = self._fallback_answer(question, scope, rag_profile, prompt_profile, trace, start, retrieval_sec)
                yield _completed_event(answer)
                return

            # v2: missing link
            gap_warnings: List[str] = []
            if self.config.enable_missing_link:
                gap_warnings, missing_step = self.missing_link.check(hits, intent, rag_profile)
                trace.append(missing_step)

            yield _phase_started("prompt_build", "Buduję prompt z kontekstu i polityki źródeł.")
            audit_warnings, audit_step = self.auditor.audit(hits, rag_profile)
            trace.append(audit_step)
            audit_warnings = list(audit_warnings) + gap_warnings

            # v2: code synth auto-switch
            suggested_key, code_step = self.code_synth.detect_and_suggest(hits, prompt_profile.key)
            trace.append(code_step)
            if suggested_key != prompt_profile.key:
                prompt_profile = get_prompt_profile(self.config.tool_root, suggested_key)

            packed_context = pack_context(hits, max_chars=rag_profile.max_context_chars)
            portal_urls = {
                "doc_user": self.config.docs_portal_doc_user,
                "doc_ai":   self.config.docs_portal_doc_ai,
            }
            prompt = build_answer_prompt(question, packed_context, audit_warnings, prompt_profile=prompt_profile, portal_urls=portal_urls)
            yield _phase_completed("prompt_build", "Prompt gotowy.", {"prompt_profile": prompt_profile.key})

            yield _phase_started("generation", f"Generuję odpowiedź modelem `{self.config.llm_model}`.")
            generation_start = time.perf_counter()
            first_token_sec: float | None = None
            raw_accumulated = ""
            accumulated = ""
            model_stats: dict[str, Any] = {}
            for payload in self.answerer.stream(prompt):
                delta = str(payload.get("response", ""))
                if delta:
                    raw_accumulated += delta
                    visible_text = strip_thinking_sections(raw_accumulated) if self.config.strip_thinking else raw_accumulated
                    if visible_text == accumulated:
                        continue
                    delta = visible_text[len(accumulated) :] if visible_text.startswith(accumulated) else visible_text
                    accumulated = visible_text
                    if first_token_sec is None:
                        first_token_sec = time.perf_counter() - start
                    yield {"type": "token", "delta": delta, "accumulated_text": accumulated}
                if payload.get("done"):
                    model_stats.update(_ollama_stats(payload))
            generation_sec = time.perf_counter() - generation_start
            yield _phase_completed("generation", "Generowanie zakończone.", {"generation_sec": generation_sec})

            answer_text = (strip_thinking_sections(raw_accumulated) if self.config.strip_thinking else accumulated).strip() or NO_ANSWER
            citations = packed_context.citations
            if is_exact_no_answer(answer_text):
                answer_text = NO_ANSWER
                citations = []
            mixed_fallback = False
            if citations and has_mixed_no_answer(answer_text):
                answer_text = remove_no_answer_markers(answer_text) or answer_text
                mixed_fallback = True

            # v2: fact checker
            fc_warnings: List[str] = []
            if self.config.enable_fact_checker and not is_exact_no_answer(answer_text):
                yield _phase_started("fact_check", "Weryfikuję odpowiedź pod kątem halucynacji...")
                _, fc_warnings, fc_step = self.fact_checker.check(answer_text, packed_context.text)
                trace.append(fc_step)
                yield _phase_completed("fact_check", fc_step.message)

            verified, verifier_warnings, verifier_step = self.verifier.verify(answer_text, citations)
            trace.append(verifier_step)
            warnings = audit_warnings + verifier_warnings + fc_warnings
            if mixed_fallback:
                verified = False
                warnings.append("Model dopisal fallback o braku danych; fallback usunieto, a odpowiedz oznaczono jako niezweryfikowana.")
            if not verified and not mixed_fallback:
                answer_text = NO_ANSWER
                citations = []
            stats = _base_stats(start, retrieval_sec, generation_sec)
            stats.update(model_stats)
            stats["time_to_first_token_sec"] = first_token_sec
            answer = OracleAnswer(
                question=question,
                answer=answer_text,
                scope=scope,
                citations=citations,
                citation_lines=build_citation_lines(citations),
                warnings=warnings,
                trace=trace,
                verified=verified,
                rag_profile=rag_profile.key,
                prompt_profile=prompt_profile.key,
                stats=stats,
            )
            yield _completed_event(answer)
        except Exception as exc:  # noqa: BLE001
            stats = _base_stats(start, retrieval_sec, generation_sec)
            yield {
                "type": "error",
                "message": "Nie udało się wygenerować odpowiedzi.",
                "technical_details": str(exc),
                "stats": stats,
            }

    def _fallback_answer(
        self,
        question: str,
        scope: str,
        rag_profile: RAGProfile,
        prompt_profile: PromptProfile,
        trace: List[AgentTraceStep],
        start: float,
        retrieval_sec: float,
    ) -> OracleAnswer:
        verified, warnings, verifier_step = self.verifier.verify(NO_ANSWER, [])
        trace.append(verifier_step)
        return OracleAnswer(
            question=question,
            answer=NO_ANSWER,
            scope=scope,
            citations=[],
            citation_lines=[],
            warnings=warnings,
            trace=trace,
            verified=verified,
            rag_profile=rag_profile.key,
            prompt_profile=prompt_profile.key,
            stats=_base_stats(start, retrieval_sec, 0.0),
        )


def _with_scope_fallback(profile: RAGProfile, source_groups: Sequence[str]) -> RAGProfile:
    groups = filter_source_groups(profile, source_groups)
    if groups == profile.source_groups:
        return profile
    return RAGProfile(
        key=profile.key,
        label=profile.label,
        description=profile.description,
        source_groups=groups,
        preferred_source_types=profile.preferred_source_types,
        type_boosts=profile.type_boosts,
        top_k_multiplier=profile.top_k_multiplier,
        per_type_k=profile.per_type_k,
        min_hits=profile.min_hits,
        max_context_chars=profile.max_context_chars,
    )


def _phase_started(phase: str, message: str) -> dict[str, Any]:
    return {"type": "phase_started", "phase": phase, "message": message}


def _phase_completed(phase: str, message: str, stats: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"type": "phase_completed", "phase": phase, "message": message}
    if stats:
        payload["stats"] = stats
    return payload


def _completed_event(answer: OracleAnswer) -> dict[str, Any]:
    return {
        "type": "completed",
        "answer": answer.answer,
        "sources": [_citation_to_dict(citation) for citation in answer.citations],
        "citation_lines": answer.citation_lines,
        "warnings": answer.warnings,
        "trace": [{"role": step.role, "message": step.message} for step in answer.trace],
        "scope": answer.scope,
        "verified": answer.verified,
        "rag_profile": answer.rag_profile,
        "prompt_profile": answer.prompt_profile,
        "stats": answer.stats,
    }


def _citation_to_dict(citation: Citation) -> dict[str, Any]:
    return {
        "source_path": citation.source_path,
        "source_group": citation.source_group,
        "source_type": citation.source_type,
        "heading_path": citation.heading_path,
        "distance": citation.distance,
        "area": citation.area,
        "entity": citation.entity,
        "table": citation.table,
        "endpoint": citation.endpoint,
    }


def _base_stats(start: float, retrieval_sec: float, generation_sec: float) -> dict[str, Any]:
    return {
        "retrieval_sec": retrieval_sec,
        "generation_sec": generation_sec,
        "total_sec": time.perf_counter() - start,
        "time_to_first_token_sec": None,
        "prompt_eval_count": None,
        "eval_count": None,
        "eval_duration_ns": None,
    }


def _ollama_stats(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "prompt_eval_count": payload.get("prompt_eval_count"),
        "eval_count": payload.get("eval_count"),
        "eval_duration_ns": payload.get("eval_duration"),
    }
