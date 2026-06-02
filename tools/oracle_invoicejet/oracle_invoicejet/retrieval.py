from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Sequence

import chromadb

from .config import AppConfig
from .embeddings import OllamaEmbeddingProvider


@dataclass(frozen=True)
class SearchHit:
    id: str
    text: str
    metadata: dict[str, Any]
    distance: float

    @property
    def source_path(self) -> str:
        return str(self.metadata.get("source_path", "-"))


class RetrievalService:
    def __init__(self, config: AppConfig, embedding_provider: OllamaEmbeddingProvider | None = None) -> None:
        self.config = config
        self.embedding_provider = embedding_provider or OllamaEmbeddingProvider(config)
        self.client = chromadb.PersistentClient(path=str(config.chroma_path))
        self.collection = self.client.get_collection(name=config.collection_name)

    def search(self, question: str, top_k: int | None = None, source_groups: Sequence[str] | None = None) -> List[SearchHit]:
        requested_top_k = top_k or self.config.top_k
        query_embedding = self.embedding_provider.embed_query(question)
        where = _build_where(source_groups)
        try:
            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=requested_top_k,
                where=where,
            )
        except Exception:
            result = self.collection.query(query_embeddings=[query_embedding], n_results=max(requested_top_k * 3, requested_top_k))
        rows = _rows_from_result(result)
        if source_groups:
            allowed = set(source_groups)
            rows = [row for row in rows if str(row.metadata.get("source_group", "")) in allowed]
        rows.sort(key=lambda hit: (hit.distance, -int(hit.metadata.get("priority", 0))))
        return rows[:requested_top_k]


def _build_where(source_groups: Sequence[str] | None) -> dict[str, Any] | None:
    if not source_groups:
        return None
    values = list(source_groups)
    if len(values) == 1:
        return {"source_group": values[0]}
    return {"source_group": {"$in": values}}


def _rows_from_result(result: dict[str, Any]) -> List[SearchHit]:
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    hits: List[SearchHit] = []
    for doc_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
        hits.append(SearchHit(id=str(doc_id), text=str(text or ""), metadata=dict(metadata or {}), distance=float(distance)))
    return hits

