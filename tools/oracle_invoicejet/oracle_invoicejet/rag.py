from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .retrieval import SearchHit


NO_ANSWER = "Nie znalazłem tego w dokumentacji."


@dataclass(frozen=True)
class Citation:
    source_path: str
    source_group: str
    heading_path: str
    distance: float


@dataclass(frozen=True)
class PackedContext:
    text: str
    citations: List[Citation]


def pack_context(hits: List[SearchHit], max_chars: int = 18000) -> PackedContext:
    blocks: List[str] = []
    citations: List[Citation] = []
    used_sources: set[tuple[str, str]] = set()
    current_size = 0

    for index, hit in enumerate(hits, start=1):
        source_path = hit.source_path
        source_group = str(hit.metadata.get("source_group", "-"))
        heading_path = str(hit.metadata.get("heading_path", hit.metadata.get("heading", "ROOT")))
        block = "\n".join(
            [
                f"[Kontekst {index}]",
                f"source_path: {source_path}",
                f"source_group: {source_group}",
                f"heading_path: {heading_path}",
                "treść:",
                hit.text.strip(),
            ]
        )
        if current_size + len(block) > max_chars and blocks:
            break
        blocks.append(block)
        current_size += len(block)
        citation_key = (source_path, heading_path)
        if citation_key not in used_sources:
            citations.append(
                Citation(
                    source_path=source_path,
                    source_group=source_group,
                    heading_path=heading_path,
                    distance=hit.distance,
                )
            )
            used_sources.add(citation_key)

    return PackedContext(text="\n\n".join(blocks), citations=citations)


def build_answer_prompt(question: str, context: PackedContext, warnings: List[str] | None = None) -> str:
    warning_text = "\n".join(f"- {warning}" for warning in (warnings or [])) or "Brak."
    return (
        "/no_think\n"
        "Jesteś Oracle InvoiceJet, lokalnym asystentem RAG dla dokumentacji InvoiceJet.\n"
        "Odpowiadasz zawsze po polsku, konkretnie i tylko na podstawie sekcji Kontekst.\n"
        "Jeśli Kontekst zawiera choć częściową odpowiedź, odpowiedz na podstawie tych fragmentów i wskaż ograniczenia.\n"
        f"Zwróć dokładnie `{NO_ANSWER}` tylko wtedy, gdy Kontekst jest pusty albo wszystkie fragmenty są nietrafione.\n"
        "Nie używaj wiedzy ogólnej do uzupełniania braków dokumentacji.\n"
        "Nie pokazuj procesu rozumowania ani sekcji thinking.\n"
        "Odwołuj się do fragmentów jako `[Kontekst N]`, gdy podajesz ustalenia.\n"
        "Na końcu odpowiedzi dodaj sekcję `Źródła` z listą użytych `source_path`.\n"
        "Jeśli ostrzeżenia wskazują konflikt źródeł, pokaż go użytkownikowi.\n\n"
        f"Ostrzeżenia:\n{warning_text}\n\n"
        f"Pytanie:\n{question}\n\n"
        f"Kontekst:\n{context.text}\n"
    )


def build_citation_lines(citations: List[Citation]) -> List[str]:
    return [
        f"{citation.source_path} | {citation.heading_path} | {citation.source_group} | distance={citation.distance:.6f}"
        for citation in citations
    ]
