# Pokrycie testami — Ekrany

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-COV-EKRANY |
| Typ dokumentu | macierz pokrycia ekranów |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Macierz pokrycia mapuje scenariusze testowe manualne na ekrany (widoki Angular) aplikacji InvoiceJet. Status pokrycia wskazuje, czy główne interakcje użytkownika z ekranem mają przypisane scenariusze testowe.

## Tabela pokrycia ekranów

| ID Ekranu | Nazwa Ekranu | Ścieżka Angular | Powiązane testy (TC-NNN) | Status pokrycia |
|---|---|---|---|---|
| SCR-LOGIN | Ekran logowania | `/login` | TC-104, TC-105 | Pełne |
| SCR-REGISTER | Ekran rejestracji | `/register` | TC-100, TC-101, TC-102, TC-103 | Pełne |
| SCR-DASHBOARD | Dashboard z statystykami | `/dashboard` | TC-157 | Pełne |
| SCR-FIRMA | Dane własnej firmy | `/dashboard/my-firm` | TC-110, TC-111, TC-112 | Pełne |
| SCR-KLIENCI | Lista klientów | `/dashboard/clients` | TC-113, TC-114 | Pełne |
| SCR-PRODUKTY | Lista produktów | `/dashboard/products` | TC-120, TC-121, TC-122, TC-123 | Pełne |
| SCR-KONTA-BANKOWE | Lista kont bankowych | `/dashboard/bank-accounts` | TC-130, TC-131, TC-132 | Pełne |
| SCR-SERIE | Lista serii dokumentów | `/dashboard/document-series` | TC-140, TC-141, TC-142, TC-143 | Pełne |
| SCR-FAKTURY | Lista faktur | `/dashboard/invoices` | TC-150, TC-153, TC-155, TC-156 | Pełne |
| SCR-DODAJ-FAKTURE | Formularz nowej faktury | `/dashboard/add-invoice` | TC-150 | Pełne |
| SCR-EDYTUJ-FAKTURE | Formularz edycji faktury | `/dashboard/edit-invoice/:id` | TC-155 | Pełne |
| SCR-PROFORMY | Lista proform | `/dashboard/invoice-proformas` | TC-151, TC-154 | Pełne |
| SCR-DODAJ-PROFORME | Formularz nowej proformy | `/dashboard/add-invoice` (documentTypeId=2) | TC-151 | Pełne |
| SCR-STORNO | Ekran stornoowania | — (dialog/akcja inline) | TC-152 | Pełne |
| SCR-TOKEN-EXPIRED | Dialog wygaśnięcia tokenu JWT | `TokenExpiredDialogComponent` (dialog) | TC-106 | Pełne |
| SCR-PDF-VIEWER | Podgląd/pobieranie PDF | Akcja inline na liście faktur/proform | TC-153, TC-154 | Pełne |

## Ekrany bez pokrycia testowego

Brak ekranów bez pokrycia testowego dla scenariuszy MVP.

## Uwagi

- **SCR-DODAJ-FAKTURE i SCR-DODAJ-PROFORME:** Formularz dodawania faktury i proformy to ten sam komponent Angular z różnym `documentTypeId` — TC-150 i TC-151 pokrywają oba warianty.
- **SCR-TOKEN-EXPIRED:** Komponent dialogowy `TokenExpiredDialogComponent` testowany jako część scenariusza TC-106 (wygaśnięcie JWT); brak możliwości bezpośredniego nawigowania do ekranu.
- Scenariusze testowe weryfikują głównie interakcje (happy path i anomalie). Weryfikacja wyglądu (pixel-perfect, responsywność) wymaga oddzielnych testów wizualnych (np. Percy, Chromatic).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
