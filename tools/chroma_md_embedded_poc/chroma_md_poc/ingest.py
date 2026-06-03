from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import time
from typing import List

import chromadb

from chroma_md_poc.config import AppConfig, load_config
from chroma_md_poc.manifest import FileManifestEntry, IndexManifest
from chroma_md_poc.markdown_processing import (
    batched,
    chunk_markdown,
    discover_markdown_files,
    read_markdown,
    sha256_text,
)


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


def _create_collection(config: AppConfig):
    config.chroma_path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(config.chroma_path))
    collection = client.get_or_create_collection(name=config.collection_name)
    return client, collection


def _delete_chunk_ids(collection, chunk_ids: List[str], batch_size: int) -> int:
    if not chunk_ids:
        return 0
    deleted = 0
    for batch in batched(chunk_ids, batch_size):
        collection.delete(ids=batch)
        deleted += len(batch)
    return deleted


def run_ingest(config: AppConfig, force_rebuild: bool) -> IngestStats:
    start = time.perf_counter()
    stats = IngestStats()

    client, collection = _create_collection(config)
    manifest = IndexManifest.load(config.manifest_path)

    if force_rebuild:
        client.delete_collection(name=config.collection_name)
        collection = client.get_or_create_collection(name=config.collection_name)
        manifest = IndexManifest()

    files, skipped = discover_markdown_files(config)
    stats.files_discovered = len(files)
    stats.files_skipped = skipped

    discovered_rel = set()
    for file_path in files:
        rel_path = file_path.relative_to(config.project_root).as_posix()
        discovered_rel.add(rel_path)

        try:
            text = read_markdown(file_path)
        except UnicodeDecodeError:
            print(f"[WARN] Unsupported encoding (expected utf-8): {rel_path}")
            stats.read_errors += 1
            continue
        except OSError as exc:
            print(f"[WARN] Could not read {rel_path}: {exc}")
            stats.read_errors += 1
            continue

        source_hash = sha256_text(text)
        source_mtime = file_path.stat().st_mtime
        existing = manifest.files.get(rel_path)
        unchanged = (
            existing is not None
            and existing.file_sha256 == source_hash
            and abs(existing.source_mtime - source_mtime) < 0.001
        )
        if unchanged:
            stats.files_unchanged += 1
            continue

        chunks = chunk_markdown(
            rel_path=rel_path,
            text=text,
            chunk_size=config.chunk_size,
            overlap=config.chunk_overlap,
        )

        if existing:
            stats.chunks_deleted += _delete_chunk_ids(collection, existing.chunk_ids, config.batch_size)

        chunk_ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        metadatas = [
            {
                "source_path": rel_path,
                "file_name": file_path.name,
                "rel_dir": str(Path(rel_path).parent).replace("\\", "/"),
                "heading": chunk.heading,
                "chunk_index": chunk.chunk_index,
                "source_sha256": source_hash,
                "char_start": chunk.char_start,
                "char_end": chunk.char_end,
                "source_mtime": source_mtime,
            }
            for chunk in chunks
        ]

        for i in range(0, len(chunk_ids), config.batch_size):
            batch_ids = chunk_ids[i : i + config.batch_size]
            batch_docs = documents[i : i + config.batch_size]
            batch_meta = metadatas[i : i + config.batch_size]
            collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_meta)
            stats.chunks_upserted += len(batch_ids)

        manifest.files[rel_path] = FileManifestEntry(
            file_sha256=source_hash,
            source_mtime=source_mtime,
            chunk_ids=chunk_ids,
        )
        stats.files_changed += 1

    removed_files = sorted(set(manifest.files.keys()) - discovered_rel)
    for rel_path in removed_files:
        entry = manifest.files.pop(rel_path)
        stats.chunks_deleted += _delete_chunk_ids(collection, entry.chunk_ids, config.batch_size)
        stats.files_deleted += 1

    manifest.save(config.manifest_path)

    elapsed = time.perf_counter() - start
    print("=== Ingest Report ===")
    print(f"Collection         : {config.collection_name}")
    print(f"Project root       : {config.project_root}")
    print(f"Chroma path        : {config.chroma_path}")
    print(f"Files discovered   : {stats.files_discovered}")
    print(f"Files skipped      : {stats.files_skipped}")
    print(f"Files changed      : {stats.files_changed}")
    print(f"Files unchanged    : {stats.files_unchanged}")
    print(f"Files deleted      : {stats.files_deleted}")
    print(f"Chunks upserted    : {stats.chunks_upserted}")
    print(f"Chunks deleted     : {stats.chunks_deleted}")
    print(f"Read errors        : {stats.read_errors}")
    print(f"Collection records : {collection.count()}")
    print(f"Elapsed seconds    : {elapsed:.2f}")
    return stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Incremental markdown ingest into local Chroma (embedded mode).")
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Delete collection and manifest, then run full reindex.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()
    run_ingest(config=config, force_rebuild=args.force_rebuild)


if __name__ == "__main__":
    main()

