# Lista i szczegóły dokumentów — Przegląd procesu

## Cel

Proces pobiera listę dokumentów wybranego typu dla aktywnej firmy użytkownika oraz pobiera szczegóły pojedynczego dokumentu po identyfikatorze.

---

## Diagram

```mermaid
flowchart TD
  A["GET ...GetDocumentTableRecords/{documentTypeId}"] --> B["GetDocumentTableRecords()"]
  B --> C["Users.GetUserFirmAsync(currentUserId)"]
  C --> D{"Aktywna firma istnieje"}
  D -->|nie| E["Zwróć pustą listę"]
  D -->|tak| F["Documents.GetAllDocumentsByType(...)"]
  F --> G["Mapowanie do List<DocumentTableRecordDto>"]
  G --> H["HTTP 200 OK"]

  I["GET ...GetDocumentById/{documentId}"] --> J["GetDocumentById()"]
  J --> K["Documents.GetDocumentWithAllInfo(documentId)"]
  K --> L["Mapowanie do DocumentRequestDto"]
  L --> M["HTTP 200 OK"]
```
