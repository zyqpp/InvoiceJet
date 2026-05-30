# Zarządzanie seriami dokumentów — Logika aplikacyjna

## Pobranie listy

1. Serwis pobiera `userFirmId`.
2. Gdy brak aktywnej firmy, zwraca pustą listę.
3. Gdy aktywna firma istnieje, pobiera serie przez `DocumentSeries.GetAllDocumentSeriesForActiveUserFirm(userId)`.
4. Serwis mapuje encje do `List<DocumentSeriesDto>`.

## Dodanie serii

1. Serwis pobiera `userFirmId`.
2. Gdy brak aktywnej firmy, rzuca `UserHasNoAssociatedFirmException`.
3. Serwis mapuje `DocumentSeriesDto` na `DocumentSeries`.
4. Serwis ustawia:
   - `documentSeries.UserFirmId = userFirmId.Value`,
   - `documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id`.
5. Serwis zapisuje rekord przez `AddAsync` i `CompleteAsync`.

## Aktualizacja serii

1. Serwis wyszukuje serię po `Id`.
2. Gdy nie istnieje, rzuca `Exception("Document Series not found")`.
3. Serwis mapuje DTO na encję i nadpisuje `DocumentTypeId`.
4. Serwis wykonuje `UpdateAsync` i `CompleteAsync`.

## Usuwanie serii

1. Serwis pobiera serie, których `Id` znajduje się w tablicy wejściowej.
2. Serwis usuwa listę przez `RemoveRangeAsync`.
3. Serwis wykonuje `CompleteAsync()`.
