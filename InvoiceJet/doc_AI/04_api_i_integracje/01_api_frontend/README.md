# 01_api_frontend — REST API frontendu InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 1.0 |
| Data | 2026-05-31 |
| Status | Obowiązujący |

## Opis biznesowy

Dokumentacja 31 endpointów REST API frontendu aplikacji InvoiceJet. Wszystkie endpointy są wystawiane przez backend ASP.NET Core 8 i konsumowane przez frontend Angular 16. Dwa endpointy są publiczne (rejestracja, logowanie); pozostałe 29 wymaga JWT Bearer Token z rolą `User`.

## Kluczowy dokument

- [`lista_api.md`](lista_api.md) — zbiorczy spis wszystkich 31 endpointów z metodami, ścieżkami, autoryzacją i linkami do szczegółowych opisów.

## Drzewo zawartości

```
01_api_frontend/
├── README.md                          ← ten plik
├── lista_api.md                       ← spis wszystkich 31 endpointów
├── auth/                              ← 2 endpointy (publiczne)
│   ├── POST_Auth_register.md          ← API-01
│   └── POST_Auth_login.md             ← API-02
├── firm/                              ← 6 endpointów (CRUD firmy i klientów + ANAF)
│   ├── POST_Firm_AddFirm.md           ← API-03
│   ├── GET_Firm_fromAnaf.md           ← API-04
│   ├── PUT_Firm_EditFirm.md           ← API-05
│   ├── GET_Firm_GetUserActiveFirm.md  ← API-06
│   ├── GET_Firm_GetUserClientFirms.md ← API-07/08
│   └── PUT_Firm_DeleteFirms.md        ← API-09
├── product/                           ← 4 endpointy (CRUD produktów)
│   ├── GET_Product_GetAll.md          ← API-10
│   ├── POST_Product_Add.md            ← API-11
│   ├── PUT_Product_Edit.md            ← API-12
│   └── PUT_Product_Delete.md          ← API-13
├── bank_account/                      ← 4 endpointy (CRUD kont bankowych)
│   ├── GET_BankAccount_GetAll.md      ← API-14
│   ├── POST_BankAccount_Add.md        ← API-15
│   ├── PUT_BankAccount_Edit.md        ← API-16
│   └── PUT_BankAccount_Delete.md      ← API-17
├── document_series/                   ← 4 endpointy (CRUD serii dokumentów)
│   ├── GET_DocumentSeries_GetAll.md   ← API-18
│   ├── POST_DocumentSeries_Add.md     ← API-19
│   ├── PUT_DocumentSeries_Update.md   ← API-20
│   └── PUT_DocumentSeries_Delete.md   ← API-21
└── document/                          ← 10 endpointów (dokumenty, PDF, statystyki)
    ├── POST_Document_Add.md           ← API-22
    ├── PUT_Document_Edit.md           ← API-23
    ├── GET_Document_GetTableRecords.md ← API-24
    ├── GET_Document_GetById.md        ← API-25
    ├── PUT_Document_Delete.md         ← API-26
    ├── GET_Document_GetAutofillInfo.md ← API-27
    ├── POST_Document_GeneratePdf.md   ← API-28 ⚠️ BUG: hardcoded InvoiceDocument
    ├── POST_Document_GetPdfStream.md  ← API-29
    ├── GET_Document_GetDashboardStats.md ← API-30
    └── PUT_Document_TransformToStorno.md ← API-31
```

## Podsumowanie według kontrolera

| Kontroler | Liczba endpointów | Podkatalog |
|---|---|---|
| AuthController | 2 | `auth/` |
| FirmController | 6 | `firm/` |
| ProductController | 4 | `product/` |
| BankAccountController | 4 | `bank_account/` |
| DocumentSeriesController | 4 | `document_series/` |
| DocumentController | 10 | `document/` |
| **Razem** | **31** | |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
