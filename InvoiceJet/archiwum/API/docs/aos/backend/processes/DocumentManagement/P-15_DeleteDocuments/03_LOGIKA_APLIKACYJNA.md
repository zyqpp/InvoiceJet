# DeleteDocuments — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera tablicę `int[]` z body i wywołuje `_documentService.DeleteDocuments(documentIds)`.
2. Serwis pobiera dokumenty z Include `DocumentProducts` filtrując po `documentIds.Contains(d.Id)`.
3. Usuwa pozycje dokumentów (`RemoveRangeAsync`) — operacja EF, brak natychmiastowego zapisu.
4. Usuwa dokumenty (`RemoveRangeAsync`) — operacja EF, brak natychmiastowego zapisu.
5. `CompleteAsync()` — jeden `SaveChangesAsync()` dla obu operacji.
6. Kontroler zwraca `200 OK` z `{ "message": "Documents deleted successfully." }`.

---

## 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.DeleteDocuments`

```csharp
[HttpPut("DeleteDocuments")]
public async Task<IActionResult> DeleteDocuments([FromBody] int[] documentIds)
{
    await _documentService.DeleteDocuments(documentIds);
    return Ok(new { Message = "Documents deleted successfully." });
}
```

---

## 2. Walidacje (faza wejściowa)

Brak walidacji. Serwis nie sprawdza:
- czy `documentIds` jest pusty,
- czy dokumenty należą do aktywnej firmy zalogowanego użytkownika,
- czy dokumenty w ogóle istnieją.

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| — | Brak walidacji | — | — |

---

## 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.DeleteDocuments`

```csharp
public async Task DeleteDocuments(int[] documentIds)
{
    var documents = await _unitOfWork.Documents.Query()
        .Include(dp => dp.DocumentProducts)
        .Where(d => documentIds.Contains(d.Id))
        .ToListAsync();

    await _unitOfWork.DocumentProducts.RemoveRangeAsync(documents.SelectMany(d => d.DocumentProducts!));
    await _unitOfWork.Documents.RemoveRangeAsync(documents);

    await _unitOfWork.CompleteAsync();
}
```

**Krok 1 — pobranie dokumentów z pozycjami:**
- `Query()` zwraca `IQueryable<Document>`.
- `Include(dp => dp.DocumentProducts)` — eager loading pozycji (konieczne do ręcznego usunięcia).
- `Where(d => documentIds.Contains(d.Id))` — filtr po Id bez sprawdzenia `UserFirmId`.
- Wynik: lista `Document` z załadowanymi `DocumentProducts`.

**Krok 2 — usunięcie pozycji:**
- `documents.SelectMany(d => d.DocumentProducts!)` — spłaszczenie wszystkich pozycji ze wszystkich dokumentów.
- `!` — null-forgiving operator; jeżeli `DocumentProducts` byłoby `null` (mimo Include), rzuci `NullReferenceException → 500`.

**Krok 3 — usunięcie dokumentów:**
- `RemoveRangeAsync(documents)` — oznacza encje jako `Deleted` w kontekście EF.

---

## 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | Opis |
|---|---|---|---|
| 1 | `RemoveRangeAsync(documentProducts)` | `DocumentProductRepository` | Oznaczenie pozycji jako `Deleted` |
| 2 | `RemoveRangeAsync(documents)` | `DocumentRepository` | Oznaczenie dokumentów jako `Deleted` |
| 3 | `CompleteAsync()` | `UnitOfWork` | Jeden `SaveChangesAsync()` dla obu operacji |

> Jeden `CompleteAsync()` obejmuje usunięcie pozycji i dokumentów — operacje są atomowe w ramach jednej transakcji EF (domyślna transakcja `SaveChangesAsync`). ✅

---

## 5. Odpowiedź

HTTP `200 OK`. Ciało:
```json
{ "message": "Documents deleted successfully." }
```

> Odpowiedź jest taka sama niezależnie od tego, czy usunięto 0 czy 100 dokumentów. Brak informacji o liczbie usuniętych rekordów.

---

## 6. Uwagi techniczne

- [UWAGA: Endpoint używa HTTP `PUT` zamiast `DELETE` dla operacji usuwania. Semantycznie niepoprawny czasownik HTTP. Kotwica: `DocumentController.cs › DocumentController.DeleteDocuments` (`[HttpPut("DeleteDocuments")]`). — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Brak sprawdzenia własności (`UserFirmId`). `DeleteDocuments` usuwa KAŻDY dokument pasujący do podanych `Id` bez weryfikacji przynależności do firmy zalogowanego użytkownika. Złośliwy użytkownik może usunąć dokumenty innych firm. Kotwica: `DocumentService.cs › DocumentService.DeleteDocuments`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Pusty `documentIds = []` → `CompleteAsync()` bez zmian → `200 OK { "message": "..." }`. Nie ma żadnego sygnału o braku zmian. — UWAGA informacyjna]

- [UWAGA: Null-forgiving `d.DocumentProducts!` — jeżeli Include nie załaduje kolekcji (np. błąd konfiguracji EF), `SelectMany` rzuci `NullReferenceException → 500`. Kotwica: `DocumentService.cs › DocumentService.DeleteDocuments`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
