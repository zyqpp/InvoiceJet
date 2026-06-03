from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

from .config import AppConfig, SourceConfig
from .taxonomy import classify_document


@dataclass(frozen=True)
class SourceDocument:
    path: Path
    relative_path: str
    source_group: str
    audience: str
    priority: int
    source_type: str
    area: str
    entity: str
    screen: str
    process: str
    table: str
    endpoint: str
    knowledge_tags: str


def normalize_markdown(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalized.startswith("\ufeff"):
        normalized = normalized[1:]
    return normalized


def read_markdown(path: Path) -> str:
    return normalize_markdown(path.read_text(encoding="utf-8"))


def _is_excluded(path: Path, exclude_dirs: Iterable[str]) -> bool:
    lower_parts = [part.lower() for part in path.parts]
    return any(excluded in lower_parts for excluded in exclude_dirs)


def discover_documents(config: AppConfig) -> Tuple[List[SourceDocument], int]:
    documents: List[SourceDocument] = []
    skipped = 0
    seen: set[Path] = set()

    for source in config.sources:
        source_root = (config.repo_root / source.relative_path).resolve()
        if not source_root.exists():
            continue
        for file_path in source_root.rglob("*"):
            if not file_path.is_file() or file_path.suffix.lower() != ".md":
                continue
            if _is_excluded(file_path, config.exclude_dirs):
                skipped += 1
                continue
            resolved = file_path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            documents.append(_to_source_document(config, source, resolved))

    return sorted(documents, key=lambda item: item.relative_path), skipped


def _to_source_document(config: AppConfig, source: SourceConfig, path: Path) -> SourceDocument:
    relative_path = path.relative_to(config.repo_root).as_posix()
    taxonomy = classify_document(relative_path)
    return SourceDocument(
        path=path,
        relative_path=relative_path,
        source_group=source.source_group,
        audience=source.audience,
        priority=source.priority,
        source_type=taxonomy.source_type,
        area=taxonomy.area,
        entity=taxonomy.entity,
        screen=taxonomy.screen,
        process=taxonomy.process,
        table=taxonomy.table,
        endpoint=taxonomy.endpoint,
        knowledge_tags=taxonomy.knowledge_tags,
    )
