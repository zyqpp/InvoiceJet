# Pobranie firmy z ANAF — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Firm/fromAnaf/{cui}` |
| Kontroler | `FirmController` |
| Metoda kontrolera | `GetFirmDataFromAnaf(string cui)` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Parametry wejściowe

| Parametr | Typ | Lokalizacja | Opis |
|---|---|---|---|
| `cui` | `string` | Trasa | Identyfikator firmy przekazywany do ANAF. |

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `FirmDto` | ANAF zwrócił odpowiedź sukcesu i JSON został sparsowany. |
| `404 Not Found` | `{ "message": string }` | `AnafFirmNotFoundException`. |
| `401 Unauthorized` | N/D | Brak poprawnego tokenu. |
| `403 Forbidden` | N/D | Brak wymaganej roli `User`. |
| `500 Internal Server Error` | `{ "message": string }` | Nieobsłużony błąd poza `AnafFirmNotFoundException`. |

---

## Kontrakt do ANAF (wywołanie z serwisu)

Serwis wykonuje `POST` do `_apiUrl` z body:

```json
[
  {
    "cui": "wartosc-z-trasy",
    "data": "yyyy-MM-dd"
  }
]
```
