# Proces biznesowy: Wystawienie storno

| Pole | Wartość |
|---|---|
| ID dokumentu | BPMN-DOC-03 |
| Typ dokumentu | proces biznesowy |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces konwersji istniejących dokumentów (faktur lub proform) na faktury storno (DocumentTypeId = 3). Użytkownik zaznacza dokumenty na liście faktur storno i klika "Transformuj na storno". Backend zmienia `DocumentTypeId` na `3` dla każdego dokumentu z listy. KRYTYCZNA ANOMALIA: zapis (`CompleteAsync`) następuje wewnątrz pętli — brak transakcji obejmującej całą operację, możliwa częściowa konwersja przy błędzie.

## Uczestnicy

| Uczestnik | Rola |
|---|---|
| Użytkownik | Inicjator akcji (wybiera dokumenty do konwersji) |
| Frontend (Angular) | Warstwa prezentacji — lista faktur storno z checkboxami |
| Backend (API) | Logika biznesowa — zmiana TypeId w pętli, brak transakcji |
| SQL Server | Trwałe przechowywanie danych dokumentów |

## Diagram procesu (Mermaid sequenceDiagram)

```mermaid
sequenceDiagram
    participant U as Użytkownik
    participant FE as Frontend (Angular)
    participant BE as Backend (API)
    participant DB as SQL Server

    U->>FE: Otwiera listę faktur storno (/dashboard/storno-invoices)
    FE->>BE: GET /api/Document/GetUserDocumentsByType/3
    BE->>DB: SELECT Documents WHERE TypeId=3 AND UserFirmId=@id
    DB-->>BE: Lista dokumentów storno
    BE-->>FE: DocumentDto[]
    FE-->>U: Lista z checkboxami

    U->>FE: Zaznacza dokumenty (faktury / proformy) do konwersji
    U->>FE: Klik "Transformuj na storno"

    FE->>BE: PUT /api/Document/TransformToStorno (int[] documentIds)
    BE->>BE: Pobierz userId z JWT claims

    loop Dla każdego documentId
        BE->>DB: SELECT Document WHERE Id = @documentId
        DB-->>BE: Document lub null
        alt Dokument istnieje
            BE->>BE: document.DocumentTypeId = 3 (StornoInvoice)
            BE->>DB: UPDATE Document SET DocumentTypeId = 3 WHERE Id = @id
            Note over BE,DB: UWAGA: COMMIT po każdym dokumencie (brak transakcji całości)
            DB-->>BE: OK
        else Dokument nie istnieje
            BE->>BE: Pomiń lub błąd (nieokreślone zachowanie)
        end
    end

    BE-->>FE: 200 OK
    FE->>BE: GET /api/Document/GetUserDocumentsByType/3
    BE-->>FE: Zaktualizowana lista storno
    FE-->>U: Lista z nowo przekonwertowanymi dokumentami

    opt Generowanie PDF storno
        U->>FE: Klik "PDF" przy dokumencie storno
        FE->>BE: POST /api/Document/GetPdfStream (DocumentRequestDto)
        BE->>DB: SELECT Document z JOINami (TypeId=3)
        DB-->>BE: Document data
        BE->>BE: InvoiceDocumentFactory.Create(3) → StornoDocument
        BE->>BE: QuestPDF GeneratePdf() → MemoryStream
        BE-->>FE: FileStreamResult (application/pdf)
        FE-->>U: PDF storno otwarty w przeglądarce
    end
```

## Kroki procesu

| # | Krok | Uczestnik | Opis |
|---|---|---|---|
| 1 | Otwarcie listy storno | Użytkownik / Frontend | Nawigacja do `/dashboard/storno-invoices`; GET GetUserDocumentsByType/3. |
| 2 | Zaznaczenie dokumentów | Użytkownik | Checkboxy przy dokumentach przeznaczonych do konwersji. |
| 3 | Inicjacja konwersji | Użytkownik | Klik "Transformuj na storno". |
| 4 | Wysłanie żądania | Frontend | PUT `/api/Document/TransformToStorno` z tablicą int[]. |
| 5 | Ekstrakcja userId | Backend | Pobierz userId z claims JWT. |
| 6 | Pętla konwersji | Backend | Dla każdego ID: SELECT → zmień TypeId=3 → UPDATE → COMMIT (osobno per dokument). |
| 7 | Odpowiedź | Backend / Frontend | HTTP 200; frontend odświeża listę storno. |
| 8 | Generowanie PDF (opcja) | Użytkownik / Frontend / Backend | POST GetPdfStream → Factory.Create(3) → StornoDocument → QuestPDF. |

## Obsługa wyjątków

| Sytuacja | Reakcja systemu |
|---|---|
| Dokument nie istnieje w DB | Pominięcie lub błąd (zachowanie nieokreślone w dokumentacji). |
| Błąd w trakcie pętli (anomalia TS-01) | Część dokumentów przekonwertowana, część nie — brak rollback. |
| Nieprawidłowy format `int[]` (anomalia TS-04) | Potencjalny HTTP 400 Bad Request (brak `[FromBody]`). |
| Brak autoryzacji | JwtInterceptor 401 → TokenExpiredDialog → /login. |
| Błąd DB | Backend 500; ExceptionMiddleware. |

## Powiązane procesy techniczne

| Proces | Link |
|---|---|
| Transformuj na storno (techniczny) | `../../02_procesy/dokumenty/transformuj_na_storno/proces.md` |
| Eksport PDF (BPMN) | `eksport_pdf.md` |
| Wystawienie faktury (BPMN) | `wystawienie_faktury.md` |

## Wątpliwości i braki

- **KRYTYCZNE (TS-01):** Brak transakcji obejmującej całą pętlę — możliwa częściowa konwersja bez możliwości cofnięcia.
- **TS-02:** Brak weryfikacji właściciela dokumentu — `GetByIdAsync` może nie filtrować po `UserFirmId`.
- **TS-03:** Numer dokumentu nie zmienia się po konwersji (`FV0001` pozostaje zamiast `STORNO0001`).
- **TS-04:** Parametr `int[]` bez jawnego `[FromBody]` — potencjalny problem z deserializacją.
- Konwersja jest nieodwracalna — brak endpointu "cofnij storno".

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — na podstawie PROC-TransformToStorno z nowym ID i formatem biznesowym. |
