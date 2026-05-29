# Register - Mapa makiet pozycji

## 1. Diagram

```mermaid
flowchart TD
  Register["/register"] --> Form["Register form"]
  Form --> Api["POST /api/Auth/register"]
  Api --> Token["localStorage authToken"]
  Token --> Dashboard["/dashboard"]
```

## 2. Linki

| Element | Typ | Route | Dokument |
|---|---|---|---|
| Rejestracja | ekran | `/register` | [E-12_Register](../../../../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-12_Register/00_METADANE.md) |
