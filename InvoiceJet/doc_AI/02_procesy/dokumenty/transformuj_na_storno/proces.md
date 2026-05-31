# Transformuj dokumenty na storno — proces techniczny

| Pole | Wartość |
|---|---|
| ID dokumentu | PROC-TransformToStorno |
| Typ dokumentu | proces |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces masowo konwertuje istniejące dokumenty (faktury, proformy) na faktury storno przez zmianę `DocumentTypeId` na wartość `3` (`StornoInvoice`). Endpoint przyjmuje tablicę ID dokumentów. KRYTYCZNA ANOMALIA: `CompleteAsync()` (alias `SaveChangesAsync()`) wywołany jest **wewnątrz pętli** po każdym dokumencie — brak transakcji obejmującej całą operację. Jeśli błąd wystąpi w połowie listy, część dokumentów zostanie przekonwertowana, część nie.

## Cel procesu

Masowo anulować wystawione dokumenty poprzez zmianę ich typu na Faktura Storno, co powoduje że pojawiają się na liście faktur storno i mogą być wydrukowane z odpowiednim szablonem.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID procesu | PROC-TransformToStorno |
| Typ | główny |
| Inicjator | [Ekran listy faktur](../../../01_ekrany/faktury/lista_faktur/ekran.md) — zaznaczenie dokumentów + „Transform to Storno" (NIE z ekranu storn!) |
| Warunki startu | Użytkownik zalogowany (JWT); wybrane co najmniej jeden dokument do konwersji |
| Warunki zakończenia (sukces) | `DocumentTypeId` każdego dokumentu zmienione na `3`; HTTP 200 |
| Warunki zakończenia (błąd) | Dokument nie istnieje (błąd lub pominięcie); błąd częściowy (TS-01) |
| Uczestnicy | Frontend (Angular), API (DocumentController), Service (DocumentService), Repository (DocumentRepository), Database (dbo.Document) |

## Diagram sekwencji

```mermaid
sequenceDiagram
    participant F as Frontend (Lista faktur)
    participant A as DocumentController
    participant S as DocumentService
    participant UW as UnitOfWork
    participant R as DocumentRepository
    participant D as Database

    F->>A: PUT /api/Document/TransformToStorno [int[] documentIds]
    A->>S: TransformToStorno(documentIds)
    S->>S: Pobierz userId z JWT claims

    loop Dla każdego documentId
        S->>R: GetByIdAsync(documentId)
        R->>D: SELECT * FROM Document WHERE Id = documentId
        D-->>R: Document lub null

        alt Dokument nie istnieje
            R-->>S: null
            Note over S: pomiń lub błąd
        else Dokument istnieje
            R-->>S: document
            S->>S: document.DocumentTypeId = 3 (StornoInvoice)
            S->>R: UpdateAsync(document)
            Note over S,D: ⚠️ ANOMALIA TS-01 — CompleteAsync wewnątrz pętli (brak wspólnej transakcji)
            S->>UW: CompleteAsync()
            UW->>D: UPDATE Document SET DocumentTypeId = 3 WHERE Id = documentId
            D-->>UW: OK
            UW-->>S: OK
        end
    end

    S-->>A: void
    A-->>F: 200 OK
```

## Kroki

1. **Odbiór żądania** — `DocumentController` odbiera tablicę `int[] documentIds` z PUT `/api/Document/TransformToStorno`.
2. **Ekstrakcja userId** — serwis pobiera `userId` z claims JWT.
3. **Pętla po ID** — dla każdego `documentId`:
   a. `DocumentRepository.GetByIdAsync(documentId)` — pobranie dokumentu. Jeśli `null` — pominięcie lub błąd.
   b. `document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice` — wartość `3`.
   c. `DocumentRepository.UpdateAsync(document)`.
   d. `UnitOfWork.CompleteAsync()` — **zapis natychmiast po każdym dokumencie** (anomalia TS-01).
4. **Odpowiedź** — HTTP 200 OK po zakończeniu pętli.

## Obsługa błędów

| Błąd | Miejsce wystąpienia | Reakcja |
|---|---|---|
| Dokument nie istnieje | DocumentService | Pominięcie lub wyjątek (zależy od implementacji) |
| Błąd w połowie pętli | DocumentService | Część dokumentów przekonwertowana, część nie — brak rollback (anomalia TS-01) |
| Błąd deserializacji `int[]` | DocumentController | HTTP 400 Bad Request (anomalia TS-04) |
| Nieautoryzowany dostęp | AuthMiddleware | HTTP 401 Unauthorized |

## Powiązania

| Typ | Dokument |
|---|---|
| Inicjujący ekran | [Lista faktur (InvoicesComponent)](../../../01_ekrany/faktury/lista_faktur/ekran.md) |
| Wynikowy ekran | [Lista storn (InvoiceStornosComponent)](../../../01_ekrany/faktury_storno/lista_faktur_storno/ekran.md) |
| API | [PUT /api/Document/TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) |
| Algorytm | [ALG-08 TransformToStorno](../../../03_algorytmy/ALG-08_TransformToStorno.md) |
| Szablon PDF storno | [pdf/storno.md](../../../09_procesy_biznesowe/dokumenty/pdf/storno.md) |
| Model | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |

## Wątpliwości i braki

- **KRYTYCZNE (TS-01):** `CompleteAsync()` wewnątrz pętli — brak atomowości; możliwa częściowa konwersja jeśli błąd w trakcie. Rozwiązanie: przenieść `CompleteAsync()` poza pętlę lub owinąć całość transakcją.
- **TS-02:** Brak weryfikacji czy dokumenty należą do zalogowanego użytkownika (`GetByIdAsync` może nie filtrować po `UserFirmId`).
- **TS-03:** Brak zmiany numeru dokumentu po konwersji na storno — dokumenty zmieniają typ bez zmiany numeru (np. `FV0001` pozostaje zamiast `STORNO0001`).
- **TS-04:** Parametr `int[]` bez `[FromBody]` — potencjalny problem z deserializacją (patrz anomalia A-07).

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z P-15_TransformToStorno.md do nowego formatu. |
