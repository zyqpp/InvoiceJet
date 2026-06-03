# TransformToStorno — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `int[]` z body i wywołuje `_documentService.TransformToStorno(documentIds)`.
2. Serwis pobiera `userFirmId` (`GetUserFirmIdAsync`) → null → `throw new Exception("User firm not found.")` → **500** ⚠️.
3. Dla każdego `documentId` w `foreach`:
   a. Pobiera dokument z filtrem `Id == documentId && UserFirmId == activeUserFirmId` (ownership check ✅).
   b. Jeżeli null → `throw new Exception("Document not found.")` → **500** ⚠️ — przerywa pętlę.
   c. Ustawia `DocumentTypeId = 3` (StornoInvoice).
   d. `UpdateAsync(document)` + `CompleteAsync()` — zapis w każdej iteracji.
4. Kontroler zwraca `200 OK` (puste body).

---

## 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.TransformToStorno`

```csharp
[HttpPut("TransformToStorno")]
public async Task<IActionResult> TransformToStorno([FromBody] int[] documentIds)
{
    await _documentService.TransformToStorno(documentIds);
    return Ok();
}
```

---

## 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma firmę | `DocumentService.cs › DocumentService.TransformToStorno` | `throw new Exception("User firm not found.")` → **500** ⚠️ |
| 2 | Dokument istnieje i należy do firmy (per iteracja) | `DocumentService.cs › DocumentService.TransformToStorno` | `throw new Exception("Document not found.")` → **500** ⚠️ |

```csharp
var activeUserFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
if (activeUserFirmId == null)
    throw new Exception("User firm not found.");
```

```csharp
if (document == null)
    throw new Exception("Document not found.");
```

> WAL-01 i WAL-02 używają `new Exception(...)` (nie domenowe wyjątki) → trafiają do catch-all ExceptionMiddleware → **500 Internal Server Error** — niespójne z resztą API.

---

## 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`

```csharp
public async Task TransformToStorno(int[] documentIds)
{
    var activeUserFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
    if (activeUserFirmId == null)
        throw new Exception("User firm not found.");

    foreach (var documentId in documentIds)
    {
        var document = await _unitOfWork.Documents.Query()
            .Where(d => d.Id == documentId && d.UserFirmId == activeUserFirmId)
            .FirstOrDefaultAsync();

        if (document == null)
            throw new Exception("Document not found.");

        document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice;
        await _unitOfWork.Documents.UpdateAsync(document);
        await _unitOfWork.CompleteAsync();
    }
}
```

**Krok 1 — Ownership check:**
- `Where(d => d.Id == documentId && d.UserFirmId == activeUserFirmId)` — filtr zabezpiecza przed modyfikacją cudzych dokumentów. ✅

**Krok 2 — Zmiana typu:**
- `document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice` = `3`.
- Zmieniana jest wyłącznie kolumna `DocumentTypeId`. Wszystkie inne pola dokumentu pozostają bez zmian.

**Krok 3 — Zapis per iteracja:**
- `UpdateAsync(document)` — oznacza encję jako `Modified` w kontekście EF.
- `CompleteAsync()` = `SaveChangesAsync()` wewnątrz pętli — każdy dokument zapisywany osobno.

### Tabela: pole encji → źródło

| Pole encji `Document` | Źródło |
|---|---|
| `DocumentTypeId` | `(int)DocumentTypeEnum.StornoInvoice` = `3` (stała) |
| (pozostałe pola) | bez zmian |

---

## 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | CompleteAsync |
|---|---|---|---|
| Per każdy documentId | `UpdateAsync(document)` | `DocumentRepository` | tak — wewnątrz pętli |

> [UWAGA: `CompleteAsync()` wywoływane wewnątrz `foreach`. Przy N dokumentach wykonywane jest N transakcji. Jeżeli 3. dokument z 5 nie zostanie znaleziony (`Exception("Document not found.")`), 2 pierwsze dokumenty **są już zapisane** jako Storno — częściowe wykonanie operacji. Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 5. Odpowiedź

HTTP `200 OK`. Puste body (`return Ok()`).

---

## 6. Uwagi techniczne

- [UWAGA: WAL-01 rzuca `new Exception("User firm not found.")` zamiast domenowego `UserHasNoAssociatedFirmException`. Niemapowany wyjątek → catch-all ExceptionMiddleware → **500 Internal Server Error** zamiast `400`. Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: WAL-02 rzuca `new Exception("Document not found.")` → **500** zamiast `404`. Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `CompleteAsync()` wewnątrz pętli — operacja nie atomowa. Częściowe storno przy błędzie w środku listy. Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `GetUserFirmIdAsync` (zwraca `int?`) użyte zamiast `GetUserFirmAsync` (zwraca encję). Niespójność z innymi metodami serwisu. — UWAGA informacyjna]
