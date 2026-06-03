from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

from .config import AppConfig
from .evaluation import result_to_row, run_eval_set
from .rag_profiles import get_rag_profile
from .retrieval import RetrievalService


@dataclass(frozen=True)
class ToolResult:
    name: str
    payload: dict[str, Any]


def search_docs(config: AppConfig, question: str, rag_profile: str = "full_app_qa", top_k: int | None = None) -> ToolResult:
    profile = get_rag_profile(rag_profile)
    hits = RetrievalService(config).search_with_profile(question, profile=profile, top_k=top_k or config.top_k)
    return ToolResult(
        name="search_docs",
        payload={
            "question": question,
            "rag_profile": profile.key,
            "hits": [_hit_to_dict(hit) for hit in hits],
        },
    )


def read_source(config: AppConfig, source_path: str, max_chars: int = 12000) -> ToolResult:
    resolved = _resolve_source_path(config, source_path)
    text = resolved.read_text(encoding="utf-8")
    return ToolResult(
        name="read_source",
        payload={
            "source_path": resolved.relative_to(config.repo_root).as_posix(),
            "text": text[:max_chars],
            "truncated": len(text) > max_chars,
        },
    )


def summarize_sources(config: AppConfig, question: str, rag_profile: str = "full_app_qa", top_k: int | None = None) -> ToolResult:
    search_result = search_docs(config, question, rag_profile=rag_profile, top_k=top_k)
    summaries = [
        {
            "source_path": hit["source_path"],
            "source_type": hit["source_type"],
            "heading_path": hit["heading_path"],
            "preview": hit["text"][:500],
        }
        for hit in search_result.payload["hits"]
    ]
    return ToolResult(name="summarize_sources", payload={"question": question, "summaries": summaries})


def compare_profiles(config: AppConfig, question: str, profiles: List[str] | None = None) -> ToolResult:
    selected = profiles or ["full_app_qa", "cross_reference", "technical_deep_dive", "user_help"]
    rows = []
    for profile_key in selected:
        result = search_docs(config, question, rag_profile=profile_key)
        rows.append(
            {
                "rag_profile": profile_key,
                "sources": [hit["source_path"] for hit in result.payload["hits"]],
                "source_types": sorted({hit["source_type"] for hit in result.payload["hits"]}),
            }
        )
    return ToolResult(name="compare_profiles", payload={"question": question, "profiles": rows})


def run_eval_tool(config: AppConfig, mode: str = "retrieval", limit: int | None = None) -> ToolResult:
    results = run_eval_set(config, mode=mode, limit=limit)
    return ToolResult(name="run_eval_set", payload={"mode": mode, "results": [result_to_row(result) for result in results]})


def _hit_to_dict(hit) -> dict[str, Any]:
    return {
        "id": hit.id,
        "source_path": hit.source_path,
        "source_group": str(hit.metadata.get("source_group", "")),
        "source_type": str(hit.metadata.get("source_type", "")),
        "heading_path": str(hit.metadata.get("heading_path", "ROOT")),
        "entity": str(hit.metadata.get("entity", "")),
        "table": str(hit.metadata.get("table", "")),
        "endpoint": str(hit.metadata.get("endpoint", "")),
        "distance": hit.distance,
        "text": hit.text,
    }


def _resolve_source_path(config: AppConfig, source_path: str) -> Path:
    relative = Path(source_path)
    if relative.is_absolute():
        raise ValueError("Only repository-relative source paths are allowed.")
    resolved = (config.repo_root / relative).resolve()
    if not str(resolved).startswith(str(config.repo_root.resolve())):
        raise ValueError("Source path escapes repository root.")
    allowed_roots = [(config.repo_root / source.relative_path).resolve() for source in config.sources]
    if not any(str(resolved).startswith(str(root)) for root in allowed_roots):
        raise ValueError("Source path is outside configured documentation sources.")
    if not resolved.exists() or resolved.suffix.lower() != ".md":
        raise FileNotFoundError(source_path)
    return resolved
