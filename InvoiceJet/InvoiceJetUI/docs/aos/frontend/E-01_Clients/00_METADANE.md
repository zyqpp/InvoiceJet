# Clients — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Firm Management  
**Klasyfikacja:** Prosty  
**Data utworzenia:** 2026-05-29  
**Status:** Roboczy

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Clients |
| **Ścieżka URL** | `/clients` |
| **Plik komponentu** | `src/app/components/firm/clients/clients.component.ts` |
| **Plik szablonu** | `src/app/components/firm/clients/clients.component.html` |
| **Plik stylów** | `src/app/components/firm/clients/clients.component.scss` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran do zarządzania listą klientów (firm zarejestrowanych jako odbiorcy) — wyświetla grid z danymi, umożliwia dodawanie, edycję i usuwanie.

---

## Powiązane dokumenty

| Dokument | Link |
|---|---|
| Przegląd ekranu | [01_PRZEGLĄD.md](01_PRZEGLĄD.md) |
| Pola i operacje | [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md) |
| Logika biznesowa | [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md) |
| Scenariusze testowe | [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md) |
| Historia zmian | [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md) |

---

## Szybkie odniesienia

### Główne serwisy
- `FirmService.service.ts` — pobieranie i zarządzanie danymi firm

### Modele danych
- `IFirm` — interfejs danych klienta

### Dialogi (jeśli istnieją)
- Dialog Dodawanie klienta: `clients-edit.dialog.component.ts`
- Dialog Edycja klienta: `clients-edit.dialog.component.ts` (reuse)

---

## Notatki

- Ekran zawiera CRUD operacje dla klientów
- Wykorzystuje Angular Material do UI
- Integruje się z backend API `/api/firms`
