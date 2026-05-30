# Edycja firmy — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Firm/EditFirm/{isClient}` |
| Kontroler | `FirmController` |
| Metoda kontrolera | `EditFirm([FromBody] FirmDto firmDto, bool isClient)` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Parametry

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `isClient` | `bool` | Trasa | Wartość flagi relacji `UserFirm.IsClient`. |
| `firmDto` | `FirmDto` | Body | Dane firmy do aktualizacji. |

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `FirmDto` | Firma istnieje i zapis zakończony sukcesem. |
| `401 Unauthorized` | N/D | Brak poprawnego tokenu. |
| `403 Forbidden` | N/D | Brak wymaganej roli `User`. |
| `500 Internal Server Error` | `{ "message": string }` | `Exception("Firm not found.")` lub inny wyjątek. |
