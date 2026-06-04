# Dashboard - Diagram sekcji

## 1. Diagram

```mermaid
flowchart TD
  Menu["Menu: Dashboard"] --> Dashboard["/dashboard"]
  Dashboard --> Stats["Karty statystyk"]
  Dashboard --> Chart["Wykres Overview"]
  Dashboard --> Filters["Year + Document Type"]
  Filters --> Api["GET /api/Document/GetDashboardStats/{year}/{documentType}"]
```

## 2. Linki

| Element | Typ | Route | Dokument |
|---|---|---|---|
| Dashboard | ekran | `/dashboard` | [Rejestr A-01](../../REJESTR_PRZEPLYWOW_APLIKACJI.md) |
| Dashboard frontend | AOS frontendu | N/D | [E-01_Dashboard](../../../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-01_Dashboard/00_METADANE.md) |
