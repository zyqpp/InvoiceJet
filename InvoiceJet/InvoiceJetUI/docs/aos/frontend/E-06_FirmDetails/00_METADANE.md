# Szczegóły firmy — Metadane

**Dokument:** Analityczny Opis Systemu (AOS) — Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Firm Management  
**Klasyfikacja:** Standardowy  
**Data utworzenia:** 2026-05-29  
**Status:** Roboczy

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Szczegóły firmy |
| **Ścieżka URL** | `/dashboard/firm-details` |
| **Plik komponentu** | `src/app/components/firm/firm-details/firm-details.component.ts` |
| **Plik szablonu** | `src/app/components/firm/firm-details/firm-details.component.html` |
| **Plik stylów** | `src/app/components/firm/firm-details/firm-details.component.scss` |
| **Klasa komponentu** | `FirmDetailsComponent` |
| **Selektor** | `app-firm-details` |
| **Wersja dokumentu** | v1 |
| **Autor dokumentu** | Agent Claud'iusz |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran edycji danych firmy użytkownika (wystawcy dokumentów). Ekran wyświetla formularz reaktywny z 6 polami identyfikacyjnymi firmy. Ekran umożliwia autouzupełnianie danych z ANAF na podstawie CUI.

---

## Powiązane dokumenty

| Dokument | Link |
|---|---|
| Przegląd ekranu | [01_PRZEGLĄD.md](01_PRZEGLĄD.md) |
| Dane i operacje | [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md) |
| Logika biznesowa | [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md) |
| Scenariusze testowe | [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md) |
| Historia zmian | [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md) |

---

## Szybkie odniesienia

### Główne serwisy
- `FirmService` (`src/app/services/firm.service.ts`) — pobieranie i edycja danych firmy użytkownika, integracja z ANAF

### Modele danych
- `IFirm` (`src/app/models/IFirm.ts`) — interfejs danych firmy: `id`, `name`, `cui`, `regCom`, `address`, `county`, `city`

### Formularz reaktywny
- `firmDetailsForm: FormGroup` — 6 pól: `firmName`, `cuiValue`, `regCom`, `address`, `county`, `city`

### Dialogi
- Ekran nie wywołuje okien modalnych.

### Powiązane ekrany
- Ekran Klienci (`E-04_Clients`) — wykorzystuje ten sam serwis `FirmService` i model `IFirm`
- Ekran Konta bankowe (`E-07_BankAccounts`) — konta bankowe przypisane do firmy użytkownika

---

## Notatki

- Ekran nie zawiera gridu. Dane prezentowane są w formularzu.
- Ekran nie zawiera sekcji filtrów.
- Ekran integruje się z zewnętrzną usługą ANAF (pobieranie danych firmy na podstawie CUI).
- [UWAGA: Pole `regCom` posiada atrybut `required` w HTML ale nie posiada walidatora `Validators.required` w `FormGroup` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Metoda `isFormChanged()` zawiera błąd — porównuje `initialFormValues.value` z `initialFormValues` zamiast `firmDetailsForm.value` z `initialFormValues` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
