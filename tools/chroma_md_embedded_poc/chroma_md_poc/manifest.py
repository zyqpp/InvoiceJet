from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Dict, List


@dataclass
class FileManifestEntry:
    file_sha256: str
    source_mtime: float
    chunk_ids: List[str]


@dataclass
class IndexManifest:
    files: Dict[str, FileManifestEntry] = field(default_factory=dict)

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
            )
        return IndexManifest(files=files)

    def save(self, path: Path) -> None:
        payload = {
            "files": {
                key: {
                    "file_sha256": entry.file_sha256,
                    "source_mtime": entry.source_mtime,
                    "chunk_ids": entry.chunk_ids,
                }
                for key, entry in sorted(self.files.items(), key=lambda item: item[0])
            }
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

