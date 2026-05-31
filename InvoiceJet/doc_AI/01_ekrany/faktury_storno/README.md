# faktury_storno — Faktury storno

Ekrany zarządzania fakturami storno (DocumentTypeId=3). Storna mogą powstać na dwa sposoby: automatycznie przez operację „Przekształć w storno" z listy faktur zwykłych, lub ręcznie przez formularz edycji. Z listy storn nie można tworzyć nowych dokumentów storno (brak przycisku „Dodaj storno"). Formularz oparty na `BaseInvoiceComponent`. Chronione przez AuthGuard.

## Drzewo zawartości

```
faktury_storno/
├── README.md                                    ← Ten plik
├── lista_faktur_storno/
│   └── ekran.md                                 ← InvoiceStornosComponent — lista storn
└── dodaj_edytuj_fakture_storno/
    └── ekran.md                                 ← AddOrEditInvoiceStornosComponent — formularz storna
```

## Kluczowe dokumenty

- `lista_faktur_storno/ekran.md` — lista storn: tabela, usunięcie, brak opcji tworzenia nowego storna z UI
- `dodaj_edytuj_fakture_storno/ekran.md` — formularz storna; `documentTypeId=3`; specyfika: storno może być tworzone automatycznie z listy faktur

## Powiązane katalogi

- `../faktury/lista_faktur/` — operacja „Przekształć w storno" inicjuje tworzenie storn
- `../00_wspolne/base_invoice_component/` — klasa bazowa formularzy dokumentów
- `../00_wspolne/modale_wspolne/pdf_viewer/` — podgląd PDF dokumentu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
