# Edycja firmy — Przegląd procesu

## Cel

Proces aktualizuje dane istniejącej firmy oraz aktualizuje flagę `IsClient` w relacji `UserFirm` dla zalogowanego użytkownika.

---

## Diagram przepływu

```mermaid
flowchart TD
  A["PUT /api/Firm/EditFirm/{isClient}"] --> B["FirmController.EditFirm()"]
  B --> C["FirmService.EditFirm(firmDto, isClient)"]
  C --> D["Firms.GetByIdAsync(firmDto.Id)"]
  D --> E{"Firma istnieje"}
  E -->|nie| F["Exception: Firm not found."]
  E -->|tak| G["Mapowanie FirmDto -> Firm"]
  G --> H["CompleteAsync()"]
  H --> I["ManageUserFirmRelation(firm.Id, isClient)"]
  I --> J["CompleteAsync()"]
  J --> K["HTTP 200 OK FirmDto"]
```

---

## Wynik procesu

| Wynik | Opis |
|---|---|
| Sukces | `200 OK` i `FirmDto` po aktualizacji. |
| Błąd | `500 Internal Server Error` dla `Exception("Firm not found.")` i innych nieobsłużonych błędów. |
