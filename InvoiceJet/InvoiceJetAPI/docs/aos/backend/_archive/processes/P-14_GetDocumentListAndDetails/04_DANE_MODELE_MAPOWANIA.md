# Lista i szczegóły dokumentów — Dane, modele i mapowania

## DTO odpowiedzi

| DTO | Rola |
|---|---|
| `DocumentTableRecordDto` | Rekord listy dokumentów. |
| `DocumentRequestDto` | Szczegóły pojedynczego dokumentu. |

---

## Źródła danych

| Metoda | Repozytorium / zapytanie |
|---|---|
| `GetDocumentTableRecords` | `DocumentRepository.GetAllDocumentsByType(...)` z `Include(Client)` i `Include(DocumentStatus)` |
| `GetDocumentById` | `DocumentRepository.GetDocumentWithAllInfo(documentId)` z relacjami `DocumentStatus`, `DocumentProducts.Product`, `Client` |

---

## Mapowania

| Źródło | Cel | Profil |
|---|---|---|
| `Document` | `DocumentTableRecordDto` | `DocumentProfile` |
| `Document` | `DocumentRequestDto` | `DocumentProfile` |
