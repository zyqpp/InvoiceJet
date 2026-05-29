# Bank Accounts — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Settings  
**Klasyfikacja:** Standardowy  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Bank Accounts |
| **Ścieżka URL** | `/dashboard/bank-accounts` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/firm/bank-accounts/bank-accounts.component.ts` |
| **Plik szablonu** | `src/app/components/firm/bank-accounts/bank-accounts.component.html` |
| **Plik stylów** | `src/app/components/firm/bank-accounts/bank-accounts.component.scss` |
| **Komponent dialogu** | `src/app/components/firm/bank-accounts/add-or-edit-bank-account-dialog/add-or-edit-bank-account-dialog.component.ts` |
| **Szablon dialogu** | `src/app/components/firm/bank-accounts/add-or-edit-bank-account-dialog/add-or-edit-bank-account-dialog.component.html` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Bank Accounts wyświetla grid kont bankowych firmy użytkownika. Ekran umożliwia filtrowanie tekstowe, sortowanie, paginację, zaznaczanie wierszy, dodawanie konta, edycję konta i usuwanie zaznaczonych kont.

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

- `BankAccountService` — wywołania HTTP dla listy kont bankowych, dodawania, edycji i usuwania.
- `MatDialog` — otwieranie dialogu Dodawanie/Edycja konta bankowego.
- `ToastrService` — wyświetlanie komunikatów sukcesu.
- `LiveAnnouncer` — komunikaty dostępności dla zmiany sortowania.

### Modele danych

- `IBankAccount` — model konta bankowego używany przez grid i formularz dialogu.
- `ICurrency` i `Currency` — słownik walut widocznych w formularzu.

### Dialogi

- Dialog Dodawanie/Edycja konta bankowego: `AddOrEditBankAccountDialogComponent`.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej wynikające z komponentów Angular i serwisów UI.
- Endpointy są podane wyłącznie jako adresy wywoływane przez `BankAccountService`.
