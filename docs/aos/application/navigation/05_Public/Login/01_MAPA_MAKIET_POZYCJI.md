# Login - Mapa makiet pozycji

## 1. Diagram

```mermaid
flowchart TD
  Login["/login"] --> Form["Login form"]
  Form --> Api["POST /api/Auth/login"]
  Api --> Token["localStorage authToken"]
  Token --> Dashboard["/dashboard"]
```

## 2. Linki

| Element | Typ | Route | Dokument |
|---|---|---|---|
| Logowanie | ekran | `/login` | [E-11_Login](../../../../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-11_Login/00_METADANE.md) |
