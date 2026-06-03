from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .profiles import PromptProfile
from .retrieval import SearchHit


NO_ANSWER = "Nie znalazłem tego w dokumentacji."


@dataclass(frozen=True)
class Citation:
    source_path: str
    source_group: str
    source_type: str
    heading_path: str
    distance: float
    area: str = ""
    entity: str = ""
    table: str = ""
    endpoint: str = ""


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
        source_type = str(hit.metadata.get("source_type", "-"))
        area = str(hit.metadata.get("area", ""))
        entity = str(hit.metadata.get("entity", ""))
        table = str(hit.metadata.get("table", ""))
        endpoint = str(hit.metadata.get("endpoint", ""))
        heading_path = str(hit.metadata.get("heading_path", hit.metadata.get("heading", "ROOT")))
        block = "\n".join(
            [
                f"[Kontekst {index}]",
                f"source_path: {source_path}",
                f"source_group: {source_group}",
                f"source_type: {source_type}",
                f"area: {area or '-'}",
                f"entity: {entity or '-'}",
                f"table: {table or '-'}",
                f"endpoint: {endpoint or '-'}",
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
                    source_type=source_type,
                    heading_path=heading_path,
                    distance=hit.distance,
                    area=area,
                    entity=entity,
                    table=table,
                    endpoint=endpoint,
                )
            )
            used_sources.add(citation_key)

    return PackedContext(text="\n\n".join(blocks), citations=citations)


def build_answer_prompt(
    question: str,
    context: PackedContext,
    warnings: List[str] | None = None,
    prompt_profile: PromptProfile | None = None,
) -> str:
    warning_text = "\n".join(f"- {warning}" for warning in (warnings or [])) or "Brak."
    if prompt_profile:
        system_prompt = prompt_profile.system_prompt
        rag_instruction = prompt_profile.rag_instruction
        answer_style = prompt_profile.answer_style
        source_policy = prompt_profile.source_policy
        profile_line = f"Prompt profile: {prompt_profile.key} v{prompt_profile.version}"
        profile_extra = _profile_extra_instruction(prompt_profile)
    else:
        system_prompt = "Jesteś Oracle InvoiceJet, lokalnym asystentem RAG dla dokumentacji InvoiceJet."
        rag_instruction = "Odpowiadasz zawsze po polsku, konkretnie i tylko na podstawie sekcji Kontekst."
        answer_style = "Odwołuj się do fragmentów jako `[Kontekst N]`, gdy podajesz ustalenia."
        source_policy = "Na końcu odpowiedzi dodaj sekcję `Źródła` z listą użytych `source_path`."
        profile_line = "Prompt profile: builtin"
        profile_extra = ""
    return (
        "/no_think\n"
        f"{system_prompt}\n"
        f"{rag_instruction}\n"
        "Jeśli Kontekst zawiera choć częściową odpowiedź, odpowiedz na podstawie tych fragmentów i wskaż ograniczenia.\n"
        f"Zwróć dokładnie `{NO_ANSWER}` tylko wtedy, gdy Kontekst jest pusty albo wszystkie fragmenty są nietrafione.\n"
        "Nie używaj wiedzy ogólnej do uzupełniania braków dokumentacji.\n"
        "Nie pokazuj procesu rozumowania ani sekcji thinking.\n"
        f"{profile_extra}"
        f"{answer_style}\n"
        f"{source_policy}\n"
        "Dla pytań przekrojowych łącz informacje z `source_type=screen`, `api`, `data_model`, `process`, `mapping` i `validation`, jeśli są w Kontekście.\n"
        "Jeśli ostrzeżenia wskazują konflikt źródeł, pokaż go użytkownikowi.\n\n"
        f"{profile_line}\n\n"
        f"Ostrzeżenia:\n{warning_text}\n\n"
        f"Pytanie:\n{question}\n\n"
        f"Kontekst:\n{context.text}\n"
    )


def _profile_extra_instruction(prompt_profile: PromptProfile) -> str:
    if prompt_profile.key != "database_sql_assistant":
        return ""
    return (
        "Tryb SQL: Kontekst opisuje schemat bazy, a nie konkretne rekordy danych. "
        "Wartosci filtrow podane w pytaniu uzytkownika sa parametrami zapytania i nie musza wystepowac w Kontekscie. "
        f"Nie zwracaj `{NO_ANSWER}` tylko dlatego, ze konkretna wartosc filtra, np. nazwa klienta, nie wystepuje w dokumentacji. "
        "Jesli Kontekst potwierdza tabele, kolumny i relacje potrzebne do SELECT, przygotuj SELECT oraz jawnie opisz zalozenia.\n"
    )


def build_citation_lines(citations: List[Citation]) -> List[str]:
    return [
        (
            f"{citation.source_path} | {citation.heading_path} | {citation.source_group} | "
            f"{citation.source_type} | entity={citation.entity or '-'} | table={citation.table or '-'} | "
            f"endpoint={citation.endpoint or '-'} | distance={citation.distance:.6f}"
        )
        for citation in citations
    ]
