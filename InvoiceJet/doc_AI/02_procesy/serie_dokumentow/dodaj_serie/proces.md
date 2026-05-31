# Dodaj serię dokumentów — proces techniczny

| Pole | Wartość |
|---|---|
| ID dokumentu | PROC-AddDocumentSeries |
| Typ dokumentu | proces |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces tworzy nową serię numeracji dokumentów i przypisuje ją do firmy użytkownika oraz wybranego typu dokumentu. Seria definiuje prefiks (`SeriesName`) i startowy numer (`CurrentNumber = 1`). Numer dokumentu generowany z serii ma format: `SeriesName + CurrentNumber.ToString("D4")`, np. `FV0001`.

## Cel procesu

Zdefiniować nową serię numeracji, której będzie można używać przy wystawianiu dokumentów danego typu.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID procesu | PROC-AddDocumentSeries |
| Typ | główny |
| Inicjator | Ekran „Serie dokumentów" + dialog „Dodaj serię" + operacja zapisu |
| Warunki startu | Użytkownik zalogowany (JWT); formularz serii wypełniony (prefiks + typ dokumentu) |
| Warunki zakończenia (sukces) | Rekord `DocumentSeries` zapisany w DB z `CurrentNumber = 1`; HTTP 201 |
| Warunki zakończenia (błąd) | Błąd DB (nieoczekiwany) |
| Uczestnicy | Frontend (Angular), API (DocumentSeriesController), Service (DocumentSeriesService), Repository (DocumentSeriesRepository), Database (dbo.DocumentSeries) |

## Diagram sekwencji

```mermaid
sequenceDiagram
    participant F as Frontend
    participant A as DocumentSeriesController
    participant S as DocumentSeriesService
    participant R as DocumentSeriesRepository
    participant D as Database

    F->>A: POST /api/DocumentSeries/Add (DocumentSeriesRequestDto)
    A->>S: Add(documentSeriesRequestDto)
    S->>S: Pobierz userId z JWT claims
    S->>R: GetUserFirmIdByUserId(userId)
    R->>D: SELECT UserFirmId FROM UserFirm WHERE UserId = @userId
    D-->>R: userFirmId
    R-->>S: userFirmId
    S->>S: Mapuj DTO → DocumentSeries; ustaw UserFirmId, CurrentNumber=1
    S->>R: AddAsync(documentSeries) + CompleteAsync()
    R->>D: INSERT INTO DocumentSeries (SeriesName, CurrentNumber, DocumentTypeId, UserFirmId)
    D-->>R: OK
    R-->>S: OK
    S-->>A: 201 Created
    A-->>F: 201 Created
```

## Kroki

1. **Odbiór żądania** — `DocumentSeriesController` odbiera `DocumentSeriesRequestDto` z POST `/api/DocumentSeries/Add`.
2. **Ekstrakcja userId** — serwis pobiera `userId` z claims JWT.
3. **Pobranie UserFirmId** — zapytanie przez repozytorium.
4. **Mapowanie i konfiguracja** — mapuje DTO → `DocumentSeries`; ustawia `UserFirmId`, `CurrentNumber = 1` (lub wartość z DTO).
5. **Zapis** — `DocumentSeriesRepository.AddAsync(documentSeries)` + `UnitOfWork.CompleteAsync()`.
6. **Odpowiedź** — HTTP 201 Created.

## Obsługa błędów

| Błąd | Miejsce wystąpienia | Reakcja |
|---|---|---|
| Nieautoryzowany dostęp | AuthMiddleware | HTTP 401 Unauthorized |
| Błąd DB (nieoczekiwany) | DocumentSeriesRepository | HTTP 500 Internal Server Error (ExceptionMiddleware) |

## Powiązania

- Wywołany z ekranu: [Serie dokumentów](../../../01_ekrany/serie_dokumentow/ekran.md)
- Powiązane API: [POST /api/DocumentSeries/Add](../../../04_api_i_integracje/01_api_frontend/document_series/POST_DocumentSeries_Add.md)
- Powiązany algorytm: [generowanie_numeru_dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md)

## Powiązania z kodem

- Kontroler: `InvoiceJetAPI/Controllers/DocumentSeriesController.cs`
- Serwis: `InvoiceJetAPI/Services/DocumentSeriesService.cs`
- Repozytorium: `InvoiceJetAPI/Repositories/DocumentSeriesRepository.cs`

## Wątpliwości i braki

- Brak walidacji unikalności prefiksu `SeriesName` per typ dokumentu per firma — możliwe zduplikowane serie.
- Niejasne czy `CurrentNumber` jest ustawiany po stronie backendu na 1, czy przesyłany z frontendu.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — wyodrębniona z P-07_ManageDocumentSeries.md (operacja Add). |
