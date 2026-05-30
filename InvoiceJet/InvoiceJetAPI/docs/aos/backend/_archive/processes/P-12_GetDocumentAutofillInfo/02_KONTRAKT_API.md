# Dane autouzupełniania dokumentu — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| Parametr trasy | `documentTypeId: int` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `DocumentAutofillDto` | Zawsze przy poprawnej autoryzacji. |
| `401 Unauthorized` | N/D | Brak tokenu. |
| `403 Forbidden` | N/D | Brak roli `User`. |

Jeżeli aktywna firma nie istnieje, odpowiedź ma postać pustego `DocumentAutofillDto`.
