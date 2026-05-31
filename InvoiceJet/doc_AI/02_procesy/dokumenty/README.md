# dokumenty

Procesy techniczne związane z zarządzaniem dokumentami handlowymi (faktury, proformy, storna) w systemie InvoiceJet.

## Drzewo zawartości

```
dokumenty/
├── README.md                              # ten plik
├── dodaj_dokument/
│   └── proces.md                          # PROC-AddDocument — wystawienie nowego dokumentu
├── edytuj_dokument/
│   └── proces.md                          # PROC-EditDocument — edycja dokumentu (delete-all-then-insert pozycji)
├── pobierz_dokumenty/
│   └── proces.md                          # PROC-GetDocuments — lista tabelaryczna + pełny dokument po id
├── usun_dokumenty/
│   └── proces.md                          # PROC-DeleteDocuments — wsadowe usunięcie (hard delete)
├── generuj_pdf/
│   └── proces.md                          # PROC-GeneratePdf — generowanie PDF (QuestPDF; dwa endpointy)
├── pobierz_autouzupelnienie/
│   └── proces.md                          # PROC-GetDocumentAutofillInfo — dane startowe formularza
├── dashboard_statystyki/
│   └── proces.md                          # PROC-GetDashboardStats — liczniki i trend miesięczny
└── transformuj_na_storno/
    └── proces.md                          # PROC-TransformToStorno — konwersja na fakturę storno (UWAGA: brak atomowości!)
```

## Kluczowe dokumenty

- `dodaj_dokument/proces.md` — POST /api/Document/Add (anomalia: dwa osobne CompleteAsync)
- `generuj_pdf/proces.md` — **KRYTYCZNA ANOMALIA PDF-01:** `GenerateInvoicePdf` zawsze generuje fakturę zwykłą
- `transformuj_na_storno/proces.md` — **KRYTYCZNA ANOMALIA TS-01:** CompleteAsync wewnątrz pętli; brak atomowości
- `usun_dokumenty/proces.md` — `DocumentProducts` usuwane kaskadowo

## Powiązane katalogi

- `../../04_api_i_integracje/01_api_frontend/document/` — dokumentacja endpointów API dokumentów
- `../../01_ekrany/faktury/` — ekrany faktur
- `../../01_ekrany/faktury_proforma/` — ekrany faktur proforma
- `../../01_ekrany/faktury_storno/` — ekrany faktur storno
- `../../01_ekrany/dashboard/` — ekran Dashboard
- `../../03_algorytmy/generowania_pdf/` — algorytmy generowania PDF
- `../../03_algorytmy/dedykowane/transformacja_na_storno.md` — algorytm transformacji na storno
- `../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md` — algorytm obliczania wartości

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — struktura podfolderów dokumenty (z P-08..P-15). |
