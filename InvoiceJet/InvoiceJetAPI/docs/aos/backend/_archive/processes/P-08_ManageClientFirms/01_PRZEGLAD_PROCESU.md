# Zarządzanie firmami-klientami — Przegląd procesu

## Cel

Proces udostępnia listę firm-klientów użytkownika oraz usuwa wskazane firmy-klientów, jeżeli nie są powiązane z dokumentami.

---

## Diagram

```mermaid
flowchart TD
  A["GET /api/Firm/GetUserClientFirms"] --> B["FirmService.GetUserClientFirms()"]
  B --> C["UserFirms.GetUserFirmClients(currentUserId)"]
  C --> D["Mapowanie do List<FirmDto>"]
  D --> E["HTTP 200 OK"]

  F["PUT /api/Firm/DeleteFirms"] --> G["FirmService.DeleteFirms(firmIds)"]
  G --> H["Pętla po firmIds"]
  H --> I["Sprawdzenie powiązania z Document.ClientId"]
  I --> J["Usunięcie firmy"]
  J --> K["CompleteAsync()"]
  K --> L["HTTP 200 OK"]
```
