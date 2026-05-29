# Settings - Diagram sekcji

## 1. Diagram

```mermaid
flowchart TD
  Settings["Menu: Settings"]
  Settings --> Firm["Firm Details"]
  Settings --> Bank["Bank Accounts"]
  Settings --> Series["Document Series"]
  Firm --> Anaf["fromAnaf"]
  Bank --> BankDialog["Dialog add/edit bank account"]
  Series --> SeriesDialog["Dialog add/edit document series"]
```

## 2. Linki

| Pozycja | Route | Dokument pozycji |
|---|---|---|
| Firm Details | `/dashboard/firm-details` | [FirmDetails](./FirmDetails/01_MAPA_MAKIET_POZYCJI.md) |
| Bank Accounts | `/dashboard/bank-accounts` | [BankAccounts](./BankAccounts/01_MAPA_MAKIET_POZYCJI.md) |
| Document Series | `/dashboard/document-series` | [DocumentSeries](./DocumentSeries/01_MAPA_MAKIET_POZYCJI.md) |
