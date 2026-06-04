# Zarządzanie firmami-klientami — Kontrakt API

## Endpoint: pobranie listy

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Firm/GetUserClientFirms` |
| Odpowiedź sukcesu | `200 OK` i `List<FirmDto>` |

## Endpoint: usuwanie

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Firm/DeleteFirms` |
| Parametr | `int[] firmIds` |
| Odpowiedź sukcesu | `200 OK` |

---

## Uwagi kontraktowe

- Metoda `DeleteFirms` w kontrolerze nie ma atrybutu `[FromBody]`. [UWAGA: źródło bindowania tablicy `firmIds` wymaga potwierdzenia testem endpointu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
