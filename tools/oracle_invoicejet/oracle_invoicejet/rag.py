from __future__ import annotations

from dataclasses import dataclass
import re
from typing import List
import unicodedata

from .profiles import PromptProfile
from .retrieval import SearchHit


NO_ANSWER = "Nie znalazłem tego w dokumentacji."
NO_ANSWER_ASCII = "nie znalazlem tego w dokumentacji"

_THINK_BLOCK_RE = re.compile(r"<think\b[^>]*>.*?</think>", re.IGNORECASE | re.DOTALL)
_OPEN_THINK_BLOCK_RE = re.compile(r"<think\b[^>]*>.*$", re.IGNORECASE | re.DOTALL)
_NO_ANSWER_LINE_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:Nie znalazłem tego w dokumentacji\.?|Nie znalazlem tego w dokumentacji\.?)\s*$"
)


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


# ---------------------------------------------------------------------------
# RAG v2.0 — prompty dla lekkich agentów pomocniczych
# ---------------------------------------------------------------------------

def build_classifier_prompt(question: str) -> str:
    """Ultra-krótki prompt dla małego modelu (qwen2.5:1.5b). Klasyfikuje intencję pytania."""
    return (
        "/no_think\n"
        "Jesteś klasyfikatorem pytań InvoiceJet. Odpowiedz JEDNYM słowem z listy:\n"
        "user_help | technical | sql | algorithm | greeting | unknown\n"
        "user_help = funkcje aplikacji, jak wystawić/dodać/edytować\n"
        "technical = API, Angular, backend, architektura, endpointy\n"
        "sql = tabele, relacje, SELECT, model danych, baza\n"
        "algorithm = VAT, wyliczenia kwot, PDF, zaokrąglenia\n"
        "greeting = powitanie, kim jesteś, co umiesz\n"
        "unknown = niejasne lub niezwiązane z InvoiceJet\n"
        f"Pytanie: {question}\n"
        "Klasa:"
    )


def build_decomposer_prompt(question: str) -> str:
    """Prompt dla małego modelu. Rozbija złożone pytanie na pod-pytania."""
    return (
        "/no_think\n"
        "Czy pytanie zawiera wiele NIEZALEŻNYCH pytań? "
        "Jeśli TAK: rozłóż na max 3 osobne pytania, jedno na linię, bez numeracji. "
        "Jeśli NIE: zwróć oryginalne pytanie dokładnie bez zmian.\n"
        f"Pytanie: {question}\n"
        "Wynik:"
    )


def build_fact_check_prompt(answer: str, context_excerpt: str) -> str:
    """Ultra-krótki prompt dla małego modelu. Wykrywa potencjalne halucynacje."""
    return (
        "/no_think\n"
        "Przeczytaj KONTEKST i ODPOWIEDŹ. "
        "Czy odpowiedź zawiera fakty których NIE MA w kontekście? "
        "Odpowiedz TYLKO słowem TAK lub NIE.\n"
        f"KONTEKST:\n{context_excerpt}\n\n"
        f"ODPOWIEDŹ:\n{answer[:800]}\n\n"
        "Ocena (TAK lub NIE):"
    )


def source_path_to_portal_url(source_path: str, doc_user_base: str, doc_ai_base: str) -> str | None:
    """Convert an indexed documentation path to a full MkDocs portal URL."""
    normalized_path = source_path.replace("\\", "/").lstrip("/")
    for prefix, base in (
        ("InvoiceJet/doc_user/", doc_user_base),
        ("InvoiceJet/doc_AI/", doc_ai_base),
    ):
        if normalized_path.startswith(prefix):
            if not base:
                return None
            rel = normalized_path.removeprefix(prefix)
            if not rel or any(part in {".", ".."} for part in rel.split("/")):
                return None
            if rel == "README.md":
                rel = "index.html"
            elif rel.endswith("/README.md"):
                rel = rel.removesuffix("/README.md") + "/index.html"
            elif rel.endswith(".md"):
                rel = rel.removesuffix(".md") + ".html"
            return f"{base.rstrip('/')}/{rel}"
    return None


def build_answer_prompt(
    question: str,
    context: PackedContext,
    warnings: List[str] | None = None,
    prompt_profile: PromptProfile | None = None,
    portal_urls: dict[str, str] | None = None,
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
    if portal_urls:
        doc_user_base = portal_urls.get("doc_user", "")
        doc_ai_base   = portal_urls.get("doc_ai", "")
        portal_hint = (
            "Portale dokumentacji – gdy tworzysz link do dokumentu, użyj pełnego URL:\n"
            f"  doc_user: {doc_user_base}/[ścieżka].html  (usuń prefiks 'InvoiceJet/doc_user/')\n"
            f"  doc_ai:   {doc_ai_base}/[ścieżka].html  (usuń prefiks 'InvoiceJet/doc_AI/')\n"
            f"Przykład: InvoiceJet/doc_user/02_procesy/P-03_konfiguracja_firmy.md "
            f"→ {doc_user_base}/02_procesy/P-03_konfiguracja_firmy.html\n"
            "Nie używaj ścieżek .md ani ścieżek względnych (../) jako href w linkach.\n"
        )
    else:
        portal_hint = ""
    return (
        "/no_think\n"
        f"{system_prompt}\n"
        f"{rag_instruction}\n"
        "Jeśli Kontekst zawiera choć częściową odpowiedź, odpowiedz na podstawie tych fragmentów i wskaż ograniczenia.\n"
        f"Zwróć dokładnie `{NO_ANSWER}` tylko wtedy, gdy Kontekst jest pusty albo wszystkie fragmenty są nietrafione.\n"
        "Nie używaj wiedzy ogólnej do uzupełniania braków dokumentacji.\n"
        "Nie pokazuj procesu rozumowania ani sekcji thinking.\n"
        f"{profile_extra}"
        f"{portal_hint}"
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


def strip_thinking_sections(text: str) -> str:
    without_closed_blocks = _THINK_BLOCK_RE.sub("", text)
    return _OPEN_THINK_BLOCK_RE.sub("", without_closed_blocks)


def is_exact_no_answer(text: str) -> bool:
    return _fold_no_answer(text.strip().strip("` .")) == NO_ANSWER_ASCII


def has_mixed_no_answer(text: str) -> bool:
    folded = _fold_no_answer(text)
    return NO_ANSWER_ASCII in folded and not is_exact_no_answer(text)


def remove_no_answer_markers(text: str) -> str:
    return _NO_ANSWER_LINE_RE.sub("", text).strip()


def _fold_no_answer(text: str) -> str:
    translation = str.maketrans({"ł": "l", "Ł": "L"})
    normalized = unicodedata.normalize("NFKD", text.translate(translation))
    ascii_text = normalized.encode("ascii", errors="ignore").decode("ascii")
    return " ".join(ascii_text.lower().split())
