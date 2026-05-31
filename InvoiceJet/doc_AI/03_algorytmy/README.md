# 03_algorytmy — Algorytmy

Opis biznesowy: [do uzupełnienia w fazie 11]

## Drzewo zawartości

```
03_algorytmy/
├── README.md
├── ALG-01_JwtAuthentication.md              ← źródłowy (zachowany)
├── ALG-02_DocumentNumberGeneration.md       ← źródłowy (zachowany)
├── ALG-03_PasswordHashingVerification.md    ← źródłowy (zachowany)
├── ALG-04_JwtTokenCreation.md              ← źródłowy (zachowany)
├── ALG-05_DocumentTotalCalculation.md       ← źródłowy (zachowany)
├── ALG-06_AnafIntegration.md               ← źródłowy (zachowany)
├── ALG-07_PdfGeneration.md                 ← źródłowy (zachowany; podzielony na dwa pliki poniżej)
├── ALG-08_TransformToStorno.md             ← źródłowy (zachowany)
├── ALG-09_ExceptionMiddlewarePipeline.md   ← źródłowy (zachowany)
├── ALG-10_DataIsolationPattern.md          ← źródłowy (zachowany)
├── walidacji/
│   ├── README.md
│   └── walidacja_hasla.md                  ← z ALG-03 (BCrypt + regex)
├── autoryzacyjne/
│   ├── README.md
│   ├── weryfikacja_tokenu_jwt.md           ← z ALG-01 (pipeline JWT)
│   └── tworzenie_tokenu_jwt.md             ← z ALG-04 (CreateToken)
├── generowania_pdf/
│   ├── README.md
│   ├── generuj_pdf_na_dysk.md              ← z ALG-07 (GenerateInvoicePdf — BUG A-KRIT-04)
│   └── generuj_pdf_stream.md               ← z ALG-07 (GetPdfStream — fabryka poprawna)
├── wyliczeniowe/
│   ├── README.md
│   └── obliczanie_wartosci_dokumentu.md    ← z ALG-05
└── dedykowane/
    ├── README.md
    ├── generowanie_numeru_dokumentu.md     ← z ALG-02 (race condition!)
    ├── integracja_anaf.md                  ← z ALG-06
    ├── transformacja_na_storno.md          ← z ALG-08 (brak atomowości)
    ├── pipeline_obslugi_wyjatkow.md        ← z ALG-09
    ├── izolacja_danych_userfirm.md         ← z ALG-10
    └── seed_typow_dokumentow.md            ← NOWY (DbSeeder — DocumentType + DocumentStatus)
```

## Kluczowe dokumenty

- [`walidacji/walidacja_hasla.md`](walidacji/walidacja_hasla.md) — regex + BCrypt; lista 7 dozwolonych znaków specjalnych
- [`autoryzacyjne/weryfikacja_tokenu_jwt.md`](autoryzacyjne/weryfikacja_tokenu_jwt.md) — pełny cykl JWT: backend + JwtInterceptor + AuthGuard; anomalie bezpieczeństwa
- [`autoryzacyjne/tworzenie_tokenu_jwt.md`](autoryzacyjne/tworzenie_tokenu_jwt.md) — AuthService.CreateToken(); claims tokenu; HmacSha512
- [`generowania_pdf/generuj_pdf_na_dysk.md`](generowania_pdf/generuj_pdf_na_dysk.md) — **BUG A-KRIT-04**: hardcoded `new InvoiceDocument()` niezależnie od typu dokumentu
- [`generowania_pdf/generuj_pdf_stream.md`](generowania_pdf/generuj_pdf_stream.md) — poprawna implementacja z `InvoiceDocumentFactory`
- [`wyliczeniowe/obliczanie_wartosci_dokumentu.md`](wyliczeniowe/obliczanie_wartosci_dokumentu.md) — wzór brutto: Price × Qty × (1 + VAT/100); backend + Angular
- [`dedykowane/generowanie_numeru_dokumentu.md`](dedykowane/generowanie_numeru_dokumentu.md) — **race condition** na CurrentNumber; dwie transakcje
- [`dedykowane/transformacja_na_storno.md`](dedykowane/transformacja_na_storno.md) — **brak atomowości**: CompleteAsync wewnątrz pętli
- [`dedykowane/pipeline_obslugi_wyjatkow.md`](dedykowane/pipeline_obslugi_wyjatkow.md) — mapa wyjątek domenowy → kod HTTP
- [`dedykowane/izolacja_danych_userfirm.md`](dedykowane/izolacja_danych_userfirm.md) — wzorzec UserFirm-based isolation; luka przy edycji zasobu
- [`dedykowane/seed_typow_dokumentow.md`](dedykowane/seed_typow_dokumentow.md) — DbSeeder.SeedDocumentTypes(); DocumentType + DocumentStatus

## Powiązane katalogi

- [`../02_procesy/`](../02_procesy/) — procesy techniczne wywołujące algorytmy
- [`../04_api_i_integracje/`](../04_api_i_integracje/) — endpointy API, przez które algorytmy są wywoływane
- [`../05_model_danych/`](../05_model_danych/) — encje i DTO używane przez algorytmy

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
| 0.2 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Reorganizacja — dodano podkatalogi kategorii z plikami algorytmów wg wytycznych (T-06). |
