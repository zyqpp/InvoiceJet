# Usuwanie dokumentów — Logika aplikacyjna

## Przepływ wykonania

1. Serwis pobiera listę dokumentów:
   - `Documents.Query().Include(dp => dp.DocumentProducts).Where(d => documentIds.Contains(d.Id)).ToListAsync()`.
2. Serwis usuwa wszystkie pozycje dokumentów:
   - `DocumentProducts.RemoveRangeAsync(documents.SelectMany(d => d.DocumentProducts))`.
3. Serwis usuwa dokumenty:
   - `Documents.RemoveRangeAsync(documents)`.
4. Serwis wykonuje `_unitOfWork.CompleteAsync()`.
5. Kontroler zwraca `200 OK` i komunikat sukcesu.

---

## Uwagi

- Proces nie sygnalizuje, które identyfikatory z żądania nie istniały w bazie.
- Proces nie zawiera dodatkowej walidacji własności dokumentów względem użytkownika. [UWAGA: zakres usuwania dokumentów wymaga potwierdzenia uprawnień domenowych — WYMAGA WERYFIKACJI Z ZESPOŁEM]
