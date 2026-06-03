from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Dict, List

from .config import AppConfig, MANIFEST_SCHEMA_VERSION


@dataclass(frozen=True)
class FileManifestEntry:
    file_sha256: str
    source_mtime: float
    chunk_ids: List[str]
    source_group: str


@dataclass
class IndexManifest:
    schema_version: int = MANIFEST_SCHEMA_VERSION
    collection_name: str = ""
    embedding_model: str = ""
    embedding_dimensions: int = 0
    chunk_size: int = 0
    chunk_overlap: int = 0
    source_signature: str = ""
    files: Dict[str, FileManifestEntry] = field(default_factory=dict)

    @staticmethod
    def for_config(config: AppConfig, embedding_dimensions: int) -> "IndexManifest":
        return IndexManifest(
            collection_name=config.collection_name,
            embedding_model=config.embedding_model,
            embedding_dimensions=embedding_dimensions,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            source_signature=_source_signature(config),
        )

    @staticmethod
    def load(path: Path) -> "IndexManifest":
        if not path.exists():
            return IndexManifest()
        raw = json.loads(path.read_text(encoding="utf-8"))
        files: Dict[str, FileManifestEntry] = {}
        for key, value in raw.get("files", {}).items():
            files[key] = FileManifestEntry(
                file_sha256=value["file_sha256"],
                source_mtime=float(value["source_mtime"]),
                chunk_ids=list(value.get("chunk_ids", [])),
                source_group=str(value.get("source_group", "")),
            )
        return IndexManifest(
            schema_version=int(raw.get("schema_version", 0)),
            collection_name=str(raw.get("collection_name", "")),
            embedding_model=str(raw.get("embedding_model", "")),
            embedding_dimensions=int(raw.get("embedding_dimensions", 0) or 0),
            chunk_size=int(raw.get("chunk_size", 0) or 0),
            chunk_overlap=int(raw.get("chunk_overlap", 0) or 0),
            source_signature=str(raw.get("source_signature", "")),
            files=files,
        )

    def is_compatible_with(self, config: AppConfig, embedding_dimensions: int) -> bool:
        if not self.files:
            return True
        return (
            self.schema_version == MANIFEST_SCHEMA_VERSION
            and self.collection_name == config.collection_name
            and self.embedding_model == config.embedding_model
            and self.embedding_dimensions == embedding_dimensions
            and self.chunk_size == config.chunk_size
            and self.chunk_overlap == config.chunk_overlap
            and self.source_signature == _source_signature(config)
        )

    def save_atomic(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        payload = {
            "schema_version": self.schema_version,
            "collection_name": self.collection_name,
            "embedding_model": self.embedding_model,
            "embedding_dimensions": self.embedding_dimensions,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "source_signature": self.source_signature,
            "files": {
                key: {
                    "file_sha256": entry.file_sha256,
                    "source_mtime": entry.source_mtime,
                    "chunk_ids": entry.chunk_ids,
                    "source_group": entry.source_group,
                }
                for key, entry in sorted(self.files.items(), key=lambda item: item[0])
            },
        }
        tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.replace(path)


def _source_signature(config: AppConfig) -> str:
    payload = {
        "sources": [
            {
                "source_group": source.source_group,
                "audience": source.audience,
                "priority": source.priority,
                "relative_path": source.relative_path,
            }
            for source in config.sources
        ],
        "exclude_dirs": sorted(config.exclude_dirs),
    }
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
