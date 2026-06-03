# PUT /api/Document/EditDocument — Edycja dokumentu

| Atrybut | Wartość |
|---|---|
| ID | API-23 |
| Metoda | PUT |
| URL | `/api/Document/EditDocument` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.EditDocument` |
| Serwis | `IDocumentService.EditDocument` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `DocumentRequestDto` z `id > 0`

Takie same pola jak w `POST_Document_Add.md`. Musi zawierać `id` istniejącego dokumentu.

## Response

### 200 OK — zwraca wejściowy `DocumentRequestDto`

### Błędy

| Status HTTP | Warunek |
|---|---|
| 400 Bad Request | `UserHasNoAssociatedFirmException` |
| 500 | `Exception("Document not found.")` — plain wyjątek, nie domenowy |
| 500 | `Exception("Product not found.")` |

## Algorytm

1. Pobierz `userFirmId` z JWT
2. Pobierz dokument po `id` → plain Exception jeśli nie znaleziony
3. Zaktualizuj: `IssueDate`, `DueDate`, `DocumentTypeId`, `DocumentStatusId`, `ClientId`, `UserFirmId`
4. `UpdateDocumentProducts()`: usuń wszystkie poprzednie pozycje, dodaj nowe
5. `CompleteAsync()`

**Uwaga:** Edycja nie zmienia numeru dokumentu ani serii.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
