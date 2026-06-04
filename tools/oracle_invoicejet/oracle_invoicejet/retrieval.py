from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, List, Sequence

import chromadb

from .config import AppConfig
from .documents import discover_documents, read_markdown
from .embeddings import OllamaEmbeddingProvider
from .rag_profiles import RAGProfile


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

    def search(
        self,
        question: str,
        top_k: int | None = None,
        source_groups: Sequence[str] | None = None,
        source_types: Sequence[str] | None = None,
    ) -> List[SearchHit]:
        requested_top_k = top_k or self.config.top_k
        query_embedding = self.embedding_provider.embed_query(question)
        return self._search_with_embedding(
            query_embedding=query_embedding,
            top_k=requested_top_k,
            source_groups=source_groups,
            source_types=source_types,
        )

    def search_with_profile(self, question: str, profile: RAGProfile, top_k: int | None = None) -> List[SearchHit]:
        requested_top_k = top_k or self.config.top_k
        query_embedding = self.embedding_provider.embed_query(question)
        query_terms = _query_terms(question)
        broad_hits = self._search_with_embedding(
            query_embedding=query_embedding,
            top_k=max(requested_top_k * profile.top_k_multiplier, requested_top_k),
            source_groups=profile.source_groups,
            source_types=None,
            apply_limit=False,
        )
        typed_hits: List[SearchHit] = []
        for source_type in profile.preferred_source_types:
            typed_hits.extend(
                self._search_with_embedding(
                    query_embedding=query_embedding,
                    top_k=profile.per_type_k,
                    source_groups=profile.source_groups,
                    source_types=[source_type],
                    apply_limit=True,
                )
            )
        lexical_hits = self._lexical_hits(question, profile, limit=max(requested_top_k, len(profile.preferred_source_types)))
        merged = _dedupe_hits([*lexical_hits, *typed_hits, *broad_hits])
        return _select_profiled_hits(merged, profile, requested_top_k, query_terms)

    def _lexical_hits(self, question: str, profile: RAGProfile, limit: int) -> List[SearchHit]:
        query_terms = _query_terms(question)
        if not query_terms:
            return []
        documents, _ = discover_documents(self.config)
        allowed_groups = set(profile.source_groups)
        preferred_types = set(profile.preferred_source_types)
        scored: List[tuple[int, SearchHit]] = []
        for document in documents:
            if allowed_groups and document.source_group not in allowed_groups:
                continue
            if preferred_types and document.source_type not in preferred_types:
                continue
            try:
                text = read_markdown(document.path)
            except OSError:
                continue
            score = _lexical_document_score(document.relative_path, text, query_terms)
            if score <= 0:
                continue
            metadata = {
                "source_path": document.relative_path,
                "relative_path": document.relative_path,
                "file_name": document.path.name,
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
                "heading": "ROOT",
                "heading_path": "ROOT",
                "chunk_index": -1,
            }
            scored.append(
                (
                    score,
                    SearchHit(
                        id=f"lexical::{document.relative_path}",
                        text=_lexical_snippet(text, query_terms),
                        metadata=metadata,
                        distance=_lexical_distance(score, profile),
                    ),
                )
            )
        scored.sort(key=lambda item: (-item[0], item[1].distance, item[1].source_path))
        ranked_hits = [hit for _, hit in scored]
        return _select_profiled_hits(ranked_hits, profile, limit, query_terms)

    def _search_with_embedding(
        self,
        query_embedding: List[float],
        top_k: int,
        source_groups: Sequence[str] | None = None,
        source_types: Sequence[str] | None = None,
        apply_limit: bool = True,
    ) -> List[SearchHit]:
        where = _build_where(source_groups, source_types)
        try:
            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
            )
        except Exception:
            result = self.collection.query(query_embeddings=[query_embedding], n_results=max(top_k * 3, top_k))
        rows = _rows_from_result(result)
        if source_groups:
            allowed = set(source_groups)
            rows = [row for row in rows if str(row.metadata.get("source_group", "")) in allowed]
        if source_types:
            allowed_types = set(source_types)
            rows = [row for row in rows if str(row.metadata.get("source_type", "")) in allowed_types]
        rows.sort(key=lambda hit: (hit.distance, -int(hit.metadata.get("priority", 0))))
        return rows[:top_k] if apply_limit else rows


def _build_where(source_groups: Sequence[str] | None, source_types: Sequence[str] | None = None) -> dict[str, Any] | None:
    filters: List[dict[str, Any]] = []
    if source_groups:
        filters.append(_field_filter("source_group", source_groups))
    if source_types:
        filters.append(_field_filter("source_type", source_types))
    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return {"$and": filters}


def _field_filter(field: str, values: Sequence[str]) -> dict[str, Any]:
    values = list(values)
    if len(values) == 1:
        return {field: values[0]}
    return {field: {"$in": values}}


