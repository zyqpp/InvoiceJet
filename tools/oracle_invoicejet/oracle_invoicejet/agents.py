from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence

from .config import AppConfig
from .embeddings import OllamaClient, OllamaEmbeddingProvider
from .rag import NO_ANSWER, Citation, build_answer_prompt, build_citation_lines, pack_context
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


class RouterAgent:
    def route(self, question: str, requested_scope: str | None = None) -> tuple[str, List[str], AgentTraceStep]:
        if requested_scope and requested_scope in SCOPE_GROUPS:
            return requested_scope, SCOPE_GROUPS[requested_scope], AgentTraceStep("Router", f"Zakres wymuszony: {requested_scope}.")

        normalized = question.lower()
        if any(word in normalized for word in ["wytyczne", "zasady", "standard", "agent", "skill", "dokumentacji"]):
            scope = "technical"
        elif any(word in normalized for word in ["api", "endpoint", "controller", "backend", "jwt", "ef core", "sql"]):
            scope = "backend"
        elif any(word in normalized for word in ["angular", "frontend", "ekran", "ui", "komponent", "formularz"]):
            scope = "frontend"
        elif any(word in normalized for word in ["użytkownik", "instrukcja", "jak wystawić", "jak dodać"]):
            scope = "user"
        elif any(word in normalized for word in ["dług", "anomalia", "ryzyko", "bug", "problem"]):
            scope = "debt"
        else:
            scope = "full"
        return scope, SCOPE_GROUPS[scope], AgentTraceStep("Router", f"Zakres dobrany automatycznie: {scope}.")


class SourceAuditorAgent:
    def audit(self, hits: Sequence[SearchHit]) -> tuple[List[str], AgentTraceStep]:
        source_groups = {str(hit.metadata.get("source_group", "")) for hit in hits if hit.metadata}
        warnings: List[str] = []
        return warnings, AgentTraceStep("Source Auditor", f"Przeanalizowano grupy źródeł: {', '.join(sorted(source_groups)) or 'brak'}.")


class RetrieverAgent:
    def __init__(self, config: AppConfig, embedding_provider: OllamaEmbeddingProvider) -> None:
        self.config = config
        self.embedding_provider = embedding_provider

    def retrieve(self, question: str, source_groups: Sequence[str]) -> tuple[List[SearchHit], AgentTraceStep]:
        service = RetrievalService(self.config, self.embedding_provider)
        hits = service.search(question=question, top_k=self.config.top_k, source_groups=source_groups)
        return hits, AgentTraceStep("Retriever", f"Pobrano {len(hits)} fragmentów kontekstu.")


class AnswererAgent:
    def __init__(self, config: AppConfig, ollama: OllamaClient) -> None:
        self.config = config
        self.ollama = ollama

    def answer(self, prompt: str) -> tuple[str, AgentTraceStep]:
        payload = self.ollama.generate(
            model=self.config.llm_model,
            prompt=prompt,
            num_ctx=self.config.num_ctx,
            temperature=self.config.temperature,
            num_predict=self.config.num_predict,
        )
        answer = str(payload.get("response", "")).strip() or NO_ANSWER
        return answer, AgentTraceStep("Answerer", "Wygenerowano odpowiedź z lokalnego modelu Ollama.")


class VerifierAgent:
    def verify(self, answer: str, citations: Sequence[Citation]) -> tuple[bool, List[str], AgentTraceStep]:
        warnings: List[str] = []
        stripped = answer.strip()
        if stripped == NO_ANSWER:
            return True, warnings, AgentTraceStep("Verifier", "Odpowiedź poprawnie wskazuje brak danych w dokumentacji.")
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

    def answer(self, question: str, requested_scope: str | None = None) -> OracleAnswer:
        trace: List[AgentTraceStep] = [AgentTraceStep("Orchestrator", "Start zapytania Oracle InvoiceJet.")]
        scope, source_groups, router_step = self.router.route(question, requested_scope)
        trace.append(router_step)

        hits, retriever_step = self.retriever.retrieve(question, source_groups)
        trace.append(retriever_step)

        if len(hits) < self.config.min_hits:
            answer = NO_ANSWER
            citations: List[Citation] = []
            verified, verifier_warnings, verifier_step = self.verifier.verify(answer, citations)
            trace.append(verifier_step)
            return OracleAnswer(
                question=question,
                answer=answer,
                scope=scope,
                citations=citations,
                citation_lines=[],
                warnings=verifier_warnings,
                trace=trace,
                verified=verified,
            )

        audit_warnings, audit_step = self.auditor.audit(hits)
        trace.append(audit_step)
        packed_context = pack_context(hits)
        prompt = build_answer_prompt(question, packed_context, audit_warnings)
        answer, answerer_step = self.answerer.answer(prompt)
        trace.append(answerer_step)
        answer_citations = packed_context.citations
        if answer.strip().startswith(NO_ANSWER):
            answer = NO_ANSWER
            answer_citations = []

        verified, verifier_warnings, verifier_step = self.verifier.verify(answer, answer_citations)
        trace.append(verifier_step)
        warnings = audit_warnings + verifier_warnings
        if not verified:
            answer = NO_ANSWER

        return OracleAnswer(
            question=question,
            answer=answer,
            scope=scope,
            citations=answer_citations,
            citation_lines=build_citation_lines(answer_citations),
            warnings=warnings,
            trace=trace,
            verified=verified,
        )
