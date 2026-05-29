# Zarządzanie seriami dokumentów — Przegląd procesu

## Cel

Proces obsługuje listowanie, dodawanie, aktualizację i usuwanie serii dokumentów aktywnej firmy użytkownika.

---

## Diagram

```mermaid
flowchart TD
  A["GET serie"] --> B["GetAllDocumentSeriesForUserId()"]
  C["POST seria"] --> D["AddDocumentSeries()"]
  E["PUT seria"] --> F["UpdateDocumentSeries()"]
  G["PUT usuwanie"] --> H["DeleteDocumentSeries()"]
```

---

## Uwagi

- `AddDocumentSeries` w kontrolerze ma lokalny `try/catch` i zwraca `BadRequest(ex.Message)`.
- Pozostałe metody kontrolera opierają się na `ExceptionMiddleware`.
