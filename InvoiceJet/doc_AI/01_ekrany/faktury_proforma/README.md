# faktury_proforma — Faktury proforma

Ekrany zarządzania fakturami proforma (DocumentTypeId=2). Struktura identyczna jak `faktury/`, lecz bez operacji „Przekształć w storno". Formularz oparty na `BaseInvoiceComponent`. Chronione przez AuthGuard.

## Drzewo zawartości

```
faktury_proforma/
├── README.md                                    ← Ten plik
├── lista_faktur_proforma/
│   └── ekran.md                                 ← InvoiceProformasComponent — lista proform
└── dodaj_edytuj_fakture_proforma/
    └── ekran.md                                 ← AddOrEditInvoiceProformaComponent — formularz proformy
```

## Kluczowe dokumenty

- `lista_faktur_proforma/ekran.md` — lista proform: tabela, usunięcie, nawigacja do formularza
- `dodaj_edytuj_fakture_proforma/ekran.md` — formularz proformy; `documentTypeId=2`; logika w `BaseInvoiceComponent`

## Powiązane katalogi

- `../00_wspolne/base_invoice_component/` — klasa bazowa formularzy dokumentów
- `../00_wspolne/modale_wspolne/pdf_viewer/` — podgląd PDF dokumentu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
