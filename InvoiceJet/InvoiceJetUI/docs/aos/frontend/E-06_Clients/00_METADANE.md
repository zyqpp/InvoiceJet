# Clients — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Inventory  
**Klasyfikacja:** Standardowy  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Clients |
| **Ścieżka URL** | `/dashboard/clients` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/firm/clients/clients.component.ts` |
| **Plik szablonu** | `src/app/components/firm/clients/clients.component.html` |
| **Plik stylów** | `src/app/components/firm/clients/clients.component.scss` |
| **Komponent dialogu** | `src/app/components/firm/add-edit-client-dialog/add-edit-client-dialog.component.ts` |
| **Szablon dialogu** | `src/app/components/firm/add-edit-client-dialog/add-edit-client-dialog.component.html` |
| **Wersja dokumentu** | 1.1 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Clients wyświetla grid klientów zalogowanego użytkownika. Ekran umożliwia filtrowanie tekstowe, sortowanie, paginację, zaznaczanie wierszy, dodawanie klienta, edycję klienta oraz usuwanie zaznaczonych klientów.

---

## Powiązane dokumenty

| Dokument | Link |
|---|---|
| Przegląd ekranu | [01_PRZEGLĄD.md](01_PRZEGLĄD.md) |
| Dane i operacje | [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md) |
| Logika frontendowa | [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md) |
| Scenariusze testowe | [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md) |
| Historia zmian | [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md) |

---

## Szybkie odniesienia

### Główne serwisy

- `FirmService` — wywołania HTTP dla listy klientów, dodawania, edycji, usuwania i pobierania danych z ANAF.
- `MatDialog` — otwieranie dialogu Dodawanie/Edycja klienta.
- `ToastrService` — wyświetlanie komunikatów sukcesu i błędu.
- `LiveAnnouncer` — komunikaty dostępności dla zmiany sortowania.

### Modele danych

- `IFirm` — model danych klienta używany przez grid i formularz dialogu.

### Dialogi

- Dialog Dodawanie/Edycja klienta: `AddEditClientDialogComponent`.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej wynikające z komponentów Angular i serwisów UI.
- Dokument nie opisuje implementacji backendu ani logiki bazy danych.
- Endpoints są podane wyłącznie jako adresy wywoływane przez `FirmService`.
