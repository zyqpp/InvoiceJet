# Pobranie aktywnej firmy użytkownika — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Firm/GetUserActiveFirm` |
| Kontroler | `FirmController` |
| Metoda kontrolera | `GetUserActiveFirm()` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `FirmDto` | Zawsze przy poprawnej autoryzacji. |
| `401 Unauthorized` | N/D | Brak poprawnego tokenu. |
| `403 Forbidden` | N/D | Brak wymaganej roli `User`. |

Jeżeli aktywna firma nie istnieje, serwis zwraca pusty obiekt `FirmDto`.
