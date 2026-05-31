# 02_procesy — Procesy techniczne

Procesy techniczne backendowe systemu InvoiceJet — od uwierzytelnienia przez zarządzanie danymi firmy aż po wystawianie i generowanie dokumentów. Każdy podfolder odpowiada jednej grupie operacji, każdy `proces.md` opisuje jeden konkretny przepływ.

## Drzewo zawartości

```
02_procesy/
├── README.md                                         # ten plik
├── P-01_RegisterUser.md                              # plik źródłowy (zachowany)
├── P-02_LoginUser.md                                 # plik źródłowy (zachowany)
├── P-03_ManageFirm.md                                # plik źródłowy (zachowany)
├── P-04_GetFirmFromAnaf.md                           # plik źródłowy (zachowany)
├── P-05_ManageBankAccounts.md                        # plik źródłowy (zachowany)
├── P-06_ManageProducts.md                            # plik źródłowy (zachowany)
├── P-07_ManageDocumentSeries.md                      # plik źródłowy (zachowany)
├── P-08_AddDocument.md                               # plik źródłowy (zachowany)
├── P-09_EditDocument.md                              # plik źródłowy (zachowany)
├── P-10_GetDocuments.md                              # plik źródłowy (zachowany)
├── P-11_DeleteDocument.md                            # plik źródłowy (zachowany)
├── P-12_GeneratePdf.md                               # plik źródłowy (zachowany)
├── P-13_GetDocumentAutofillInfo.md                   # plik źródłowy (zachowany)
├── P-14_GetDashboardStats.md                         # plik źródłowy (zachowany)
├── P-15_TransformToStorno.md                         # plik źródłowy (zachowany)
├── autentykacja/
│   ├── README.md
│   ├── rejestracja/
│   │   └── proces.md                                 # PROC-RegisterUser
│   └── logowanie/
│       └── proces.md                                 # PROC-LoginUser
├── firma/
│   ├── README.md
│   ├── dodaj_firme/
│   │   └── proces.md                                 # PROC-AddFirm
│   ├── edytuj_firme/
│   │   └── proces.md                                 # PROC-EditFirm
│   ├── pobierz_aktywna_firme/
│   │   └── proces.md                                 # PROC-GetUserActiveFirm
│   ├── pobierz_firmy_klientow/
│   │   └── proces.md                                 # PROC-GetUserClientFirms
│   ├── usun_firme/
│   │   └── proces.md                                 # PROC-DeleteFirms
│   └── pobierz_z_anaf/
│       └── proces.md                                 # PROC-GetFirmFromAnaf
├── produkty/
│   ├── README.md
│   ├── pobierz_produkty/
│   │   └── proces.md                                 # PROC-GetAllProducts
│   ├── dodaj_produkt/
│   │   └── proces.md                                 # PROC-AddProduct
│   ├── edytuj_produkt/
│   │   └── proces.md                                 # PROC-EditProduct
│   └── usun_produkty/
│       └── proces.md                                 # PROC-DeleteProducts
├── konta_bankowe/
│   ├── README.md
│   ├── pobierz_konta/
│   │   └── proces.md                                 # PROC-GetAllBankAccounts
│   ├── dodaj_konto/
│   │   └── proces.md                                 # PROC-AddBankAccount
│   ├── edytuj_konto/
│   │   └── proces.md                                 # PROC-EditBankAccount
│   └── usun_konta/
│       └── proces.md                                 # PROC-DeleteBankAccounts (KRYTYCZNA ANOMALIA: CASCADE DELETE dokumentów!)
├── serie_dokumentow/
│   ├── README.md
│   ├── pobierz_serie/
│   │   └── proces.md                                 # PROC-GetAllDocumentSeries
│   ├── dodaj_serie/
│   │   └── proces.md                                 # PROC-AddDocumentSeries
│   ├── edytuj_serie/
│   │   └── proces.md                                 # PROC-UpdateDocumentSeries
│   └── usun_serie/
│       └── proces.md                                 # PROC-DeleteDocumentSeries
└── dokumenty/
    ├── README.md
    ├── dodaj_dokument/
    │   └── proces.md                                 # PROC-AddDocument
    ├── edytuj_dokument/
    │   └── proces.md                                 # PROC-EditDocument
    ├── pobierz_dokumenty/
    │   └── proces.md                                 # PROC-GetDocuments (GetTableRecords + GetDocumentById)
    ├── usun_dokumenty/
    │   └── proces.md                                 # PROC-DeleteDocuments
    ├── generuj_pdf/
    │   └── proces.md                                 # PROC-GeneratePdf (GenerateInvoicePdf + GetPdfStream)
    ├── pobierz_autouzupelnienie/
    │   └── proces.md                                 # PROC-GetDocumentAutofillInfo
    ├── dashboard_statystyki/
    │   └── proces.md                                 # PROC-GetDashboardStats
    └── transformuj_na_storno/
        └── proces.md                                 # PROC-TransformToStorno (KRYTYCZNA ANOMALIA: brak atomowości!)
```

## Kluczowe dokumenty

- `konta_bankowe/usun_konta/proces.md` — **ANOMALIA KRYTYCZNA BA-01:** usunięcie konta kasuje kaskadowo dokumenty
- `dokumenty/generuj_pdf/proces.md` — **ANOMALIA KRYTYCZNA PDF-01:** GenerateInvoicePdf hardkoduje zawsze fakturę zwykłą
- `dokumenty/transformuj_na_storno/proces.md` — **ANOMALIA KRYTYCZNA TS-01:** brak atomowości w pętli

## Powiązane katalogi

- `../04_api_i_integracje/01_api_frontend/` — dokumentacja endpointów API
- `../01_ekrany/` — ekrany aplikacji wywołujące procesy
- `../03_algorytmy/` — algorytmy używane przez procesy

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
| 0.2 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Rozbudowanie drzewa po reorganizacji — 30 plików proces.md w 6 grupach. |
