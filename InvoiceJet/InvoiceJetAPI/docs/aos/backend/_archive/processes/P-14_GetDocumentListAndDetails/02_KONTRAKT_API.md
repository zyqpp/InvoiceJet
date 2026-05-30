# Lista i szczegóły dokumentów — Kontrakt API

## Endpoint: lista dokumentów

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDocumentTableRecords/{documentTypeId}` |
| Parametr | `documentTypeId: int` |
| Odpowiedź | `List<DocumentTableRecordDto>` |

## Endpoint: szczegóły dokumentu

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDocumentById/{documentId}` |
| Parametr | `documentId: int` |
| Odpowiedź | `DocumentRequestDto` |

---

## Kody odpowiedzi

| Status | Warunek |
|---|---|
| `200 OK` | Oba endpointy zwracają dane lub wartości puste/null. |
| `401 Unauthorized` | Brak tokenu. |
| `403 Forbidden` | Brak roli `User`. |
| `500 Internal Server Error` | Nieobsłużony wyjątek infrastruktury. |
