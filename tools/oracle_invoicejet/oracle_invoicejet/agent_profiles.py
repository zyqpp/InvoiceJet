from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict, List

from .profiles import ModelProfile, get_model_profile


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
    top_p: float = 0.9
    llm_top_k: int = 40
    repeat_penalty: float = 1.1
    seed: int | None = None
    timeout_sec: int = 900
    min_hits: int = 1
    model_profile: str = "balanced"
    prompt_profile: str = "oracle_rag_default"
    rag_profile: str = "full_app_qa"
    notes: str = ""
    tooltip: str = ""
    capabilities: List[str] | None = None
    limitations: List[str] | None = None
    examples: List[str] | None = None

    @property
    def required_models(self) -> List[str]:
        models = [self.llm_model, self.embedding_model]
        return list(dict.fromkeys(models))


def list_agent_profiles() -> List[AgentProfile]:
    return list(_load_agent_profiles().values())


def get_agent_profile(key: str) -> AgentProfile:
    profiles = _load_agent_profiles()
    return profiles.get(key, profiles["mietek"])


def _load_agent_profiles() -> Dict[str, AgentProfile]:
    tool_root = Path(__file__).resolve().parents[1]
    path = tool_root / "profiles" / "agent_profiles.json"
    rows = _read_json_list(path, _default_agent_rows())
    profiles: Dict[str, AgentProfile] = {}
    for row in rows:
        model_profile_key = str(row.get("model_profile", "balanced"))
        model_profile = get_model_profile(tool_root, model_profile_key)
        profile = _profile_from_row(row, model_profile)
        profiles[profile.key] = profile
    if "mietek" not in profiles:
        fallback_model = get_model_profile(tool_root, "balanced")
        fallback = _profile_from_row(_default_agent_rows()[0], fallback_model)
        profiles[fallback.key] = fallback
    return profiles


def _profile_from_row(row: dict[str, Any], model: ModelProfile) -> AgentProfile:
    return AgentProfile(
        key=str(row["key"]),
        name=str(row["name"]),
        role=str(row["role"]),
        description=str(row.get("description", "")),
        default_scope=str(row.get("default_scope", "full")),
        llm_model=str(row.get("llm_model", model.llm_model)),
        embedding_model=str(row.get("embedding_model", model.embedding_model)),
        top_k=int(row.get("top_k", model.top_k)),
        num_ctx=int(row.get("num_ctx", model.num_ctx)),
        temperature=float(row.get("temperature", model.temperature)),
        num_predict=int(row.get("num_predict", model.num_predict)),
        top_p=float(row.get("top_p", model.top_p)),
        llm_top_k=int(row.get("llm_top_k", model.llm_top_k)),
        repeat_penalty=float(row.get("repeat_penalty", model.repeat_penalty)),
        seed=int(row["seed"]) if row.get("seed") is not None else model.seed,
        timeout_sec=int(row.get("timeout_sec", model.timeout_sec)),
        min_hits=int(row.get("min_hits", 1)),
        model_profile=str(row.get("model_profile", model.key)),
        prompt_profile=str(row.get("prompt_profile", "oracle_rag_default")),
        rag_profile=str(row.get("rag_profile", "full_app_qa")),
        notes=str(row.get("notes", "")),
        tooltip=str(row.get("tooltip", "")),
        capabilities=[str(item) for item in row.get("capabilities", [])],
        limitations=[str(item) for item in row.get("limitations", [])],
        examples=[str(item) for item in row.get("examples", [])],
    )


def _read_json_list(path: Path, fallback: List[dict[str, Any]]) -> List[dict[str, Any]]:
    if not path.exists():
        return fallback
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Agent profile file must contain a list: {path}")
    return [dict(item) for item in payload]


def _default_agent_rows() -> List[dict[str, Any]]:
    return [
        {
            "key": "mietek",
            "name": "Mietek",
            "role": "Asystent ogólny",
            "description": "Najbezpieczniejszy profil do codziennego pytania o dokumentację InvoiceJet.",
            "default_scope": "full",
            "model_profile": "balanced",
            "prompt_profile": "oracle_rag_default",
            "rag_profile": "full_app_qa",
            "min_hits": 1,
        }
    ]
