# Dane autouzupełniania dokumentu — Logika aplikacyjna

## Przepływ wykonania

1. Serwis pobiera `userId` i `userFirmId`.
2. Gdy `userFirmId` jest puste, serwis zwraca `new DocumentAutofillDto()`.
3. Serwis pobiera klientów:
   - firmy z relacją `UserFirms` dla `userId` i `IsClient == true`.
4. Serwis pobiera serie dokumentów:
   - rekordy `DocumentSeries` dla `userFirmId` i `documentTypeId`,
   - z `Include(ds => ds.DocumentType)`.
5. Serwis pobiera wszystkie statusy dokumentów.
6. Serwis pobiera produkty dla `userFirmId`.
7. Serwis mapuje listy encji do list DTO i zwraca `DocumentAutofillDto`.