def _rows_from_result(result: dict[str, Any]) -> List[SearchHit]:
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    hits: List[SearchHit] = []
    for doc_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
        hits.append(SearchHit(id=str(doc_id), text=str(text or ""), metadata=dict(metadata or {}), distance=float(distance)))
    return hits


def _dedupe_hits(hits: Sequence[SearchHit]) -> List[SearchHit]:
    best_by_id: dict[str, SearchHit] = {}
    for hit in hits:
        existing = best_by_id.get(hit.id)
        if existing is None or hit.distance < existing.distance:
            best_by_id[hit.id] = hit
    return list(best_by_id.values())


def _profiled_distance(hit: SearchHit, profile: RAGProfile, query_terms: Sequence[str] | None = None) -> float:
    source_type = str(hit.metadata.get("source_type", ""))
    return hit.distance - float(profile.type_boosts.get(source_type, 0.0)) - _lexical_bonus(hit, query_terms or [])


def _select_profiled_hits(
    hits: Sequence[SearchHit],
    profile: RAGProfile,
    top_k: int,
    query_terms: Sequence[str] | None = None,
) -> List[SearchHit]:
    ranked = sorted(
        hits,
        key=lambda hit: (_profiled_distance(hit, profile, query_terms), -int(hit.metadata.get("priority", 0)), hit.source_path),
    )
    selected: List[SearchHit] = []
    selected_ids: set[str] = set()
    for suffix in _query_specific_suffixes(query_terms or []):
        candidate = next(
            (
                hit
                for hit in ranked
                if hit.id not in selected_ids and hit.source_path.lower().endswith(suffix)
            ),
            None,
        )
        if candidate is None:
            continue
        selected.append(candidate)
        selected_ids.add(candidate.id)
        if len(selected) >= top_k:
            return selected
    if profile.key == "database_sql":
        for suffix in _sql_table_suffixes(query_terms or []):
            candidate = next(
                (
                    hit
                    for hit in ranked
                    if hit.id not in selected_ids and hit.source_path.lower().endswith(suffix)
                ),
                None,
            )
            if candidate is None:
                continue
            selected.append(candidate)
            selected_ids.add(candidate.id)
            if len(selected) >= top_k:
                return selected
        for hit in ranked:
            if hit.id in selected_ids or hit.metadata.get("source_type") != "data_model":
                continue
            selected.append(hit)
            selected_ids.add(hit.id)
            if len(selected) >= min(top_k, max(profile.per_type_k, 4)):
                break
    if profile.key == "algorithm_calculation":
        for suffix in _algorithm_calculation_suffixes(query_terms or []):
            candidate = next(
                (
                    hit
                    for hit in ranked
                    if hit.id not in selected_ids and hit.source_path.lower().endswith(suffix)
                ),
                None,
            )
            if candidate is None:
                continue
            selected.append(candidate)
            selected_ids.add(candidate.id)
            if len(selected) >= top_k:
                return selected
    for source_type in profile.preferred_source_types:
        candidate = next((hit for hit in ranked if hit.id not in selected_ids and hit.metadata.get("source_type") == source_type), None)
        if candidate is None:
            continue
        selected.append(candidate)
        selected_ids.add(candidate.id)
        if len(selected) >= top_k:
            return selected
    for hit in ranked:
        if hit.id in selected_ids:
            continue
        selected.append(hit)
        selected_ids.add(hit.id)
        if len(selected) >= top_k:
            break
    return selected


def _sql_table_suffixes(query_terms: Sequence[str]) -> List[str]:
    terms = set(query_terms)
    suffixes: List[str] = []
    if "document" in terms:
        suffixes.append("/dbo.document.md")
    if terms & {"firm", "client", "kontrahent", "klient"}:
        suffixes.append("/dbo.firm.md")
    if terms & {"userfirm", "client", "kontrahent", "klient", "firm"}:
        suffixes.append("/dbo.userfirm.md")
    if terms & {"documentstatus", "document_status", "status"}:
        suffixes.append("/dbo.documentstatus.md")
    return suffixes


def _query_specific_suffixes(query_terms: Sequence[str]) -> List[str]:
    suffixes: List[str] = []
    terms = set(query_terms)
    if "product" in terms and _has_endpoint_intent(query_terms) and not _has_calculation_intent(query_terms):
        suffixes.append("/04_api_i_integracje/01_api_frontend/product/get_product_getall.md")
    if _has_pdf_intent(query_terms):
        suffixes.extend(
            [
                "/04_api_i_integracje/01_api_frontend/document/post_document_generatepdf.md",
                "/04_api_i_integracje/01_api_frontend/document/post_document_getpdfstream.md",
            ]
        )
    if _has_role_intent(query_terms):
        suffixes.extend(
            [
                "/06_role_i_uprawnienia/readme.md",
                "/_mapowania/mapa_uprawnien_api.md",
            ]
        )
    return suffixes


