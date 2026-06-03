from __future__ import annotations

import json
import time
from typing import Any, Iterator

import chromadb
import requests

from chroma_md_poc.config import load_config


OLLAMA_BASE_URL = "http://127.0.0.1:11434"
NO_CONTEXT_ANSWER = "Brak informacji w dokumentacji."

QueryRow = tuple[str, str, dict[str, Any], float]
RagEvent = dict[str, Any]


def query_rows(question: str, top_k: int, source_contains: str) -> list[QueryRow]:
    config = load_config()
    client = chromadb.PersistentClient(path=str(config.chroma_path))
    collection = client.get_collection(name=config.collection_name)

    query_limit = max(top_k * 5, top_k) if source_contains else top_k
    result = collection.query(query_texts=[question], n_results=query_limit)
    rows = list(
        zip(
            result.get("ids", [[]])[0],
            result.get("documents", [[]])[0],
            result.get("metadatas", [[]])[0],
            result.get("distances", [[]])[0],
        )
    )
    if source_contains:
        rows = [row for row in rows if row[2] and source_contains in str(row[2].get("source_path", ""))]
    return rows[:top_k]


def build_rag_prompt(question: str, rows: list[QueryRow]) -> str:
    context_blocks: list[str] = []
    for index, (_doc_id, document, metadata, _distance) in enumerate(rows, start=1):
        source_path = metadata.get("source_path", "-") if metadata else "-"
        heading = metadata.get("heading", "ROOT") if metadata else "ROOT"
        context_blocks.append(
            "\n".join(
                [
                    f"[Kontekst {index}]",
                    f"source_path: {source_path}",
                    f"heading: {heading}",
                    "tresc:",
                    document or "",
                ]
            )
        )

    context_text = "\n\n".join(context_blocks)
    return (
        "Jestes asystentem technicznym pracujacym na dokumentacji projektu InvoiceJet.\n"
        "Odpowiadaj po polsku. Odpowiedz ma byc konkretna i oparta wylacznie na kontekscie.\n"
        "Jesli nie ma danych w kontekscie, napisz jasno: 'Brak informacji w dokumentacji'.\n"
        "Na koncu podaj sekcje Zrodla z lista source_path.\n\n"
        f"Pytanie uzytkownika:\n{question}\n\n"
        f"Kontekst:\n{context_text}\n"
    )


def stream_rag_answer(
    question: str,
    model_name: str,
    top_k: int,
    source_contains: str,
    temperature: float,
    num_ctx: int,
    max_tokens: int,
    timeout_sec: int,
) -> Iterator[RagEvent]:
    total_start = time.perf_counter()
    stats = _empty_stats()
    final_event: dict[str, Any] = {}

    try:
        yield _event(
            "phase_started",
            phase="retrieval",
            message="1/3: Wyszukiwanie kontekstu w Chroma...",
        )
        retrieval_start = time.perf_counter()
        rows = query_rows(question=question.strip(), top_k=int(top_k), source_contains=source_contains.strip())
        stats["retrieval_sec"] = time.perf_counter() - retrieval_start
        yield _event(
            "phase_completed",
            phase="retrieval",
            message=f"Znaleziono {len(rows)} fragmentow kontekstu w {stats['retrieval_sec']:.2f}s.",
            stats={"retrieval_sec": stats["retrieval_sec"]},
        )

        if not rows:
            stats["total_sec"] = time.perf_counter() - total_start
            yield _event(
                "completed",
                answer=NO_CONTEXT_ANSWER,
                sources=[],
                stats=stats.copy(),
            )
            return

        yield _event(
            "phase_started",
            phase="prompt_build",
            message="2/3: Budowanie promptu RAG...",
        )
        prompt = build_rag_prompt(question=question, rows=rows)
        yield _event(
            "phase_completed",
            phase="prompt_build",
            message="Prompt RAG jest gotowy.",
        )

        yield _event(
            "phase_started",
            phase="generation",
            message="3/3: Generowanie odpowiedzi przez model lokalny...",
        )
        generation_start = time.perf_counter()
        chunks: list[str] = []
        first_token_seen = False
        for final_event in _iter_ollama_generate_events(
            model_name=model_name,
            prompt=prompt,
            temperature=float(temperature),
            num_ctx=int(num_ctx),
            max_tokens=int(max_tokens),
            timeout_sec=int(timeout_sec),
        ):
            piece = str(final_event.get("response", ""))
            if piece:
                if not first_token_seen:
                    stats["time_to_first_token_sec"] = time.perf_counter() - total_start
                    first_token_seen = True
                chunks.append(piece)
                yield _event("token", delta=piece, accumulated_text="".join(chunks))

            if bool(final_event.get("done", False)):
                break

        stats["generation_sec"] = time.perf_counter() - generation_start
        stats["prompt_eval_count"] = int(final_event.get("prompt_eval_count", 0) or 0)
        stats["eval_count"] = int(final_event.get("eval_count", 0) or 0)
        stats["eval_duration_ns"] = int(final_event.get("eval_duration", 0) or 0)
        stats["total_sec"] = time.perf_counter() - total_start
        answer = "".join(chunks).strip()
        sources = _dedupe_sources(rows)

        yield _event(
            "phase_completed",
            phase="generation",
            message=f"Zakonczono generowanie odpowiedzi w {stats['generation_sec']:.2f}s.",
            stats={"generation_sec": stats["generation_sec"]},
        )
        yield _event(
            "completed",
            answer=answer,
            sources=sources,
            stats=stats.copy(),
        )

    except Exception as exc:  # noqa: BLE001
        stats["total_sec"] = time.perf_counter() - total_start
        yield _event(
            "error",
            message="Blad agenta podczas przetwarzania zapytania.",
            technical_details=str(exc),
        )


def _iter_ollama_generate_events(
    model_name: str,
    prompt: str,
    temperature: float,
    num_ctx: int,
    max_tokens: int,
    timeout_sec: int,
) -> Iterator[dict[str, Any]]:
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_ctx": num_ctx,
            "num_predict": max_tokens,
        },
    }

    with requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        stream=True,
        timeout=(10, timeout_sec),
    ) as response:
        response.raise_for_status()

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            if isinstance(line, bytes):
                line = line.decode("utf-8", errors="replace")
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            yield event


def _empty_stats() -> dict[str, float | int]:
    return {
        "retrieval_sec": 0.0,
        "generation_sec": 0.0,
        "total_sec": 0.0,
        "time_to_first_token_sec": 0.0,
        "prompt_eval_count": 0,
        "eval_count": 0,
        "eval_duration_ns": 0,
    }


def _dedupe_sources(rows: list[QueryRow]) -> list[str]:
    sources: list[str] = []
    seen: set[str] = set()
    for _doc_id, _document, metadata, _distance in rows:
        if not metadata:
            continue
        source = str(metadata.get("source_path", "")).strip()
        if source and source not in seen:
            seen.add(source)
            sources.append(source)
    return sources


def _event(event_type: str, **payload: Any) -> RagEvent:
    return {"type": event_type, **payload}
