from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class AgentProfile:
    key: str
    name: str
    role: str
    description: str
    default_scope: str
    llm_model: str
    embedding_model: str
    top_k: int
    num_ctx: int
    temperature: float
    num_predict: int
    min_hits: int = 1
    notes: str = ""

    @property
    def required_models(self) -> List[str]:
        models = [self.llm_model, self.embedding_model]
        return list(dict.fromkeys(models))


AGENT_PROFILES: Dict[str, AgentProfile] = {
    "mietek": AgentProfile(
        key="mietek",
        name="Mietek",
        role="Asystent ogólny",
        description="Najbezpieczniejszy profil do codziennego pytania o dokumentację InvoiceJet.",
        default_scope="full",
        llm_model="gemma3:4b",
        embedding_model="bge-m3",
        top_k=5,
        num_ctx=8192,
        temperature=0.1,
        num_predict=512,
    ),
    "stefan": AgentProfile(
        key="stefan",
        name="Stefan",
        role="Techniczny analityk",
        description="Profil do pytań technicznych, architektury, procesów i dokumentacji AOS.",
        default_scope="technical",
        llm_model="gemma3:4b",
        embedding_model="bge-m3",
        top_k=6,
        num_ctx=8192,
        temperature=0.1,
        num_predict=640,
    ),
    "wojtek": AgentProfile(
        key="wojtek",
        name="Wojtek",
        role="Przewodnik użytkownika",
        description="Profil nastawiony na instrukcje użytkownika i proste odpowiedzi krok po kroku.",
        default_scope="user",
        llm_model="gemma3:4b",
        embedding_model="bge-m3",
        top_k=5,
        num_ctx=8192,
        temperature=0.1,
        num_predict=512,
    ),
    "albercik": AgentProfile(
        key="albercik",
        name="Albercik",
        role="Szybki tryb",
        description="Lekki profil do szybkiego sprawdzenia, czy indeks i Ollama odpowiadają.",
        default_scope="full",
        llm_model="gemma3:1b",
        embedding_model="bge-m3",
        top_k=4,
        num_ctx=4096,
        temperature=0.1,
        num_predict=384,
    ),
    "hania": AgentProfile(
        key="hania",
        name="Hania",
        role="Testerka jakości",
        description="Profil ostrożny: więcej źródeł, niska temperatura i nacisk na weryfikację.",
        default_scope="full",
        llm_model="gemma3:4b",
        embedding_model="bge-m3",
        top_k=8,
        num_ctx=8192,
        temperature=0.0,
        num_predict=640,
    ),
    "zosia": AgentProfile(
        key="zosia",
        name="Zosia",
        role="Eksperyment",
        description="Profil do porównywania zachowania innego modelu. Nie jest domyślny.",
        default_scope="full",
        llm_model="qwen3:4b",
        embedding_model="bge-m3",
        top_k=5,
        num_ctx=8192,
        temperature=0.1,
        num_predict=1024,
        notes="Na tej instalacji qwen3:4b może zużywać budżet odpowiedzi na thinking.",
    ),
}


def list_agent_profiles() -> List[AgentProfile]:
    return list(AGENT_PROFILES.values())


def get_agent_profile(key: str) -> AgentProfile:
    return AGENT_PROFILES.get(key, AGENT_PROFILES["mietek"])