def _algorithm_calculation_suffixes(query_terms: Sequence[str]) -> List[str]:
    terms = set(query_terms)
    suffixes = [
        "/03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md",
        "/03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md",
        "/03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md",
    ]
    if terms & {"documentproduct", "product", "pozycja", "pozycji", "produkt", "produktu"}:
        suffixes.append("/05_model_danych/01_db/dbo/dbo.documentproduct.md")
    if terms & {"document", "dokument", "dokumentu", "suma", "sumy", "totalprice"}:
        suffixes.append("/05_model_danych/01_db/dbo/dbo.document.md")
    return suffixes


def _query_terms(question: str) -> List[str]:
    terms = re.findall(r"[a-zA-Z0-9_ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", question.lower())
    technical_short_terms = {"api", "dto", "pdf", "db", "ui", "sql"}
    expanded = [term for term in terms if len(term) >= 4 or term in technical_short_terms]
    aliases = {
        "logowania": ["login", "auth"],
        "logowanie": ["login", "auth"],
        "rejestracji": ["register", "auth"],
        "rejestracja": ["register", "auth"],
        "serii": ["series", "documentseries", "document_series"],
        "dokumentow": ["document", "documentseries", "document_series"],
        "dokumentów": ["document", "documentseries", "document_series"],
        "kont": ["account", "bankaccount", "bank_account"],
        "bankowych": ["bankaccount", "bank_account"],
        "produktow": ["product"],
        "produktów": ["product"],
        "produkty": ["product"],
        "produktach": ["product"],
        "fakture": ["invoice", "document"],
        "fakturę": ["invoice", "document"],
        "dokument": ["document"],
        "dokumentu": ["document"],
        "dokumenty": ["document"],
        "kontrahent": ["firm", "client", "userfirm"],
        "kontrahenta": ["firm", "client", "userfirm"],
        "klient": ["firm", "client", "userfirm"],
        "klienta": ["firm", "client", "userfirm"],
        "nazwisko": ["name", "firm"],
        "nazwisku": ["name", "firm"],
        "nazwie": ["name", "firm"],
        "nazwa": ["name", "firm"],
        "status": ["documentstatus", "document_status"],
        "statusie": ["documentstatus", "document_status"],
        "statusu": ["documentstatus", "document_status"],
        "kolumna": ["column"],
        "kolumny": ["column"],
        "sprzedazy": ["issuedate"],
        "sql": ["select", "join", "where"],
        "select": ["sql", "join", "where"],
        "pdf": ["generatepdf", "getpdfstream"],
        "generowany": ["generatepdf", "getpdfstream"],
        "generowanie": ["generatepdf", "getpdfstream"],
        "strumien": ["getpdfstream"],
        "strumień": ["getpdfstream"],
        "uprawnienia": ["role", "permissions", "authorize"],
        "uprawnien": ["role", "permissions", "authorize"],
        "uprawnień": ["role", "permissions", "authorize"],
        "rola": ["role", "authorize"],
        "role": ["role", "authorize"],
        "dashboard": ["dashboardstats"],
        "statystyki": ["dashboardstats"],
        "statystyk": ["dashboardstats"],
        "dto": ["dto"],
        "kwota": ["totalprice", "unitprice"],
        "kwoty": ["totalprice", "unitprice"],
        "cena": ["price", "unitprice", "totalprice"],
        "ceny": ["price", "unitprice", "totalprice"],
        "suma": ["sum", "totalprice", "document"],
        "sumy": ["sum", "totalprice", "document"],
        "wartosc": ["value", "totalprice"],
        "wartosci": ["value", "totalprice"],
        "wyliczanie": ["calculate", "calculation", "totalprice", "unitprice", "quantity", "vatrate"],
        "wyliczana": ["calculate", "calculation", "totalprice", "unitprice", "quantity", "vatrate"],
        "obliczanie": ["calculate", "calculation", "totalprice", "unitprice", "quantity", "vatrate"],
        "obliczana": ["calculate", "calculation", "totalprice", "unitprice", "quantity", "vatrate"],
        "pozycja": ["documentproduct", "product", "quantity"],
        "pozycji": ["documentproduct", "product", "quantity"],
        "produkt": ["product", "documentproduct"],
        "produktu": ["product", "documentproduct"],
    }
    for term in terms:
        expanded.extend(aliases.get(term, []))
    return list(dict.fromkeys(expanded))


