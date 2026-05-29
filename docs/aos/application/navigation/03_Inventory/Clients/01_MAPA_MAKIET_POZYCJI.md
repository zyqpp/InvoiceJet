# Clients - Mapa makiet pozycji

## 1. Diagram

```mermaid
flowchart TD
  Menu["Clients"] --> List["/dashboard/clients"]
  List --> AddDialog["AddEditClientDialogComponent add"]
  List --> EditDialog["AddEditClientDialogComponent edit"]
  List --> Delete["DeleteFirms"]
  AddDialog --> Anaf["GET /api/Firm/fromAnaf/{cui}"]
```

## 2. Linki

| Element | Typ | Route | Dokument |
|---|---|---|---|
| Lista klientow | ekran | `/dashboard/clients` | [E-06_Clients](../../../../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-06_Clients/00_METADANE.md) |
| Dialog klienta | dialog | N/D | [Rejestr A-06](../../../REJESTR_PRZEPLYWOW_APLIKACJI.md) |
