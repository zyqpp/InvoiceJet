# 04_api_i_integracje — API i integracje zewnętrzne

Opis biznesowy: [do uzupełnienia w fazie 11]

## Drzewo zawartości

```
04_api_i_integracje/
├── README.md
├── 01_api_frontend/
│   ├── README.md
│   ├── lista_api.md                     ← spis wszystkich 31 endpointów
│   ├── auth/
│   │   ├── POST_Auth_register.md        ← API-01
│   │   └── POST_Auth_login.md           ← API-02
│   ├── firm/
│   │   ├── POST_Firm_AddFirm.md         ← API-03
│   │   ├── GET_Firm_fromAnaf.md         ← API-04
│   │   ├── PUT_Firm_EditFirm.md         ← API-05
│   │   ├── GET_Firm_GetUserActiveFirm.md ← API-06
│   │   ├── GET_Firm_GetUserClientFirms.md ← API-07/08
│   │   └── PUT_Firm_DeleteFirms.md      ← API-09
│   ├── product/
│   │   ├── GET_Product_GetAll.md        ← API-10
│   │   ├── POST_Product_Add.md          ← API-11
│   │   ├── PUT_Product_Edit.md          ← API-12
│   │   └── PUT_Product_Delete.md        ← API-13
│   ├── bank_account/
│   │   ├── GET_BankAccount_GetAll.md    ← API-14
│   │   ├── POST_BankAccount_Add.md      ← API-15
│   │   ├── PUT_BankAccount_Edit.md      ← API-16
│   │   └── PUT_BankAccount_Delete.md   ← API-17
│   ├── document_series/
│   │   ├── GET_DocumentSeries_GetAll.md ← API-18
│   │   ├── POST_DocumentSeries_Add.md  ← API-19
│   │   ├── PUT_DocumentSeries_Update.md ← API-20
│   │   └── PUT_DocumentSeries_Delete.md ← API-21
│   └── document/
│       ├── POST_Document_Add.md         ← API-22
│       ├── PUT_Document_Edit.md         ← API-23
│       ├── GET_Document_GetTableRecords.md ← API-24
│       ├── GET_Document_GetById.md      ← API-25
│       ├── PUT_Document_Delete.md       ← API-26
│       ├── GET_Document_GetAutofillInfo.md ← API-27
│       ├── POST_Document_GeneratePdf.md ← API-28 ⚠️ hardcoded bug
│       ├── POST_Document_GetPdfStream.md ← API-29
│       ├── GET_Document_GetDashboardStats.md ← API-30
│       └── PUT_Document_TransformToStorno.md ← API-31
└── 02_systemy_dziedzinowe/
    ├── README.md
    └── anaf/
        └── pobierz_dane_firmy.md        ← GET ANAF CUI lookup
```

## Kluczowe dokumenty

- [`01_api_frontend/lista_api.md`](01_api_frontend/lista_api.md) — spis wszystkich 31 endpointów

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
