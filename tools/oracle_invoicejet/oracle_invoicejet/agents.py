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

    def answer(
        self,
        question: str,
        requested_scope: str | None = None,
        requested_rag_profile: str | None = None,
        prompt_profile_key: str | None = None,
    ) -> OracleAnswer:
        start = time.perf_counter()
        trace: List[AgentTraceStep] = [AgentTraceStep("Orchestrator", "Start zapytania Oracle InvoiceJet.")]
        scope, source_groups, router_step = self.router.route(question, requested_scope)
        trace.append(router_step)
        rag_profile = infer_rag_profile(question, scope=scope, requested_profile=requested_rag_profile)
        rag_profile = _with_scope_fallback(rag_profile, source_groups)
        prompt_profile = get_prompt_profile(self.config.tool_root, prompt_profile_key)

        retrieval_start = time.perf_counter()
        hits, retriever_step = self.retriever.retrieve(question, rag_profile)
        retrieval_sec = time.perf_counter() - retrieval_start
        trace.append(retriever_step)

        if len(hits) < max(self.config.min_hits, rag_profile.min_hits):
            return self._fallback_answer(question, scope, rag_profile, prompt_profile, trace, start, retrieval_sec)

        audit_warnings, audit_step = self.auditor.audit(hits, rag_profile)
        trace.append(audit_step)
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

        verified, verifier_warnings, verifier_step = self.verifier.verify(answer, answer_citations)
        trace.append(verifier_step)
        warnings = audit_warnings + verifier_warnings
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
            scope, source_groups, router_step = self.router.route(question, requested_scope)
            trace.append(router_step)
            rag_profile = infer_rag_profile(question, scope=scope, requested_profile=requested_rag_profile)
            rag_profile = _with_scope_fallback(rag_profile, source_groups)
            prompt_profile = get_prompt_profile(self.config.tool_root, prompt_profile_key)

            yield _phase_started("retrieval", f"Wyszukuję kontekst profilem RAG `{rag_profile.key}`.")
            retrieval_start = time.perf_counter()
            hits, retriever_step = self.retriever.retrieve(question, rag_profile)
            retrieval_sec = time.perf_counter() - retrieval_start
            trace.append(retriever_step)
            yield _phase_completed(
                "retrieval",
                f"Znaleziono {len(hits)} fragmentów.",
                {"retrieval_sec": retrieval_sec, "rag_profile": rag_profile.key},
            )

            if len(hits) < max(self.config.min_hits, rag_profile.min_hits):
                answer = self._fallback_answer(question, scope, rag_profile, prompt_profile, trace, start, retrieval_sec)
                yield _completed_event(answer)
                return

            yield _phase_started("prompt_build", "Buduję prompt z kontekstu i polityki źródeł.")
            audit_warnings, audit_step = self.auditor.audit(hits, rag_profile)
            trace.append(audit_step)
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
            verified, verifier_warnings, verifier_step = self.verifier.verify(answer_text, citations)
            trace.append(verifier_step)
            warnings = audit_warnings + verifier_warnings
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
