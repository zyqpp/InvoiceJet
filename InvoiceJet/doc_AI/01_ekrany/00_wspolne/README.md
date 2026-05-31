# 00_wspolne — Komponenty wspólne i szkielet layoutu

Katalog zawiera dokumentację komponentów Angular, które stanowią szkielet aplikacji InvoiceJet: pasek nawigacji (Navbar), boczne menu (Sidebar), modale globalne (wygaśnięcie sesji, podgląd PDF) oraz abstrakcyjną klasę bazową formularzy dokumentów. Komponenty z tego katalogu nie są samodzielnymi ekranami — działają jako elementy layoutu lub biblioteka wielokrotnego użytku osadzona w ekranach dziedzinowych.

## Drzewo zawartości

```
00_wspolne/
├── README.md                            ← Ten plik
├── navbar/
│   └── ekran.md                         ← NavbarComponent — górna belka aplikacji
├── sidebar/
│   └── ekran.md                         ← SidebarComponent — boczne menu nawigacyjne
├── modale_wspolne/
│   ├── token_expired_dialog/
│   │   └── modal.md                     ← TokenExpiredDialogComponent — sesja wygasła
│   └── pdf_viewer/
│       └── modal.md                     ← PdfViewerComponent — podgląd PDF dokumentu
└── base_invoice_component/
    └── ekran.md                         ← BaseInvoiceComponent — klasa bazowa formularzy dokumentów
```

## Kluczowe dokumenty

- `navbar/ekran.md` — NavbarComponent: wyświetla użytkownika i przycisk wylogowania
- `sidebar/ekran.md` — SidebarComponent: menu nawigacyjne z linkami do wszystkich sekcji
- `modale_wspolne/token_expired_dialog/modal.md` — globalny dialog wygaśnięcia sesji JWT (10 min)
- `modale_wspolne/pdf_viewer/modal.md` — podgląd PDF; używany z ekranów dodaj/edytuj dokument
- `base_invoice_component/ekran.md` — wspólna logika dla formularzy faktury, proformy i storna

## Powiązane katalogi

- `../faktury/dodaj_edytuj_fakture/` — używa `BaseInvoiceComponent` i `PdfViewerComponent`
- `../faktury_proforma/dodaj_edytuj_fakture_proforma/` — używa `BaseInvoiceComponent`
- `../faktury_storno/dodaj_edytuj_fakture_storno/` — używa `BaseInvoiceComponent`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
