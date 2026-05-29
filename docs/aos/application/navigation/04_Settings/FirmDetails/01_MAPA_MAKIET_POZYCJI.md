# Firm Details - Mapa makiet pozycji

## 1. Diagram

```mermaid
flowchart TD
  Menu["Firm Details"] --> Form["/dashboard/firm-details"]
  Form --> Load["GetUserActiveFirm"]
  Form --> Anaf["fromAnaf/{cui}"]
  Form --> Add["AddFirm/{isClient=false}"]
  Form --> Edit["EditFirm/{isClient=false}"]
```

## 2. Linki

| Element | Typ | Route | Dokument |
|---|---|---|---|
| Dane firmy | ekran | `/dashboard/firm-details` | [E-08_FirmDetails](../../../../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-08_FirmDetails/00_METADANE.md) |