def _lexical_bonus(hit: SearchHit, query_terms: Sequence[str]) -> float:
    if not query_terms:
        return 0.0
    haystack = " ".join(
        [
            hit.source_path,
            str(hit.metadata.get("heading_path", "")),
            str(hit.metadata.get("entity", "")),
            str(hit.metadata.get("endpoint", "")),
            hit.text[:700],
        ]
    ).lower()
    matches = sum(1 for term in query_terms if term in haystack)
    return min(matches * 0.025, 0.125)


def _lexical_distance(score: int, profile: RAGProfile) -> float:
    if profile.key == "database_sql":
        return max(0.001, 1.0 / (score + 1))
    return max(0.01, 0.55 - score * 0.05)


def _lexical_document_score(relative_path: str, text: str, query_terms: Sequence[str]) -> int:
    path_haystack = relative_path.lower()
    text_haystack = text[:6000].lower()
    score = 0
    for term in query_terms:
        if term in path_haystack:
            score += 3
        if term in text_haystack:
            score += 1
    if _has_table_intent(query_terms) and ("/01_db/" in path_haystack or "/dbo/" in path_haystack):
        score += 8
    if "document" in query_terms and path_haystack.endswith("/dbo.document.md"):
        score += 12
    if any(term in query_terms for term in {"firm", "client", "kontrahent", "klient"}) and path_haystack.endswith("/dbo.firm.md"):
        score += 12
    if "userfirm" in query_terms and path_haystack.endswith("/dbo.userfirm.md"):
        score += 8
    if any(term in query_terms for term in {"documentstatus", "document_status", "status"}) and path_haystack.endswith("/dbo.documentstatus.md"):
        score += 12
    if _has_endpoint_intent(query_terms) and "/01_api_frontend/" in path_haystack:
        score += 5
    if _has_endpoint_intent(query_terms) and re.search(r"/(get|post|put|patch|delete)_", path_haystack):
        score += 8
    if "product" in query_terms and path_haystack.endswith("/product/get_product_getall.md"):
        score += 16
    if _has_pdf_intent(query_terms) and path_haystack.endswith("/document/post_document_generatepdf.md"):
        score += 16
    if _has_pdf_intent(query_terms) and path_haystack.endswith("/document/post_document_getpdfstream.md"):
        score += 16
    if _has_role_intent(query_terms) and "/06_role_i_uprawnienia/" in path_haystack:
        score += 14
    if _has_role_intent(query_terms) and path_haystack.endswith("/_mapowania/mapa_uprawnien_api.md"):
        score += 10
    if _has_calculation_intent(query_terms) and "/03_algorytmy/wyliczeniowe/" in path_haystack:
        score += 12
    if _has_calculation_intent(query_terms) and path_haystack.endswith("/obliczanie_ceny_pozycji.md"):
        score += 18
    if _has_calculation_intent(query_terms) and path_haystack.endswith("/aktualizacja_produktow_dokumentu.md"):
        score += 14
    if _has_calculation_intent(query_terms) and path_haystack.endswith("/obliczanie_wartosci_dokumentu.md"):
        score += 14
    if _has_calculation_intent(query_terms) and path_haystack.endswith("/dbo.documentproduct.md"):
        score += 8
    if _has_calculation_intent(query_terms) and path_haystack.endswith("/dbo.document.md"):
        score += 6
    return score


def _has_table_intent(query_terms: Sequence[str]) -> bool:
    return any(term in {"tabela", "tabele", "tabeli", "przechowuje", "sql", "select", "join", "column"} for term in query_terms)


def _has_endpoint_intent(query_terms: Sequence[str]) -> bool:
    return any(term in {"endpoint", "endpointu", "endpointy", "api"} for term in query_terms)


def _has_pdf_intent(query_terms: Sequence[str]) -> bool:
    return any(term in {"pdf", "generatepdf", "getpdfstream", "generowanie", "generowany"} for term in query_terms)


def _has_role_intent(query_terms: Sequence[str]) -> bool:
    return any(term in {"role", "rola", "uprawnienia", "uprawnien", "permissions", "authorize"} for term in query_terms)


def _has_calculation_intent(query_terms: Sequence[str]) -> bool:
    calculation_terms = {
        "kwota",
        "kwoty",
        "cena",
        "ceny",
        "suma",
        "sumy",
        "wartosc",
        "wartosci",
        "wyliczanie",
        "wyliczana",
        "obliczanie",
        "obliczana",
        "totalprice",
        "unitprice",
        "quantity",
        "vatrate",
        "calculation",
        "calculate",
    }
    return any(term in calculation_terms for term in query_terms)


def _lexical_snippet(text: str, query_terms: Sequence[str], max_chars: int = 1800) -> str:
    lowered = text.lower()
    first_match = min((lowered.find(term) for term in query_terms if lowered.find(term) >= 0), default=0)
    start = max(first_match - 300, 0)
    return text[start : start + max_chars]
