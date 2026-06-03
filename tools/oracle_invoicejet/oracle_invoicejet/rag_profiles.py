from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence


@dataclass(frozen=True)
class RAGProfile:
    key: str
    label: str
    description: str
    source_groups: List[str]
    preferred_source_types: List[str]
    type_boosts: Dict[str, float] = field(default_factory=dict)
    top_k_multiplier: int = 3
    per_type_k: int = 2
    min_hits: int = 1
    max_context_chars: int = 18000


RAG_PROFILES: Dict[str, RAGProfile] = {
    "full_app_qa": RAGProfile(
        key="full_app_qa",
        label="Pełne QA aplikacji",
        description="Ogólne pytania o InvoiceJet z dokumentacji technicznej i użytkownika.",
        source_groups=["doc_ai", "doc_user"],
        preferred_source_types=["mapping", "screen", "process", "api", "data_model", "business"],
        type_boosts={"mapping": 0.04, "screen": 0.02, "process": 0.02},
    ),
    "cross_reference": RAGProfile(
        key="cross_reference",
        label="Pytania przekrojowe",
        description="Łączy ekran, pole, proces, API, mapowania i model danych.",
        source_groups=["doc_ai", "doc_user"],
        preferred_source_types=["mapping", "screen", "api", "data_model", "process", "validation"],
        type_boosts={"mapping": 0.09, "screen": 0.07, "api": 0.06, "data_model": 0.06, "validation": 0.04},
        top_k_multiplier=5,
        per_type_k=2,
        max_context_chars=24000,
    ),
    "technical_deep_dive": RAGProfile(
        key="technical_deep_dive",
        label="Techniczna analiza",
        description="Backend, API, algorytmy, model danych, role i testy.",
        source_groups=["doc_ai"],
        preferred_source_types=["api", "data_model", "algorithm", "process", "mapping", "role", "test"],
        type_boosts={"api": 0.05, "data_model": 0.05, "algorithm": 0.04, "mapping": 0.04},
        top_k_multiplier=4,
        per_type_k=2,
        max_context_chars=22000,
    ),
    "database_sql": RAGProfile(
        key="database_sql",
        label="Model danych i SQL",
        description="Tabele, kolumny, relacje, slowniki i podstawowe zapytania SELECT.",
        source_groups=["doc_ai"],
        preferred_source_types=["data_model", "mapping", "process", "api", "algorithm", "validation"],
        type_boosts={"data_model": 0.1, "mapping": 0.08, "process": 0.05, "api": 0.04, "algorithm": 0.03},
        top_k_multiplier=6,
        per_type_k=3,
        max_context_chars=26000,
    ),
    "user_help": RAGProfile(
        key="user_help",
        label="Pomoc użytkownika",
        description="Instrukcje i procesy z dokumentacji użytkownika.",
        source_groups=["doc_user"],
        preferred_source_types=["screen", "process"],
        type_boosts={"screen": 0.04, "process": 0.03},
        top_k_multiplier=3,
        per_type_k=2,
        max_context_chars=16000,
    ),
}


CROSS_REFERENCE_MARKERS = {
    "ekran",
    "pole",
    "formularz",
    "tabela",
    "kolumna",
    "endpoint",
    "api",
    "dto",
    "walidacja",
    "walidacje",
    "proces",
    "pobierane",
    "pobiera",
    "źródło",
    "zrodlo",
    "sql",
    "select",
    "join",
    "kolumna",
    "kolumny",
    "status",
    "kontrahent",
    "klient",
}


def list_rag_profiles() -> List[RAGProfile]:
    return list(RAG_PROFILES.values())


def get_rag_profile(key: str | None) -> RAGProfile:
    if key and key in RAG_PROFILES:
        return RAG_PROFILES[key]
    return RAG_PROFILES["full_app_qa"]


def infer_rag_profile(question: str, scope: str | None = None, requested_profile: str | None = None) -> RAGProfile:
    if requested_profile:
        return get_rag_profile(requested_profile)
    if scope == "user":
        return RAG_PROFILES["user_help"]
    if scope in {"technical", "backend", "debt"}:
        return RAG_PROFILES["technical_deep_dive"]
    normalized = question.lower()
    marker_hits = sum(1 for marker in CROSS_REFERENCE_MARKERS if marker in normalized)
    if marker_hits >= 2:
        return RAG_PROFILES["cross_reference"]
    return RAG_PROFILES["full_app_qa"]


def filter_source_groups(profile: RAGProfile, fallback_groups: Sequence[str] | None = None) -> List[str]:
    if profile.source_groups:
        return profile.source_groups
    return list(fallback_groups or [])
