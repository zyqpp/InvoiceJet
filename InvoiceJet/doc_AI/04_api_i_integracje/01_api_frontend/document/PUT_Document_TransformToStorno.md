# PUT /api/Document/TransformToStorno — Przekształcenie w storno

| Atrybut | Wartość |
|---|---|
| ID | API-31 |
| Metoda | PUT |
| URL | `/api/Document/TransformToStorno` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.TransformToStorno` |
| Serwis | `IDocumentService.TransformToStorno` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `[FromBody] int[]`

```json
[1, 2]
```

Tablica ID faktur do przekształcenia w storno.

## Response

### 200 OK — pusta odpowiedź

### Błędy

| Status HTTP | Warunek |
|---|---|
| 500 | `Exception("User firm not found.")` — brak aktywnej firmy |
| 500 | `Exception("Document not found.")` — dokument nie znaleziony lub nie należy do firmy |

## Algorytm

```csharp
var activeUserFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(userId);

foreach (var documentId in documentIds)
{
    var document = await ... .Where(d => d.Id == documentId && d.UserFirmId == activeUserFirmId)
                             .FirstOrDefaultAsync();
    if (document == null) throw new Exception("Document not found.");

    document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice; // = 3
    await _unitOfWork.Documents.UpdateAsync(document);
    await _unitOfWork.CompleteAsync(); // ← SaveChanges WEWNĄTRZ pętli!
}
```

**Anomalia:** `CompleteAsync()` wewnątrz pętli — każdy dokument w oddzielnej transakcji. Przy błędzie N-tego dokumentu, dokumenty 1..N-1 są już przetransformowane (brak rollback).

## Zachowanie po stronie frontendu

`InvoicesComponent.transformToStorno()` — przekształca zaznaczone faktury. Brak możliwości tworzenia storno z poziomu `InvoiceStornosComponent` (tylko edycja).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny z anomalią. |
