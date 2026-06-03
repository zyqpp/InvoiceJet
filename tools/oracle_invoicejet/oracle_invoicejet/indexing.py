from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import time
from typing import Iterable, List

import chromadb

from .chunking import chunk_markdown, sha256_text
from .config import AppConfig
from .documents import SourceDocument, discover_documents, read_markdown
from .embeddings import OllamaEmbeddingProvider
from .manifest import FileManifestEntry, IndexManifest


@dataclass
class IngestStats:
    files_discovered: int = 0
    files_skipped: int = 0
    files_changed: int = 0
    files_unchanged: int = 0
    files_deleted: int = 0
    chunks_upserted: int = 0
    chunks_deleted: int = 0
    read_errors: int = 0
    collection_records: int = 0
    elapsed_seconds: float = 0.0
    source_counts: dict[str, int] = field(default_factory=dict)
    source_type_counts: dict[str, int] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


def batched(items: List, batch_size: int) -> Iterable[List]:
    for index in range(0, len(items), batch_size):
        yield items[index : index + batch_size]


class ChromaIndexRepository:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.config.chroma_path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(config.chroma_path))
        self.collection = self.client.get_or_create_collection(name=config.collection_name)

    def rebuild_collection(self) -> None:
        try:
            self.client.delete_collection(self.config.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(name=self.config.collection_name)

    def delete_ids(self, chunk_ids: List[str], batch_size: int) -> int:
        deleted = 0
        for batch in batched(chunk_ids, batch_size):
            if batch:
                self.collection.delete(ids=batch)
                deleted += len(batch)
        return deleted

    def upsert_chunks(
        self,
        document: SourceDocument,
        source_hash: str,
        source_mtime: float,
        chunks,
        embeddings: List[List[float]],
    ) -> int:
        if not chunks:
            return 0
        ids = [chunk.chunk_id for chunk in chunks]
        texts = [chunk.text for chunk in chunks]
        metadatas = [
            {
                "source_path": document.relative_path,
                "relative_path": document.relative_path,
                "file_name": Path(document.relative_path).name,
                "source_group": document.source_group,
                "audience": document.audience,
                "priority": document.priority,
                "source_type": document.source_type,
                "area": document.area,
                "entity": document.entity,
                "screen": document.screen,
                "process": document.process,
                "table": document.table,
                "endpoint": document.endpoint,
                "knowledge_tags": document.knowledge_tags,
                "heading": chunk.heading,
                "heading_path": chunk.heading_path,
                "chunk_index": chunk.chunk_index,
                "sha256": source_hash,
                "source_sha256": source_hash,
                "char_start": chunk.char_start,
                "char_end": chunk.char_end,
                "source_mtime": source_mtime,
            }
            for chunk in chunks
        ]

        upserted = 0
        for index in range(0, len(ids), self.config.batch_size):
            self.collection.upsert(
                ids=ids[index : index + self.config.batch_size],
                documents=texts[index : index + self.config.batch_size],
                embeddings=embeddings[index : index + self.config.batch_size],
                metadatas=metadatas[index : index + self.config.batch_size],
            )
            upserted += len(ids[index : index + self.config.batch_size])
        return upserted

    def count(self) -> int:
        return int(self.collection.count())


class IndexManager:
    def __init__(self, config: AppConfig, embedding_provider: OllamaEmbeddingProvider | None = None) -> None:
        self.config = config
        self.embedding_provider = embedding_provider or OllamaEmbeddingProvider(config)

    def run_ingest(self, force_rebuild: bool = False) -> IngestStats:
        start = time.perf_counter()
        stats = IngestStats()
        embedding_dimensions = self.embedding_provider.dimensions()
        repository = ChromaIndexRepository(self.config)
        manifest = IndexManifest.load(self.config.manifest_path)

        if force_rebuild:
            repository.rebuild_collection()
            manifest = IndexManifest.for_config(self.config, embedding_dimensions)
        elif not manifest.is_compatible_with(self.config, embedding_dimensions):
            raise RuntimeError(
                "Manifest indeksu nie pasuje do aktualnej konfiguracji. "
                "Uruchom `oracle-ingest --force-rebuild`."
            )
        elif not manifest.collection_name:
            manifest = IndexManifest.for_config(self.config, embedding_dimensions)

        documents, skipped = discover_documents(self.config)
        stats.files_discovered = len(documents)
        stats.files_skipped = skipped
        discovered_paths = {document.relative_path for document in documents}

        for document in documents:
            stats.source_counts[document.source_group] = stats.source_counts.get(document.source_group, 0) + 1
            stats.source_type_counts[document.source_type] = stats.source_type_counts.get(document.source_type, 0) + 1
            try:
                text = read_markdown(document.path)
            except UnicodeDecodeError:
                stats.read_errors += 1
                stats.warnings.append(f"Nieobsługiwane kodowanie UTF-8: {document.relative_path}")
                continue
            except OSError as exc:
                stats.read_errors += 1
                stats.warnings.append(f"Nie można odczytać {document.relative_path}: {exc}")
                continue

            source_hash = sha256_text(text)
            source_mtime = document.path.stat().st_mtime
            existing = manifest.files.get(document.relative_path)
            unchanged = (
                existing is not None
                and existing.file_sha256 == source_hash
                and abs(existing.source_mtime - source_mtime) < 0.001
            )
            if unchanged:
                stats.files_unchanged += 1
                continue

            chunks = chunk_markdown(document, text, self.config.chunk_size, self.config.chunk_overlap)
            if existing:
                stats.chunks_deleted += repository.delete_ids(existing.chunk_ids, self.config.batch_size)

            for chunk_batch in batched(chunks, self.config.batch_size):
                embeddings = self.embedding_provider.embed_documents([chunk.text for chunk in chunk_batch])
                stats.chunks_upserted += repository.upsert_chunks(
                    document=document,
                    source_hash=source_hash,
                    source_mtime=source_mtime,
                    chunks=chunk_batch,
                    embeddings=embeddings,
                )

            manifest.files[document.relative_path] = FileManifestEntry(
                file_sha256=source_hash,
                source_mtime=source_mtime,
                chunk_ids=[chunk.chunk_id for chunk in chunks],
                source_group=document.source_group,
            )
            stats.files_changed += 1

        removed_paths = sorted(set(manifest.files.keys()) - discovered_paths)
        for relative_path in removed_paths:
            entry = manifest.files.pop(relative_path)
            stats.chunks_deleted += repository.delete_ids(entry.chunk_ids, self.config.batch_size)
            stats.files_deleted += 1

        manifest.save_atomic(self.config.manifest_path)
        stats.collection_records = repository.count()
        stats.elapsed_seconds = time.perf_counter() - start
        return stats
