# Zarządzanie seriami dokumentów — Kontrakt API

## Endpointy

| Operacja | HTTP | Ścieżka | Wejście | Wyjście |
|---|---|---|---|---|
| Pobranie listy | `GET` | `/api/DocumentSeries/GetAllDocumentSeriesForUserId` | Brak | `List<DocumentSeriesDto>` |
| Dodanie serii | `POST` | `/api/DocumentSeries/AddDocumentSeries` | `DocumentSeriesDto` (`[FromBody]`) | `200 OK` |
| Aktualizacja serii | `PUT` | `/api/DocumentSeries/UpdateDocumentSeries` | `DocumentSeriesDto` (`[FromBody]`) | `200 OK` |
| Usunięcie serii | `PUT` | `/api/DocumentSeries/DeleteDocumentSeries` | `int[] documentSeriesIds` | `200 OK` |

---

## Uwagi kontraktowe

- `DeleteDocumentSeries(int[] documentSeriesIds)` nie ma `[FromBody]`. [UWAGA: źródło bindowania tablicy wymaga potwierdzenia testem endpointu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
