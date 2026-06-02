# Dodaj dokument — proces techniczny

| Pole | Wartość |
|---|---|
| ID dokumentu | PROC-AddDocument |
| Typ dokumentu | proces |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces wystawia nowy dokument (faktura, proforma lub faktura storno) w imieniu zalogowanego użytkownika. Jeden endpoint obsługuje wszystkie trzy typy dokumentów przez parametr `DocumentTypeId`. Backend pobiera serię numeracyjną, generuje numer dokumentu, zapisuje pozycje (`DocumentProduct`), oblicza sumy i inkrementuje licznik serii. Operacja składa się z dwóch osobnych `CompleteAsync()` — brak atomowości.

## Cel procesu

Stworzyć i zapisać nowy dokument handlowy z przypisanym numerem, danymi kontrahenta, pozycjami i sumami, gotowy do wydruku i wysyłki.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID procesu | PROC-AddDocument |
| Typ | główny |
| Inicjator | Ekran dodaj/edytuj fakturę (lub proformę/storno) + operacja „Zapisz" |
| Warunki startu | Użytkownik zalogowany (JWT); formularz dokumentu wypełniony z wybraną serią, klientem, kontem bankowym i co najmniej jedną pozycją |
| Warunki zakończenia (sukces) | Rekord `Document` + `DocumentProduct[]` zapisane; `DocumentSeries.CurrentNumber` zinkrementowany; HTTP 201 |
| Warunki zakończenia (błąd) | Seria dokumentów nie istnieje (404) |
| Uczestnicy | Frontend (Angular), API (DocumentController), Service (DocumentService), Repository (DocumentSeriesRepository, DocumentRepository), Database (dbo.Document, dbo.DocumentProduct, dbo.DocumentSeries) |

## Diagram sekwencji

→ Przeniesiony do: [BP-DOC-01 Wystawienie faktury zwykłej](../../../09_procesy_biznesowe/dokumenty/BP-DOC-01_wystawienie_faktury.md#diagram-sekwencji)

## Kroki

1. **Odbiór żądania** — `DocumentController` odbiera `DocumentRequestDto` z POST `/api/Document/Add`.
2. **Ekstrakcja userId** — serwis pobiera `userId` z claims JWT.
3. **Pobranie UserFirmId** — zapytanie przez repozytorium.
4. **Walidacja serii** — `DocumentSeriesRepository.GetByIdAsync(documentSeries.Id)`. Jeśli `null` → `DocumentSeriesNotFoundException` (HTTP 404).
5. **Generowanie numeru** — `DocumentNumber = SeriesName + CurrentNumber.ToString("D4")`.
6. **Mapowanie** — `AutoMapper` mapuje `DocumentRequestDto` → `Document`.
7. **Ustawienie pól systemowych** — `UserFirmId`, `DocumentNumber`, `DocumentStatusId`, `IssueDate`.
8. **Dodanie pozycji** — `DocumentProduct[]` z DTO dodane do encji dokumentu.
9. **Obliczenie TotalPrice** — suma `Price * Quantity * (1 + VatRate/100)` dla każdej pozycji.
10. **Zapis dokumentu** — `DocumentRepository.AddAsync(document)` + `UnitOfWork.CompleteAsync()` (ZAPIS #1).
11. **Inkrementacja serii** — `documentSeries.CurrentNumber++` + `UnitOfWork.CompleteAsync()` (ZAPIS #2 — osobny, brak atomowości z krokiem 10).
12. **Odpowiedź** — HTTP 201 Created.

## Obsługa błędów

| Błąd | Miejsce wystąpienia | Reakcja |
|---|---|---|
| `DocumentSeriesNotFoundException` | DocumentService | HTTP 404 Not Found — seria nie istnieje |
| Race condition (duplikat numeru) | DocumentService | Brak obsługi — anomalia AD-01 |
| Nieautoryzowany dostęp | AuthMiddleware | HTTP 401 Unauthorized |
| Błąd DB po ZAPIS #1 przed ZAPIS #2 | Database | Dokument zapisany, licznik nie zinkrementowany — niespójność (anomalia AD-03) |

## Powiązania

- Wywołany z ekranu: [Dodaj/edytuj fakturę](../../../01_ekrany/faktury/dodaj_edytuj_fakture/ekran.md), [Dodaj/edytuj proformę](../../../01_ekrany/faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md), [Dodaj/edytuj storno](../../../01_ekrany/faktury_storno/dodaj_edytuj_fakture_storno/ekran.md)
- Powiązane API: [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md)
- Powiązany algorytm: [generowanie_numeru_dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md), [obliczanie_wartosci_dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md)
- Powiązane algorytmy (uzupełnienie): [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/ALG-02_DocumentNumberGeneration.md), [Obliczanie ceny pozycji (frontend)](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md), [UpdateDocumentProducts](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md)

## Powiązania z kodem

- Kontroler: `InvoiceJetAPI/Controllers/DocumentController.cs`
- Serwis: `InvoiceJetAPI/Services/DocumentService.cs`
- Repozytorium: `InvoiceJetAPI/Repositories/DocumentRepository.cs`, `InvoiceJetAPI/Repositories/DocumentSeriesRepository.cs`

## Wątpliwości i braki

- **Race condition (AD-01):** Brak lock/transakcji przy inkrementacji `CurrentNumber` — możliwe duplikaty numerów przy równoległych żądaniach.
- **Brak walidacji właściciela serii (AD-02):** Seria przekazywana z frontendu jako obiekt — backend nie weryfikuje czy należy do zalogowanego użytkownika.
- **Brak atomowości (AD-03):** Dwa osobne `CompleteAsync()` — jeśli drugi zawiedzie, dokument jest zapisany ale licznik nie zinkrementowany.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z P-08_AddDocument.md do nowego formatu. |
