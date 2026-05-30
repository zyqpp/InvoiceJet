<!--
SZABLON 00 — METADANE (wizytówka procesu)
Wypełnij na podstawie kodu. Zastąp [...] wartościami. Usuń sekcje "Przykład" przed oddaniem.
Definicja ukończenia: patrz docs/BackendAgentAI/03_MARKERY_I_WERYFIKACJA.md → sekcja 3.
-->

# [NAZWA PROCESU] — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `[Nazwa zdolności biznesowej]` |
| Numer procesu | `P-XX` |
| Kontroler(y) | `[Controller]` |
| Serwis(y) aplikacyjny | `[Service]` |
| Metoda(y) serwisu | `[Service.Method]` |
| DTO żądania | `[Dto]` / N/D |
| DTO odpowiedzi | `[Dto]` / N/D |
| Encje | `[Entity, ...]` |
| Repozytoria | `[IRepository, ...]` |
| Wyjątki | `[Exception, ...]` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | `[ANAF / QuestPDF / brak]` |
| Autoryzacja | `[Authorize(Roles = "...")]` / N/D |
| Status dokumentu | Roboczy |
| Data utworzenia | RRRR-MM-DD |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu
<!-- Wymień KAŻDY endpoint należący do procesu (zasada dekompozycji: 04_REGULY_DEKOMPOZYCJI.md). -->

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-XX` | `[HTTP] /api/[Controller]/[Action]` | `[Controller].[Method]` | [krótko] |

## Komponenty (kotwice)
<!-- Plik.cs › Klasa.Metoda dla każdego kluczowego komponentu. To punkty wejścia do dalszych plików. -->

| Rola | Kotwica |
|---|---|
| Kontroler | `[Controller].cs › [Controller].[Method]` |
| Serwis | `[Service].cs › [Service].[Method]` |
| Repozytorium | `[Repository].cs › [...]` |

---
<!-- ===== PRZYKŁAD WYPEŁNIENIA (usuń przed oddaniem) — proces P-01 =====

| Atrybut | Wartość |
|---|---|
| Proces | `Wystawienie nowej faktury` |
| Numer procesu | `P-01` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.AddDocument`, `UpdateDocumentProducts`, `IncreaseDocumentSeriesNumber` |
| Encje | `Document`, `DocumentProduct`, `Product`, `DocumentSeries`, `BankAccount` |
| Wyjątki | `UserHasNoAssociatedFirmException`, `NoBankAccountAddedException` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

Endpointy:
| `API-02` | `POST /api/Document/AddDocument` | `DocumentController.AddDocument` | Zapis nowej faktury |
===== KONIEC PRZYKŁADU ===== -->
