# faktury — Faktury zwykłe

Ekrany zarządzania fakturami zwykłymi (DocumentTypeId=1). Obejmuje listę faktur z operacjami CRUD i przekształceniem w storno oraz formularz tworzenia i edycji faktury oparty na `BaseInvoiceComponent`. Ekrany chronione przez AuthGuard (rola: User).

## Drzewo zawartości

```
faktury/
├── README.md                            ← Ten plik
├── lista_faktur/
│   └── ekran.md                         ← InvoicesComponent — lista faktur
└── dodaj_edytuj_fakture/
    └── ekran.md                         ← AddOrEditInvoiceComponent — formularz faktury
```

## Kluczowe dokumenty

- `lista_faktur/ekran.md` — lista faktur: tabela, filtrowanie, operacje batch (usuń, transformuj w storno), nawigacja do formularza
- `dodaj_edytuj_fakture/ekran.md` — formularz faktury (tryb dodaj + tryb edytuj); logika w `BaseInvoiceComponent`; wywołanie podglądu PDF

## Powiązane katalogi

- `../00_wspolne/base_invoice_component/` — klasa bazowa formularzy dokumentów
- `../00_wspolne/modale_wspolne/pdf_viewer/` — podgląd PDF dokumentu
- `../faktury_storno/` — storna tworzone przez „Przekształć w storno" z listy faktur

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
