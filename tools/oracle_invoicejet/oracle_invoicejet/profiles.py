from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class ModelProfile:
    key: str
    name: str
    description: str
    llm_model: str
    embedding_model: str
    top_k: int
    num_ctx: int
    temperature: float
    num_predict: int
    top_p: float = 0.9
    llm_top_k: int = 40
    repeat_penalty: float = 1.1
    seed: int | None = None
    timeout_sec: int = 900
    think: bool | str | None = None
    strip_thinking: bool = True


@dataclass(frozen=True)
class PromptProfile:
    key: str
    name: str
    description: str
    version: str
    system_prompt: str
    rag_instruction: str
    answer_style: str
    source_policy: str
    is_default: bool = False


def list_model_profiles(tool_root: Path) -> List[ModelProfile]:
    return list(_load_model_profiles(tool_root).values())


def get_model_profile(tool_root: Path, key: str | None) -> ModelProfile:
    profiles = _load_model_profiles(tool_root)
    if key and key in profiles:
        return profiles[key]
    return profiles.get("balanced", next(iter(profiles.values())))


def list_prompt_profiles(tool_root: Path) -> List[PromptProfile]:
    return list(_load_prompt_profiles(tool_root).values())


def get_prompt_profile(tool_root: Path, key: str | None) -> PromptProfile:
    profiles = _load_prompt_profiles(tool_root)
    if key and key in profiles:
        return profiles[key]
    for profile in profiles.values():
        if profile.is_default:
            return profile
    return next(iter(profiles.values()))


def _load_model_profiles(tool_root: Path) -> Dict[str, ModelProfile]:
    path = tool_root / "profiles" / "model_profiles.json"
    rows = _read_json_list(path, _default_model_profiles())
    profiles = {
        str(row["key"]): ModelProfile(
            key=str(row["key"]),
            name=str(row["name"]),
            description=str(row.get("description", "")),
            llm_model=str(row["llm_model"]),
            embedding_model=str(row["embedding_model"]),
            top_k=int(row["top_k"]),
            num_ctx=int(row["num_ctx"]),
            temperature=float(row["temperature"]),
            num_predict=int(row["num_predict"]),
            top_p=float(row.get("top_p", 0.9)),
            llm_top_k=int(row.get("llm_top_k", 40)),
            repeat_penalty=float(row.get("repeat_penalty", 1.1)),
            seed=int(row["seed"]) if row.get("seed") is not None else None,
            timeout_sec=int(row.get("timeout_sec", 900)),
            think=_parse_think(row.get("think")),
            strip_thinking=bool(row.get("strip_thinking", True)),
        )
        for row in rows
    }
    if not profiles:
        raise ValueError("No model profiles configured.")
    return profiles


def _load_prompt_profiles(tool_root: Path) -> Dict[str, PromptProfile]:
    path = tool_root / "profiles" / "prompt_profiles.json"
    rows = _read_json_list(path, _default_prompt_profiles())
    profiles = {
        str(row["key"]): PromptProfile(
            key=str(row["key"]),
            name=str(row["name"]),
            description=str(row.get("description", "")),
            version=str(row.get("version", "1")),
            system_prompt=str(row["system_prompt"]),
            rag_instruction=str(row["rag_instruction"]),
            answer_style=str(row.get("answer_style", "")),
            source_policy=str(row.get("source_policy", "")),
            is_default=bool(row.get("is_default", False)),
        )
        for row in rows
    }
    if not profiles:
        raise ValueError("No prompt profiles configured.")
    return profiles


def _read_json_list(path: Path, fallback: List[dict[str, Any]]) -> List[dict[str, Any]]:
    if not path.exists():
        return fallback
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Profile file must contain a list: {path}")
    return [dict(item) for item in payload]


def _default_model_profiles() -> List[dict[str, Any]]:
    return [
        {
            "key": "balanced",
            "name": "Balanced",
            "description": "Domyślny profil jakości dla RTX 2060 6GB.",
            "llm_model": "gemma3:4b",
            "embedding_model": "bge-m3",
            "top_k": 6,
            "num_ctx": 8192,
            "temperature": 0.1,
            "num_predict": 640,
            "top_p": 0.9,
            "llm_top_k": 40,
            "repeat_penalty": 1.1,
            "timeout_sec": 900,
            "think": None,
            "strip_thinking": True,
        }
    ]


def _parse_think(value: Any) -> bool | str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if not text or text == "auto":
        return None
    if text in {"true", "on", "yes", "1"}:
        return True
    if text in {"false", "off", "no", "0"}:
        return False
    if text in {"low", "medium", "high"}:
        return text
    raise ValueError(f"Unsupported think profile value: {value}")


def _default_prompt_profiles() -> List[dict[str, Any]]:
    return [
        {
            "key": "oracle_rag_default",
            "name": "Oracle RAG Default",
            "description": "Bezpieczna odpowiedź tylko na podstawie dokumentacji.",
            "version": "1",
            "is_default": True,
            "system_prompt": "Jesteś Oracle InvoiceJet, lokalnym asystentem RAG dla dokumentacji InvoiceJet.",
            "rag_instruction": "Odpowiadasz zawsze po polsku, konkretnie i tylko na podstawie sekcji Kontekst.",
            "answer_style": "Podawaj ustalenia, ograniczenia i cytowania do fragmentów kontekstu.",
            "source_policy": "Na końcu odpowiedzi dodaj sekcję Źródła z listą użytych source_path.",
        }
    ]
