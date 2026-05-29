# Dane autouzupełniania dokumentu — Przegląd procesu

## Cel

Proces zwraca zestaw danych potrzebnych do wypełnienia formularza dokumentu: klientów, serie dokumentów, statusy dokumentu i produkty aktywnej firmy.

---

## Diagram

```mermaid
flowchart TD
  A["GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}"] --> B["DocumentService.GetDocumentAutofillInfo()"]
  B --> C["Pobranie currentUserId i userFirmId"]
  C --> D{"Aktywna firma istnieje"}
  D -->|nie| E["Zwróć nowy DocumentAutofillDto()"]
  D -->|tak| F["Pobranie Clients, DocumentSeries, DocumentStatuses, Products"]
  F --> G["Mapowanie do DTO list"]
  G --> H["HTTP 200 OK DocumentAutofillDto"]
```
